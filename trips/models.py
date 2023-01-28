import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import reverse
from rest_framework_api_key.models import AbstractAPIKey

class User(AbstractUser):
    photo = models.ImageField(upload_to='photos', null=True, blank=True)

    @property
    def group(self):
        groups = self.groups.all()
        return groups[0].name if groups else None

class UserAPIKey(AbstractAPIKey):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="api_keys",
    )

class Trip(models.Model):
    REQUESTED = 'REQUESTED'
    STARTED = 'STARTED'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    STATUSES = (
        (REQUESTED, REQUESTED),
        (STARTED, STARTED),
        (IN_PROGRESS, IN_PROGRESS),
        (COMPLETED, COMPLETED),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    pick_up_address = models.CharField(max_length=255)
    drop_off_address = models.CharField(max_length=255)
    image = models.ImageField(upload_to='trips', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUSES, default=REQUESTED)
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='trips_as_driver'
    )
    rider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='trips_as_rider'
    )

    def __str__(self):
        return f'{self.id}'

    def get_absolute_url(self):
        return reverse('trip:trip_detail', kwargs={'trip_id': self.id})
