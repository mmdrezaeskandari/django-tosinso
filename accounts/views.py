from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(username = data['user_name'],
                                        email = data['email'],
                                        first_name = data['first_name'],
                                        last_name = data['last_name'],
                                        password = data['password_1'])
            user.save()
            messages.success(request, 'حساب کاربری با موفقیت ساخته شد.', 'success')
            return redirect('home:home')
        else:
            messages.error(request, 'حساب کاربری ساخته نشد، دوباره تلاش کنید.', 'danger')
    else:
        form = UserRegisterForm()

    context = {'form': form}
    return render(request, 'accounts/register.html', context)

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = authenticate(request, username=User.objects.get(email=data['user']).username, password=data['password'])
            except:
                user = authenticate(request, username=data['user'], password=data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'با موفقیت وارد شدید :)', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'نام کاربری یا رمزعبور اشتباه است. دوباره امتحان کنید.', 'danger')
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})

@login_required(login_url='accounts:user_login')
def user_logout(request):
    logout(request)
    messages.success(request, 'شما با موفقیت خارج شدید', 'info')
    return redirect('home:home')

@login_required(login_url='accounts:user_login')
def user_profile(request):
    profile = Profile.objects.get(user_id = request.user.id)
    context = {
    'profile': profile
    }
    return render(request, 'accounts/profile.html', context)

@login_required(login_url='accounts:user_login')
def user_profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'تغییرات با موفقیت اعمال شد.')
            return redirect('accounts:user_profile')

    else:
        user_form =  UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
    'user_update_form': user_form,
    'profile_update_form': profile_form,
    }

    return render(request, 'accounts/user_update.html', context)

@login_required(login_url='accounts:user_login')
def user_change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'پسوورد شما با موفقیت تغییر یافت.', 'success')
            return redirect('accounts:user_profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/user_change_password.html', {'form': form})
