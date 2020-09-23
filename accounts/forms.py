from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

# class Signup(forms.ModelForm):
#     name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Your Username" }))
#     first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Your First Name" }))
#     last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Your Last Name" }))
#     phone_number = forms.CharField(widget=forms.IntegerField(attrs={"class": "form-control form-control-lg", "placeholder": "Your phone number" }))
#     email = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Your Email" }))
#     pass_one = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Password" }))
#     re_pass = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Repeat your password" }))
#     agree-term = forms.CharField(required=True, widget=forms.BooleanField(attrs={"class": "form-control form-control-lg" }))

class PasswordResetForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Enter Your Email", 'autofocus': 'True' }))
    class Meta():
        model = User
        fields = ('email',)

class PasswordResetConfirmViewForm(forms.ModelForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control form-control-lg", "placeholder": "Enter Password" }))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control form-control-lg", "placeholder": "Repeat Password" }))
    class Meta():
        model = User
        fields = ('password',)
