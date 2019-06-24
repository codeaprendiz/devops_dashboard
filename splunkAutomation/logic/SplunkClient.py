import splunklib.client as client
import splunklib.results as results
import sys
from time import sleep
import paramiko,sys
from splunkAutomation.logic.Constants import Constants





class SplunkClient:
    def __init__(self, hostname, port, username, password):
        self.hostname=hostname
        self.port=port
        self.username=username
        self.password=password
        self.service = client.connect(host=self.hostname, port=self.port,username=self.username, password=self.password)
        self.jobs = self.service.jobs
        

    def createJob(self, searchQuery):
        list_of_hostnames = []
        job = self.jobs.create(searchQuery)
        while True:
            while not job.is_ready():
                pass
            stats = {"isDone": job["isDone"],
            "doneProgress": float(job["doneProgress"])*100,
            "scanCount": int(job["scanCount"]),
            "eventCount": int(job["eventCount"]),
            "resultCount": int(job["resultCount"])}
            status = ("\r%(doneProgress)03.1f%%   %(scanCount)d scanned   ""%(eventCount)d matched   %(resultCount)d results") % stats
            sys.stdout.write(status)
            sys.stdout.flush()
            if stats["isDone"] == "1":
                sys.stdout.write("\n\nDone!\n\n")
                break
        sleep(2)
        resultReader = results.ResultsReader(job.results())
        #resultReader = results.ResultsReader(job.preview())
        for item in resultReader:
            for key in item.keys():
                if key == "host":
                    list_of_hostnames.append(item[key])
        return list_of_hostnames


    def rawResult(self, searchQuery):
        list_of_hostnames = []
        job = self.jobs.create(searchQuery)
        while True:
            while not job.is_ready():
                pass
            stats = {"isDone": job["isDone"],
            "doneProgress": float(job["doneProgress"])*100,
            "scanCount": int(job["scanCount"]),
            "eventCount": int(job["eventCount"]),
            "resultCount": int(job["resultCount"])}
            status = ("\r%(doneProgress)03.1f%%   %(scanCount)d scanned   ""%(eventCount)d matched   %(resultCount)d results") % stats
            sys.stdout.write(status)
            sys.stdout.flush()
            if stats["isDone"] == "1":
                sys.stdout.write("\n\nDone!\n\n")
                break
        sleep(2)
        resultReader = results.ResultsReader(job.results())
        
        return resultReader




"""
splunkProdInst = SplunkProd()
myList=splunkProdInst.createJob("search index=estore host=commerceapp* earliest=-15m sourcetype=serverlog_ | dedup host")
print("printing item hosts now")
print(myList)



hostname = "commerceapp-279244892-1-351584262.prod.commerce.ukgrsps.dfw6.prod.company.com"
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=hostname, username='app', password=None, key_filename="/Users/asr000p/.ssh/id_rsa.pub")
stdin, stdout, stderr = ssh.exec_command("hostname -f")
output = stdout.readlines()
print(output)
ssh.close()

"""




