from django.urls import path
from .views import *


urlpatterns = [
    #--------------------product/list/single-----------------------
    path('product_list/', product_list, name='product_list'),
    path('product/<slug:slug>/', product_detail, name='product'),

    #--------------------category/list/single-----------------------
    path('category_list/', category_list, name='category_list'),
    path('category/<slug:slug>/', category_detail, name='category'),

    #-------------cart&cartitems-add/update/delete--------------------
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('update_cartitem/', update_cartitem, name='update_cartitem'),
    path('delete_cartitem/<int:pk>/', delete_cartitem, name='delete_cartitem'),

    #-----------------review-add/update/delete--------------------------
    path('add_review/', add_review, name='add_review'),
    path('update_review/<int:pk>/', update_review, name='update_review'),
    path('delete_review/<int:pk>/', delete_review, name='delete_review'),

    #---------------------wishlist------searchproduct--------------------
    path('add_to_wishlist/', add_wishlist, name='add_to_wishlist'),
    path('product_search', search_product, name='product_search'),
    
    #------------------------payment/order/stripe----------------------------------------------
    path('create_checkout_session/', create_checkout_session, name='create_checkout_session'),
    path('webhook/', my_webhook_view, name='webhook'),
]
