from django.contrib import admin
from .models import Hospital, TypeOfAccommodation, HealthUnits, HospitalBeds

class HospitalBedsAdmin(admin.ModelAdmin):
    fields = ('name', 'health_units', 'is_active', 'extra', 'status')

admin.site.register(Hospital)
admin.site.register(TypeOfAccommodation)
admin.site.register(HealthUnits)
admin.site.register(HospitalBeds, HospitalBedsAdmin)
