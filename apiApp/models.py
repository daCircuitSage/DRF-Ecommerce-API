from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser, BaseUserManager



class CustomUser(AbstractUser):
    email = models.EmailField(verbose_name='Email', unique=True)
    profile_picture = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.email
    

class Category(models.Model):
    name = models.CharField(unique=True, max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='category_img', blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            unique_slug = self.slug
            counter = 1
            while Product.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{self.slug}-{counter}"
                counter += 1
            self.slug=unique_slug
        super().save(*args, **kwargs)
        


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='product_img', blank=True, null=True)
    featured = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products',blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            unique_slug = self.slug
            counter = 1
            while Product.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{self.slug}-{counter}"
                counter += 1
            self.slug=unique_slug
        super().save(*args, **kwargs)



class Cart(models.Model):
    cart_code = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cart_code
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='item')
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart {self.cart.cart_code}"
    


class Rating(models.Model):
    RATING_CHOICES = [
        (1,'1 - Poor'),
        (2,'2 - Fair'),
        (3,'3 - Good'),
        (4,'4 - Very Good'),
        (5,'5 - Execellent'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    review = models.TextField()
    created_at =  models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s raitng on {self.product.name}"
    
    class Meta:
        unique_together = ['user','product']
        ordering = ['-created_at']



class ProductRating(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='rating')
    average_rating = models.FloatField(default=0.0)
    total_review = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.product.name} - {self.average_rating}  ({self.total_review}) Reviews'
        

    
class WishList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlist')
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user','product']

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    

    

class Order(models.Model):
    stripe_checkout_id = models.CharField(max_length=500, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    customer_email = models.EmailField(max_length=255)
    status = models.CharField(max_length=20, choices=[('Pending','Pending'), ('Paid','Paid')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.stripe_checkout_id} - {self.status}'
    
class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_product')
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'Order {self.product.name} - {self.order.stripe_checkout_id}'
    
    