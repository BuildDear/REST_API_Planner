from django.urls import path
from .views import *

urlpatterns = [

    path('', UserView.as_view(), name='create'),
    path('<int:pk>/', UserView.as_view(), name='create-id'),

]