class Constants:
################################################################################################################################################
	# 									VIEW SPECIFIC URLS AND CORRESPONDING URL NAMES
################################################################################################################################################
	
	URL_FOR_THEME1_INDEX_PAGE='theme1/'
	NAME_OF_URL_FOR_THEME1_INDEX_PAGE='url_for_theme1_index_page'

	URL_FOR_THEME2_INDEX_PAGE='theme2/'
	NAME_OF_URL_FOR_THEME2_INDEX_PAGE='url_for_theme2_index_page'

	URL_FOR_THEME2_ELEMENTS_PAGE='theme2/elements/'
	NAME_OF_URL_FOR_THEME2_ELEMENTS_PAGE='url_for_theme2_elements_page'

	URL_FOR_ALL_SPLUNK_QUERIES_PAGE='splunkQueries/'
	NAME_OF_URL_FOR_ALL_SPLUNK_QUERIES_PAGE='url_for_all_splunk_queries_page'

	URL_FOR_ALL_GENERIC_ISSUES_PAGE='genericIssues/'
	NAME_OF_URL_FOR_ALL_GENERIC_ISSUES_PAGE='url_for_generic_issues_page'

	URL_FOR_GENERIC_ISSUES_RESOLVE_PAGE='genericIssues/<int:issue_id>'
	NAME_OF_URL_FOR_GENERIC_ISSUES_RESOLVE_PAGE='url_for_generic_issues_resolve_page'

	URL_FOR_QUERY_SPECIFIC_RESULTS_PAGE='splunkQueries/check/<int:query_id>'
	NAME_OF_URL_FOR_QUERY_SPECIFIC_RESULTS_PAGE='url_for_query_specific_page'


	URL_FOR_QUERY_RESOLUTION_RESULTS_PAGE='splunkQueries/check/<int:query_id>/resolve'
	NAME_OF_URL_FOR_QUERY_RESOLUTION_RESULTS_PAGE='url_for_query_resolution_results_page'


	URL_FOR_PROGRESS_BAR_PAGE='splunkQueries/check/progress'
	NAME_OF_URL_FOR_PROGRESS_BAR_PAGE='url_for_progress_bar_page'

	URL_FOR_LOADER_PAGE='splunkQueries/check/loader'
	NAME_OF_URL_FOR_LOADER_PAGE='name_of_url_for_loader_page'

	URL_FOR_POP_UP_WINDOW_PAGE='splunkQueries/check/popUp'
	NAME_OF_URL_FOR_POP_UP_WINDOW_PAGE='url_for_pop_up_window_page'



################################################################################################################################################
	# 												ONEOPS CONSTANTS
################################################################################################################################################
	
	ONEOPS_USERNAME=""
	ONEOPS_PASSWORD=""
	ONEOPS_GET_HOSTNAMES = "https://cloud.prod.com/{organization}/assemblies/{assembly}/operations/environments/{environment}/platforms/{platform}/components/{component}/instances.json?instances_state=all"
	ONEOPS_GET_ENVIRONMENTS = "https://cloud.prod.com/{organization}/assemblies/{assembly}/transition/environments"
	ONEOPS_GET_ASSEMBLIES = "https://cloud.prod.com/{organization}/assemblies"
	ONEOPS_GET_PLATFORMS = "https://cloud.prod.com/{organization}/assemblies/{assembly}/transition/environments/{environment}/platforms"


################################################################################################################################################
	# 												TEMPLATE LOCATION CONSTANTS
################################################################################################################################################


	TEMPLATE_THEME1_INDEX_HTML="splunkAutomation/theme1/index.html"
	TEMPLATE_THEME2_INDEX_HTML="splunkAutomation/theme2/index.html"
	TEMPLATE_THEME2_ELEMENTS_HTML="splunkAutomation/theme2/elements.html"
	TEMPLATE_THEME2_TABLE_VIEW_IN_CONTAINER_WITH_BUTTONS="splunkAutomation/theme2/tableViewInContainerWithButtons.html"
	TEMPLATE_THEME2_TABLE_VIEW_IN_CONTAINER_WITH_BUTTONS_GENERIC_ISSUES="splunkAutomation/theme2/tableViewInContainerWithButtonsGenericIssues.html"
	TEMPLATE_THEME2_DISPLAY_OUTPUT="splunkAutomation/theme2/containerForDisplayOutput.html"
	TEMPLATE_THEME2_CONTAINER_WITH_CHECKBOX_AND_BUTTONS="splunkAutomation/theme2/containerWithCheckBoxAndButtons.html"
	TEMPLATE_THEME2_CONTAINER_WITH_PROGRESS_BAR="splunkAutomation/theme2/containerWithProgressBar.html"
	TEMPLATE_THEME2_CONTAINER_WITH_LOADER="splunkAutomation/theme2/containerWithLoader.html"
	TEMPLATE_THEME2_POP_UP_WINDOW="splunkAutomation/theme2/popUpForm.html"
	TEMPLATE_THEME2_DISPLAY_PROGRESS="splunkAutomation/theme2/display_progress.html"



################################################################################################################################################
	# 												 SPLUNK CONSTANTS
################################################################################################################################################
	SPLUNK_PROD_HOSTNAME1 = '.prod.com'
	SPLUNK_PROD_HOSTNAME2 = '.prod.com'
	SPLUNK_PROD_PORT = 8089
	SPLUNK_PROD_USERNAME = ''
	SPLUNK_PROD_PASSWORD = ''

	SPLUNK_QA_HOSTNAME1 = '.qa.splunk-qa.ukgrsps.prod.com'
	SPLUNK_QA_PORT = 8089
	SPLUNK_QA_USERNAME = ''
	SPLUNK_QA_PASSWORD = ''





	



################################################################################################################################################
	# 												 SPLUNK QUERIES
################################################################################################################################################
	
	#GROCERY SEARCH
	QUERY_GROCERY_SEARCH_WHERE_SERVER_LOG_FILE_PRESENT ="search index=estore host=commerceapp* earliest=-15m sourcetype=serverlog_ | dedup host"




	#SPLUNK QA QUERIES
	QUERY_PQAESTORE = "search index=pqaestore earliest=-15m | dedup host"
	QUERY_PQAGROCERY_SEARCH_APP = "search index=pqa_grocerysearchapp earliest=-15m | dedup host"
	QUERY_PQA_SSO_UI = "search index=pqa_sso_profile earliest=-15m | dedup host"



################################################################################################################################################
	# 												SSH CONNECTION RELATED
################################################################################################################################################

	PUBLIC_KEY_LOCATION="/Users/asr000p/.ssh/id_rsa.pub"
	USER="app"



################################################################################################################################################
	# 												COMMANDS TO BE EXECUTED
################################################################################################################################################

	COMMANDS_CHECK_SERVER_LOG_FILE_AND_RESTART_JBOSS_IF_NECESSARY='[ -f /log/server.log ] && echo "- Server Log File Exists" || /etc/init.d/jboss-container restart'
	COMMANDS_TO_START_SPLUNK_FORWARDERS='source /app/splunkforwarder/bin/setSplunkEnv; splunk status; splunk start'
	
