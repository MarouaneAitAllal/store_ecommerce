from django.contrib import admin
from .models import Product, Category, Order, OrderItem

# 🔹 Product Admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    search_fields = ('name',)

# 🔹 Category Admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

# 🔥 OrderItem Inline (المهم)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

# 🔥 Order Admin
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'status', 'created_at')
    inlines = [OrderItemInline]

# 🔹 Register
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)