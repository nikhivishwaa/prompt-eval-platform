from django.db import models
from accounts.models import User
from challenge.models import Participation, Event
import datetime as dt

class Task(models.Model):
    LABEL = [('r1', 'Round 1'), 
             ('r2', 'Round 2')]
    detail = models.TextField(null=False, blank=False)
    active_status = models.BooleanField(default=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    task_label = models.CharField(max_length=2, choices=LABEL, default='r1')

    def __str__(self):
        return f"#{self.id} : {self.task_label} : {self.detail}"

    
    def save(self, *args, **kwargs):
        self.last_updated = dt.datetime.now(dt.timezone.utc)
        super().save(*args, **kwargs)

class ImageTask(models.Model):
    LABEL = [('r1', 'Round 1'), 
             ('r2', 'Round 2')]
    detail = models.TextField(null=False, blank=False)    
    ref_image = models.FileField(upload_to='ref_image/', null=True, blank=True)
    active_status = models.BooleanField(default=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    task_label = models.CharField(max_length=2, choices=LABEL, default='r1')

    def __str__(self):
        return f"#{self.id} : {self.task_label} : {self.detail}"

    
    def save(self, *args, **kwargs):
        self.last_updated = dt.datetime.now(dt.timezone.utc)
        super().save(*args, **kwargs)


class EventRound1(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    desc = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.event} : {self.title}"

    class Meta:
        unique_together = ['event', 'task']

class EventRound2(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    task = models.ForeignKey(ImageTask, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    desc = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.event} : {self.title}"

    class Meta:
        unique_together = ['event', 'task']

class Round1Submission(models.Model):
    participant = models.ForeignKey(Participation, on_delete=models.CASCADE)
    round1_task = models.ForeignKey(EventRound1, on_delete=models.CASCADE)
    prompt = models.TextField(null=False, blank=False)
    submitted_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    last_updated = models.DateTimeField(auto_now=True)
    evaluated = models.BooleanField(default=False, null=False, blank=False)
    clarity = models.FloatField(default=0.0, null=False, blank=False)
    creativity = models.FloatField(default=0.0, null=False, blank=False)
    relavance = models.FloatField(default=0.0, null=False, blank=False)
    optimization = models.FloatField(default=0.0, null=False, blank=False)
    score = models.FloatField(default=0.0, null=False, blank=False)
    def __str__(self):
        return f"{self.participant.user} : {self.round1_task} : {self.prompt}"

    def getscore(self):
        score = 0.4 * self.creativity + 0.3 * self.clarity + 0.2 * self.relavance + 0.1 * self.optimization
        return score

    def save(self, *args, **kwargs):
        self.score = self.getscore()
        self.last_updated = dt.datetime.now(dt.timezone.utc)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['submitted_at']
        unique_together = ['participant', 'round1_task']

class Round2Submission(models.Model):
    participant = models.ForeignKey(Participation, on_delete=models.CASCADE)
    round2_task = models.ForeignKey(EventRound2, on_delete=models.CASCADE)
    generated_image = models.FileField(upload_to='generated_image/', null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    last_updated = models.DateTimeField(auto_now=True)
    # scoring
    evaluated = models.BooleanField(default=False, null=False, blank=False)
    clarity = models.FloatField(default=0.0, null=False, blank=False)
    creativity = models.FloatField(default=0.0, null=False, blank=False)
    relavance = models.FloatField(default=0.0, null=False, blank=False)
    watermark_detection = models.FloatField(default=0.0, null=False, blank=False)
    similarity = models.FloatField(default=0.0, null=False, blank=False)
    authenticity = models.FloatField(default=0.0, null=False, blank=False)
    score = models.FloatField(default=0.0, null=False, blank=False)
    # plagrism
    plagrism_checked = models.BooleanField(default=False, null=False, blank=False)
    plagrism_detected = models.BooleanField(default=False, null=False, blank=False)
    plagrism_result = models.JSONField(null=True, blank=True)
    def __str__(self):
        return f"{self.participant.user} : {self.round2_task} : {self.generated_image}"

    def getscore(self):
        score = sum([
                    0.2 * self.creativity,
                    0.15 * self.clarity,
                    0.2 * self.relavance,
                    0.1 * self.watermark_detection,
                    0.15 * self.similarity,
                    0.2 * self.authenticity
                ])

        if self.plagrism_detected == True:
            score = score * 0.8
        return score

    def save(self, *args, **kwargs):
        self.score = self.getscore()
        self.last_updated = dt.datetime.now(dt.timezone.utc)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['submitted_at']
        unique_together = ['participant', 'round2_task']