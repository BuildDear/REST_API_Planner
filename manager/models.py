from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from Calendario import settings


class EventCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    class Meta:
        db_table = 'event_category'

    def __str__(self):
        return self.name

    def get_event_count(self):
        return self.events.count()


class Note(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'note'

    def __str__(self):
        return f'name: {self.name}'

    def get_age(self):
        return timezone.now() - self.created


class Event(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=20)
    is_public = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    notes = models.ManyToManyField('Note')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_events')
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='attended_events')
    category = models.ForeignKey('EventCategory', on_delete=models.SET_NULL, null=True, related_name='events')

    class Meta:
        db_table = 'event'

    def __str__(self):
        return f'name: {self.name}'

    def get_attendee_count(self):
        return self.attendees.count()

    def add_note(self, note):
        self.notes.add(note)

    def is_upcoming(self):
        return self.created > timezone.now()


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    events = models.ManyToManyField(Event, related_name='tasks', blank=True)

    class Meta:
        db_table = 'task'

    def __str__(self):
        return self.title

    def is_overdue(self):
        return self.due_date < timezone.now() and not self.completed

    def mark_as_complete(self):
        self.completed = True
        self.save()


