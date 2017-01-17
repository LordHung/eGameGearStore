from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
# from products.views import ProductDetailView
from .views import ProductDetailView
from products import views as prod_detail

urlpatterns = [
    # functionview sample, error multiple id here??
    # url(r'^(?P<id>\d+)',prod_detail.product_detail_view_func,name='product_detail_view_function'),
    # classbaseview sample
    url(r'^(?P<pk>\d+)',ProductDetailView.as_view(),name='product_detail'),
]
