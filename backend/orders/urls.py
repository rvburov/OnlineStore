from django.urls import path
from .views import OrdersView, OrdersAddView, OrdersDeleteView, HistoryOrdersView

app_name = 'orders'

urlpatterns = [
    path('orders/', OrdersView.as_view(), name='orders'),
    path('orders_add/', OrdersAddView.as_view(), name='orders_add'),
    path('orders_delete/<int:order_id>/', OrdersDeleteView.as_view(), name='orders_delete'),
    path('history_orders/', HistoryOrdersView.as_view(), name='history_orders'),
]
