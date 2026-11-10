from django.urls import path
from . import views

urlpatterns = [
    # 🏠 HOME
    path('', views.home, name='home'),

    # 📦 PRODUCTS
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('category/<int:category_id>/', views.category_view, name='category'),

    # 🛒 CART
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),

    # 💳 CHECKOUT
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),

    # 🔐 AUTH
    path('auth/', views.auth_view, name='auth'),
    path('logout/', views.logout_view, name='logout'),
    
    path('profile/', views.profile, name='profile'),
    
]