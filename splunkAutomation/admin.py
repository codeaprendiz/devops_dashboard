from django.contrib import admin

from splunkAutomation.models import SplunkQuery
from splunkAutomation.models import GenericIssue

admin.site.register(SplunkQuery)
admin.site.register(GenericIssue)