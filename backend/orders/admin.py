from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['order']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'name', 'time', 'status', 'user')
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'order')
