from django import forms


class GuestCheckoutForm(forms.Form):
    email = forms.EmailField()
    verifyEmail = forms.EmailField(label='Verify email')

    def clean_verify_email(self):
        email = self.cleaned_data('email')
        verifyEmail = self.cleaned_data('verifyEmail')

        if verifyEmail == email:
            return email
        else:
            raise forms.ValidationError('Please confirm emails are the same')
