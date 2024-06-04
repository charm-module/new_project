
from re import template
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MypasswordChangeForm, MypasswordResetForm
urlpatterns = [
     path('', views.ProductView.as_view(), name="home"),
     path('product-detail/<int:pk>',
          views.ProductDetailView.as_view(), name='product-detail'),
     path('checkout/',views.checkout,name="checkout"),

     path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
     path('cart/', views.show_cart, name='showcart'),
     path('plusecart/', views.plus_cart),
     path('minuscart/', views.minus_cart),
     path('removecart/', views.remove_cart),



     path('buy/', views.buy_now, name='buy-now'),
     path('profile/', views.ProfileView.as_view(), name='profile'),
     path('address/', views.address, name='address'),
     path('orders/', views.orders, name='orders'),
     path('order_details/<str:id>/', views.order_details, name='order_details'),
     path('mobile/', views.mobile, name='mobile'),
     path('mobile/<slug:data>', views.mobile, name='mobiledata'),
     path('paymentdone/', views.payment_done, name='paymentdone'),
     # path('accounts/login/', auth_views.LoginView.as_view
     #      (template_name='app/login.html', authentication_form=LoginForm), name='login'),
     path('accounts/login/',views.logins,name='login'),
     path('logout/', auth_views.LogoutView.as_view
          (next_page='login'), name='logout'),

     path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/Passwordchange.html',
                                                                      form_class=MypasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),

     path('passwordchangedone/', auth_views.PasswordChangeView.as_view(
          template_name='app/Passwordchangedone.html'), name='passwordchangeddone'),

     path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',
                                                                 form_class=MypasswordResetForm), name='password_reset'),

     path('password-reset/done', auth_views.PasswordResetView.as_view
          (template_name='app/password_reset_done.html',
          form_class=MypasswordResetForm), name='password_reset_done'),

     path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view
          (template_name='app/password_reset_confirm.html', form_class=MypasswordResetForm),
          name='password_reset_confirm'),

     path('password-reset-complete', auth_views.PasswordResetView.as_view
          (template_name='app/password_reset_complete.html',
          form_class=MypasswordResetForm), name='password_reset_complete'),

      path('my_order/', views.all_orders, name='my_orders'),



     path('registration/', views.customerregistration,
          name='customerregistration'),

     path('getcartcount/', views.getcartcount, name='cartcount'),
     path('submit_feedback/<str:id>/',views.submit_order_feedback,name='submit_feedback'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
