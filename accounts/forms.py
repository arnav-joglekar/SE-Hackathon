from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile,Domain


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email','password1','password2']

class UserProfileForm(forms.ModelForm):
    domains = forms.ModelMultipleChoiceField(queryset=Domain.objects.all(), widget=forms.SelectMultiple)

    class Meta:
        model = UserProfile
        fields = ['courses', 'preferred_study_methods', 'goals', 'domains', 'availability']