from django import forms

from django.contrib.auth import get_user_model

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
    billing_address = forms.CharField()
    shipping_address = forms.CharField()
