from devOpsDashboardAdmin import celery_app
from time import sleep
from celery import shared_task
from splunkAutomation.models import SplunkQuery
import json
from splunkAutomation.logic.SplunkClient import SplunkClient
from splunkAutomation.logic.Constants import Constants

 
@celery_app.task()
def UploadTask(message):
 
    # Update the state. The meta data is available in task.info dicttionary
    # The meta data is useful to store relevant information to the task
    # Here we are storing the upload progress in the meta. 
 
    UploadTask.update_state(state='PROGRESS', meta={'progress': 0})
    sleep(30)
    UploadTask.update_state(state='PROGRESS', meta={'progress': 30})
    sleep(30)
    return message
 
 
def get_task_status(task_id):
 
    # If you have a task_id, this is how you query that task 
    task = UploadTask.AsyncResult(task_id)
 
    status = task.status
    progress = 0
 
    if status == u'SUCCESS':
        progress = 100
    elif status == u'FAILURE':
        progress = 0
    elif status == 'PROGRESS':
        progress = task.info['progress']
 
    return {'status': status, 'progress': progress}


#splunkClientProd = SplunkClient(Constants.SPLUNK_QA_HOSTNAME1,Constants.SPLUNK_QA_PORT,Constants.SPLUNK_QA_USERNAME,Constants.SPLUNK_QA_PASSWORD)
#curl -u admin:asda@splunk -k http://searchheadcluster-318834219-1-318931733.qa.splunk-qa.ukgrsps.prod.company.com:8089/services/search/jobs -d search="search *"
#curl -u admin:asda@splunk -k https://searchheadcluster-318834219-1-318931733.qa.splunk-qa.ukgrsps.prod.company.com:8089/services/search/jobs/1258421375.19/results/ --get -d output_mode=csv




@shared_task
def executeSplunkQuery(argList):
    queryList=SplunkQuery.objects.all()
    query_id=argList
    searchQuery=""
    for query in queryList:
        if query.id == query_id:
            searchQuery=query.query_text
    searchQuery="search " + searchQuery
    splunkClientQA = SplunkClient(Constants.SPLUNK_QA_HOSTNAME1,Constants.SPLUNK_QA_PORT,Constants.SPLUNK_QA_USERNAME,Constants.SPLUNK_QA_PASSWORD)
    list_of_hostnames=splunkClientQA.createJob(searchQuery)
    #list_of_hostnames=splunkClientQA.createJob(Constants.QUERY_PQAESTORE)
    return list_of_hostnames
