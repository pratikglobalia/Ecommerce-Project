from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home, name='home'),
    path('about/', views.About, name='about'),
    path('products/', views.Product, name='products'),
    path('single_product/<int:pk>/', views.Single_product, name='single_product'),
    path('cart/', views.ShoppingCart, name='cart'),
    path('remove/<int:pk>/', views.RemoveCartProduct, name='remove'),
    path('contact/', views.Contact, name='contact'),
    path('signup/', views.Signup, name='signup'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('profile/', views.Profile, name='profile'),
    path('changepass/', views.ChangePassword, name='changepass'),
    path('forgotpass/', views.ForgotPassword, name='forgotpass'),
    path('otp/', views.UserOTP, name='otp'),
    path('resetotp/', views.ResetOTP, name='resetotp'),
    path('library/', views.Library, name='library'),
    path('search/', views.Search, name='search'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)