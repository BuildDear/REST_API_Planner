from django.urls import path, include
from rest_framework.routers import DefaultRouter
from manager.views import NoteViewSet, EventViewSet, EventCategoryViewSet, TaskViewSet

router = DefaultRouter()
router.register(r'notes', NoteViewSet)
router.register(r'events', EventViewSet)
router.register(r'event-categories', EventCategoryViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),

]
