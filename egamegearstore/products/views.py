from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404
from .models import Product
from django.utils import timezone
# Create your views here.


class ProductListView(ListView):
    model = Product

    # overriding context data of ListView
    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args,**kwargs)
        # print(context)
        context['now'] = timezone.now()
        return context

class ProductDetailView(DetailView):
    model = Product
    # template_name=<appname>/<modelname>_detail.html


def product_detail_view_func(id, request):
    product_instance = Product.objects.get(id)
    # cách 1
    product_instance = get_object_or_404(Product, id=id)
    # cách 2
    try:
        product_instance = Product.objects.get(id)
    except Product.DoesNotExists:
        raise Http404

    template = 'products/product_detail.html'
    context = {
        'object': product_instance
    }
    return render(request, template, context)
