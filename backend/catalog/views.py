from django.shortcuts import render
from django.views import View
from .models import Product
from cart.models import Cart
from collections import defaultdict

class ProductListView(View):
    """Представление для отображения списка продуктов по категориям"""

    template_name = "catalog/product_list.html"
    
    def get(self, request):
        """Обрабатывает GET-запрос для отображения продуктов по категориям"""

        # Получаем продукты и группируем их по категориям
        products = Product.objects.all()
        products_by_category = defaultdict(list)
        for product in products:
            products_by_category[product.category].append(product)
        
        if request.user.is_authenticated:
            cart_products = Cart.objects.filter(user=request.user)
            products_in_cart = cart_products.values_list('products_id', flat=True)
        else:
            cart = request.session.get('cart', {})
            products_in_cart = cart.keys()
            cart_products = [{'products_id': int(product_id), 'weight': weight} for product_id, weight in cart.items()]

        context = {
            "products_by_category": products_by_category.items(),  # Здесь важно вызвать `.items()`
            "products_in_cart": products_in_cart,
            "cart_products": cart_products,
        }
        return render(request, self.template_name, context)
