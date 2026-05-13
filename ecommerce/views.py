from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.shortcuts import  get_object_or_404
from .models import Product, Order, OrderItem
from .forms import CheckoutForm, CardPaymentForm, RegistrationForm
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('product_list')



def send_order_email(request):
    user = request.user
    subject = "Order Confirmation"
    message = f"""
    Dear {user.username},
    We are pleased to inform you that your order has been created successfully.
    Thank you for shopping with us."""
    send_mail(subject,message,settings.DEFAULT_FROM_EMAIL,[user.email],fail_silently=False)


@login_required
def profile(request):
    return render(request, 'profile/profile.html')



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
    return render(request, 'product/cart_detail.html', {'products': products,'total': total})




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
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            checkout_data = form.cleaned_data
            request.session['checkout_data'] = checkout_data
            payment_method = checkout_data['payment_method']
            if payment_method == 'card':
                return redirect('card_payment')
            return redirect('complete_order')
    else:
        form = CheckoutForm()
    return render(request, 'product/checkout.html', {'form': form})





@login_required
def order_history(request):
    orders = request.user.order_set.all().order_by('-created_at')
    return render(request, 'product/order_history.html', {'orders': orders})





@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    send_order_email(request)
    return render(request, 'product/order_success.html', {'order': order})




@login_required
def card_payment(request):
    if request.method == 'POST':
        form = CardPaymentForm(request.POST)
        if form.is_valid():
            card_number = form.cleaned_data['card_number']
            # if len(card_number) != 16:
            #     messages.error(request, "Invalid card")
            #     return redirect('card_payment')
            request.session['payment_success'] = True
            return redirect('complete_order')
    else:
        form = CardPaymentForm()
    return render(request, 'product/card_payment.html', {'form': form})



@login_required
def complete_order(request):
    checkout_data = request.session.get('checkout_data')
    if not checkout_data:
        return redirect('checkout')
    payment_method = checkout_data['payment_method']
    if payment_method == 'stub':
        payment_success = request.session.get('payment_success',False)
        if not payment_success:
            return redirect('card_payment')
    cart = request.session.get('cart', {})
    order = Order.objects.create(user=request.user,payment_method=payment_method)
    total_price = 0
    products = Product.objects.filter(id__in=cart.keys())
    for product in products:
        quantity = cart[str(product.id)]['quantity']
        subtotal = product.price * quantity
        total_price += subtotal
        product.stock -= quantity
        product.save()
        OrderItem.objects.create(order=order,product=product,quantity=quantity,price=product.price)
    order.total_price = total_price
    order.save()
    request.session['cart'] = {}
    request.session['payment_success'] = False
    return redirect('order_success',order_id=order.id)
