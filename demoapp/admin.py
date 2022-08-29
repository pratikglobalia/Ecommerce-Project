from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = ['password2']

admin.site.register(ContactModel)

admin.site.register(CartModel)

@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'upload', 'product_name', 'product_price', 'product_disc']