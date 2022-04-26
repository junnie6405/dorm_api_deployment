from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import Cusomized_User_Creation_Form, Customized_User_Change_Form
from .models import Customized_User, Dorm, Review, Room

class CustomUserAdmin(UserAdmin):
    add_form = Cusomized_User_Creation_Form
    form = Customized_User_Change_Form
    model = Customized_User
    list_display = ["email", "username"]

admin.site.register(Customized_User, CustomUserAdmin)
admin.site.register(Dorm)
admin.site.register(Review)
admin.site.register(Room)
