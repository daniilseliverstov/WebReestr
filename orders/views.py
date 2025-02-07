from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order
from .forms import OrderForm
from datetime import datetime


@login_required
def user_dashboard(request):
    user = request.user
    orders = None

    if user.department.name == "Коммерческий":
        orders = Order.objects.filter(manager=user)
        template = "users/dashboard_commercial.html"
    elif user.department.name == "Конструкторский":
        orders = Order.objects.filter(status='accepted')
        template = "users/dashboard_design.html"
    elif user.department.name == "Технический":
        orders = Order.objects.filter(technologist=user)
        template = "users/dashboard_technical.html"
    else:
        return redirect('login')

    return render(request, template, {"orders": orders})


@login_required
def create_order(request):
    if request.user.department.name != 'Коммерческий':
        return redirect('user_dashboard')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.manager = request.user
            order.status = 'accepted'
            order.year = datetime.now().year  # Устанавливаем текущий год
            order.save()
            return redirect('user_dashboard')
    else:
        form = OrderForm()

    return render(request, 'orders/create_order.html', {'form': form})
