from tabnanny import verbose

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app_users.models import UserProfileInfo


class UserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta():
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2')

        # widgets = {
        # "password":"forms.PasswordInput()",
        # }

        labels = {
            'password1': 'Password',
            'password2': 'Confirm Password',
            'username': 'логин'

        }


class UserProfileInfoForm(forms.ModelForm):

    class Meta():
        model = UserProfileInfo
        fields = ('bio', 'profile_pic', 'user_type')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ['bio', 'profile_pic']


class ProfileForm2(forms.ModelForm):
    class Meta():
        model = User
        fields = ('first_name',
                  'email')
