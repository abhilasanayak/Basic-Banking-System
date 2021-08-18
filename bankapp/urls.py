from django.urls import path
from bankapp import views

app_name = 'bankapp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('customers/', views.customerView, name='customer'),
    path('transactions/', views.transactionView, name='transaction'),
    path('transfer/', views.transferView, name='transfer'),
    path('transfer/confirm/', views.confirmTransferView, name='confirm'),
]
