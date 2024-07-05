from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from .models import Order, OrderItem
from catalog.models import Product
from .forms import OrderForm
from .telegram_message import send_telegram_message_sync


def orders(request):
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
        total_price = sum(cart.price for cart in carts)
    else:
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
    templates = 'orders/orders.html'
    return render(request, templates, context)

def orders_add(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                order.user = request.user
                order.save()
                carts = Cart.objects.filter(user=request.user)
                for cart in carts:
                    OrderItem.objects.create(
                        order=order,
                        product_image=cart.products.image,
                        product_name=cart.products.name,
                        product_weight=cart.weight,
                        product_price=cart.price
                    )
                # Пересчитываем и сохраняем общую и доставочную стоимость заказа
                order_items = OrderItem.objects.filter(order=order)
                order_total_price = sum(item.product_price for item in order_items)
                delivery_price = 0 if order_total_price >= 1500 else 300
                order.total_price = order_total_price
                order.delivery_price = delivery_price
                order.save()
                # Формируем текст сообщения с информацией о заказе и его позициях
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

                chat_ids = ['784184639', '535774072']
                result = send_telegram_message_sync(chat_ids, message)
                if not result:
                    print("Ошибка при отправке сообщения в Telegram")

                carts.delete()
        return redirect('orders:history_orders')
    else:
        message = "Для создания и сохранение истории ваших заказов необходимо зарегистрироваться."
        context = {
            'message': message,
        }
        return render(request, 'orders/orders-history.html', context)

@login_required
def orders_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == "POST":
        order.delete()
    return redirect('orders:history_orders')

def history_orders(request):
    if request.user.is_authenticated:
        history_orders = Order.objects.filter(user=request.user)
        context = {
            'history_orders': history_orders,
        }
        template = 'orders/orders-history.html'
        return render(request, template, context)
    else:
        message = "Для просмотра истории заказов необходимо зарегистрироваться."
        context = {
            'message': message,
        }
        return render(request, 'orders/orders-history.html', context)