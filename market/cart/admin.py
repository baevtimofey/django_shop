from django.contrib import admin
from .models import Delivery, Order, OrderItem


class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('delivery_option', 'delivery_fee', 'express_delivery_fee', 'order_total_for_free_delivery')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created', 'updated', 'status', 'payment_date', 'delivery', 'delivery_adress', 'get_total_cost')
    list_filter = ('status', 'created', 'payment_date')
    search_fields = ('user__username', 'delivery_adress')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'offer', 'quantity', 'get_cost')
    list_filter = ('order__status', 'date_added')
    search_fields = ('offer__product',)


admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
