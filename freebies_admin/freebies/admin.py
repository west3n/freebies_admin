from django.contrib import admin
from .models import UserProfile, Category, Advert, Review, BlockedUsers, ExplicitWords, SendMessage
# from django.contrib.admin.models import LogEntry
#
# # удаление истории правок админ-панели
# LogEntry.objects.all().delete()


class UserProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('tg', 'username', 'fullname', 'contact', 'region', 'city', 'rating')
    list_display = ('tg', 'fullname', 'region', 'city', 'rating')
    list_filter = ['region']
    search_fields = ['tg', 'fullname']

    class Meta:
        model = UserProfile


class AdvertAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'date', 'photos', 'author', 'region', 'city', 'caption', 'delivery']
    list_display = ['id', 'date', 'author', 'category', 'caption', 'status']
    list_filter = ['category', 'region', 'status']
    search_fields = ['id', 'city', 'author__tg', 'author__fullname']

    class Meta:
        model = Advert


class BlockedUsersAdmin(admin.ModelAdmin):
    list_display = ['blocked_user', 'reason']

    class Meta:
        model = BlockedUsers


class FirstLetterFilter(admin.SimpleListFilter):
    title = 'Первая буква'
    parameter_name = 'Первая буква'

    def lookups(self, request, model_admin):
        blocked_users = model_admin.model.objects.values_list('word', flat=True)
        first_letters = {word[0].upper() for word in blocked_users}
        return [(letter, letter) for letter in sorted(first_letters)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(word__istartswith=self.value())
        return queryset


class ExplicitWordsAdmin(admin.ModelAdmin):
    list_filter = [FirstLetterFilter]

    class Meta:
        model = BlockedUsers
        ordering = ['word']


class SendMessageAdmin(admin.ModelAdmin):
    list_display = ['message_type', 'text']

    class Meta:
        model = SendMessage


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['author', 'user_id', 'text']

    class Meta:
        model = SendMessage


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Advert, AdvertAdmin)
admin.site.register(Category)
admin.site.register(Review, ReviewAdmin)
admin.site.register(BlockedUsers, BlockedUsersAdmin)
admin.site.register(ExplicitWords, ExplicitWordsAdmin)
