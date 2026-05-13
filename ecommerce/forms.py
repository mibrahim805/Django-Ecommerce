from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from ecommerce.models import CustomUser


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']




class CheckoutForm(forms.Form):
    PAYMENT_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('card', 'Card Payment'),]
    full_name = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    address = forms.CharField(widget=forms.Textarea)
    city = forms.CharField(max_length=100)
    postal_code = forms.CharField(max_length=20)
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea)
    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect)



class CardPaymentForm(forms.Form):
    card_holder = forms.CharField(max_length=255)
    card_number = forms.CharField(max_length=16)
    expiry = forms.CharField(max_length=5)
    cvv = forms.CharField(max_length=4)




