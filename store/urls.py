from .views import *
from django.urls import path

urlpatterns = [
    path('', home, name="homepage"),
    path('register/', register, name="register"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('create/', create_product, name="create"),
    path('cart/<int:product_id>', add_to_cart, name="cart"),
    path('viewcart/', view_cart, name="viewcart"),
    path('cart/<int:cart_item_id>', update_cart, name="updatecart"),
    path('checkout/', checkout, name="checkoutcart"),
    path('search/', search_products, name="search"),
    #path('category/', category, name="category"),
]