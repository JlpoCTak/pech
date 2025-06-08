from django.urls import path
from . import views
from django.views.generic.base import TemplateView

app_name = 'katalog'  # Это определяет namespace

urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('robots.txt', TemplateView.as_view(
                template_name='robots.txt',
                content_type='text/plain')
        ),
    path('privacy-policy/',
             TemplateView.as_view(template_name='katalog/privacy_policy.html'),
             name='privacy_policy'),
]