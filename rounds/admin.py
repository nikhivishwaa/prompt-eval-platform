from django.contrib import admin
from .models import Task, Round1Submission, EventRound1, EventRound2, Participation, ImageTask, Round2Submission


# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'detail', 'task_label','active_status')
    search_fields = ('detail',)
    list_filter = ('active_status','task_label')
    ordering = ('id',)
    model = Task

@admin.register(ImageTask)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'detail', 'task_label','active_status', 'ref_image')
    search_fields = ('detail',)
    list_filter = ('active_status','task_label')
    ordering = ('id',)
    model = ImageTask


@admin.register(EventRound1)
class EventRound1Admin(admin.ModelAdmin):
    list_display = ('id', 'event_name', 'title', 'task','total_participant', 'total_submission')
    search_fields = ('title',)
    # list_filter = ('evaluated',)
    ordering = ('id',)
    model = EventRound1

    def total_participant(self, obj):
        participant = Participation.objects.filter(event=obj.event).count()
        return participant

    def total_submission(self, obj):
        submission = Round1Submission.objects.filter(round1_task=obj).count()
        return submission

    def event_name(self, obj):
        return f"{obj.event}"

    def task(self, obj):
        return f"{str(obj.task.title)[:30]}..."

@admin.register(EventRound2)
class EventRound2Admin(admin.ModelAdmin):
    list_display = ('id', 'event_name', 'title', 'task','total_participant', 'total_submission')
    search_fields = ('title',)
    # list_filter = ('evaluated',)
    ordering = ('id',)
    model = EventRound2

    def total_participant(self, obj):
        participant = Participation.objects.filter(event=obj.event).count()
        return participant

    def total_submission(self, obj):
        submission = Round2Submission.objects.filter(round2_task=obj).count()
        return submission

    def event_name(self, obj):
        return f"{obj.event}"

    def task(self, obj):
        return f"{str(obj.task.title)[:30]}..."

@admin.register(Round1Submission)
class Round1SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_name', 'user','task','evaluated', 'clarity', 'creativity', 'relavance', 'optimization', 'score', 'submitted_at')
    search_fields = ('prompt',)
    list_filter = ('evaluated',)
    ordering = ('id','submitted_at',)
    model = Round1Submission

    def score(self, obj):
        score = 0.4 * obj.creativity + 0.3 * obj.clarity + 0.2 * obj.relavance + 0.1 * obj.optimization
        return score

    def event_name(self, obj):
        return f"{obj.participant.event}"

    def user(self, obj):
        return f"{obj.participant.user}"
    def task(self, obj):
        return f"{str(obj.round1_task.title)[:30]}..."

@admin.register(Round2Submission)
class Round2SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_name', 'user','task', 'generated_image', 'evaluated', 'clarity', 'creativity', 'relavance', 'authenticity', 'similarity', 'watermark_detection', 'score', 'plagrism_detected', 'submitted_at')
    # search_fields = ('prompt',)
    list_filter = ('evaluated',)
    ordering = ('id','submitted_at',)
    model = Round2Submission

    def score(self, obj):
        return obj.getscore()

    def event_name(self, obj):
        return f"{obj.participant.event}"

    def user(self, obj):
        return f"{obj.participant.user}"
    def task(self, obj):
        return f"{str(obj.round2_task.title)[:30]}..."
