from __future__ import unicode_literals
from decimal import Decimal as D
from datetime import datetime
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
