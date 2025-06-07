
from django.contrib import admin
from .models import Customer, Product, Bill, BillItem

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'created_at']
    search_fields = ['name', 'phone']
    list_filter = ['created_at']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']

class BillItemInline(admin.TabularInline):
    model = BillItem
    extra = 0

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['bill_number', 'customer', 'bill_date', 'grand_total']
    search_fields = ['bill_number', 'customer__name']
    list_filter = ['bill_date']
    inlines = [BillItemInline]
    readonly_fields = ['bill_number', 'subtotal', 'tax_amount', 'grand_total']
