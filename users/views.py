from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomAuthenticationForm


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('profile')  # Название представления profile, еще не готово
            else:
                form.add_error(None, "Неверное имя пользователя или пароль")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})
