from django.contrib import admin
from .models import Task

# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'completed', 'due_at', 'posted_at')
    list_filter = ('priority', 'completed')
    ordering = ('-priority', '-posted_at')
