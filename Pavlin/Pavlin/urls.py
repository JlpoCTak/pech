from django.conf import settings
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from katalog import views
"""
URL configuration for Pavlin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
app_name = 'katalog'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('', include('katalog.urls', namespace='katalog')),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('robots.txt', TemplateView.as_view(
                template_name='robots.txt',
                content_type='text/plain')
        ),
    path('privacy-policy/',
             TemplateView.as_view(template_name='katalog/privacy_policy.html'),
             name='privacy_policy'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
