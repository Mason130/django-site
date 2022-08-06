from django.contrib import admin
from .models import Contact


# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['user']}),
        (None,               {'fields': ['first_name']}),
        (None,               {'fields': ['last_name']}),
        (None,               {'fields': ['email_address']}),
        (None,               {'fields': ['message']}),
        (None,               {'fields': ['received_date']}),
    ]
    list_display = ('user', 'first_name', 'last_name', 'email_address', 'message','received_date')


admin.site.register(Contact, ContactAdmin)
