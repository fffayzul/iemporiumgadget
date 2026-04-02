from decimal import Decimal
from .models import Category


def cart_and_categories(request):
    categories = Category.objects.all()

    cart = request.session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values())
    cart_total = sum(Decimal(str(item['price'])) * item['quantity'] for item in cart.values())

    return {
        'categories': categories,
        'cart_count': cart_count,
        'cart_total': cart_total,
    }
