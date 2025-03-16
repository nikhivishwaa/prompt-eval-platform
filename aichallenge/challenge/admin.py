from django.contrib import admin
from challenge.models import Event, Participation


# Register your models here.

@admin.register(Event)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_name', 'event_description', 'status')
    search_fields = ('event_name', 'event_description')
    ordering = ('id',)
    model = Event

    def status(self, obj):
        import datetime as dt

        if obj.start_ts < dt.datetime.now(dt.timezone.utc) < obj.end_ts:
            return 'Ongoing'
        elif obj.end_ts < dt.datetime.now(dt.timezone.utc):
            return 'Completed'
        else:
            return 'Upcoming'

    def participant(self, obj):
        count = Participation.objects.filter(event=obj).count()
        return count

@admin.register(Participation)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'user', 'joined_at', 'finished_at')
    aggregate_fields = ('event',)
    ordering = ('id',)
    model = Participation

    # def participant(self, obj):
    #     count = Participation.objects.filter(event=obj).count()
    #     return count