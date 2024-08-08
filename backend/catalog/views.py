from django.shortcuts import render
from django.views import View
from .models import Product
from cart.models import Cart

class ProductListView(View):
    """Представление для отображения списка продуктов"""

    template_name = "catalog/product_list.html"
    
    def get(self, request):
        """Обрабатывает GET-запрос для отображения списка всех продуктов"""

        # Получаем все продукты из базы данных
        products = Product.objects.all()
        
        if request.user.is_authenticated:
            # Если пользователь аутентифицирован, получаем продукты в корзине из базы данных
            cart_products = Cart.objects.filter(user=request.user)
            products_in_cart = cart_products.values_list('products_id', flat=True)
        else:
            # Если пользователь не аутентифицирован, получаем корзину из сессии
            cart = request.session.get('cart', {})
            products_in_cart = cart.keys()
            cart_products = [{'products_id': int(product_id), 'weight': weight} for product_id, weight in cart.items()]

        context = {
            "products": products,
            "products_in_cart": products_in_cart,
            "cart_products": cart_products,
        }
        return render(request, self.template_name, context)
