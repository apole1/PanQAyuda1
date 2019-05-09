from django.test import TestCase
from django.db import models
from django.core.paginator import Paginator
from .models import Product, Category
from django.template.defaultfilters import slugify


class OrderTest(TestCase):
    def setUp(self):
        c = Category.objects.create(name="Test Categoria", slug=slugify("Test Categoria"))

    # 60 products stores in a pagination of 12 products per page should return 5 pages
    def test_pagination(self):
        c = Category.objects.get(name="Test Categoria")
        for i in range(60):
            Product.objects.create(category=c, name=str(i), slug=slugify(str(i)), price=i,
                                   available=True, created=models.DateTimeField(auto_now_add=True),
                                   updated=models.DateTimeField(auto_now=True))
        p = Paginator(Product.objects.all(), 12)
        self.assertEqual(p.count, 60)
        self.assertEqual(p.num_pages, 5)
        self.assertEqual(list(p.page_range), [1, 2, 3, 4, 5])

    #Not enough products to have more than one page
    def test_false_next(self):
        c = Category.objects.get(name="Test Categoria")
        for i in range(5):
            Product.objects.create(category=c, name=str(i), slug=slugify(str(i)), price=i,
                                   available=True, created=models.DateTimeField(auto_now_add=True),
                                   updated=models.DateTimeField(auto_now=True))
        paginator = Paginator(Product.objects.all(), 12)
        p = paginator.page(1)
        self.assertFalse(p.has_next())
        self.assertFalse(p.has_previous())

    def test_true_next(self):
        c = Category.objects.get(name="Test Categoria")
        for i in range(58):
            Product.objects.create(category=c, name=str(i), slug=slugify(str(i)), price=i,
                                   available=True, created=models.DateTimeField(auto_now_add=True),
                                   updated=models.DateTimeField(auto_now=True))
        paginator = Paginator(Product.objects.all(), 12)
        p = paginator.page(1)
        self.assertEqual(12, p.end_index())
        self.assertTrue(p.has_other_pages())
        self.assertTrue(p.has_next())
        p = paginator.page(5)
        self.assertFalse(p.has_next())
        self.assertEqual(58, p.end_index())