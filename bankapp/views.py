from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.db import connection
from bankapp.models import Customer, Transaction

# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'

def customerView(request):
    customers_list = Customer.objects.raw('SELECT * FROM public.bankapp_customer ORDER BY account_number ASC')
    customers_dict = {'customers':customers_list}
    return render(request,'customer.html',context=customers_dict)

def transactionView(request):
    transactions_list = Transaction.objects.raw('SELECT * FROM public.bankapp_transaction ORDER BY time DESC')
    transactions_dict = {'transactions':transactions_list}
    return render(request, 'transactions.html', context=transactions_dict)

def transferView(request):
    if request.method == 'POST':
        account_number_1 = request.POST['account_number_1']
        account_number_2 = request.POST['account_number_2']

        data_one = Customer.objects.filter(account_number=account_number_1)
        data_two = Customer.objects.filter(account_number=account_number_2)

        if data_one and data_two:
            request.session['account_number_1'] = account_number_1
            request.session['account_number_2'] = account_number_2

            s_data = Customer.objects.raw('SELECT * FROM public.bankapp_customer WHERE account_number={}'.format(account_number_1))
            r_data = Customer.objects.raw('SELECT * FROM public.bankapp_customer WHERE account_number={}'.format(account_number_2))

            my_dict = {'s_data':s_data, 'r_data':r_data}

            return render(request, 'confirm_transfer.html', context=my_dict)

        else:
            if not data_one:
                message = 'Invalid Sender A/C Number'
            else:
                message = 'Invalid Receiver A/C Number'

            my_msg_dict = {'message':message}
            return render(request, 'transfer.html', context=my_msg_dict)

    return render(request, 'transfer.html')


def confirmTransferView(request):
    account_number_1 = request.session['account_number_1']
    account_number_2 = request.session['account_number_2']

    data1 = Customer.objects.filter(account_number=account_number_1).values()

    print(data1)

    sender_bal = int(data1[0]['balance'])

    if request.method == 'POST':

        amount = int(request.POST['amount'])

        if amount > sender_bal:
            message = 'Insufficient Balance'

            my_error_dict = {'message':message}
            return render(request, 'transfer.html', context=my_error_dict)
        else:
            with connection.cursor() as c:
                c.execute('CALL public.transfer({},{},{})'.format(account_number_1,account_number_2,amount))
            message = 'Transaction Successful'

            my_success_dict = {'message':message}
            return render(request, 'index.html', context=my_success_dict)
    return render(request, 'confirm_transfer.html')
