from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save

# Create your models here.


class ProductQuerySet(models.query.QuerySet):

    def active(self):
        return self.filter(active=True)


class ProductManager(models.Manager):

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self, *args, **kawrgs):
        return self.get_queryset().active()


class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    active = models.BooleanField(default=True)
    # slug
    # inventory

    objects = ProductManager()

    def __str__(self):  # giống với def __unicode__(self),__init__: trong python2
        return self.title

    # lấy đường dẫn tuyệt đối product_detail
    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})


class Variation(models.Model):
    product = models.ForeignKey(Product)
    title = models.CharField(max_length=120)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    sale_price = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True)
    active = models.BooleanField(default=True)
    # refer none == unlimited amount
    inventory = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_price(self):
        if self.price is not None:
            return self.sale_price
        else:
            return self.price

    def get_absolute_url(self):
        return self.product.get_absolute_url()

# make sure create default variation for product
def product_saved_receiver(sender, instance, created, *args, **kwargs):
    product = instance
    variations = product.variation_set.all()
    if variations.count() == 0:
        new_var = Variation()
        new_var.product = product
        new_var.title = "Default"
        new_var.price = product.price
        new_var.save()

post_save.connect(product_saved_receiver, sender=Product)

# Product Images

# Product Category
