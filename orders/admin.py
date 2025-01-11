from django.contrib import admin
from .models import Department, Profile, Customer


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'code', 'manager')
    list_filter = ('manager',)
    search_fields = ('name', 'code')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Ограничиваем выбор менеджеров только коммерческим отделом."""
        if db_field.name == 'manager':
            kwargs['queryset'] = Profile.objects.filter(department='commercial')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Profile)
