from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Customized_User

class Cusomized_User_Creation_Form(UserCreationForm):

    class Meta:
        model = Customized_User
        fields = ['first_name', 'last_name', 'email', 'password', 'username']

class Customized_User_Change_Form(UserChangeForm):
    class Meta:
        model = Customized_User
        fields = '__all__'