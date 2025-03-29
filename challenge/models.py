from django.db import models
from accounts.models import User
import datetime as dt

# Create your models here.
class Event(models.Model):
    event_name = models.CharField(max_length=100, blank=False, null=False)
    event_desc = models.TextField()
    event_rules = models.TextField()
    # round 1
    round1_start_ts = models.DateTimeField(null=False, blank=False)
    round1_end_ts = models.DateTimeField(null=False, blank=False)
    round1_threshold = models.IntegerField(default=60, null=False, blank=False)
    # round 2
    round2_start_ts = models.DateTimeField(null=False, blank=False)
    round2_end_ts = models.DateTimeField(null=False, blank=False)
    round2_threshold = models.IntegerField(default=30, null=False, blank=False)
    # event
    open_event = models.BooleanField(default=True, null=False, blank=False)
    stop_entry = models.BooleanField(default=False, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null= False)
    last_updated = models.DateTimeField(auto_now=True, blank=False, null=False)

    def __str__(self):
        return self.event_name

    def event_status(self):
        now = dt.datetime.now(dt.timezone.utc)
        if self.round1_start_ts < now < self.round2_end_ts:
            return "Ongoing"
        elif now > self.round2_end_ts:
            return "Finished"
        else:
            return "Upcoming"

    def round1_status(self):
        now = dt.datetime.now(dt.timezone.utc)
        if self.round1_start_ts < now < self.round1_end_ts:
            return "Ongoing"
        elif now > self.round1_end_ts:
            return "Finished"
        else:
            return "Upcoming"

    def round2_status(self):
        now = dt.datetime.now(dt.timezone.utc)
        if self.round2_start_ts < now < self.round2_end_ts:
            return "Ongoing"
        elif now > self.round2_end_ts:
            return "Finished"
        else:
            return "Upcoming"
    
    def save(self, *args, **kwargs):
        self.last_updated = dt.datetime.now(dt.timezone.utc)
        super().save(*args, **kwargs)

class Participation(models.Model):
    CHOICES = (('qualified', 'Qualified'),
                ('not-qualified', 'Not Qualified')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now=True, null=False, blank=False)
    started_at = models.DateTimeField(blank=True, null= True)
    finished_at = models.DateTimeField(blank=True, null= True)
    last_updated = models.DateTimeField(auto_now=True, blank=False, null=False)
    #  round 1
    round1_score = models.FloatField(null=True, blank=True)
    round1_evaluated = models.BooleanField(default=False, null=True, blank=True)
    round1_finish_time = models.DateTimeField(null=True, blank=True)
    round1_status = models.CharField(max_length=20, choices=CHOICES, null=True, blank=True)
    round1_rank = models.IntegerField(null=True, blank=True)

    #  round 2
    round2_score = models.FloatField(null=True, blank=True)
    round2_evaluated = models.BooleanField(default=False, null=True, blank=True)
    round2_finish_time = models.DateTimeField(null=True, blank=True)
    round2_status = models.CharField(max_length=20, choices=CHOICES, null=True, blank=True)
    round2_rank = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f'{self.event} - {self.user}'

    def save(self, *args, **kwargs):
        self.last_updated = dt.datetime.now(dt.timezone.utc)
        super().save(*args, **kwargs)