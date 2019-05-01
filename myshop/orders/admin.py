from django.contrib import admin
from .models import Order, OrderItem, Postal_Code


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'paid',
                    'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]

@admin.register(Postal_Code)
class Postal_CodeAdmin(admin.ModelAdmin):
    list_display = ['postal_code']