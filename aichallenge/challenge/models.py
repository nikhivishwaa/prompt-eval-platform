from django.db import models
from accounts.models import User

# Create your models here.
class Event(models.Model):
    event_name = models.CharField(max_length=100)
    event_description = models.TextField()
    event_rules = models.TextField()
    start_ts = models.DateTimeField(null=False, blank=False)
    end_ts = models.DateTimeField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null= False)
    last_updated = models.DateTimeField(auto_now=True, blank=False, null=False)

    def __str__(self):
        return self.event_name

class Participation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now=True, null=False, blank=False)
    finished_at = models.DateTimeField(blank=True, null= True)
    last_updated = models.DateTimeField(auto_now=True, blank=False, null=False)

    def __str__(self):
        return f'{self.event.event_name} - {self.user.last_name}'