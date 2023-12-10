from rest_framework import serializers

from user.models import User
from .models import Note, Event, EventCategory, Task


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True, read_only=True)
    attendees = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Event
        fields = '__all__'


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
