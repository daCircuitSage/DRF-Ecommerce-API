from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Product,
    Category,
    Cart,
    CartItem,
    Rating,
    WishList,
)



class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','slug','image','price']



class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','description','slug','image','price']




class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','image','slug']



class CategoryDetailSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id','name','image','products']





#---------------------------------------cart



class CartItemSerializerser(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    sub_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id','product','quantity','sub_total']

    def get_sub_total(self, cartitem):
        return cartitem.product.price * cartitem.quantity
    

class CartSeralizer(serializers.ModelSerializer):
    cartitems = CartItemSerializerser(many=True, read_only=True)
    cart_total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id','cart_code','cartitems','cart_total']

    def get_cart_total(self, cart):
        total = sum([item.quantity*item.product.price for item in cart.cartitems.all()])
        return total 
    

class CartStartSerializer(serializers.ModelSerializer):
    total_quantity = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id','cart_code','total_quantity']

    def get_total_quantity(self, cart):
        items = cart.cartitems.all()
        total = sum([item.quantity for item in items])
        return total 
    

#--------------------------------reviews-----------------------------------------


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id','first_name','last_name','email','profile_picture']

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Rating
        fields = ['id','user','rating','review','created_at','updated_at']

class WishlistSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductListSerializer(read_only=True)
    class Meta:
        model = WishList
        fields = ['id','user','product','created_at']