from django.contrib import admin

from core.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',)
    list_filter = ('is_staff', 'is_active', 'is_superuser',)
    search_fields = (
        'username__startswith',
        'email__startswith',
        'first_name__startswith',
        'last_name__startswith',
    )
    exclude = ('password',)
    readonly_fields = ('last_login', 'date_joined',)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
