from django.shortcuts import render
from .models import OrderItem, Postal_Code
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created


def order_create(request):
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
        return render(request,
                          'orders/order/created.html',
                          {'order': order})
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
                return render(request,
                              'orders/order/created.html',
                              {'order': order})
        return render(request,
                          'orders/order/create.html',
                          {'cart': cart, 'form': form})
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})
