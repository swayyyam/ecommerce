from django.contrib import admin
from .models import CustomUser,Products,CartItem,CheckoutCart

admin.site.register(CustomUser)
admin.site.register(Products)
admin.site.register(CartItem)
admin.site.register(CheckoutCart)