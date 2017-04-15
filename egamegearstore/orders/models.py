from django.conf import settings
from django.db import models

# Create your models here.


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

# class Order(models.Model):
    # order_id
    # cart
    # usercheckout required
    # billingaddress
    # shippingaddress
    # shipping total price
    # order total(carttotal + shipping)
