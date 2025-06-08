from django.contrib import admin
from .models import Category, Product, Order


admin.site.register(Category)
admin.site.register(Product)


#@admin.register(Product)
#class ProductAdmin(admin.ModelAdmin):
#    list_display = ['name', 'category', 'price', 'available']
#    list_filter = ['category', 'available']
#    search_fields = ['name', 'description']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'total_price', 'status', 'created_at', 'order_link')

    def order_link(self, obj):
        from django.urls import reverse
        from django.utils.html import format_html
        url = reverse('katalog:order_detail', args=[obj.id])
        return format_html('<a href="{}">Просмотреть</a>', url)

    order_link.short_description = "Ссылка"