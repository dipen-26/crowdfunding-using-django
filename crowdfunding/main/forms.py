from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Campaign

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CampaignForm(forms.ModelForm):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Campaign
        fields = ['title', 'description', 'category', 'custom_category', 'funding_needed', 'due_date']

    def save(self, commit=True):
        campaign = super().save(commit=False)
        if commit:
            campaign.save()
        return campaign
