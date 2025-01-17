from django import forms
from django.forms.models import modelformset_factory
from .models import Variation, Category


class ProductFilterForm(forms.Form):
    q = forms.CharField(label='Search', required=False)
    category_id = forms.ModelMultipleChoiceField(
        label='Category',
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    max_price = forms.DecimalField(
        decimal_places=12, max_digits=12, required=False)
    min_price = forms.DecimalField(
        decimal_places=12, max_digits=12, required=False)


class VariationInventoryForm(forms.ModelForm):
    """docstring for VariationInventory."""
    class Meta:
        model = Variation
        fields = [
            'title',
            'price',
            'sale_price',
            'inventory',
            'active'
        ]


VariationInventoryFormSet = modelformset_factory(
    Variation, form=VariationInventoryForm, extra=0)
