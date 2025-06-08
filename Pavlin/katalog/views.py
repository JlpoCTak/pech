from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem, OrderItem, Order
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .forms import OrderForm


def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart = get_object_or_404(Cart, id=cart_id)
        else:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
    return cart


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Получаем или создаем корзину
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart = get_object_or_404(Cart, id=cart_id)
        else:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id

    # Добавляем товар в корзину
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'price': product.price}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.price = product.price * cart_item.quantity
        cart_item.save()

    messages.success(request, f'Товар "{product.name}" добавлен в корзину')
    return redirect('katalog:cart_detail')


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('katalog:cart_detail')


def cart_detail(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        cart_id = request.session.get('cart_id')
        cart = Cart.objects.filter(id=cart_id).first() if cart_id else None

    if not cart:
        # Создаем пустую корзину, если не существует
        if request.user.is_authenticated:
            cart = Cart.objects.create(user=request.user)
        else:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id

    return render(request, 'katalog/cart.html', {'cart': cart})


@require_POST
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    quantity = int(request.POST.get('quantity', 1))

    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.price = cart_item.product.price * quantity
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('katalog:cart_detail')


def checkout(request):
    cart = get_or_create_cart(request)  # Используем вашу существующую функцию

    if not cart.items.exists():
        messages.warning(request, "Ваша корзина пуста")
        return redirect('katalog:cart_detail')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.privacy_policy_accepted = form.cleaned_data['privacy_policy']
            if not order.email and request.user.is_authenticated:
                order.email = request.user.email
            if request.user.is_authenticated:
                order.user = request.user
                if not order.customer_name:  # Если имя не указано, берем из профиля
                    order.customer_name = request.user.get_full_name() or request.user.username
            order.total_price = cart.total_price
            order.save()

            # Переносим товары из корзины в заказ
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.price
                )

            # Очищаем корзину
            cart.items.all().delete()

            messages.success(request, "Ваш заказ успешно оформлен!")
            return redirect('katalog:order_detail', order_id=order.id)
    else:
        # Предзаполняем данные для авторизованных пользователей
        initial = {}
        if request.user.is_authenticated:
            initial = {
                'customer_name': request.user.get_full_name(),
                'email': request.user.email,
                'phone': request.user.phone if hasattr(request.user, 'phone') else ''
            }
        form = OrderForm(initial=initial)
    if form.is_valid():
        order = form.save(commit=False)
        order.user = request.user if request.user.is_authenticated else None
        order.total_price = cart.total_price
        order.save()

        # Переносим товары из корзины в заказ
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.price
            )

        # Очищаем корзину
        cart.items.all().delete()

        messages.success(request, "Ваш заказ успешно оформлен!")
        return redirect('katalog:order_detail', order_id=order.id)  # Вот эта ссылка

    return render(request, 'katalog/checkout.html', {
        'cart': cart,
        'form': form
    })




def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'katalog/order_detail.html', {'order': order})
