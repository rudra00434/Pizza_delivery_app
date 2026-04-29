from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Pizza, PizzaCategory, Cart, CartItems


# -----------------------------
# Home Page
# -----------------------------
def home(request):
    pizzas = Pizza.objects.all()
    context = {
        'pizzas': pizzas
    }
    return render(request, 'home.html', context)


# -----------------------------
# Register View
# -----------------------------
def register_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Validation
        if not username or not password:
            messages.error(request, "All fields are required")
            return redirect('/register/')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken')
            return redirect('/register/')

        # Create user
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()

        messages.success(request, 'Account created successfully')
        return redirect('home')

    return render(request, 'register.html')


# -----------------------------
# Login View
# -----------------------------
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, "Invalid credentials")
            return redirect('/login/')

        login(request, user)
        return redirect('home')

    return render(request, 'login.html')


# -----------------------------
# Logout View
# -----------------------------
def logout_page(request):
    logout(request)
    return redirect('/login/')


# -----------------------------
# Add to Cart
# -----------------------------
@login_required
def add_cart(request, pizza_uid):
    pizza = get_object_or_404(Pizza, uid=pizza_uid)

    # Get or create cart
    cart, _ = Cart.objects.get_or_create(user=request.user, is_paid=False)

    # Check if item already exists
    cart_item, created = CartItems.objects.get_or_create(
        cart=cart,
        pizza=pizza
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, "Item added to cart")
    return redirect('/')
@login_required(login_url='login')
def my_cart(request):
    carts = Cart.objects.filter(user=request.user,is_paid=False).first()
    context={
        'cart':carts
    }
    return render(request,'my_carts.html',context)

def remove_cart_item(request,item_uid):
    cart_item = get_object_or_404(CartItems,uid=item_uid)
    cart_item.delete()
    messages.info(request,"The item is removed successfully")
    return redirect('my_carts')

