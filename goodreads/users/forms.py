from django import forms

from users.models import CustomUser

class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email')

    
    def clean_password2(self):
        cd = self.cleaned_data
        password1 = cd.get("password")
        password2 = cd.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password mismatch!")
        return password2
    



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'profile_picture')
