from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Product
# Create your views here.


class ProductDetailView(DetailView):

    model = Product

    def product_detail_view_func(id, request):

        product_instance = Product.objects.get(self.id=id)
        template = 'products/product_detail.html'
        context = {
            'objext' = product_instance
        }
        return render(request, template, context)
