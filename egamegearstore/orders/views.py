from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView, CreateView
from django.views.generic.list import ListView
# Create your views here.

from .forms import AddressForm, UserAddressForm
from .models import UserAddress, UserCheckout, Order
from .mixins import CartOrderMixin, LoginRequiredMixin


class OrderList(LoginRequiredMixin, ListView):
    queryset = Order.objects.all()

    def get_queryset(self):
        # user_check_id = self.request.session.get('user_checkout_id')
        # order related to user, only work if got RequiredMixin
        user_check_id = self.request.user.id
        user_checkout = UserCheckout.objects.get(id=user_check_id)
        return super(OrderList, self).get_queryset().filter(user=user_checkout)


class UserAddressCreateView(CreateView):
    form_class = UserAddressForm
    template_name = 'forms.html'
    success_url = '/checkout/address/'

    def get_checkout_user(self):
        user_check_id = self.request.session.get('user_checkout_id')
        user_checkout = UserCheckout.objects.get(id=user_check_id)
        return user_checkout

    def form_valid(self, form, *args, **kwargs):
        form.instance.user = self.get_checkout_user()
        return super(UserAddressCreateView, self).form_valid(
            form, *args, **kwargs)


class AddressSelectFormView(CartOrderMixin, FormView):
    form_class = AddressForm
    template_name = 'address_select.html'

    def dispatch(self, *args, **kwargs):
        bil_address, shi_address = self.get_addresses()
        # if user have no bill|ship address, redirect to
        if bil_address.count() == 0:
            messages.success(
                self.request, 'Please add a billing_address before continuing'
            )
            return redirect('user_address_create')
        elif shi_address.count() == 0:
            messages.success(
                self.request, 'Please add a shipping_address before continuing'
            )
            return redirect('user_address_create')
        return super(AddressSelectFormView, self).dispatch(*args, **kwargs)

    def get_addresses(self, *args, **kwargs):
        user_check_id = self.request.session.get('user_checkout_id')
        user_checkout = UserCheckout.objects.get(id=user_check_id)
        bil_address = UserAddress.objects.filter(
            user=user_checkout,
            type='billing',
        )
        shi_address = UserAddress.objects.filter(
            user=user_checkout,
            type='shipping',
        )
        return bil_address, shi_address

    def get_form(self, *args, **kwargs):
        form = super(AddressSelectFormView, self).get_form(*args, **kwargs)
        print(form.fields)

        bil_address, shi_address = self.get_addresses()
        form.fields['billing_address'].queryset = bil_address
        form.fields['shipping_address'].queryset = shi_address
        return form

    def form_valid(self, form, *args, **kwargs):
        billing_address = form.cleaned_data['billing_address']
        shipping_address = form.cleaned_data['shipping_address']
        order = self.get_order()
        order.billing_address = billing_address
        order.shipping_address = shipping_address
        order.save()
        return super(AddressSelectFormView, self).form_valid(
            form, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        return '/checkout/'
