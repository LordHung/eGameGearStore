from decimal import Decimal
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
# Create your models here.
from carts.models import Cart


class UserCheckout(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, null=True, blank=True)
    email = models.EmailField(unique=True)  # required
    # merchant_id

    def __str__(self):
        return self.email


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
    ('completed', 'Completed')
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

    def __str__(self):
        return str(self.cart.id)

    def mark_completed(self):
        self.status = 'completed'
        self.save()


def order_pre_save(sender, instance, *args, **kwargs):
    shipping_total_price = instance.shipping_total_price
    cart_total = instance.cart.total
    order_total = Decimal(shipping_total_price) + cart_total
    instance.order_total = order_total

pre_save.connect(order_pre_save, sender=Order)
