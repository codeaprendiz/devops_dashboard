import json
from django.http import HttpResponse
from celery_progress.backend import Progress
from rest_framework import status
from rest_framework.response import Response


def get_progress(request, task_id):
    progress = Progress(str(task_id))
    if progress.get_info()['complete'] == False:
    	content = {'please move along': 'nothing to see here'}
    	return HttpResponse(content, status=status.HTTP_404_NOT_FOUND)

    return HttpResponse(json.dumps(progress.get_info()), content_type='application/json')
