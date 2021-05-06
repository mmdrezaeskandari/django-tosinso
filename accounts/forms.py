from django import forms
from django.contrib.auth.models import User
from .models import *

class UserRegisterForm(forms.Form):
    user_name =     forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'نام کاربری خود را وارد کنید'}))
    email =         forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'ایمیل خود را وارد کنید'}))
    first_name =    forms.CharField(max_length=50)
    last_name =     forms.CharField(max_length=50)
    password_1 =    forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'رمز خود را وارد کنید'}))
    password_2 =    forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'رمز خود را وارد کنید'}))

    def clean_user_name(self):
        user = self.cleaned_data['user_name']
        if User.objects.filter(username=user).exists():
            raise forms.ValidationError('Username Exists')
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email Exists')
        return email

    def clean_password_2(self):
        password_1 = self.cleaned_data['password_1']
        password_2 = self.cleaned_data['password_2']

        if password_1 != password_2:
            raise forms.ValidationError('Password Does Not Match.')
        elif len(password_2) < 6:
            raise forms.ValidationError('Password should be at least 6 characters')
        elif not any(x.isupper() for x in password_2):
            raise forms.ValidationError('Password should contain at least 1 Uppercase Alphabet.')
        return password_2


class UserLoginForm(forms.Form):
    user =          forms.CharField(max_length=50)
    password =      forms.CharField(max_length=50)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model =     User
        fields =    ['username', 'first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model =     Profile
        fields =    ['phone', 'address']
