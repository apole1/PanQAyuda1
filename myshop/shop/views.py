from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.core.paginator import Paginator
from django.db.models import Q
import operator
from functools import reduce


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products_list = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products_list = products_list.filter(category=category)
    query = request.GET.get("q")
    if query:
        query_list = query.split()
        products_list = products_list.filter(
            reduce(operator.and_, (Q(name__icontains=q) for q in query_list)) |
            reduce(operator.and_, (Q(description__icontains=q) for q in query_list))
        ).distinct()
    paginator = Paginator(products_list, 12) # Show 12 products per page
    page = request.GET.get('page')
    products = paginator.get_page(page)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})

def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})
