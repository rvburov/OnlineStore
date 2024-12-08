from .models import Cart

def cart_total_items(request):
    if request.user.is_authenticated:
        # Если пользователь аутентифицирован, получаем корзину из базы данных
        total_items = Cart.objects.filter(user=request.user).count()
    else:
        # Если пользователь не аутентифицирован, получаем корзину из сессии
        cart = request.session.get('cart', {})
        total_items = len(cart)

    return {
        'total_items': total_items
    }
