from django.contrib import admin
from .models import UserProfile, Category, Advert, Review, BlockedUsers


class UserProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('tg', 'username', 'fullname', 'contact', 'region', 'city')
    list_display = ('tg', 'fullname', 'region', 'city')
    list_filter = ['region']
    search_fields = ['tg', 'fullname']

    class Meta:
        model = UserProfile


class AdvertAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'date', 'photos', 'author']
    list_display = ['id', 'date', 'author', 'category', 'caption']
    list_filter = ['category', 'region']
    search_fields = ['id', 'city', 'author']

    class Meta:
        model = Advert


class BlockedUsersAdmin(admin.ModelAdmin):
    list_display = ['blocked_user', 'reason']

    class Meta:
        model = BlockedUsers


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Advert, AdvertAdmin)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(BlockedUsers, BlockedUsersAdmin)
