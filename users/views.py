from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomAuthenticationForm


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('profile')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('login')


@login_required
def profile(request):
    orders = request.user.assigned_orders.all()
    return render(request, 'users/profile.html', {'orders': orders})
