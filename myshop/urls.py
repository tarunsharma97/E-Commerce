from django.contrib.auth.forms import AuthenticationForm
from django.utils import html
from myshop.forms import LoginForm
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', views.Home, name='home'),

    path('category/<int:id>/products', views.Categories, name='category'),

    path('all-category-products/', views.Allcategories, name='all_category'),

    path('product-detail/<int:id>/', views.ProductDetail, name='product_detail'),

    path('profile/', views.MyProfile.as_view(), name='profile'),

    path('search/', views.Search, name='search'),

    path('review/', views.Review_rate, name='review'),

    path('add-to-cart/', views.Add_to_cart, name='add_to_cart'),

    path('cart-item/', views.CartItem, name='cart_item'),

    path('buyNow/', views.BuyNow, name='buyNow'),

    path('checkout/', views.Checkout.as_view(), name='checkout'),

    path('orders/', views.Orders, name='orders'),

    path('plus_minus_item/', views.Plus_Minus_Item,
         name='plus_minus_item'),

    path('registration/', views.CustomerRegistration.as_view(),
         name='customerregistration'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html',
                                                         authentication_form=LoginForm), name='login'),

    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html',
                                                                   form_class=MyPasswordChangeForm, success_url='/password-change-done/'), name='password_change'),

    path('password-change-done/', auth_views.PasswordResetView.as_view(template_name='password_change_done.html'),
         name='password_change_done'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html',
                                                                 form_class=MyPasswordResetForm), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),

    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
