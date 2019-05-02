from django.shortcuts import render, redirect
from django.urls import reverse
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart

def order_create(request):
    valid = True
    invalid = ""
    cart = Cart(request)
    if request.method == 'POST' and 'store_pickup' in request.POST:
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.address = 'En tienda'
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                        product=item['product'],
                                        price=item['price'],
                                        quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            #order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect to the payment
        return redirect(reverse('payment:process'))
        #return render(request, 'orders/order/created.html', {'order': order})
    elif request.method == 'POST' and 'home_delivery' in request.POST:
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            #order.postal_code = Postal_Code.postal_code.filter(postal_code=0)
            if order.postal_code and order.address:
                order.save()
                for item in cart:
                    OrderItem.objects.create(order=order,
                                            product=item['product'],
                                            price=item['price'],
                                            quantity=item['quantity'])
                # clear the cart
                cart.clear()
                # launch asynchronous task
                #order_created.delay(order.id)
                return redirect(reverse('payment:process'))
                #return render(request, 'orders/order/created.html', {'order': order})
        #address and postal_code not introduced
        valid = False
        invalid = "Para entregas a domicilio por favor ingrese una dirección"
        return render(request,
                          'orders/order/create.html',
                          {'cart': cart, 'form': form, 'valid':valid, 'invalid':invalid})
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})
