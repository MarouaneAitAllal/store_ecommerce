from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Product, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# 🏠 HOME
def home(request):
    if 'cart' not in request.session:
        request.session['cart'] = {}

    products = Product.objects.all().order_by('order')
    return render(request, 'shop/index.html', {'products': products})


# 📦 DETAIL
def product_detail(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return redirect('home')

    return render(request, 'shop/detail.html', {'product': product})


# 🛒 ADD TO CART (AJAX)
def add_to_cart(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)] += 1
    else:
        cart[str(id)] = 1

    request.session['cart'] = cart

    return JsonResponse({
        'success': True,
        'cart_count': sum(cart.values())
    })


# 🧺 CART
def cart(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            product.quantity = quantity
            product.total_price = product.price * quantity
            total += product.total_price
            products.append(product)
        except Product.DoesNotExist:
            pass

    return render(request, 'shop/cart.html', {
        'products': products,
        'total': total
    })


# ❌ REMOVE
def remove_from_cart(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        del cart[str(id)]

    request.session['cart'] = cart
    return redirect('cart')


# ➕➖ QUANTITY
def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1

    request.session['cart'] = cart
    return redirect('cart')


def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] -= 1

        if cart[str(product_id)] <= 0:
            del cart[str(product_id)]

    request.session['cart'] = cart
    return redirect('cart')


# 📂 CATEGORY
def category_view(request, category_id):
    products = Product.objects.filter(category_id=category_id)
    return render(request, 'shop/index.html', {'products': products})


def checkout(request):

    # ❌ منع الدخول إلا ما كانش user مسجل
    if not request.user.is_authenticated:
        return redirect('home')

    cart = request.session.get('cart', {})

    products = []
    total = 0   # ✅ مهم بزاف

    # 🧮 نحسب total و products
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        product.quantity = quantity
        product.total_price = product.price * quantity

        total += product.total_price
        products.append(product)

    # 🟢 POST → إنشاء الطلب
    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            total=total   # ✅ مهم
        )

        for product in products:
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=product.quantity,
                price=product.price
            )

        # 🧹 نفرغ panier
        request.session['cart'] = {}

        return redirect('success')

    # 🟢 GET → عرض الصفحة
    return render(request, 'shop/checkout.html', {
        'products': products,
        'total': total
    })
# ✅ SUCCESS
def success(request):
    return render(request, 'shop/success.html')


# 🔐 AUTH (LOGIN + REGISTER)
def auth_view(request):
    if request.method == 'POST':

        form_type = request.POST.get('form_type')
        username = request.POST.get('username')
        password = request.POST.get('password')
def auth_view(request):
    if request.method == 'POST':

        form_type = request.POST.get('form_type')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # LOGIN
        if form_type == 'login':
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                return redirect('home')

        # REGISTER
        elif form_type == 'register':

            if User.objects.filter(username=username).exists():
                return redirect('home')

            user = User.objects.create_user(username=username, password=password)
            login(request, user)

            next_url = request.GET.get('next', 'home')
            return redirect(next_url)

    return redirect('home')


# 🚪 LOGOUT
def logout_view(request):
    logout(request)
    return redirect('home')



@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/profile.html', {'orders': orders})

