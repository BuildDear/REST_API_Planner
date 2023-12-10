from django.contrib import admin
from .models import EventCategory, Note, Event, Task
from user.models import User


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created']
    search_fields = ['name']
    list_filter = ['created', 'name']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'is_public', 'created', 'get_attendee_count']
    search_fields = ['name']
    list_filter = ['is_public', 'created']
    filter_horizontal = ['notes', 'attendees']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'due_date', 'completed', 'is_overdue']
    search_fields = ['title']
    list_filter = ['due_date', 'completed']

    def display_events(self, obj):
        return ", ".join([event.name for event in obj.events.all()])

    display_events.short_description = 'Events'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_superuser']
    search_fields = ['username', 'email']
    list_filter = ['is_superuser', "username", "email"]
