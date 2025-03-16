from django.contrib import admin
from challenge.models import Event, Participation


# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_name', 'event_description', 'status','participants')
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

    def participants(self, obj):
        count = Participation.objects.filter(event=obj).count()
        return count

@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_name', 'user', 'enrolled_at', 'round1_score', 'round2_score')
    aggregate_fields = ('event_name',)
    ordering = ('enrolled_at','finished_at', 'round1_score', 'round2_score')
    model = Participation

    def event_name(self, obj):
        return obj.event.event_name