from django import forms

from django.contrib.auth import get_user_model

from .models import UserAddress
User = get_user_model()


class GuestCheckoutForm(forms.Form):
    email = forms.EmailField()
    verifyEmail = forms.EmailField(label='Verify email')

    def clean_verifyEmail(self):
        email = self.cleaned_data['email']
        verifyEmail = self.cleaned_data['verifyEmail']

        if email == verifyEmail:
            user_exists = User.objects.filter(email=email).count()
            # if user does not exists
            if user_exists != 0:
                raise forms.ValidationError(
                    'This User already exists. Please login instead.')
            return email
        else:
            raise forms.ValidationError('Please confirm emails are the same')


class AddressForm(forms.Form):
    # Default mchofield is Dropdown select
    billing_address = forms.ModelChoiceField(
        queryset=UserAddress.objects.filter(type='billing'),
        widget=forms.RadioSelect,
        empty_label=None,
    )
    shipping_address = forms.ModelChoiceField(
        queryset=UserAddress.objects.filter(type='shipping'),
        widget=forms.RadioSelect,
        empty_label=None,
    )


class UserAddressForm(forms.ModelForm):

    class Meta:
        model = UserAddress
        fields = [
            'street',
            'city',
            'state',
            'zipcode',
            'type',
        ]
