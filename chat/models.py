from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


def set_avatar_path(self, filepath):
    return 'profile/' + str(self.pk) + '/avatar.png'


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


# class AccountManager(BaseUserManager):

#     def create_user(self, email, username, password=None):
#         if not email:
#             raise ValueError("Email must be set.")
#         if not username:
#             raise ValueError("Username must be set.")
#         user = self.model(
#             email=self.normalize_email(email),
#             username=username,
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, username, password):
#         user = self.create_user(
#             email=self.normalize_email(email),
#             username=username,
#             password=password,
#         )
#         user.is_admin = True
#         user.is_staff = True
#         user.is_superuser = True
#         return user


# class AppAccount(AbstractBaseUser):
#     username = models.CharField(max_length=30, unique=True)
#     email = models.EmailField(verbose_name="email", max_length=60, unique=True)
#     date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
#     last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
#     is_admin = models.BooleanField(default=False) 
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False) 
#     is_superuser = models.BooleanField( default=False)
#     avatar = models.ImageField(max_length=255, upload_to=set_avatar_path, null=True, blank=True,
#     default=default_avatar)
#     hide_eamil = models.BooleanField(default=True)

#     objects = AccountManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     def __str__(self):
#         return self.username

#     def get_avatar_filename(self):
#         return str(self.avatar)[str(self.avatar).index(f'avatar_images/{self.pk}/'):]

#     def has_permission(self, permission, obj=None):
#         return self.is_admin

#     def has_module_permission(self, app_label):
#         return True
