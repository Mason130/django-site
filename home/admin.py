from django.contrib import admin
from .models import Contactor


# Register your models here.
class ContactorAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['first_name']}),
        (None,               {'fields': ['last_name']}),
        (None,               {'fields': ['email_address']}),
        (None,               {'fields': ['message']}),
    ]
    list_display = ('first_name', 'last_name', 'email_address', 'message')


admin.site.register(Contactor, ContactorAdmin)
