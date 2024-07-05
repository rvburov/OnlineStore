from django.shortcuts import render
from .models import Product
from cart.models import Cart


def product_list(request):
    products = Product.objects.all()
    
    if request.user.is_authenticated:
        cart_products = Cart.objects.filter(user=request.user)
        products_in_cart = cart_products.values_list('products_id', flat=True)
    else:
        cart = request.session.get('cart', {})
        products_in_cart = cart.keys()
        cart_products = [{'products_id': int(product_id), 'weight': weight} for product_id, weight in cart.items()]

    context = {
        "products": products,
        "products_in_cart": products_in_cart,
        "cart_products": cart_products,
    }
    template = "catalog/product_list.html"
    return render(request, template, context)
