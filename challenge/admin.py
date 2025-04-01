from django.contrib import admin
from challenge.models import Event, Participation
from django.http import HttpResponse
from challenge.reports import round1_report, round2_report
import csv


# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_name', 'event_status','r1_status','round1_threshold','r2_status','round2_threshold','participants')
    search_fields = ('event_name',)
    # list_filter = ('event_status','r1_status','r2_status')
    ordering = ('id',)
    model = Event
    actions = ['generate_round1_report','generate_round2_report']

    def generate_round1_report(self, request, queryset):
        # Creating a CSV file
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="round1_report.csv"'

        writer = csv.writer(response)

        for event in queryset:
            report = round1_report(event.id)
            writer.writerow(report['columns'])
            writer.writerows(report['data'])
        
            return response

    def generate_round2_report(self, request, queryset):
        # Creating a CSV file
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="round2_report.csv"'

        writer = csv.writer(response)

        for event in queryset:
            report = round1_report(event.id)
            writer.writerow(report['columns'])
            writer.writerows(report['data'])
        
            return response

    generate_round1_report.short_description = "Generate CSV Report for Round1 of Selected Event"
    generate_round2_report.short_description = "Generate CSV Report for Round2 of Selected Event"


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