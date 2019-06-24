from django.urls import path, re_path
from splunkAutomation.logic.Constants import Constants
from . import views

app_name = 'splunkAutomation'
urlpatterns = [
    path(Constants.URL_FOR_THEME1_INDEX_PAGE, views.viewForIndexPageTheme1, name=Constants.NAME_OF_URL_FOR_THEME1_INDEX_PAGE),
    path(Constants.URL_FOR_THEME2_INDEX_PAGE, views.viewForIndexPageTheme2, name=Constants.NAME_OF_URL_FOR_THEME2_INDEX_PAGE),
    path(Constants.URL_FOR_THEME2_ELEMENTS_PAGE, views.viewForElementsPageTheme2, name=Constants.NAME_OF_URL_FOR_THEME2_ELEMENTS_PAGE),
    path(Constants.URL_FOR_ALL_SPLUNK_QUERIES_PAGE,views.viewForSeeingAllSplunkQueries, name=Constants.NAME_OF_URL_FOR_ALL_SPLUNK_QUERIES_PAGE),
    path(Constants.URL_FOR_QUERY_SPECIFIC_RESULTS_PAGE,views.viewForSeeingQuerySpecificResults, name=Constants.NAME_OF_URL_FOR_QUERY_SPECIFIC_RESULTS_PAGE),
    path(Constants.URL_FOR_ALL_GENERIC_ISSUES_PAGE,views.viewForSeeingGenericIssues, name=Constants.NAME_OF_URL_FOR_ALL_GENERIC_ISSUES_PAGE),
    path(Constants.URL_FOR_GENERIC_ISSUES_RESOLVE_PAGE,views.viewForSeeingGenericIssuesResults, name=Constants.NAME_OF_URL_FOR_GENERIC_ISSUES_RESOLVE_PAGE),    

    #############################################################
    			# Adding test views
    #############################################################

    path(Constants.URL_FOR_PROGRESS_BAR_PAGE,views.viewForShowingProgressBar ,name=Constants.NAME_OF_URL_FOR_PROGRESS_BAR_PAGE),
    path(Constants.URL_FOR_LOADER_PAGE,views.viewForShowingLoader,name=Constants.NAME_OF_URL_FOR_LOADER_PAGE),
    path(Constants.URL_FOR_POP_UP_WINDOW_PAGE,views.viewForShowingPopUpWindow,name=Constants.NAME_OF_URL_FOR_POP_UP_WINDOW_PAGE),
    path('get_hostname_output_log/',views.get_hostname_output_log, name='get_hostname_output_log'),
   #re_path(r'get_hostname_output_log/$', views.get_hostname_output_log, name='get_hostname_output_log'),
    re_path(r'results/$', views.results, name='results'),
    #re_path(r'^get_hostname_output_log/$', views.get_hostname_output_log, name='get_hostname_output_log'),    
    #re_path(r'^results/$', views.results, name='results'),


    #path('splunkQueries/check/progress/celery',views.progress_view,name='url_for_progress_bar_celery'),
    #path('splunkQueries/check/getProgress/celery',views.progress_view,name='url_for_progress_bar_celery'),


    #############################################################

    path(Constants.URL_FOR_QUERY_RESOLUTION_RESULTS_PAGE,views.viewForSeeingQueryResolutionResults, name=Constants.NAME_OF_URL_FOR_QUERY_RESOLUTION_RESULTS_PAGE),
    path('splunkQueries/resolve/<int:query_id>',views.querySpeficResolve, name='querySpeficResolve'),
]




