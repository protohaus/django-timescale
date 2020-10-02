from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.http import HttpResponse

from farms.models import SensorReading, Sensor

# Create your views here.


class CreateSensorReadingView(View):
    def post(self, request, *args, **kwargs):
        sensor = Sensor.objects.get(id="f1a1febd-10e7-4012-a655-2dee7c15b049")
        sensor_reading = SensorReading.objects.create(
            time="2020-10-01 22:33:52.507782+00:00",
            sensor=sensor,
            value=float(request.POST["value"]),
        )

        return HttpResponse(content=sensor_reading)