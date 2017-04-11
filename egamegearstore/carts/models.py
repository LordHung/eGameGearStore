from decimal import Decimal
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete

from products.models import Variation
# Create your models here.


class CartItem(models.Model):
    cart = models.ForeignKey("Cart")
    item = models.ForeignKey(Variation)
    quantity = models.PositiveIntegerField(default=1)
    line_item_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.item.title

    def remove(self):
        return self.item.remove_from_cart()


# Nếu nhiều item sẽ nhân với số lượng
def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
    qty = Decimal(instance.quantity)
    if qty >= 1:
        price = instance.item.get_price()
        line_item_total = qty * price
        instance.line_item_total = line_item_total


pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)


# post_save chạy khi item đã lưu vào db rồi
def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
    instance.cart.update_subtotal()


post_save.connect(cart_item_post_save_receiver, sender=CartItem)

# post_delete to update subtotal =0 when all item are removed
post_delete.connect(cart_item_post_save_receiver, sender=CartItem)


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    itemList = models.ManyToManyField(Variation, through=CartItem)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    subtotal = models.DecimalField(
        max_digits=50, decimal_places=2, default=0.00)
    tax_percentage = models.DecimalField(
        max_digits=10, decimal_places=5, default=0.085)
    tax_total = models.DecimalField(
        max_digits=50, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)

    # subtotal price
    # taxes total
    # discounts
    # total price

    def __str__(self):
        return str(self.id)

    def update_subtotal(self):
        print('updating...')
        subtotal = 0
        itemList = self.cartitem_set.all()
        for item in itemList:
            subtotal += item.line_item_total
        self.subtotal = '%.2f' % (subtotal)
        self.save()


def do_tax_and_total_receiver(sender, instance, *args, **kwargs):
    subtotal = Decimal(instance.subtotal)
    tax_total = round(subtotal * Decimal(instance.tax_percentage), 2)
    total = subtotal + tax_total

    print(instance.tax_percentage)
    instance.tax_total = '%.2f' % (tax_total)
    instance.total = '%.2f' % (total)
    # instance.save()

pre_save.connect(do_tax_and_total_receiver, sender=Cart)
