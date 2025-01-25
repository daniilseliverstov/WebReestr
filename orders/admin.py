from django.contrib import admin
from .models import Order, OrderFile, OrderComment


admin.site.register(Order)
admin.site.register(OrderFile)
admin.site.register(OrderComment)
