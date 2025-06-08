from .models import Cart
from django.conf import settings

def cart(request):
    cart = None
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart = Cart.objects.filter(id=cart_id).first()

    return {'cart': cart}

def site_info(request):
    return {
        'site_url': settings.SITE_URL,
        'debug': settings.DEBUG
    }

