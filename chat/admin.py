from django.contrib import admin
from .models import FriendList, FriendRequest, ProfileAvatar


# Register your models here.
class FriendListAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user']
    readonly_fields = ['user']

    class Meta:
        model = FriendList


admin.site.register(FriendList, FriendListAdmin)


class FriendRequestAdmin(admin.ModelAdmin):
    list_filter = ['requester', 'receiver']
    list_display = ['requester', 'receiver']
    search_fields = ['requester__username', 'requester__email', 'receiver__username', 'receiver__email']

    class Meta:
        model = FriendRequest


admin.site.register(FriendRequest, FriendRequestAdmin)


class ProfileAvatarAdmin(admin.ModelAdmin):
    list_filter = ['related_user']
    list_display = ('related_user', 'avatar')

    class Meta:
        model = ProfileAvatar


admin.site.register(ProfileAvatar, ProfileAvatarAdmin)
