from django.test import TestCase
from django.db import models
from shop.models import Category, Product
from orders.models import  Order, Postal_Code, OrderItem
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils.timezone import datetime
import pytz


class OrderTest(TestCase):
    def setUp(self):
        u = User.objects.create(username="UsuarioPrueba", password="PasswordPrueba")
        zip = Postal_Code.objects.create(postal_code="12345")
        o = Order.objects.create(user=u, first_name="Señor", last_name="Prueba", email="correo@prue.ba", phone="1234567890",
                  address="Dir Prueba", postal_code=zip, status="Creado",
                  created=models.DateTimeField(auto_now_add=True), updated=models.DateTimeField(auto_now=True),
                  paid=False)
        c1 = Category.objects.create(name="Test Categoria", slug=slugify("Test Categoria"))
        p1 = Product.objects.create(category=c1, name="Test Producto", slug=slugify("Test Producto"), price=10,
                  available=True, created=models.DateTimeField(auto_now_add=True),
                  updated=models.DateTimeField(auto_now=True))
        p2 = Product.objects.create(category=c1, name="Test Producto 2", slug=slugify("Test Producto 2"), price=5.5,
                                    available=True, created=models.DateTimeField(auto_now_add=True),
                                    updated=models.DateTimeField(auto_now=True))
        oi1 = OrderItem.objects.create(order=o, product=p1, price=p1.price, quantity=1)
        oi2 = OrderItem.objects.create(order=o, product=p2, price=p2.price, quantity=2)

    #Check fields are correctly saved
    def test_string_order(self):
        u = User.objects.get(username="UsuarioPrueba")
        o = Order.objects.get(user=u)
        zip = Postal_Code.objects.get(postal_code="12345")
        #login = self.client.login(username='UsuarioPrueba', password='PasswordPrueba')
        self.assertEqual(o.user, u)
        self.assertEqual(o.first_name, "Señor")
        self.assertEqual(o.last_name, "Prueba")
        self.assertEqual(o.postal_code, zip)

    # Check the cost for individual products of an order
    def test_partial_order1(self):
        u = User.objects.get(username="UsuarioPrueba")
        o = Order.objects.get(user=u)
        p1 = Product.objects.get(name="Test Producto")
        oi1 = OrderItem.objects.get(order=o, product=p1)
        self.assertEqual(oi1.get_cost(), 10)

    # Check for multiple products of the same type of an order
    def test_partial_order2(self):
        u = User.objects.get(username="UsuarioPrueba")
        o = Order.objects.get(user=u)
        p2 = Product.objects.get(name="Test Producto 2")
        oi1 = OrderItem.objects.get(order=o, product=p2)
        self.assertEqual(oi1.get_cost(), 11)

    # Check the total cost of the order
    def test_total_order(self):
        u = User.objects.get(username="UsuarioPrueba")
        o = Order.objects.get(user=u)
        p = Order.objects.get()

        #oi1 = OrderItem.objects.get(order=o, product=p1, price=p1.price, quantity=1)
        self.assertEqual(o.get_total_cost(), 21)

class OrderDefaultTest(TestCase):
    def setUp(self):
        u = User.objects.create(username="UsuarioPrueba", password="PasswordPrueba")
        zip = Postal_Code.objects.create(postal_code="12345")
        o = Order.objects.create(user=u, first_name="Señor", last_name="Prueba", email="correo@prue.ba", phone="1234567890",
                  address="Dir Prueba", postal_code=zip, status="Creado",
                  created=models.DateTimeField(auto_now_add=True), updated=models.DateTimeField(auto_now=True))

    #Check orders are created as not paid, even if it's not explicitly indicated
    def test_default_paid(self):
        u = User.objects.get(username="UsuarioPrueba")
        o = Order.objects.get(user=u)
        self.assertEqual(o.paid, False)

class OrderTimeCreated(TestCase):
    def setUp(self):
        u = User.objects.create(username="UsuarioPrueba", password="PasswordPrueba")
        zip = Postal_Code.objects.create(postal_code="12345")
        o = Order.objects.create(user=u, first_name="Señor", last_name="Prueba", email="correo@prue.ba", phone="1234567890",
                  address="Dir Prueba", postal_code=zip, status="Creado",
                  created=models.DateTimeField(datetime.now()), updated=models.DateTimeField(auto_now=True))
    #Check orders time
    def test_order(self):
        u = User.objects.get(username="UsuarioPrueba")
        o = Order.objects.get(user=u)
        utc = pytz.UTC
        date = o.created.replace(tzinfo=utc)
        a = datetime.now().replace(tzinfo=utc)
        self.assertLess(a, o.created)

