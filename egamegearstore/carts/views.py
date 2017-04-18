from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.edit import FormMixin
# Create your views here.

from orders.forms import GuestCheckoutForm
from orders.mixins import CartOrderMixin
from orders.models import UserCheckout, UserAddress, Order
from products.models import Variation
from .models import Cart, CartItem


class ItemCountView(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            cart_id = self.request.session.get('cart_id')
            if cart_id is None:
                count = 0
            else:
                cart = Cart.objects.get(id=cart_id)
                count = cart.itemList.count()
            request.session['cart_items_count'] = count
            return JsonResponse({'count': count})
        else:
            raise Http404


class CartView(SingleObjectMixin, View):
    model = Cart
    template_name = 'carts/view.html'

    def get_object(self, *args, **kwargs):
        self.request.session.set_expiry(0)  # second
        cart_id = self.request.session.get('cart_id')
        if cart_id is None:
            cart = Cart()
            # set tax percent here
            # self.request.user.get_tax_percentage()
            cart.tax_percentage = 0.075
            cart.save()
            cart_id = cart.id
            self.request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
        # bind self.request user to cart.user
        if self.request.user.is_authenticated():
            cart.user = self.request.user
            cart.save()
        return cart

    def get(self, request, *args, **kwargs):
        cart = self.get_object()
        item_id = request.GET.get('item')
        delete_item = request.GET.get('delete', False)
        flash_msg = ''
        item_added = False

        if item_id:
            item_instance = get_object_or_404(Variation, id=item_id)
            qty = request.GET.get("qty", 1)
            try:
                if int(qty) < 1:
                    delete_item = True
            except:
                raise Http404

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, item=item_instance)
            if created:
                flash_msg = 'Successfully added to the cart.'
                item_added = True
            if delete_item:
                flash_msg = 'Item removed successfully.'
                cart_item.delete()
            else:
                if not created:
                    flash_msg = 'Quantity has been updated successfully.'
                cart_item.quantity = qty
                cart_item.save()
            if not request.is_ajax():
                return HttpResponseRedirect(reverse('cart'))
                # return cart_item.cart.get_absolute_url()

        if request.is_ajax():
            try:
                total = cart_item.line_item_total
                print(total)
            except:
                total = None
            try:
                subtotal = cart_item.cart.subtotal
            except:
                subtotal = None
            try:
                tax_total = cart_item.cart.tax_total
            except:
                tax_total = None
            try:
                cart_total = cart_item.cart.total
            except:
                cart_total = None
            try:
                total_items = cart_item.cart.itemList.count()
            except:
                total_items = 0

            return JsonResponse({
                'deleted': delete_item,
                'item_added': item_added,
                'line_total': total,
                'subtotal': subtotal,
                'tax_total': tax_total,
                'cart_total': cart_total,
                'flash_msg': flash_msg,
                'total_items': total_items,
            })

        context = {
            'object': self.get_object()
        }
        template = self.template_name
        return render(request, template, context)


class CheckoutView(CartOrderMixin,FormMixin, DetailView):
    model = Cart
    template_name = 'carts/checkout_view.html'
    form_class = GuestCheckoutForm

    # def get_order(self, *args, **kwargs):
    #     new_order_id = self.request.session.get('order_id')
    #     cart = self.get_object()
    #     if new_order_id is None:
    #         new_order = Order.objects.create(cart=cart)
    #         self.request.session['order_id'] = new_order.id
    #     else:
    #         new_order = Order.objects.get(id=new_order_id)
    #     return new_order

    def get_object(self, *args, **kwargs):
        cart = self.get_cart()
        if cart is None:
            return None
        return cart

    def get_context_data(self, *args, **kwargs):
        context = super(CheckoutView, self).get_context_data(*args, **kwargs)
        user_can_continue = False
        user_check_id = self.request.session.get('user_checkout_id')
        # print(user_checkout_id)

        # create user checkout if user is authenticated
        if self.request.user.is_authenticated():
            user_can_continue = True
            user_checkout, created = UserCheckout.objects.get_or_create(
                email=self.request.user.email)
            user_checkout.user = self.request.user
            user_checkout.save()
            self.request.session['user_checkout_id'] = user_checkout.id
        elif not self.request.user.is_authenticated() \
                and user_check_id is None:
            context['login_form'] = AuthenticationForm()
            context['next_url'] = self.request.build_absolute_uri()
        else:
            pass

        if user_check_id is not None:
            user_can_continue = True

        context['order'] = self.get_order()
        context['user_can_continue'] = user_can_continue
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user_checkout, created = UserCheckout.objects.get_or_create(
                email=email)
            # print(user_checkout)
            self.request.session['user_checkout_id'] = user_checkout.id
            # print(user_checkout.id)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('checkout')

    def get(self, request, *args, **kwargs):
        get_data = super(CheckoutView, self).get(request, *args, **kwargs)
        cart=self.get_object()
        # if remove everything and try to checkout, it'll redirect to cart
        if cart is None:
            return redirect('cart')
        new_order = self.get_order()

        user_checkout_id = request.session.get('user_checkout_id')
        if user_checkout_id is not None:
            user_checkout = UserCheckout.objects.get(id=user_checkout_id)

            if new_order.billing_address is None or new_order.shipping_address is None:
                return redirect('order_address')

            new_order.user = user_checkout
            new_order.save()
        return get_data
