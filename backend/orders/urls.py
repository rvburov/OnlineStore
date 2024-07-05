from django.urls import path
from . import views


app_name = 'orders'

urlpatterns = [
    path('orders/', views.orders, name='orders'),
    path('orders_add', views.orders_add, name='orders_add'),
    path('orders_delete/<int:order_id>/', views.orders_delete, name='orders_delete'),
    path('history_orders/', views.history_orders, name='history_orders'),
]
