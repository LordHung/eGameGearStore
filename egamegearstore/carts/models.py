from django.conf import settings
from django.db import models

from products.models import Variation
# Create your models here.


class CartItem(models.Model):
    cart = models.ForeignKey("Cart")
    item = models.ForeignKey(Variation)
    quantity = models.PositiveIntegerField(default=1)
    # line item total

    def __str__(self):
        return self.item.title

    def remove(self):
        return self.item.remove_from_cart()



class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    itemList = models.ManyToManyField(Variation, through=CartItem)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    # subtotal price
    # taxes total
    # discounts
    # total price

    def __str__(self):
        """TODO: to be defined1. """
        return str(self.id)
