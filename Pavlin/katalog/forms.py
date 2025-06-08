from django import forms
from .models import Order
from django.core.exceptions import ValidationError


class OrderForm(forms.ModelForm):
    privacy_policy = forms.BooleanField(
        required=True,
        label='Я согласен на обработку персональных данных',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        error_messages={
            'required': 'Необходимо дать согласие на обработку данных'
        }
    )

    class Meta:
        model = Order
        fields = ['customer_name', 'phone', 'email', 'address', 'comment', 'privacy_policy_accepted']

    def clean_privacy_policy(self):
        accepted = self.cleaned_data.get('privacy_policy')
        if not accepted:
            raise ValidationError("Необходимо дать согласие на обработку данных")
        return accepted