#!/usr/bin/python2.7
import json
import OpenSSL
import socket
import os
import requests
import time
import sys
import random
from sets import Set
from argparse import ArgumentParser
from getpass import getpass

PAYLOAD = False
VERBOSE = False
TLS = False

STDOUT = sys.stdout

global KeyStore , KeyStore_PEM, PassPhrase
# openssl pkcs12 -in dummy.wal_mart.com.p12 -out dummy.wal_mart.com.pem

class PasswordContext(requests.packages.urllib3.contrib.pyopenssl.OpenSSL.SSL.Context):
	def __init__(self, method):
		super(PasswordContext, self).__init__(method)
		def passwd_cb(maxlen, prompt_twice, userdata):
			return PassPhrase if len(PassPhrase) < maxlen else ''
		self.set_passwd_cb(passwd_cb)
requests.packages.urllib3.contrib.pyopenssl.OpenSSL.SSL.Context = PasswordContext

class Crypto:
	def __init__(self):

		#load keys
		self.pub = None
		self.priv = None
		if os.path.exists(KeyStore):
			with open(KeyStore, "rb") as f:
				p12 = OpenSSL.crypto.load_pkcs12(f.read(), PassPhrase)
				pub_key = OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM, p12.get_certificate().get_pubkey())
				pub_key = pub_key.lstrip().rstrip()
				pub_key = "\n".join(pub_key.split("\n")[1:-1])
				priv_key = p12.get_privatekey()
				self.priv = priv_key
				self.pub = pub_key

	def getPub(self):
		return self.pub

	def sign(self, data):
		s = OpenSSL.crypto.sign(self.priv, data, "sha256").encode("base64").replace("\n", "")
		return s

class MessageLogger:
	def __init__(self):
		self.w = sys.stdout

	def log(self, fmt, *args):
		if len(args) != 0:
			self.w.write(fmt%args)
		else:
			self.w.write(fmt)
		self.w.write("\n")

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

	def register(self):
		payload = {
			"clientName" : self.clientName,
			"zoneName" : self.zoneName,
			"publicKey" : self.crypto.getPub(),
			"signAlgo" : "SHA256withRSA",
			"ownerEmail" : DL,
			"sign" : self.crypto.sign(self.clientName+self.zoneName+self.crypto.getPub()+DL)
		}

		if PAYLOAD:
			self.L.log(json.dumps(payload, indent=2, separators=[",", ":"]))

		res = requests.post( AppVault.URL +  AppVault.REGISTER, json=payload, cert=(KeyStore_PEM), verify=KeyStore_PEM)

		jr = json.loads(res.content)

		self.L.log("Register response : %d : %s", jr["status"], jr["message"])
		if VERBOSE:
			 self.L.log(json.dumps(jr, indent=2, separators=[",", ":"]))

	def login(self):
		payload = {
			"clientName" : self.clientName,
			"zoneName" : self.zoneName,
			"signAlgo" : "SHA256withRSA",
			"sign" : self.crypto.sign(self.clientName+self.zoneName)
		}

		if PAYLOAD:
			self.L.log(json.dumps(payload, indent=2, separators=[",", ":"]))

		res = requests.post( AppVault.URL +  AppVault.LOGIN, json=payload, cert=(KeyStore_PEM), verify=KeyStore_PEM)

		jr = json.loads(res.content)

		self.L.log("Login %s status : %d", self.clientName, res.status_code)
		if VERBOSE:
			self.L.log(json.dumps(jr, indent=2, separators=[",", ":"]))

		if "token" in jr.keys():
			self.token = jr["token"]

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

	def retrieve(self, dataRefId):
		if self.token is None:
			self.L.log("Client %s is not logged in ", self.clientName)
			return

		payload = {
			"dataRefId" : dataRefId
		}

		h = {
			"Authorization" : "Bearer {}".format(self.token)
		}
		if PAYLOAD:
			self.L.log("Authorization: Bearer {}".format(self.token))
			self.L.log(json.dumps(payload, indent=2, separators=[",", ":"]))

		res = requests.post( AppVault.URL +  AppVault.RETREIVE, json=payload, headers=h, cert=(KeyStore_PEM), verify=KeyStore_PEM)

		jr = json.loads(res.content)

		self.L.log("Retrieve {} status : {}".format(dataRefId, res.status_code))
		self.L.log(json.dumps(jr, indent=2, separators=[",", ":"]))

	def update(self, dataRefId, data, dataDesc, authz=[], file_mode=False, file=None):
		if self.token is None:
			self.L.log("Client %s is not logged in ", self.clientName)
			return

		if file_mode == True and not file is None and len(file) != 0:
			if os.path.exists(file):
				with open(file, "rb") as f:
					data = f.read()

		payload = {
			"data" : data,
			"dataDesc" : dataDesc,
			"authz" : authz,
			"dataRefId" : dataRefId
		}

		h = {
			"Authorization" : "Bearer {}".format(self.token)
		}

		if PAYLOAD:
			self.L.log("Authorization: Bearer {}".format(self.token))
			self.L.log(json.dumps(payload, indent=2, separators=[",", ":"]))

		res = requests.post( AppVault.URL +  AppVault.UPDATE, json=payload, headers=h, cert=(KeyStore_PEM), verify=KeyStore_PEM)

		jr = json.loads(res.content)

		self.L.log("Update {} status : {}".format(dataDesc, res.status_code))
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

def getAuthz():
	authz = []
	add_authz = "y"
	while add_authz == "y":
		add_authz = raw_input("Add authorizations ?(y/n) : ")
		if add_authz != "y":
			break

		authClientName = raw_input("ClientName : ")
		authZoneName   = raw_input("ZoneName ([P]CI/[N]onPCI) : ")

		if len(authClientName) == 0 or len(authZoneName) == 0:
			STDOUT.write("Invalid data, skipping")
			continue

		if authZoneName.lower() in ["p", "pci"]:
			authZoneName = "PCI"
		elif authZoneName.lower() in ["n", "nonpci"]:
			authZoneName = "NonPCI"
		else:
			STDOUT.write("Invalid data, skipping")
			continue

		authz.append({"clientName" : authClientName, "zoneName" : authZoneName})
	return authz


if __name__ == "__main__":
	#init config info from config.json
	config = None;
	if os.path.exists("config.json"):
		with open("config.json", "r") as f:
			config = json.loads(f.read())

	if config is None:
		STDOUT.write("Config initialization failed. Please check if the config.json is present and accessible")
		sys.exit(-1);

	clientName = str(config["clientName"])
	zoneName = str(config["zoneName"])
	DL = str(config["clientDL"])

	KeyStore = str(config["clientCert"]["path"])
	KeyStore_PEM = str(config["serverCert"]["path"])
	PassPhrase = str(config['clientCert'].get("passPhrase", ""))

	VERBOSE = config["verbose"]
	PAYLOAD = config["payload"]
	TLS = config["tls"]

	# sys.argv[0] script name
	_args = sys.argv[1:]

	if len(Set(_args).intersection(Set(["cmdui", "store", "retrieve", "handles", "delete"]))) == 0:
		_args = ["cmdui"] + _args

	p = ArgumentParser()
	p.add_argument("mode", help="quick modes (cmdui, store, retrieve, handles, delete)", default="cmdui")
	p.add_argument("-k", "--no-tls", help="Do NOT use tls", dest="tls", action="store_true")
	p.add_argument("-v", "--verbose", help="increase verbosity", dest="verbose", action="store_true")
	p.add_argument("-p", "--payload", help="log payload", dest="payload", action="store_true")
	p.add_argument("-dd", "--data-desc", help="Mode specific - dataDescription", dest="dataDesc", default="")
	p.add_argument("-dref", "--data-ref-id", help="Mode specific - data Ref Id", dest="dataRefId", default="")
	p.add_argument("-cp", help="client cert password prompt (overrides the config.json)", dest="certPass", action="store_true")

	g = p.add_mutually_exclusive_group()
	g.add_argument("-d", "--data", help="Mode specific - data", dest="data", default="")
	g.add_argument("-f", "--file", help="Mode Specific - file mode", dest="file", default="")

	args = p.parse_args(_args)

	VERBOSE = VERBOSE | args.verbose
	PAYLOAD = PAYLOAD | args.payload
	TLS = not args.tls

	if len(PassPhrase) == 0 or args.certPass == True:
		PassPhrase = getpass("Client Cert Password : ")

	v3 = AppVault(clientName, zoneName, DL, config["serviceUrl"]["http"], config["serviceUrl"]["https"])

	if config["autoLogin"]:
		try:
			v3.login();
		except Exception as e:
			print e
			sys.exit(-1)

	try:
		if args.mode == "store":
			if v3.token is None:
				v3.login()
			if (len(args.data) == 0 and len(args.file) == 0) or len(args.dataDesc) == 0:
				STDOUT.write("Invalid or incomplete input")
				sys.exit(0)
			file_mode = False

			if len(args.file) != 0:
				file_mode = True

			v3.store(args.data, args.dataDesc, [], file_mode, args.file)
			sys.exit(0)

		elif args.mode == "retrieve":
			if v3.token is None:
				v3.login()
			if len(args.dataRefId) == 0:
				STDOUT.write("Invalid or incomplete input")
				sys.exit(0)

			v3.retrieve(args.dataRefId)
			sys.exit(0)

		elif args.mode == "handles":
			if v3.token is None:
				v3.login()

			v3.handles()
			sys.exit(0)

		elif args.mode == "delete":
			if v3.token is None:
				v3.login()

			v3.delete(args.dataRefId)
			sys.exit(0)
	except Exception as e:
		print e
		sys.exit(-1)

	s = ("\n\n" +
		"\t1. Re[g]ister \n" +
		"\t2. [L]ogin \n" +
		"\t3. [S]tore\n" +
		"\t4. [R]etrieve\n" +
		"\t5. [H]andles\n" +
		"\t6. [U]pdate\n" +
		"\t7. [D]elete\n" +
		"\t8. E[x]it" +
		"\n\n")
	while True:
		try:
			STDOUT.write(s)
			opt = raw_input("Option : ")
			opt = opt.lower()

			if opt == 'g': v3.register()
			if opt == 'l': v3.login()
			if opt == 's':
				dataDesc = raw_input("Data description : ")
				input_type = raw_input("[s]tdin / [f]ile : ")
				data = None

				file_mode = False
				file = None

				if input_type.lower() == 's':
					data = raw_input("Data : ")
				elif input_type.lower() == 'f':
					file_mode = True
					file = raw_input("File path : ")

				authz = getAuthz()

	 			v3.store(data, dataDesc, authz, file_mode, file)

			if opt == 'r':
				d = raw_input("DataRefId : ")
				v3.retrieve(d)

			if opt == 'h' : v3.handles()

			if opt == 'u' :
				d = raw_input("DataRefId : ")
				dataDesc = raw_input("Data description : ")
				input_type = raw_input("[s]tdin / [f]ile : ")
				data = None

				file_mode = False
				file = None

				if input_type.lower() == 's':
					data = raw_input("Data : ")
				elif input_type.lower() == 'f':
					file_mode = True
					file = raw_input("File path : ")

				authz = getAuthz()

	 			# v3.store(data, dataDesc, authz, file_mode, file)
				v3.update(d, data, dataDesc, authz, file_mode, file)

			if opt == 'd' :
				d = raw_input("DataRefId : ")
				v3.delete(d)

			if opt == 'x': sys.exit(0)
		except Exception as e:
			print e