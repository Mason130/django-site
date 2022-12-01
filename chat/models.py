from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


def set_avatar_path(self, filepath):
    return 'profile/' + str(self.related_user.pk) + '/avatar.png'


def default_avatar():
    return "profile/default.png"


class ProfileAvatar(models.Model):
    related_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="related_user")
    avatar = models.ImageField(max_length=255, upload_to=set_avatar_path, default=default_avatar, null=True, blank=True)
    
    def get_avatar_filename(self):
        return str(self.avatar)[str(self.avatar).index('profile/' + str(self.pk) + '/'):]


@receiver(post_save, sender=User)
def user_save(sender, instance, **kwargs):
    FriendList.objects.get_or_create(user=instance)


class FriendList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    friends = models.ManyToManyField(User, blank=True, related_name="friends")

    def __str__(self):
        return self.user.username

    def add_friend(self, account):
        if account not in self.friends.all():
            self.friends.add(account)
            self.save()

    def remove_friend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removee):
        remover_list = self
        remover_list.remove_friend(removee)
        removee_list = FriendList.objects.get(user=removee)
        removee_list.remove_friend(self.user)

    def is_friend(self, friend):
        if friend in self.friends.all():
            return True
        return False


class FriendRequest(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requester")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    is_active = models.BooleanField(blank=True, null=False, default=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.requester.username

    def accept(self):
        receiver_list = FriendList.objects.get(user=self.receiver)
        if receiver_list:
            receiver_list.add_friend(self.requester)
            requester_list = FriendList.objects.get(user=self.requester)
            if requester_list:
                requester_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        self.is_active = False
        self.save()

    def cancel(self):
        self.is_active = False
        self.save()
