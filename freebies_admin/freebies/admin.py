from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('tg', 'username', 'fullname', 'contact', 'region', 'city')
    list_display = ('tg', 'fullname', 'region', 'city')
    list_filter = ['region']
    search_fields = ['tg', 'fullname']

    class Meta:
        model = UserProfile


admin.site.register(UserProfile, UserProfileAdmin)
