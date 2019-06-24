import json
import requests
import sys
from splunkAutomation.logic.Constants import Constants
from splunkAutomation.models import SplunkQuery
from splunkAutomation.models import GenericIssue




class MessageLogger:
	def __init__(self):
		self.w = sys.stdout

	def log(self, fmt, *args):
		if len(args) != 0:
			self.w.write(fmt%args)
		else:
			self.w.write(fmt)
		self.w.write("\n")

class Utilities:


	def __init__(self):
		dummy = "variable"

	def getModelValues(self,issue_id):
		dictObj={}
		objList = GenericIssue.objects.all()
		for obj in objList:
			if issue_id==obj.id:
				dictObj['issue']=obj.issue
				dictObj['command_set']=obj.command_set
				dictObj['organization']=obj.organization
				dictObj['assembly']=obj.assembly
				dictObj['environment']=obj.environment
				dictObj['platform']=obj.platform
				dictObj['component']=obj.component
				dictObj['application']=obj.application
				dictObj['resolve_conf']=obj.resolve_conf
		return dictObj
