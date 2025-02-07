from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from orders.forms import OrderForm
from orders.models import Order
from .forms import CustomAuthenticationForm


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.username}!')
                return redirect(user_dashboard_redirect(user))  # Перенаправляем
            messages.error(request, 'Неверное имя пользователя или пароль')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')

    return render(request, 'users/login.html', {'form': CustomAuthenticationForm()})


def user_dashboard_redirect(user):
    """Определяет, в какой личный кабинет отправлять пользователя."""
    department = user.department
    if department:
        if department.name == "Коммерческий отдел":
            return 'commercial_dashboard'
        elif department.name == "Технический отдел":
            return 'technical_dashboard'
        elif department.name == "Конструкторский отдел":
            return 'design_dashboard'
        elif department.name == "Отдел снабжения":
            return 'supply_dashboard'
    return 'default_dashboard'


# Коммерческий отдел - создание заказа
@login_required
def create_order(request):
    if request.user.department.name != 'Коммерческий':
        return redirect('user_dashboard')  # если не коммерческий, редирект на личный кабинет

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.manager = request.user
            order.status = 'accepted'  # Заказ автоматически получает статус "Принят"
            order.save()
            return redirect('user_dashboard')  # Перенаправление на личный кабинет
    else:
        form = OrderForm()
    return render(request, 'orders/create_order.html', {'form': form})


# Конструкторский отдел - просмотр заказов
@login_required
def constructor_dashboard(request):
    if request.user.department.name != 'Конструкторский':
        return redirect('user_dashboard')  # Если не из конструкторского отдела, редирект

    orders = Order.objects.filter(status='accepted')  # только заказы со статусом "Принят"

    if request.method == 'POST':
        # Логика назначения исполнителя
        pass

    return render(request, 'orders/constructor_dashboard.html', {'orders': orders})


# Технический отдел - просмотр заказов
@login_required
def technician_dashboard(request):
    if request.user.department.name != 'Технический':
        return redirect('user_dashboard')  # Если не из технического, редирект

    orders = Order.objects.filter(technologist=request.user)  # Только заказы, назначенные этому пользователю
    week_filter = request.GET.get('week')  # Получаем фильтр по неделе
    if week_filter:
        orders = orders.filter(week=week_filter)

    total_area = sum(order.total_area for order in orders)  # Суммируем квадратуру заказов за неделю

    return render(request, 'orders/technician_dashboard.html', {'orders': orders, 'total_area': total_area})
