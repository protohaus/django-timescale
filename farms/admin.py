from django.contrib import admin

from farms.models import Sensor, SensorReading
# Register your models here.

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    pass

@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    pass