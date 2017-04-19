"""egamegearstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from egamegearstore import views as egamegearstore_view
from newsletter import views as newsletter_view
from carts.views import CartView, ItemCountView, CheckoutView,\
    CheckoutFinalView
from orders.views import AddressSelectFormView, UserAddressCreateView,\
    OrderList, OrderDetail
# from products import views as products_view

urlpatterns = [
    # Examples:
    url(r'^$', newsletter_view.home, name='home'),
    url(r'^contact/$', newsletter_view.contact, name='contact'),
    url(r'^about/$', egamegearstore_view.about, name='about'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^admin/', admin.site.urls),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^products/', include('products.urls')),
    url(r'^categories/', include('products.urls_categories')),
    url(r'^orders/(?P<pk>\d+)$', OrderDetail.as_view(), name='order_detail'),
    url(r'^orders/$', OrderList.as_view(), name='orders'),
    url(r'^cart/$', CartView.as_view(), name='cart'),
    url(r'^cart/count', ItemCountView.as_view(), name='item_count'),
    url(r'^checkout/$', CheckoutView.as_view(), name='checkout'),
    url(r'^checkout/address/$', AddressSelectFormView.as_view(),
        name='order_address'),
    url(r'^checkout/address/add/$',
        UserAddressCreateView.as_view(), name='user_address_create'),
    url(r'^checkout/final/$', CheckoutFinalView.as_view(),
        name='checkout_final'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
