from django.urls import path
from splunkAutomation.logic.Constants import Constants
from . import views

app_name = 'celery_progress'
urlpatterns = [
    path('task_progress/<int:task_id>/',views.get_progress, name='task_status'),
]

