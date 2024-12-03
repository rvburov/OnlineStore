from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from cart.models import Cart
from catalog.models import Product
from django.http import JsonResponse

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

            total_price = sum(item.weight * item.products.fix_price for item in Cart.objects.filter(user=request.user))
            # Общее количество товаров в корзине в навигаторе
            total_items = Cart.objects.filter(user=request.user).count()
        else:
            # Если пользователь не аутентифицирован, обновляем корзину в сессии
            cart = request.session.get('cart', {})
            if str(product_id) in cart:
                cart[str(product_id)] += 0.5
            else:
                cart[str(product_id)] = 0.5
            request.session['cart'] = cart
            request.session.modified = True

            total_price = sum(
                weight * Product.objects.get(id=int(product_id)).fix_price
                for product_id, weight in cart.items()
            )
            # Общее количество товаров в корзине в навигаторе
            total_items = len(cart)
        # Перенаправляем обратно на страницу, с которой пришел запрос
        return JsonResponse({
            "weight": cart.weight if request.user.is_authenticated else cart[str(product_id)],
            "price": cart.price if request.user.is_authenticated else cart[str(product_id)] * product.fix_price,
            "total_price": total_price,
            "total_items": total_items,  # Общее количество товаров в корзине в навигаторе
        })

class CartRemoveView(View):
    """Представление для удаления продукта из корзины"""

    def post(self, request, product_id):
        """Обрабатывает POST-запрос для удаления продукта из корзины"""

        product = get_object_or_404(Product, id=product_id)
        product_removed = False  # Флаг для удаления продукта из корзины
        is_cart_empty = False  # Флаг для проверки, пуста ли корзина
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
                    product_removed = True  # Обновляем флаг при удалении продукта
            # Проверка, пуста ли корзина
            is_cart_empty = not Cart.objects.filter(user=request.user).exists()
            total_price = sum(
                item.weight * item.products.fix_price
                for item in Cart.objects.filter(user=request.user)
            )
            total_items = Cart.objects.filter(user=request.user).count()
        else:
            # Если пользователь не аутентифицирован, обновляем корзину в сессии
            cart = request.session.get('cart', {})
            if str(product_id) in cart:
                if cart[str(product_id)] > 0.5:
                    cart[str(product_id)] -= 0.5
                else:
                    del cart[str(product_id)]
                    product_removed = True  # Обновляем флаг при удалении продукта
                request.session['cart'] = cart
                request.session.modified = True

            # Проверка, пуста ли корзина
            is_cart_empty = not cart
            # Пересчитываем общую стоимость корзины для сессии
            total_price = sum(
                weight * Product.objects.get(id=int(product_id)).fix_price
                for product_id, weight in cart.items()
            )
            total_items = len(cart)

        # Возвращаем JSON-ответ с актуальными данными
        return JsonResponse({
            "weight": 0 if product_removed else (cart.weight if request.user.is_authenticated else cart.get(str(product_id), 0)),
            "price": 0 if product_removed else (cart.price if request.user.is_authenticated else cart.get(str(product_id), 0) * product.fix_price),
            "total_price": total_price,
            "total_items": total_items,  # Общее количество товаров
            "removed": product_removed,  # Указывает, что продукт удалён
            "is_cart_empty": is_cart_empty,  # Указывает, пуста ли корзина
        })
