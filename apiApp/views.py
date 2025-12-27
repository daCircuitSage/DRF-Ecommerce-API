import stripe
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
# from django.contrib.postgres.search import SearchVector,  SearchQuery
from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import (
    Product,
    Category,
    Cart,
    CartItem,
    Rating,
    WishList,
    Order,
    OrderItems
)
from .serializers import (
    ProductListSerializer,
    CategoryListSerializer,
    CategoryDetailSerializer,
    ProductDetailSerializer,
    CartSeralizer,
    CartItemSerializerser,
    CartStartSerializer,
    ReviewSerializer,
    WishlistSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

endpoint_secret = settings.WEBHOOK_SECRET
stripe.api_key = settings.STRIPE_SECRET_KEY
User = get_user_model()

@api_view(['GET'])
def product_list(request):
    products = Product.objects.filter(featured=True)
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    serializer = ProductDetailSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategoryListSerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def category_detail(request,slug):
    category = Category.objects.get(slug=slug)
    serializer = CategoryDetailSerializer(category)
    return Response(serializer.data, status=status.HTTP_200_OK)



#-----------------------------------------------------------------------cart-----------------------------------------------------------

@api_view(['POST'])
def add_to_cart(request):
    cart_code = request.data.get('cart_code')
    product_id = request.data.get('product_id')

    if not cart_code or not product_id:
        return Response(
            {'error': 'cart_code and product_id are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response(
            {'error': 'Product not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    cart, cart_created = Cart.objects.get_or_create(cart_code=cart_code)

    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    serializer = CartSeralizer(cart)

    return Response(
        {
            'message': 'Product added to cart successfully',
            'cart': serializer.data
        },
        status=status.HTTP_201_CREATED if item_created else status.HTTP_200_OK
    )




@api_view(['PUT'])
def update_cartitem(request):
    cartitem_id = request.data.get('cartitem_id')
    cartitem_quantity = request.data.get('quantity')

    if not cartitem_quantity or cartitem_id is None:
        return Response('Invalid Cart id or CartItem quantity')

    try:
        cartitem = CartItem.objects.get(id=cartitem_id)
    except CartItem.DoesNotExist:
        return Response('Cart does not exist', status=status.HTTP_404_NOT_FOUND)
    
    cartitem.quantity = int(cartitem_quantity)
    cartitem.save()

    serializer = CartItemSerializerser(cartitem)
    return Response({
        'Data':serializer.data,
        'msg':'CartItem Update Successfully!'
    })

@api_view(['DELETE'])
def delete_cartitem(request,pk):
    try:
        new_review = CartItem.objects.get(id=pk)
    except CartItem.DoesNotExist:
        return Response({'error': 'CartItem Does not Exist'}, status=status.HTTP_404_NOT_FOUND)
    
    new_review.delete()
    return Response({'msg':'CartItem Deleted Successfully!!'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_review(request):
    product_id = request.data.get('product_id')
    rating = request.data.get('rating')
    review_text = request.data.get('review_text')
    email = request.data.get('email')

    if not product_id or rating is None or not review_text:
        return Response({'error': 'Product, rating, and review_text are required.'},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product does not exist!'},
                        status=status.HTTP_404_NOT_FOUND)

    user = User.objects.get(email=email)

    if Rating.objects.filter(product=product, user=user).exists():
        return Response({'error': 'You have already reviewed this product!'},
                        status=status.HTTP_400_BAD_REQUEST)

    review = Rating.objects.create(
        product=product,
        user=user,
        rating=rating,
        review=review_text
    )

    serializer = ReviewSerializer(review, context={'request': request})

    return Response({
        'data': serializer.data,
        'msg': 'Review added successfully!'
    }, status=status.HTTP_201_CREATED)



@api_view(['PUT'])
def update_review(request,pk):
    try:
        new_review = Rating.objects.get(id=pk)
    except Rating.DoesNotExist:
        return Response({'error': 'Review Does not Exist'}, status=status.HTTP_404_NOT_FOUND)
    
    rating = request.data.get('rating')
    review = request.data.get('review')

    if not rating or not review:
        return Response({'error':'Rating or Review is in valid'}, status=status.HTTP_400_BAD_REQUEST)
    
    new_review.rating=int(rating)
    new_review.review=review
    new_review.save()

    serializer = ReviewSerializer(new_review)

    return Response({
        'msg':'Review updated successfully!',
        'data':serializer.data
    }, status=status.HTTP_200_OK)



@api_view(['DELETE'])
def delete_review(request,pk):
    try:
        new_review = Rating.objects.get(id=pk)
    except Rating.DoesNotExist:
        return Response({'error': 'Review Does not Exist'}, status=status.HTTP_404_NOT_FOUND)
    
    new_review.delete()
    return Response({'msg':'Review Deleted Successfully!!'}, status=status.HTTP_200_OK)



@api_view(['POST'])
def add_wishlist(request):
    email = request.data.get('email')
    product_id = request.data.get('product_id')

    try:
        user = User.objects.get(email=email)
        product = Product.objects.get(id=product_id)
    except User.DoesNotExist:
        return Response({'error':'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Product.DoesNotExist:
        return Response({'error':'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    wish_list = WishList.objects.filter(user=user, product=product)

    if wish_list.exists():
        wish_list.delete()
        return Response({'msg':'Wishlist deleted successfully!!'}, status=status.HTTP_200_OK)
    
    new_wishlist = WishList.objects.create(user=user, product=product)
    serializer = WishlistSerializer(new_wishlist)
    return Response({'msg':'Wishlist added!', 'data':serializer.data}, status=status.HTTP_201_CREATED)



@api_view(['GET'])
def search_product(request):
    search = request.query_params.get('search')

    if not search:
        return Response('No query provided', status=status.HTTP_400_BAD_REQUEST)
    
    products = Product.objects.filter(Q(name__icontains=search) |
                                      Q(description__icontains=search) |
                                      Q(category__name__icontains=search))
    if not products.exists():
        return Response({'msg': 'No products found matching your query.'})
    
    serializer = ProductListSerializer(products, many=True)
    product_count = products.count()

    return Response(
        {
            'product_count':product_count,
            'data':serializer.data
        }, status=status.HTTP_200_OK
    )
        



@api_view(['post'])
def create_checkout_session(request):
    cart_code = request.data.get('cart_code')
    email = request.data.get('email')

    try:
        cart = Cart.objects.get(cart_code=cart_code)
    except Cart.DoesNotExist:
        return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email=email,
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(item.product.price * 100),
                        'product_data': {'name': item.product.name}
                    },
                    'quantity': item.quantity,
                }
                for item in cart.cartitems.all()
            ],
            mode='payment',
            success_url='http://localhost:3000/success/',
            cancel_url='http://localhost:3000/cancel/',
            metadata={'cart_code':cart_code}
        )
        return Response({'id': checkout_session.id, 'data': checkout_session})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@csrf_exempt
def my_webhook_view(request):
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, endpoint_secret
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)

  if (
    event['type'] == 'checkout.session.completed'
    or event['type'] == 'checkout.session.async_payment_succeeded'
  ):
    session = event['data']['object']
    cart_code=session.get('metadata',{}).get('cart_code')

    fulfill_checkout(session,cart_code)

  return HttpResponse(status=200)


def fulfill_checkout(session, cart_code):
    order = Order.objects.create(
        stripe_checkout_id=session['id'],
        amount=session['amount_total'],
        currency=session['currency'],
        customer_email=session['customer_email'],
        status='Paid'
    )

    cart = Cart.objects.get(cart_code=cart_code)
    cartitems = cart.cartitems.all()

    for item in cartitems:
        orderitem = OrderItems.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity
        )

    cart.delete()