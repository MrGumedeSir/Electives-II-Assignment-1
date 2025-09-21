from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    # extra fields could be added here
    pass

class Activity(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.title

class Session(models.Model):
    activity = models.ForeignKey(Activity, related_name='sessions', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    capacity = models.IntegerField(default=10)
    def __str__(self):
        return f"{self.activity.title} @ {self.start_time}"

class Booking(models.Model):
    STATUS_CHOICES = [('pending','pending'),('confirmed','confirmed'),('cancelled','cancelled')]
    user = models.ForeignKey('User', related_name='bookings', on_delete=models.CASCADE)
    session = models.ForeignKey(Session, related_name='bookings', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)

class HydrationLog(models.Model):
    user = models.ForeignKey('User', related_name='hydration_logs', on_delete=models.CASCADE)
    amount_ml = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=timezone.now)

class ActivityLog(models.Model):
    user = models.ForeignKey('User', related_name='activity_logs', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    duration_minutes = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=timezone.now)