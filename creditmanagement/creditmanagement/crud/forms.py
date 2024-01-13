from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class SignUpForm(UserCreationForm):
  class Meta:
    model = User
    fields = ["username", "email", "password1", "password2"]

class AcountsUpdateForm(forms.ModelForm):
  class Meta:
    model = User
    fields = (
      'username', 'email',
    )
  
  def __int__(self, *args, **kwargs):
    super().__int__(*args, **kwargs)
    for field in self.field.values():
        field.widget.attrs['class'] = 'form-control'

class SiteAuthDataForm(forms.Form):
  user_id = forms.CharField(label="ユーザID")
  password = forms.CharField(label="パスワード", widget=forms.PasswordInput(), min_length=8)

