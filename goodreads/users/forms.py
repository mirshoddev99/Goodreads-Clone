from django import forms
from django.core.mail import send_mail

from users.models import CustomUser

class CustomUserCreateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def save(self, commit=True):
        # Commit = True -> Store data to tha database right now.
        # Commit = False -> Store data temporary not to tha database right now.

        user = super().save(commit)
        # Password security
        user.set_password(self.cleaned_data['password'])
        # Save a new user object
        user.save()

        return user




class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'profile_picture')
