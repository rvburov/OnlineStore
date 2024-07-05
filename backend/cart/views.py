from django.shortcuts import render, redirect, get_object_or_404
from cart.models import Cart
from catalog.models import Product

def cart(request):
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
        total_price = sum(cart.weight * cart.products.fix_price for cart in carts)
    else:
        cart = request.session.get('cart', {})
        carts = [{'product': Product.objects.get(id=product_id), 'weight': weight, 'price': weight * Product.objects.get(id=product_id).fix_price} for product_id, weight in cart.items()]
        total_price = sum(item['price'] for item in carts)

    context = {
        "carts": carts,
        "total_price": total_price,
    }
    template = "cart/cart.html"
    return render(request, template, context)

def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(products=product, user=request.user)
            cart.weight += 0.5
            cart.price = cart.weight * product.fix_price
            cart.save()
        else:
            cart = request.session.get('cart', {})
            if str(product_id) in cart:
                cart[str(product_id)] += 0.5
            else:
                cart[str(product_id)] = 0.5
            request.session['cart'] = cart
            request.session.modified = True
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            cart = Cart.objects.filter(products=product, user=request.user).first()
            if cart:
                if cart.weight > 0.5:
                    cart.weight -= 0.5
                    cart.price = cart.weight * product.fix_price
                    cart.save()
                else:
                    cart.delete()
        else:
            cart = request.session.get('cart', {})
            if str(product_id) in cart:
                if cart[str(product_id)] > 0.5:
                    cart[str(product_id)] -= 0.5
                else:
                    del cart[str(product_id)]
                request.session['cart'] = cart
                request.session.modified = True
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
