from django.contrib import admin


# Register your models here.


class NotifyMeAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('email',)
