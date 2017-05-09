from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
# from products.views import ProductDetailView
# from products import views as prod_detail
from .views import ProductDetailView, ProductListView, VariationListView
from products import views as products_view


urlpatterns = [
    # functionview sample, error multiple id here??
    # url(r'^(?P<id>\d+)',prod_detail.product_detail_view_func,name='product_detail_view_function'),
    # classbaseview sample
    url(r'^$', ProductListView.as_view(), name='product_list'),
    # url(r'^$', products_view.product_list, name='product_list'),
    url(r'^(?P<pk>\d+)/$', ProductDetailView.as_view(), name='product_detail'),
    url(r'(?P<pk>\d+)/inventory/$',
        VariationListView.as_view(), name='product_inventory'),
]
