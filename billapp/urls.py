from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.dashboard, name='dashboard'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/add/', views.customer_add, name='customer_add'),
    path('customers/edit/<int:pk>/', views.customer_edit, name='customer_edit'),
    path('customers/delete/<int:pk>/', views.customer_delete, name='customer_delete'),
    
 
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/edit/<int:pk>/', views.product_edit, name='product_edit'),
    path('products/delete/<int:pk>/', views.product_delete, name='product_delete'),
    path('bills/', views.bill_list, name='bill_list'),
    path('bills/create/', views.bill_create, name='bill_create'),
    path('bills/view/<int:pk>/', views.bill_view, name='bill_view'),
    path('bills/print/<int:pk>/', views.bill_print, name='bill_print'),
    path('api/product-price/<int:pk>/', views.get_product_price, name='get_product_price'),
]
