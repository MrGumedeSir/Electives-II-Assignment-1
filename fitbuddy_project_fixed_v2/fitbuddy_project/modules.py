from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    def __str__(self):
        return self.get_full_name() or self.username

class Activity(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    default_capacity = models.PositiveIntegerField(default=12)
    def __str__(self):
        return self.title

class Session(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='sessions')
    start_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    capacity = models.PositiveIntegerField(null=True, blank=True)
    class Meta:
        ordering = ['start_time']
    def __str__(self):
        return f"{self.activity.title} @ {self.start_time:%Y-%m-%d %H:%M}"
    @property
    def effective_capacity(self):
        return self.capacity if self.capacity is not None else self.activity.default_capacity
    def confirmed_count(self):
        return self.bookings.filter(status='confirmed').count()
    def waiting_count(self):
        return self.bookings.filter(status='waiting').count()

class Booking(models.Model):
    STATUS_CHOICES = [('confirmed','Confirmed'),('waiting','Waiting'),('cancelled','Cancelled')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    position = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['created_at']
    
    @classmethod
    @transaction.atomic
    def create_booking(cls, user, session):
        if session.confirmed_count() < session.effective_capacity:
            status = 'confirmed'
            position = None
        else:
            status = 'waiting'
            position = session.waiting_count() + 1
        return cls.objects.create(user=user, session=session, status=status, position=position)

    @transaction.atomic
    def cancel(self):
        self.status = 'cancelled'
        self.save()
        if self.position is not None:
            # Shift remaining waitlisted users up
            Booking.objects.filter(session=self.session, status='waiting', position__gt=self.position).update(position=models.F('position') - 1)
            self.position = None
        else:
            # If a confirmed booking is cancelled, promote the next waitlisted user
            nxt = Booking.objects.filter(session=self.session, status='waiting').order_by('position','created_at').first()
            if nxt:
                nxt.status = 'confirmed'
                nxt.position = None
                nxt.save()
                waitings = Booking.objects.filter(session=self.session, status='waiting').order_by('created_at')
                for i,w in enumerate(waitings, start=1):
                    w.position = i
                    w.save()

class HydrationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hydration_logs')
    amount_ml = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    duration_minutes = models.PositiveIntegerField(default=10)
    calories_est = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    kind = models.CharField(max_length=20, choices=[('hydration','Hydration'),('workout','Workout')])
    remind_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['remind_at']    