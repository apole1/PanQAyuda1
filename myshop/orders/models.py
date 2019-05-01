from django.db import models
from shop.models import Product
from django.contrib.auth.models import User

class Postal_Code(models.Model):
    postal_code = models.IntegerField(db_index=True, default=0)

    class Meta:
        ordering = ('postal_code',)
        verbose_name = 'Postal Code'
        verbose_name_plural = 'Postal Codes'

    def __str__(self):
        return self.postal_code.__str__()

class Order(models.Model):
    user = models.ForeignKey(User, related_name='Client', on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250, blank=True)
    postal_code = models.ForeignKey(Postal_Code, related_name='zipcode', on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
