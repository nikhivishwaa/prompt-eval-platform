from django.contrib import admin
from .models import Task, PromptTask, Submission


# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'task', 'active_status')
    search_fields = ('title', 'description')
    list_filter = ('active_status',)
    ordering = ('id',)
    model = Task


@admin.register(Submission)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'evaluated', 'clarity', 'creativity', 'relavance', 'optimization', 'score')
    search_fields = ('prompt',)
    list_filter = ('evaluated',)
    ordering = ('id',)
    model = Submission

    def score(self, obj):
        score = 0.4 * obj.creativity + 0.3 * obj.clarity + 0.2 * obj.relavance + 0.1 * obj.optimization
        return score

# admin.site.register(PromptTask)