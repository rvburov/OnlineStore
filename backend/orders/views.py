from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from cart.models import Cart
from .models import Order, OrderItem
from catalog.models import Product
from .forms import OrderForm
from .telegram_message import send_telegram_message_sync
from decouple import config

class OrdersView(View):
    """Представление для отображения заказа покупок"""
    template_name = 'orders/orders.html'

    def get(self, request):
        """Обрабатывает GET-запрос для отображения текущей корзины пользователя"""
        if request.user.is_authenticated:
            # Если пользователь аутентифицирован, получаем корзину из базы данных
            carts = Cart.objects.filter(user=request.user)
            total_price = sum(cart.price for cart in carts)
        else:
            # Если пользователь не аутентифицирован, получаем корзину из сессии
            cart = request.session.get('cart', {})
            carts = [{'products': Product.objects.get(id=product_id), 'weight': weight, 'price': weight * Product.objects.get(id=product_id).fix_price} for product_id, weight in cart.items()]
            total_price = sum(item['price'] for item in carts)
        
        delivery_price = 0 if total_price >= 1500 else 300
        forms = OrderForm()
        context = {
            "forms": forms,
            "carts": carts,
            "total_price": total_price,
            "delivery_price": delivery_price,
        }
        return render(request, self.template_name, context)

class OrdersAddView(View):
    """Представление для создания заказа покупок"""
    template_name = 'orders/orders-history.html'

    def post(self, request):
        """Обрабатывает POST-запрос для создания нового заказа"""
        if not request.user.is_authenticated:
            # Если пользователь не аутентифицирован, отображаем сообщение об ошибке
            return self._render_error_message(request, "Для создания и сохранение истории ваших заказов необходимо зарегистрироваться.")
        
        form = OrderForm(request.POST)
        if not form.is_valid():
            # Если форма заказа не валидна, отображаем сообщение об ошибке
            return self._render_error_message(request, "Неверные данные формы.")

        # Создаем заказ, элементы заказа и обновляем цены
        order = self._create_order(form, request.user)
        self._create_order_items(order, request.user)
        self._update_order_prices(order)
        self._send_order_notification(order)

        # Удаляем все корзины пользователя после успешного создания заказа
        Cart.objects.filter(user=request.user).delete()
        return redirect('orders:history_orders')

    def _create_order(self, form, user):
        """Создает и сохраняет заказ"""
        order = form.save(commit=False)
        order.user = user
        order.save()
        return order

    def _create_order_items(self, order, user):
        """Создает элементы заказа на основе корзины пользователя"""
        carts = Cart.objects.filter(user=user)
        for cart in carts:
            OrderItem.objects.create(
                order=order,
                product_image=cart.products.image,
                product_name=cart.products.name,
                product_weight=cart.weight,
                product_price=cart.price
            )

    def _update_order_prices(self, order):
        """Обновляет общую стоимость заказа и стоимость доставки"""
        order_items = OrderItem.objects.filter(order=order)
        order_total_price = sum(item.product_price for item in order_items)
        delivery_price = 0 if order_total_price >= 1500 else 300
        order.total_price = order_total_price
        order.delivery_price = delivery_price
        order.save()

    def _send_order_notification(self, order):
        """Отправляет уведомление о новом заказе через Telegram"""
        order_items = OrderItem.objects.filter(order=order)
        message = f'***** Новый заказ создан! *****\n\n'
        message += f'Имя: {order.name}\n'
        message += f'Телефон: {order.phone}\n'
        message += f'Адрес: {order.address}\n'
        message += f'Дата и время доставки: {order.time}\n\n'
        message += f'Список продуктов:\n'
        for item in order_items:
            message += f'{item.product_name} - {item.product_weight} кг - {item.product_price} руб\n\n'
        message += f'Итоговая стоимость: {order.total_price}\n'
        message += f'Стоимость доставки: {order.delivery_price}\n'

        # Использование ID чатов из .env
        send_telegram_message_sync(config('TELEGRAM_CHAT_IDS').split(','), message)

    def _render_error_message(self, request, message):
        """Отображает сообщение об ошибке пользователю"""
        context = {'message': message}
        return render(request, self.template_name, context)

class OrdersDeleteView(LoginRequiredMixin, View):
    """Представление для удаление заказа покупок"""

    def post(self, request, order_id):
        """Обрабатывает POST-запрос для удаления заказа"""
        order = get_object_or_404(Order, id=order_id, user=request.user)
        order.delete()
        return redirect('orders:history_orders')

class HistoryOrdersView(View):
    """Представление для отображения истории заказа покупок"""
    template_name = 'orders/orders-history.html'

    def get(self, request):
        """Обрабатывает GET-запрос для отображения истории заказов пользователя"""
        if request.user.is_authenticated:
            # Если пользователь аутентифицирован, получаем историю заказов из базы данных
            history_orders = Order.objects.filter(user=request.user).order_by('-created_at')
            context = {'history_orders': history_orders}
        else:
            # Если пользователь не аутентифицирован, отображаем сообщение о необходимости регистрации
            message = "Для просмотра истории заказов необходимо зарегистрироваться."
            context = {'message': message}
        return render(request, self.template_name, context)
