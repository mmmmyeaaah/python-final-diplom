from django.contrib import admin
from users.models import Contact, ConfirmEmailToken, User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    model = User

    fieldsets = (
        (None, {'fields': ('email', 'password', 'type')}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {
            'fields': ('is_staff', 'is_superuser', 'is_active', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'type', 'is_active')
    ordering = ('date_joined',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'street', 'house', 'apartment', 'phone',)


@admin.register(ConfirmEmailToken)
class ConfirmEmailTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'created_at',)

