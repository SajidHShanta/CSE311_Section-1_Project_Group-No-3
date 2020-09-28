from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Account


class AccountRegisterForm(UserCreationForm):
    CHOICES = [('is_employee', 'Employee'), ('is_employer', 'Employer')]
    user_types = forms.CharField(label='User Type', widget=forms.RadioSelect(choices=CHOICES))

    class Meta:
        model = Account
        fields = ['email', 'first_name', 'last_name']

