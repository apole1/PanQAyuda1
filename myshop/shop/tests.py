from __future__ import unicode_literals
from decimal import Decimal as D
from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify
from shop.models import *  # noqa
from myshop import settings as scs
from django.http import Http404, HttpResponseRedirect
# Create your tests here.


def create_categorization(model, name, **kwargs):
    filters = {
        'name': name,
        'slug': slugify(name),
    }
    filters.update(kwargs)
    return model.objects.language().create(**filters)

def create_product(name, unit_price=100, **kwargs):
    filters = {
        'category': 'Categoria1',
        'name': name,
        'slug': slugify(name),
        'description': 'SOy el producto',
        'price': D(unit_price),
    }
    filters.update(kwargs)
    return Product.objects.language().create(**filters)


def create_category(name, **kwargs):
    return create_categorization(Category, name, **kwargs)


#class CatalogModelTestCase(TestCase):
 #   def setUp(self):
  #      TestCatalogModel = type(str('TestCatalogModel'), (CatalogModel,),
   #                             {'__module__': __name__})
    #    self.model = TestCatalogModel(
     #       pk=1, active=True, date_added=datetime.now,
      #      last_modified=datetime.now)
#
 #   def test_get_absolute_url(self):
  #          self.assertIsNone(self.model.get_absolute_url())
#
 #   def test_get_name(self):
  #              self.assertEquals(self.model.get_name(), '1')

   # def test_get_slug(self):
    #            self.assertEquals(self.model.get_slug(), '1')

    #def test_as_dict(self):
     #           self.assertIsInstance(self.model.as_dict, dict)
class CategoryTestCase(TestCase):

    def setUp(self):

        self.cat = Category.objects.create(name='Cat', slug='cat')

    def test_get_absolute_url(self):

        self.assertEquals(

            self.cat.get_absolute_url(),
            return HttpResponseRedirect(reverse('/shop', args=['cat'])))
