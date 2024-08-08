from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from cart.models import Cart
from catalog.models import Product

class CartView(View):
    """Представление для отображения корзины покупок"""

    template_name = "cart/cart.html"
    
    def get(self, request):
        """Обрабатывает GET-запрос для отображения содержимого корзины"""

        if request.user.is_authenticated:
            # Если пользователь аутентифицирован, получаем корзину из базы данных
            carts = Cart.objects.filter(user=request.user)
            # Рассчитываем общую стоимость корзины
            total_price = sum(cart.weight * cart.products.fix_price for cart in carts)
        else:
            # Если пользователь не аутентифицирован, получаем корзину из сессии
            cart = request.session.get('cart', {})
            carts = [{'product': Product.objects.get(id=product_id),
                      'weight': weight,
                      'price': weight * Product.objects.get(id=product_id).fix_price}
                      for product_id, weight in cart.items()
            ]
            # Рассчитываем общую стоимость корзины
            total_price = sum(item['price'] for item in carts)

        context = {
            "carts": carts,
            "total_price": total_price,
        }
        return render(request, self.template_name, context)

class CartAddView(View):
    """Представление для добавления продукта в корзину"""

    def post(self, request, product_id):
        """Обрабатывает POST-запрос для добавления продукта в корзину"""

        product = get_object_or_404(Product, id=product_id)
        if request.user.is_authenticated:
            # Если пользователь аутентифицирован, обновляем корзину в базе данных
            cart, created = Cart.objects.get_or_create(products=product, user=request.user)
            cart.weight += 0.5
            cart.price = cart.weight * product.fix_price
            cart.save()
        else:
            # Если пользователь не аутентифицирован, обновляем корзину в сессии
            cart = request.session.get('cart', {})
            if str(product_id) in cart:
                cart[str(product_id)] += 0.5
            else:
                cart[str(product_id)] = 0.5
            request.session['cart'] = cart
            request.session.modified = True
        # Перенаправляем обратно на страницу, с которой пришел запрос
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

class CartRemoveView(View):
    """Представление для удаления продукта из корзины"""

    def post(self, request, product_id):
        """Обрабатывает POST-запрос для удаления продукта из корзины"""

        product = get_object_or_404(Product, id=product_id)
        if request.user.is_authenticated:
            # Если пользователь аутентифицирован, обновляем корзину в базе данных
            cart = Cart.objects.filter(products=product, user=request.user).first()
            if cart:
                if cart.weight > 0.5:
                    cart.weight -= 0.5
                    cart.price = cart.weight * product.fix_price
                    cart.save()
                else:
                    cart.delete()
        else:
            # Если пользователь не аутентифицирован, обновляем корзину в сессии
            cart = request.session.get('cart', {})
            if str(product_id) in cart:
                if cart[str(product_id)] > 0.5:
                    cart[str(product_id)] -= 0.5
                else:
                    del cart[str(product_id)]
                request.session['cart'] = cart
                request.session.modified = True
        # Перенаправляем обратно на страницу, с которой пришел запрос
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
