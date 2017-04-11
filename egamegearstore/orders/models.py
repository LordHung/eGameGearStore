from django.conf import settings
from django.db import models

# Create your models here.


class UserCheckout(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, null=True, blank=True)
    email = models.EmailField()  # required
    # merchant_id

    def __str__(self):
        return self.email


# class Order(models.Model):
    # order_id
    # cart
    # usercheckout required
    # billingaddress
    # shippingaddress
    # shipping total price
    # order total(carttotal + shipping)
