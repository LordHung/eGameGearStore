from django.contrib import admin
from .models import Product, Variation, ProductImage, Category, ProductFeatured


class VariationInline(admin.TabularInline):
    model = Variation
    # Show only one variation to add, can append more
    extra = 0
    max_num=10


class ProductImage(admin.TabularInline):
    model = ProductImage
    extra =0
    max_num=10


class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'price']
    inlines = [VariationInline,ProductImage]

    class Meta:
        model = Product


# Register your models here.
admin.site.register(Product, ProductAdmin)
# admin.site.register(Variation)
# admin.site.register(ProductImage)
admin.site.register(Category)
admin.site.register(ProductFeatured)
