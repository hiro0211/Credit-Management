from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

class LoginForm(AuthenticationForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields.values():
      field.widget.attrs["class"] = 'form-control'
      field.widget.attrs['placeholder'] = field.label

class SignUpForm(UserCreationForm):
  class Meta:
    model = User
    fields = ["username", "email", "password1", "password2"]

class SiteAuthDataForm(forms.Form):
  user_id = forms.CharField(label="ユーザID")
  password = forms.CharField(label="パスワード", widget=forms.PasswordInput(), min_length=8)