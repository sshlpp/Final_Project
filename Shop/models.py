from django.contrib.auth.models import AbstractUser
from django.db import models, transaction, IntegrityError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class SwapedUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    seller = models.BooleanField(default=False)
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=10000)
    city = models.CharField(max_length=50, blank=False, null=False)
    country = models.CharField(max_length=50, blank=False, null=False)
    rating = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    def __str__(self):
        return self.username
    
class Category(models.Model):
    name = models.CharField(max_length=20)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name='subcategories')
    
class Product(models.Model):
    seller = models.ForeignKey(SwapedUser, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='product_images/', blank=False, null=False)
    name = models.CharField(max_length=50, null=False, blank=False)
    size = models.CharField(max_length=20, null=False, blank=False)
    brand = models.CharField(max_length=20)
    price  = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    description = models.TextField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    condition = models.CharField(max_length=20, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.name

    
class Purchase(models.Model):
    STATUS_CHOICES = [
        ('not_purchased', 'Product not purchased'),
        ('paid', 'Paid, awaiting shipment'),
        ('shipped', 'Sent by seller'),
        ('delivered', 'Received by the buyer'),
        ('cancelled', 'Canceled'),
    ]

    buyer = models.ForeignKey(SwapedUser, on_delete=models.CASCADE, related_name='purchases')
    seller = models.ForeignKey(SwapedUser, on_delete=models.CASCADE, related_name='salles')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_address = models.CharField(max_length=255, blank=True, null=True)
    customer_first_name = models.CharField(max_length=20, blank=True, null=True)
    customer_last_name = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_purchased')

    def shipped(self):
        if self.status == 'paid':
            self.status = 'shipped'
            self.save()

    def confirm_delivery(self):
        if self.status == 'shipped':
            self.status = 'delivered'
            self.seller.wallet += self.total_price
            self.seller.save()
            self.save()

    def purchase_transaction(self):

        if not self.product or self.product.is_active == False:
            raise IntegrityError("Product not found")
        
        if self.buyer.wallet < self.total_price:
            raise IntegrityError("Not enough money")
        
        if self.buyer == self.seller:
            raise IntegrityError("You cant buy this product")
        
        with transaction.atomic():

            self.buyer.wallet -= self.total_price
            self.buyer.save()

            # self.seller.wallet += self.product.price
            # self.seller.save()

            self.product.is_active = False
            self.product.save()
            self.status = 'paid'
            self.save()


