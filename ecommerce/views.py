from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.shortcuts import render
from .models import Product, Order, OrderItem

def product_list(request):
    products = Product.objects.all()
    print(products)
    return render(request, 'product/product_list.html', {'products': products})



def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product/product_detail.html', {'product': product})



def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    product_id_str = str(product.id)
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        cart[product_id_str] = {'quantity': 1}
    request.session['cart'] = cart
    return redirect('cart_detail')



def cart_detail(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0
    for id, item in cart.items():
        product = Product.objects.get(id=id)
        quantity = item['quantity']
        subtotal = product.price * quantity
        total += subtotal
        products.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal})
    return render(request, 'product/cart_detail.html', {
        'products': products,
        'total': total})




def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)
    if product_id in cart:
        del cart[product_id]
    request.session['cart'] = cart
    return redirect('cart_detail')





def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)
    if product_id in cart:
        cart[product_id]['quantity'] += 1
    request.session['cart'] = cart
    return redirect('cart_detail')




def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)
    if product_id in cart:
        cart[product_id]['quantity'] -= 1
        if cart[product_id]['quantity'] <= 0:
            del cart[product_id]
    request.session['cart'] = cart
    return redirect('cart_detail')


@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart_detail')
    order = Order.objects.create(
        user=request.user,
        payment_method='cod')
    total_price = 0
    for product_id, item in cart.items():
        product = Product.objects.get(id=product_id)
        quantity = item['quantity']
        subtotal = product.price * quantity
        total_price += subtotal
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price)
    order.total_price = total_price
    order.save()
    request.session['cart'] = {}
    return render(request, 'product/order_success.html', {'order': order})



@login_required
def order_history(request):
    orders = request.user.order_set.all().order_by('-created_at')
    return render(request, 'product/order_history.html', {'orders': orders})