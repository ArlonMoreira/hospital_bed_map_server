from django.contrib import admin
from .models import Hospital, typeOfAccommodation, healthUnits, hospitalBeds

class HospitalBedsAdmin(admin.ModelAdmin):
    fields = ('name', 'health_units', 'is_active', 'extra', 'status')

admin.site.register(Hospital)
admin.site.register(typeOfAccommodation)
admin.site.register(healthUnits)
admin.site.register(hospitalBeds, HospitalBedsAdmin)
