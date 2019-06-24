from django.db import models


class SplunkQuery(models.Model):
    query_text = models.CharField(max_length=1000, default="")
    query_resolution_commands = models.CharField(max_length=300, default="")
    resolve_conf = models.CharField(max_length=50, default="")
    organization = models.CharField(max_length=10, default="ukgrsps")
    assembly = models.CharField(max_length=30, default="")
    environment = models.CharField(max_length=30, default="")
    platform = models.CharField(max_length=30, default="")
    component = models.CharField(max_length=30, default="")
    application = models.CharField(max_length=30, default="")

    def __str__(self):
        return self.query_text


class GenericIssue(models.Model):

    issue = models.CharField(max_length=300, default="")
    command_set = models.CharField(max_length=300)
    organization = models.CharField(max_length=10, default="ukgrsps")
    assembly = models.CharField(max_length=30)
    environment = models.CharField(max_length=30)
    platform = models.CharField(max_length=30)
    component = models.CharField(max_length=30)
    application = models.CharField(max_length=30)
    resolve_conf = models.CharField(max_length=100)



    

    def __str__(self):
        return self.issue