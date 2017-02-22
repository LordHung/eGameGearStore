from django.db.models import Q
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404
from .models import Product
from django.utils import timezone
# Create your views here.


class ProductListView(ListView):
    model = Product
    queryset = Product.objects.all()
    #queryset = Product.objects.filter(active=False)

    # overriding context data of ListView
    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(
            *args, **kwargs)
        # print(context)
        context['now'] = timezone.now()
        context['query'] = self.request.GET.get('q')
        return context

    # search query
    def get_queryset(self, *args, **kwargs):
        qs = super(ProductListView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')
        if query:
            qs = self.model.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
            try:
                qs2 = self.model.objects.filter(
                    Q(price=query)
                )
                qs = (qs | qs2).distinct()
            except:
                pass
        return qs


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
