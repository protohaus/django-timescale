import uuid
from datetime import timedelta, datetime

from django.db import models, IntegrityError, connection
from django.utils.dateparse import parse_datetime


class Sensor(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=50)
    unit = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class SensorReading(models.Model):
    time = models.DateTimeField(primary_key=True, default=datetime.now)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    value = models.FloatField()

    def save(self, *args, **kwargs):
        self.save_and_smear_timestamp(*args, **kwargs)
    
    def save_and_smear_timestamp(self, *args, **kwargs):
        """Recursivly try to save by incrementing the timestamp on duplicate error"""
        try:
            super().save(*args, **kwargs)
        except IntegrityError as exception:
            # Only handle the error:
            #   psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint "1_1_farms_sensorreading_pkey"
            #   DETAIL:  Key ("time")=(2020-10-01 22:33:52.507782+00) already exists.
            if all (k in exception.args[0] for k in ("Key","time", "already exists")):
                # Increment the timestamp by 1 µs and try again
                self.time = str(parse_datetime(self.time) + timedelta(microseconds=1))
                self.save_and_smear_timestamp(*args, **kwargs)

    def __str__(self):
        return f"{self.value}@{self.time}"