from decimal import Decimal
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save
# Create your models here.
from carts.models import Cart


import braintree

# Braintree config
if settings.DEBUG:
    # braintree.Configuration.configure(
    #     braintree.Environment.Sandbox,
    #     'nmn2ddgvqdwmny6d',
    #     'hnnd7jzyrdcgnj2z',
    #     'e8a55aa7ae57dcb9dfb10cf97ee0037f'
    # )
    braintree.Configuration.configure(
        braintree.Environment.Sandbox,
        merchant_id=settings.BRAINTREE_MERCHANT_ID,
        public_key=settings.BRAINTREE_PUBLIC,
        private_key=settings.BRAINTREE_PRIVATE
    )


class UserCheckout(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, null=True, blank=True)
    email = models.EmailField(unique=True)  # required
    braintree_id = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.email

    @property
    def get_braintree_id(self):
        instance = self
        if not instance.braintree_id:
            # update it
            result = braintree.Customer.create({
                "email": instance.email,
            })

            if result.is_success:
                print(result)
                instance.braintree_id = result.customer.id
                instance.save()
        return instance.braintree_id

    def get_client_token(self):
        customer_id = self.get_braintree_id
        if customer_id:
            client_token = braintree.ClientToken.generate({
                "customer_id": customer_id
            })
            return client_token
        return None


def update_braintree_id(sender, instance, *args, **kwargs):
    if not instance.braintree_id:
        # update it
        instance.get_braintree_id


post_save.connect(update_braintree_id, sender=UserCheckout)


# billing: store in db; Billing: display on form
ADDRESS_TYPE = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping')
)


class UserAddress(models.Model):
    user = models.ForeignKey(UserCheckout)
    type = models.CharField(max_length=50, choices=ADDRESS_TYPE)
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=50)

    def __str__(self):
        return self.street

    def get_address(self):
        return '%s, %s, %s %s' % (
            self.street, self.state, self.city, self.zipcode)


ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('completed', 'Completed'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)


class Order(models.Model):
    status = models.CharField(
        max_length=100, choices=ORDER_STATUS_CHOICES, default='created')
    cart = models.ForeignKey(Cart)
    user = models.ForeignKey(UserCheckout, null=True)
    billing_address = models.ForeignKey(
        UserAddress, related_name='billing_address', null=True)
    shipping_address = models.ForeignKey(
        UserAddress, related_name='shipping_address', null=True)
    shipping_total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    order_id = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return str(self.cart.id)

    class Meta:
        # order order id reverse
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'pk': self.pk})

    def mark_completed(self, order_id=None):
        self.status = 'paid'
        if order_id and not self.order_id:
            self.order_id = order_id
        self.save()


def order_pre_save(sender, instance, *args, **kwargs):
    shipping_total_price = instance.shipping_total_price
    cart_total = instance.cart.total
    order_total = Decimal(shipping_total_price) + cart_total
    instance.order_total = order_total


pre_save.connect(order_pre_save, sender=Order)


# if order status == refunded
# braintree refund ...
