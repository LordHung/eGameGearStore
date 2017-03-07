from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404, redirect
from .forms import VariationInventoryFormSet
from .models import Product, Variation, Category
from .mixins import StaffRequiredMixin, LoginRequiredMixin
from django.utils import timezone
# from django.core.urlresolvers import reverse
# Create your views here.


class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.all()
    template_name = "products/product_list.html"


class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(
            *args, **kwargs)
        obj = self.get_object()
        product_set = obj.product_set.all()
        default_products = obj.default_category.all()
        products = (product_set | default_products).distinct()
        context['products'] = products
        return context


class VariationListView(StaffRequiredMixin, ListView):
    """docstring for VariationListView."""
    model = Variation
    queryset = Variation.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(VariationListView, self).get_context_data(
            *args, **kwargs)
        context['formset'] = VariationInventoryFormSet(
            queryset=self.get_queryset())
        return context

    def get_queryset(self, *args, **kwargs):
        product_pk = self.kwargs.get('pk')
        if product_pk:
            product = get_object_or_404(Product, pk=product_pk)
            queryset = Variation.objects.filter(product=product)
        return queryset

    def post(self, request, *args, **kwargs):
        #
        formset = VariationInventoryFormSet(request.POST, request.FILES)
        print(request.POST)
        if formset.is_valid():
            formset.save(commit=False)
            for form in formset:
                new_item = form.save(commit=False)
                product_pk = self.kwargs.get('pk')
                product = get_object_or_404(Product, pk=product_pk)
                new_item.product = product
                new_item.save()

            messages.success(
                request, 'Your inventory and pricing has been updated.')
            return redirect('/products/')
        raise Http404


class ProductListView(ListView):
    model = Product
    queryset = Product.objects.all()
    # queryset = Product.objects.filter(active=False)

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

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(
            *args, **kwargs)
        instance = self.get_object()
        # order by ?, limit to 6 products
        context['related'] = Product.objects.get_related(
            instance).order_by('?')[:6]
        return context


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
