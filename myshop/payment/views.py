from decimal import Context, Decimal, getcontext
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm
from orders.models import Order
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def payment_done(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    order.paid = True
    order.status = "Pedido"
    order.save()
    return render(request,'payment/done.html', {'order':order})


@csrf_exempt
def payment_canceled(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    order.status = "Pedido"
    order.save()
    return render(request,'payment/canceled.html')


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    order.status = 'Pedido'
    order.save()
    host = request.get_host()
    if request.method == 'POST' and 'cash_payment' in request.POST:
        return render(request, 'orders/order/created.html', {'order': order})

    paypal_dict ={
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': order.get_total_cost(),
        #'amount': '%.2f'% decimal (order.get_total_cost()).quantize(decimal('.01')),
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'MXN',
        'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,reverse('payment:done')),
        'cancel_return': 'http://{}{}'.format(host,reverse('payment:canceled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request,'payment/process.html',{'order':order,'form':form})
