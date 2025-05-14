from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number', 'total_lontong_large', 'total_lontong_small', 'total_price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'phone_number', 'address')
    readonly_fields = ('total_price',)