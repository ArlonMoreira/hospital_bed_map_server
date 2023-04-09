from django.contrib import admin
from .models import Hospital

class HospitalAdmin(admin.ModelAdmin):
    fields = ('name', 'acronym', 'is_active')

admin.site.register(Hospital, HospitalAdmin)
