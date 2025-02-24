from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Campaign

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['title', 'description', 'category', 'custom_category', 'funding_needed', 'due_date']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']