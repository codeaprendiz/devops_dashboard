import json
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from splunkAutomation.models import SplunkQuery
from splunkAutomation.models import GenericIssue
from splunkAutomation.logic.SplunkClient import SplunkClient
from splunkAutomation.logic.OneOpsUtilities import OneOpsClient
from splunkAutomation.logic.Utilities import Utilities
from splunkAutomation.logic.Constants import Constants
import paramiko,sys
from celery.result import AsyncResult
from celery import task
from celery import shared_task
from celery_progress.backend import ProgressRecorder
import time
from splunkAutomation.tasks import executeSplunkQuery
from celery_progress.backend import Progress


##########################################################################################################################################
                                    # Tasks
##########################################################################################################################################







##########################################################################################################################################

def viewForIndexPageTheme1(request):
    return render(request, Constants.TEMPLATE_THEME1_INDEX_HTML)


def viewForIndexPageTheme2(request):
    with open("/tmp/python.txt") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    dict1={}
    listOfList=[]
    i=0
    for line in content:
        obj=line.replace("[","").replace("]","").split("--")
        dict1[str(i)]=[]
        for str1 in obj:
            dict1[str(i)].append(str1.replace("'","").strip())
        listOfList.append(dict1[str(i)])
        i=i+1

    context = {'listOfList' : listOfList}
    return render(request, Constants.TEMPLATE_THEME2_INDEX_HTML,context)


def viewForElementsPageTheme2(request):
    return render(request, Constants.TEMPLATE_THEME2_ELEMENTS_HTML)

def viewForSeeingGenericIssues(request):
    latest_query_list = GenericIssue.objects.all()
    context = {'latest_query_list': latest_query_list}
    return render(request,Constants.TEMPLATE_THEME2_TABLE_VIEW_IN_CONTAINER_WITH_BUTTONS_GENERIC_ISSUES, context)

setOutput=set()
def get_hostname_output_log_ssh(list_hostnames,index,command_set):
    ## Your code comes here
    if index >= len(list_hostnames):
        return None
    host=list_hostnames[index]
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname=host, username=Constants.USER, password=None, key_filename=Constants.PUBLIC_KEY_LOCATION)
    except  e:
        print(e)

    stdin, stdout, stderr = ssh.exec_command(command_set)
    output = stdout.readlines()
    output1 = stderr.readlines()
    setOutput.add('Hostname : '+host+'  '+'STDOUT : '.join(output)+' STDERR : '.join(output1)+"                                                                               ")
    ssh.close()
    return setOutput

    



def get_hostname_output_log(request):
    index = 0
    if "command_set" in request.session:
        command_set = request.session['command_set']
    if "index" in request.session:
        index = int(request.session['index'])
    if "list_hostnames" in request.session:
        list_hostnames=request.session['list_hostnames']   
    results = get_hostname_output_log_ssh(list_hostnames,index,command_set)
    if results is None:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    request.session['index'] = int(index + 1)
    return HttpResponse(results)


def results(request):
    if "index" in request.session:
        index = int(request.session['index'])
    if "command_set" in request.session:
        command_set = request.session['command_set']
    if "list_hostnames" in request.session:
        list_hostnames=request.session['list_hostnames']       
    results = get_hostname_output_log_ssh(list_hostnames,index,command_set)
    if results is None:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    request.session['index'] = int(index + 1)
    return render(request,Constants.TEMPLATE_THEME2_DISPLAY_OUTPUT)


def viewForSeeingGenericIssuesResults(request, issue_id):
    setOutput.clear()
    list_hostnames=[]

    dictObj = Utilities().getModelValues(issue_id)
    oneOpsClient = OneOpsClient(dictObj)
    list_hostnames=oneOpsClient.getHostNames()
    oneOpsClient.getCloudWiseInstanceDetails()
    request.session['index'] = int(0)
    request.session['command_set'] = dictObj['command_set']
    request.session['list_hostnames'] = list_hostnames
    return HttpResponseRedirect(reverse('splunkAutomation:results'))






def viewForSeeingAllSplunkQueries(request):
    latest_query_list = SplunkQuery.objects.all()
    context = {'latest_query_list': latest_query_list}
    return render(request,Constants.TEMPLATE_THEME2_TABLE_VIEW_IN_CONTAINER_WITH_BUTTONS, context)





def viewForSeeingQuerySpecificResults(request, query_id):
    #res = executeSplunkQuery.delay()
    #progress = Progress(res.id)
    #res=executeSplunkQuery.apply_async((argList),task_id=str(18))
    argList=[]
    argList.append(query_id)
    #res=executeSplunkQuery.apply_async((argList), task_id=str(220))
    #res=executeSplunkQuery.apply_async(argList)
    queryList=SplunkQuery.objects.all()
    searchQuery=""
    for query in queryList:
        if query.id == query_id:
            searchQuery=query.query_text
            commands_to_execute = query.query_resolution_commands
            host_resolve_conf = query.resolve_conf
            org=query.organization
            assembly=query.assembly
            env=query.environment
            platform=query.platform
            component=query.component

    searchQuery="search " + searchQuery
    #splunkClient = SplunkClient(Constants.SPLUNK_PROD_HOSTNAME1,Constants.SPLUNK_PROD_PORT,Constants.SPLUNK_PROD_USERNAME,Constants.SPLUNK_PROD_PASSWORD)
    #splunkClient = SplunkClient(Constants.SPLUNK_QA_HOSTNAME1,Constants.SPLUNK_QA_PORT,Constants.SPLUNK_QA_USERNAME,Constants.SPLUNK_QA_PASSWORD)
    
    #list_of_hostnames=splunkClient.createJob(searchQuery)

    list_of_hostnames=[]
    vip_list=[]
    oneOpsClient = OneOpsClient(org,assembly,env,platform,component);
    res=oneOpsClient.getHostNames()
    jr = json.loads(res.content)
    i=0
    while i<len(jr):
      item=jr[i]
      str=item['ciAttributes']['entries']
      str=str.replace('{','').replace('}','').replace('"','').replace('[','').replace(']','')
      list=str.split(',')
      host=list[1].split(':')
      list_of_hostnames.append(host[0])
      vip_list.append(host[0].split(".pqa.grocery-search.ukgrsps.qa.company.com")[0])
      i+=1

    context = {'myList': vip_list,'query_id':query_id}
    res=""
    list_of_hostnames=""
    return render(request, Constants.TEMPLATE_THEME2_CONTAINER_WITH_CHECKBOX_AND_BUTTONS, context)  

###########################################################################################################################
                # Views for sample templates
###########################################################################################################################


def viewForShowingProgressBar(request):
    return render(request, Constants.TEMPLATE_THEME2_CONTAINER_WITH_PROGRESS_BAR)


def viewForShowingLoader(request):
    return render(request, Constants.TEMPLATE_THEME2_CONTAINER_WITH_LOADER)

def viewForShowingPopUpWindow(request):
    return render(request, Constants.TEMPLATE_THEME2_POP_UP_WINDOW)











###########################################################################################################################
                # Views for other templates
###########################################################################################################################   





def viewForSeeingQueryResolutionResults(request, query_id):
    #if request.method == "POST":
    # Do validation stuff here
    hostnameList = request.POST.getlist('hostname') 
    #hostname = hostnameList[0]
    #hostname = hostname + ".prod.commerce.ukgrsps.dal1.prod.company.com"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    queryList=SplunkQuery.objects.all()
    searchQuery=""
    myList = []

    for query in queryList:
        if query.id == query_id:
            searchQuery=query.query_text
            commands_to_execute = query.query_resolution_commands
            host_resolve_conf = query.resolve_conf
            org=query.organization
            assembly=query.assembly
            env=query.environment
            platform=query.platform
            component=query.component

    oneOpsClient = OneOpsClient(org,assembly,env,platform,component);
    res=oneOpsClient.getHostNames()
    jr = json.loads(res.content)
    i=0
    while i<len(jr):
      item=jr[i]
      str=item['ciAttributes']['entries']
      str=str.replace('{','').replace('}','').replace('"','').replace('[','').replace(']','')
      list=str.split(',')
      host=list[1].split(':')
      i+=1


    for hostname in hostnameList:    
        ssh.connect(hostname=hostname+host_resolve_conf, username=Constants.USER, password=None, key_filename=Constants.PUBLIC_KEY_LOCATION)
        stdin, stdout, stderr = ssh.exec_command(commands_to_execute)
        output = stdout.readlines()
        output1 = stderr.readlines()
        myList.append(output+output1)
        ssh.close()
    context = {'myList': myList,'query_id':query_id}
    
    return render(request, Constants.TEMPLATE_THEME2_CONTAINER_WITH_PROGRESS_BAR, context)
    


def querySpeficResolve(request, query_id):
    hostname = "commerceapp-279244892-1-351584262.prod.commerce.ukgrsps.dfw6.prod.company.com"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username='app', password=None, key_filename="/Users/asr000p/.ssh/id_rsa.pub")
    stdin, stdout, stderr = ssh.exec_command('[ -f /log/server.log ] && echo "- Server Log File Exists" || /etc/init.d/jboss-container restart')
    output = stdout.readlines()
    myList = []
    myList.append(output)
    context = {'myList': myList}
    ssh.close()
    return render(request, 'SplunkAutomation/Theme2/querySpecific.html', context)







