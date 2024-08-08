from django.urls import path
from .views import CartView, CartAddView, CartRemoveView

app_name = 'cart'

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart_add/<int:product_id>/', CartAddView.as_view(), name='cart_add'),
    path('cart_remove/<int:product_id>/', CartRemoveView.as_view(), name='cart_remove'),
]
