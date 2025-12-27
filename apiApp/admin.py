from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    list_display = ('username','email','first_name','last_name')
admin.site.register(CustomUser, CustomUserAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name','price','featured','slug')
    ordering = ('id',)
admin.site.register(Product, ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
admin.site.register(Category, CategoryAdmin)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id','cart','product','quantity')
admin.site.register(CartItem, CartItemAdmin)

admin.site.register([Cart, Rating, ProductRating, WishList, Order, OrderItems])
