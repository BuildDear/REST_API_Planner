from django.urls import path
from .views import *

# urlpatterns = [
#     path('task/all/', TaskView.as_view(), name='view-task'),
#     path('task/search/', TaskSearchView.as_view(), name='search-task'),
#     path('task/create/', TaskCreateView.as_view(), name='create-task'),
#     path('task/delete/<str:name>/', TaskDeleteView.as_view(), name='delete-task'),
#     path('task/edit/<str:name>/', TaskEditView.as_view(), name='task-edit'),
# ]