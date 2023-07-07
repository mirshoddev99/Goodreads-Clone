import smtplib
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from users.forms import UserCreateForm, UserUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from users.tasks import sending_email



class RegisterView(View):
    def get(self, request):
        user_form = UserCreateForm()
        contex = {'form':user_form}
        return render(request, 'users/register.html', contex)



    def post(self, request):
        user_form = UserCreateForm(data=request.POST)
        if user_form.is_valid():
            email = user_form.cleaned_data['email']
            username = user_form.cleaned_data['username']
            sending_email(email, username)
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            messages.success(request, "You have successfully registered")
            return redirect('users:login')
        
        contex = {'form': user_form}
        return render(request, 'users/register.html', contex)





class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        contex = {"login_form":login_form}

        return render(request, 'users/login.html', contex)


    def post(self, request):
        # for testing
        print(request.POST['username'], request.POST['password'])

        # AuthenticationForm - Formani validatsiya qilib beradi
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            # get_user() - yuborilgan formadan userni olib beradi
            user = login_form.get_user()
            login(request, user)
            # Temporary message method
            messages.success(request, "You have successfully logged in!")
            return redirect("books:list")

        else:
            contex = {"login_form":login_form}
            return render(request, 'users/login.html', contex)





class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        contex = {"user":user}
        return render(request, "users/profile.html", contex)




class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect("landing_page")




class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        user_update_form = UserUpdateForm(instance=request.user)
        contex = {"form":user_update_form}
        return render(request, 'users/profile_edit.html', contex)


    def post(self, request):
        user_update_form = UserUpdateForm(instance=request.user, data=request.POST, files=request.FILES)

        if user_update_form.is_valid():
            user_update_form.save()
            messages.success(request, "You have successfully updated your profile")
            return redirect("users:profile")

        return render(request, "users/profile_edit.html", {"form":user_update_form})
