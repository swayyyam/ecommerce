from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from .models import CustomUser,Products,CartItem,CheckoutCart



def home(request):
    categories = Products.PRODUCT_TYPE
    selected_category = request.GET.get('category', None)

    if selected_category:
        products = Products.objects.filter(product_type=selected_category)
    else:
        products = Products.objects.all()

    context = {
        'categories': categories,
        'products': products,
    }
    
    return render(request, 'homepage.html', context)


def register(request):
    all_data = None
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        password = request.POST.get('password')
        email = request.POST.get('email')

        CustomUser.objects.create(first_name=first_name,last_name=last_name, email=email, password=make_password(password))
        all_data = CustomUser.objects.all()
        messages.success(request, "User registered successfully!")
        return redirect('login')
    
    return render(request, 'registerpage.html', context={'data':all_data})

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful!")
            return redirect('homepage') 
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'loginpage.html')

    return render(request, 'loginpage.html')

def logout(request):
    auth_logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')

def create_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        category=request.POST.get('category')
        try:
            Products.objects.create(name=name,price=price, description=description, image=image, product_type=category)
            messages.success(request, "Product created successfully!")
            return redirect('homepage')
        except Exception as e:
            messages.error(request, str(e))
    return render(request, 'createproduct.html')


def add_to_cart(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart_items= CartItem.objects.filter(
        user=request.user, 
        product=product,
    )
    if cart_items.exists():
        cart_item = cart_items.first()
        cart_item.quantity += quantity
        cart_item.save()
    else:
        CartItem.objects.create(
            user=request.user,
            product=product,
            quantity=quantity
        )
        cart_items = CartItem.objects.filter(user=request.user)
        return redirect('viewcart')
    return render(request, 'cart.html', {'cart_items': cart_items})


def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
    
    total_price = sum(item.total_price for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)

def update_cart(request, cart_item_id):
    cart_items = CartItem.objects.filter(id=cart_item_id, user=request.user)
    if cart_items.exists():
        cart_item = cart_items.first()
        new_quantity = int(request.POST.get('quantity', cart_item.quantity))
        cart_item.quantity = new_quantity
        cart_item.save()
    return redirect('viewcart')

def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    delivery_charges = 100  
    
    if request.method == 'POST':
        checkout_cart = CheckoutCart.objects.create(
            total_price=total_price,
            delivry_charges=delivery_charges
        )
        checkout_cart.cart_items.set(cart_items)
        cart_items.delete()
        messages.success(request, 'Your order has been placed successfully!')
        return redirect('homepage') 
    
    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'delivery_charges': delivery_charges
    })

def search_products(request):
    query = request.GET.get('q', '')  
    if query:
        
        products = Products.objects.filter(name__icontains=query)
    else:
        products = Products.objects.all()  

    context = {
        'products': products,
        'query': query,
    }

    return render(request, 'search.html', context)













