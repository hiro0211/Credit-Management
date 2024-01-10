from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class SignUpForm(UserCreationForm):
  class Meta:
    model = User
    fields = ["username", "email", "password1", "password2"]

class SiteAuthDataForm(forms.Form):
  user_id = forms.CharField(label="ユーザID")
  password = forms.CharField(label="パスワード", widget=forms.PasswordInput(), min_length=8)

