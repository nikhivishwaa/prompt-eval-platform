from django.db import models
from accounts.models import User
from challenge.models import Participation

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    task = models.TextField(null=False, blank=False)
    active_status = models.BooleanField(default=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class Submission(models.Model):
    participant = models.ForeignKey(Participation, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    prompt = models.TextField(null=False, blank=False)
    submitted_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    last_updated = models.DateTimeField(auto_now=True)
    evaluated = models.BooleanField(default=False, null=False, blank=False)
    clarity = models.FloatField(default=0.0, null=False, blank=False)
    creativity = models.FloatField(default=0.0, null=False, blank=False)
    relavance = models.FloatField(default=0.0, null=False, blank=False)
    optimization = models.FloatField(default=0.0, null=False, blank=False)
    def __str__(self):
        return self.prompt

    def getscore(self):
        score = 0.4 * self.creativity + 0.3 * self.clarity + 0.2 * self.relavance + 0.1 * self.optimization
        return score

    class Meta:
        ordering = ['submitted_at']
        unique_together = ['participant', 'task']
        

class PromptTask(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    submitted_at = models.DateTimeField()
    started_at = models.DateTimeField()