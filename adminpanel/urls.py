from django.urls import path
from adminpanel import views

urlpatterns = [
     path('', views.admin_login, name="admin_login"),
     path('admin_logout', views.admin_logout, name="admin_logout"),
     path('admin_home', views.admin_home, name="admin_home"),
     path('admin_product', views.admin_product, name='admin_product'),
     path('add_product', views.add_product, name='add_product'),
     path('save_admin_add_product',
          views.save_add_product, name='save_add_product'),
     path('edit_product/<str:id>', views.edit_product, name='edit_product'),
     path('save_admin_edit_product',
          views.save_edit_product, name='save_edit_product'),
     path('delete_product/<str:id>', views.delete_product, name="delete_product"),

     path('customers', views.customers, name='customers'),
     path('edit_customer/<str:id>', views.edit_customers, name='edit_customer'),
     path('save_edit_customer', views.save_edit_customer, name='save_edit_customer'),
     path('delete_customer/<str:id>', views.delete_customer, name='delete_customer'),
     path('admin_orders', views.admin_orders, name='admin_orders'),
     path('order_delete/<str:id>',views.delete_order,name="order_delete"),
     path('order_status_change', views.order_status_change,
          name='order_status_change'),
     path('order_details',views.get_order_details,name="order_details"),



]
