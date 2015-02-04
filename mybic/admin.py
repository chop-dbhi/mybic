from django.contrib import admin
from django.contrib.auth.models import User, Group
from django import forms

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.forms.models import inlineformset_factory

from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.password = '!'
        if commit:
            user.save()
        return user


class MyUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)