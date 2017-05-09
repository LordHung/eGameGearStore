from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404, redirect
from .forms import VariationInventoryFormSet, ProductFilterForm
from .models import Product, Variation, Category
from .mixins import StaffRequiredMixin, LoginRequiredMixin
from django.utils import timezone

from django_filters import FilterSet, CharFilter, NumberFilter, filters
import random
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


class ProductFilter(FilterSet):
    # lookup_type is deprecated, now we use lookup_expr the same
    title = CharFilter(
        name='title', lookup_expr='icontains', distinct=True)
    category = CharFilter(
        name='categories__title', lookup_expr='icontains', distinct=True)
    category_id = CharFilter(
        name='categories__id', lookup_expr='icontains', distinct=True)
    # some_price_gte=somequery, variation__price to get the related field price
    min_price = NumberFilter(name='variation__price',
                             lookup_expr='gte', distinct=True)
    max_price = NumberFilter(name='variation__price',
                             lookup_expr='lte', distinct=True)

    class Meta:
        """ define model """
        model = Product
        fields = [
            'min_price',
            'max_price',
            'category',
            'title',
            'description',
        ]


# def product_list(request):
#     """ test filter with func base view """
#     qs = Product.objects.all()
#     ordering = request.GET.get('ordering')
#     if ordering:
#         qs = Product.objects.all().order_by(ordering)
#     f = ProductFilter(request.GET, queryset=qs)
#     # need .qs because in ver 1.0 filterset no longer have __iter__ function
# return render(request, 'products/product_list.html', {'object_list':
# f.qs})


class FilterMixin(object):
    filter_class = None
    search_ordering_param = 'ordering'

    def get_queryset(self, *args, **kwargs):
        try:
            qs = super(FilterMixin, self).get_queryset(*args, **kwargs)
            return qs
        except:
            raise ImproperlyConfigured(
                'You must have a qs in order to use FilterMixin')

    def get_context_data(self, *args, **kwargs):
        context = super(FilterMixin, self).get_context_data(*args, **kwargs)
        qs = self.get_queryset()
        ordering = self.request.GET.get(self.search_ordering_param)
        if ordering:
            qs = qs.order_by(ordering)
        filter_class = self.filter_class
        if filter_class:
            f = filter_class(self.request.GET, queryset=qs)
            context['object_list'] = f.qs
        return context


class ProductListView(FilterMixin, ListView):
    model = Product
    queryset = Product.objects.all()
    filter_class = ProductFilter
    # queryset = Product.objects.filter(active=False)

    # overriding context data of ListView
    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(
            *args, **kwargs)
        # print(context)
        context['now'] = timezone.now()
        context['query'] = self.request.GET.get('q')
        context['filter_form'] = ProductFilterForm(
            data=self.request.GET or None)
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
        # order_by['-title'] can be replace below; limit to 6 products
        context['related'] = sorted(Product.objects.get_related(
            instance)[:6], key=lambda x: random.random(), reverse=True)
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
