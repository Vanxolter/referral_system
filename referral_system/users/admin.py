from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Админ-панель модели юзера
    """
    list_display = ('phone_number', 'invite_code', 'is_active', 'is_staff')
