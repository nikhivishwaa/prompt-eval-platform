from django.contrib import admin
from challenge.models import Event, Participation


# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_name', 'event_status','r1_status','round1_threshold','r2_status','round2_threshold','participants')
    search_fields = ('event_name',)
    # list_filter = ('event_status','r1_status','r2_status')
    ordering = ('id',)
    model = Event

    def event_status(self, obj):
        import datetime as dt

        if obj.round1_start_ts < dt.datetime.now(dt.timezone.utc) < obj.round2_end_ts:
            return 'Ongoing'
        elif obj.round2_end_ts < dt.datetime.now(dt.timezone.utc):
            return 'Completed'
        else:
            return 'Upcoming'

    def r1_status(self, obj):
        import datetime as dt

        if obj.round1_start_ts < dt.datetime.now(dt.timezone.utc) < obj.round1_end_ts:
            return 'Ongoing'
        elif obj.round1_end_ts < dt.datetime.now(dt.timezone.utc):
            return 'Completed'
        else:
            return 'Upcoming'

    def r2_status(self, obj):
        import datetime as dt

        if obj.round2_start_ts < dt.datetime.now(dt.timezone.utc) < obj.round2_end_ts:
            return 'Ongoing'
        elif obj.round2_end_ts < dt.datetime.now(dt.timezone.utc):
            return 'Completed'
        else:
            return 'Upcoming'

    def participants(self, obj):
        count = Participation.objects.filter(event=obj).count()
        return count

@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_name', 'user', 
                    'enrolled_at', 'round1_score','round1_rank',
                    'round1_evaluated','round1_end_reason','round1_status', 'round2_score',
                    'round2_rank','round2_evaluated','round2_end_reason','round2_status')
    aggregate_fields = ('event_name',)
    # list_filter = ('event_name','round1_status','round2_status','round1_end_reason','round2_end_reason')
    ordering = ('enrolled_at','finished_at', 'round1_score', 'round2_score','round1_rank','round2_rank',)
    model = Participation

    def event_name(self, obj):
        return obj.event.event_name