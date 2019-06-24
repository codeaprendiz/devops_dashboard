import json
import requests
import sys
from splunkAutomation.logic.Constants import Constants
from splunkAutomation.models import SplunkQuery
from splunkAutomation.models import GenericIssue


res = requests.get("https://prod.com/ukgrsps/assemblies/commerce/operations/environments/prod/platforms/commerceApp/components/hostname/instances.json?instances_state=all",auth=("username", "password"))

"""
url_assembly="https://cloud.prod.com/ukgrsps/assemblies"
url_env="https://cloud.prod.com/ukgrsps/assemblies/{assembly}/transition/environments"
url_platform="https://cloud.prod.com/ukgrsps/assemblies/{assembly}/transition/environments/{environment}/platforms"
url_host="https://cloud.prod.com/ukgrsps/assemblies/{assembly}/operations/environments/{environment}/platforms/{platform}/components/{component}/instances.json?instances_state=all"
username="username"
password="wHat@123"




import json
import requests
auth=(username,password)
h = {"Content-Type" : "application/json", "Accept" : "application/json"}
responseObj = requests.get(url, auth=auth, headers=h)
jr = json.loads(responseObj.content)
list_assemblies=[]
while i<len(jr):
	item=jr[i]
	str=item['ciName']
	list_assemblies.append(str)
	i+=1


responseObj = requests.get(url_env, auth=auth, headers=h)
list_env=[]
while i<len(jr):
	item=jr[i]
	str=item['ciName']
	list_env.append(str)
	i+=1








"""

class MessageLogger:
	def __init__(self):
		self.w = sys.stdout

	def log(self, fmt, *args):
		if len(args) != 0:
			self.w.write(fmt%args)
		else:
			self.w.write(fmt)
		self.w.write("\n")

class OneOpsClient:


	def __init__(self, dictObj=None ):
		self.organization=dictObj['organization']
		self.assembly=dictObj['assembly']
		self.environment=dictObj['environment']
		self.platform=dictObj['platform']
		self.component=dictObj['component']

	def getHostNames(self):
		url=Constants.ONEOPS_GET_HOSTNAMES
		url=url.replace("{organization}",self.organization)
		url=url.replace("{assembly}",self.assembly)
		url=url.replace("{environment}",self.environment)
		url=url.replace("{platform}",self.platform)
		url=url.replace("{component}",self.component)
		auth=(Constants.ONEOPS_USERNAME, Constants.ONEOPS_PASSWORD)
		responseObj = requests.get(url, auth=auth)
		jr = json.loads(responseObj.content)
		i=0
		list_hostnames=[]
		while i<len(jr):
			item=jr[i]
			str=item['ciAttributes']['entries']
			cloudData=item['cloud']['toCi']['ciName']
			str=str.replace('{','').replace('}','').replace('"','').replace('[','').replace(']','')
			list=str.split(',')
			host=list[1].split(':')
			list_hostnames.append(host[0])
			i+=1
		return list_hostnames

	def getHostnameAndCloud(self):
		url=Constants.ONEOPS_GET_HOSTNAMES
		url=url.replace("{organization}",self.organization)
		url=url.replace("{assembly}",self.assembly)
		url=url.replace("{environment}",self.environment)
		url=url.replace("{platform}",self.platform)
		url=url.replace("{component}",self.component)
		auth=(Constants.ONEOPS_USERNAME, Constants.ONEOPS_PASSWORD)
		responseObj = requests.get(url, auth=auth)
		jr = json.loads(responseObj.content)
		i=0
		list_hostnames=[]
		hostCloud={}
		while i<len(jr):
			item=jr[i]
			str=item['ciAttributes']['entries']
			cloudData=item['cloud']['toCi']['ciName']
			str=str.replace('{','').replace('}','').replace('"','').replace('[','').replace(']','')
			list=str.split(',')
			host=list[1].split(':')
			list_hostnames.append(host[0])
			hostCloud[host[0]]=cloudData
			i+=1
		print(hostCloud)
		return hostCloud


	def getEnvironments(self):
		url=Constants.ONEOPS_GET_ENVIRONMENTS
		url=url.replace("{organization}",self.organization)
		url=url.replace("{assembly}",self.assembly)
		auth=(Constants.ONEOPS_USERNAME, Constants.ONEOPS_PASSWORD)
		responseObj = requests.get(url, auth=auth)
		jr = json.loads(responseObj.content)
		i=0
		list_env=[]
		while i<len(jr):
			item=jr[i]
			str=item['ciName']
			list_env.append(str)
			i+=1
		return list_env


	def getCloudWiseInstanceDetails(self):
		url=Constants.ONEOPS_GET_HOSTNAMES
		url=url.replace("{organization}",self.organization)
		url=url.replace("{assembly}",self.assembly)
		url=url.replace("{environment}",self.environment)
		url=url.replace("{platform}",self.platform)
		url=url.replace("{component}",self.component)
		auth=(Constants.ONEOPS_USERNAME, Constants.ONEOPS_PASSWORD)
		responseObj = requests.get(url, auth=auth)
		jr = json.loads(responseObj.content)
		i=0
		list_hostnames=[]
		dictOfInstaToCloud={}
		dictOfCloudToInstances={}
		clouds=set()
		while i<len(jr):
			item=jr[i]
			str=item['ciAttributes']['entries']
			cloudData=item['cloud']['toCi']['ciName']
			str=str.replace('{','').replace('}','').replace('"','').replace('[','').replace(']','')
			list=str.split(',')
			host=list[1].split(':')
			list_hostnames.append(host[0])
			dictOfInstaToCloud[host[0]]=cloudData
			i+=1
		for key, value in dictOfInstaToCloud.items():
			clouds.add(value)
			dictOfCloudToInstances[value]=0
		for key, value in dictOfInstaToCloud.items():
			dictOfCloudToInstances[value]=dictOfCloudToInstances[value]+1
		print(dictOfCloudToInstances)
		return dictOfCloudToInstances






class AppVault:
	REGISTER = "/v3/auth/KeypairAuth/register"
	LOGIN = "/v3/auth/KeypairAuth/login"

	RENEW = "/v3/auth/renew"
	SIGN = "/v3/auth/sign"

	STORE = "/v3/data/store"
	RETREIVE = "/v3/data/retrieve"
	DELETE = "/v3/data/delete"
	UPDATE = "/v3/data/update"
	HANDLES = "/v3/data/handles"

	def __init__(self, clientName, zoneName, DL, url_http, url_https=None):
		self.clientName = clientName
		self.zoneName = zoneName
		self.DL = DL;
		self.crypto = Crypto()
		self.token = None
		self.L = MessageLogger()
		AppVault.URL = url_http
		if TLS:
			AppVault.URL = url_https
		self.L.log("AppVault URL is " + AppVault.URL)

	def store(self, data, dataDesc, authz=[], file_mode=False, file=None):
		if self.token is None:
			self.L.log("Client %s is not logged in ", self.clientName)
			return

		if file_mode == True and not file is None and len(file) != 0:
			if os.path.exists(file):
				with open(file, "rb") as f:
					data = f.read()
			else:
				self.L.log("File does not exists !")
				return

		payload = {
			"data" : unicode(data, errors="ignore"),
			"dataDesc" : dataDesc,
			"authz" : authz
		}

		h = {
			"Authorization" : "Bearer {}".format(self.token)
		}

		if PAYLOAD:
			self.L.log("Authorization: Bearer {}".format(self.token))
			self.L.log(json.dumps(payload, indent=2, separators=[",", ":"]))

		res = requests.post( AppVault.URL +  AppVault.STORE, json=payload, headers=h, cert=(KeyStore_PEM), verify=KeyStore_PEM)

		jr = json.loads(res.content)

		self.L.log("Store %s status : %d", dataDesc, res.status_code)

		if VERBOSE:
			self.L.log(json.dumps(jr, indent=2, separators=[",", ":"]))

	def delete(self, dataRefId=None):
		if self.token is None:
			self.L.log("Client %s is not logged in ", self.clientName)
			return

		h = {
			"Authorization" : "Bearer {}".format(self.token)
		}

		if PAYLOAD:
			self.L.log("Authorization: Bearer {}".format(self.token))
			self.L.log(AppVault.URL + AppVault.DELETE + "?dataRefId=%s", dataRefId)

		res = requests.delete( AppVault.URL +  AppVault.DELETE + "?dataRefId={}".format(dataRefId), headers=h, cert=(KeyStore_PEM), verify=KeyStore_PEM)
		jr = json.loads(res.content)

		self.L.log("Delete {} status : {}".format(dataRefId, res.status_code))
		if VERBOSE:
			self.L.log(json.dumps(jr, indent=2, separators=[",", ":"]))


	def handles(self):
		if self.token is None:
			self.L.log("Client %s is not logged in ", self.clientName)
			return

		h = {
			"Authorization" : "Bearer {}".format(self.token)
		}

		if PAYLOAD:
			self.L.log("Authorization: Bearer %s", self.token)
			self.L.log(AppVault.URL + AppVault.HANDLES)

		res = requests.get(AppVault.URL + AppVault.HANDLES, headers=h, cert=(KeyStore_PEM), verify=KeyStore_PEM);
		jr = json.loads(res.content)

		if VERBOSE:
			self.L.log("Handles status %d", jr["status"])
			self.L.log(json.dumps(jr, indent=2, separators=[",", ":"]))
		else:
			self.L.log("\n".join("DataRefId:{}, Data Desc:{}, Data Owner:{}".format(x["dataRefId"], x["dataDesc"], x["ownerName"]) for x in jr["handles"]))
