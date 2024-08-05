from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.utils.translation import gettext_lazy as _



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')

        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractUser): 
    email = models.EmailField(unique=True)
    first_name=models.CharField(max_length=39, null=True, blank=True)
    last_name=models.CharField(max_length=92, null=True, blank=True)
    username=None
    is_superuser=models.BooleanField(default=False)
    
    
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    objects=CustomUserManager()


class Products(models.Model): 
    PRODUCT_TYPE=(
        ("clothes", "clothes"),
        ("footwear", "footwear"),
        ("electronics", "electronics"),
        ("suplements", "suplements"),
        ("watches", "watches")
    )
    product_type=models.CharField(max_length=50, choices=PRODUCT_TYPE, null=True)
    name = models.CharField(max_length=60) 
    price = models.IntegerField(default=0) 
    description = models.CharField( 
        max_length=250, default='', blank=True, null=True) 
    image = models.FileField(upload_to='product_img/', blank=True, null=True)
 

class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'product')

class CheckoutCart(models.Model):
    cart_items = models.ManyToManyField(CartItem)
    total_price = models.PositiveIntegerField()
    delivry_charges = models.PositiveBigIntegerField()





