from django import forms
from django.core.mail import send_mail

from users.models import CustomUser

class CustomUserCreateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password', "password2")

    
    def clean_password(self):
        cd = self.cleaned_data
        password1 = cd.get("password")
        password2 = cd.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password mismatch!")
        return password2
    
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
