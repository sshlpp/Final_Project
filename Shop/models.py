from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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
    
class Product(models.Model):
    seller = models.ForeignKey(SwapedUser, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='product_images/', blank=False, null=False)
    name = models.CharField(max_length=50, null=False, blank=False)
    product_type = models.CharField(max_length=20, null=False, blank=False)
    size = models.CharField(max_length=20, null=False, blank=False)
    brand = models.CharField(max_length=20)
    price  = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    description = models.TextField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    condition = models.CharField(max_length=20, blank=False, null=False, default="good")


    def __str__(self):
        return self.name

    
class Purchase(models.Model):
    buyer = models.ForeignKey(SwapedUser, on_delete=models.CASCADE, related_name='purchases')
    seller = models.ForeignKey(SwapedUser, on_delete=models.CASCADE, related_name='salles')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
