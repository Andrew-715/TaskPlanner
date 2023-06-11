from django.contrib import admin


from bot.models import TgUser


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ['telegram_chat_id']
    readonly_fields = ['verification_code']
    search_fields = ['telegram_chat_id']
