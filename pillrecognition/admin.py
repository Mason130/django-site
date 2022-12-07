from django.contrib import admin
from .models import PillsInformation


class PillsInformationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['ndc11']}),
        (None,               {'fields': ['rxcui']}),
        (None,               {'fields': ['pill_name']}),
        (None,               {'fields': ['generic_name']}),
    ]
    list_display = ('ndc11', 'rxcui', 'pill_name', 'generic_name')


admin.site.register(PillsInformation, PillsInformationAdmin)
