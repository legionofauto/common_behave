import requests 
from behave import given, when, then
from common_functions import get_usr_prop


"""
Representational state transfer is a software architectural style that defines a set 
of constraints to be used for creating Web services. Web services that conform to 
the REST architectural style, called RESTful Web services, provide interoperability 
between computer systems on the Internet.Requests is an elegant and simple HTTP 
library for Python, built for human beings.

Requests quick reference guide:
https://requests.readthedocs.io/en/master/user/quickstart/#make-a-request
"""


@given('all GET Requests are successfully executed against the data table')
def given_all_get_requests_are_successfully_executed_against_the_data_table(context):
    """
    This function tests the user's ability to successfully execute GET REST requests 
    to the specific URLs listed in the tables outlined. All URLs used in the step
    will be held in a list for executing other REST methods. 
    
    Use GET requests to retrieve resource representation/information only - and not 
    to modify it in any way. As GET requests do not change the state of the resource, 
    these are said to be safe methods. Additionally, GET APIs should be idempotent, 
    which means that making multiple identical requests must produce the same result 
    every time until another API (POST or PUT) has changed the state of the resource 
    on the server.
    
    :table url: (str) Uniform Resource Locator.
    :table username: (str) Optional - If the resource requires a login, this is the
        user account title you log in with.
    :table user_pass: (str) Optional - If the resource requires a login, this is the
        user account password you log in with.
    """
    context.rest = []
    #For every value contained with each row.
    for row in context.table:
        #The website you are retrieving the restful state from.
        table_url=row['url']
        
        try:
            table_username=row['username']
            table_user_password=row['user_pass']
        except:
            table_username=None
            table_user_password=None
        
        
        if table_username is not None:
            table_username = get_usr_prop(context, table_username)
            table_user_password = get_usr_prop(context, table_user_password)
            r = requests.get(str(table_url), auth=(table_username, table_user_password))
        else:
            r = requests.get(str(table_url))
        
        context.rest.append(r)
        
        assert r.status_code == 200, 'Get REST request for "{}" Failed!'.format(table_url)


@when('all POST Requests are successfully executed from the data table against all GET Requests')
def when_all_post_requests_are_successfully_executed_from_the_data_table_against_all_get_requests(context):
    """
    Sends a REST PUT command to each URL in context.rest. 
    
    Use POST APIs to create new subordinate resources, e.g., a file is subordinate to a 
    directory containing it or a row is subordinate to a database table. Talking strictly 
    in terms of REST, POST methods are used to create a new resource into the collection 
    of resources.

    Ideally, if a resource has been created on the origin server, the response SHOULD be 
    HTTP response code 201 (Created) and contain an entity which describes the status of 
    the request and refers to the new resource, and a Location header.
    
    :table key: (str) the key in the Key/Value pairs used to post to the URL.
    :table value: (str) the value in the Key/Value pairs used to post to the URL.
    :param context: Expects rest
    """
    #Count is used to iterate over the context.rest list along with the row for loop.
    rest_count = 0
    
    for row in context.table:
        table_key=row['key']
        table_value=row['value']
        r = requests.post(str(context.rest[rest_count]), data = {table_key:table_value})

        assert r.status_code == 201, 'POST REST request for "{}" Failed!'.format(context.rest[rest_count])
        rest_count += 1


@when('all PUT Requests are successfully executed from the data table against all GET Requests')
def when_all_put_requests_are_successfully_executed_from_the_data_table_against_all_get_requests(context):
    """
    Sends a REST PUT command to each URL in context.rest. 
    
    Use PUT APIs primarily to update existing resource (if the resource does not exist, 
    then API may decide to create a new resource or not). If a new resource has been 
    created by the PUT API, the origin server MUST inform the user agent via the HTTP 
    response code 201 (Created) response and if an existing resource is modified, either 
    the 200 (OK) or 204 (No Content) response codes SHOULD be sent to indicate 
    successful completion of the request.
    
    If the request passes through a cache and the Request-URI identifies one or more 
    currently cached entities, those entries SHOULD be treated as stale. Responses to 
    this method are not cacheable.
    
    :table key: (str) the key in the Key/Value pairs used to replace data in the URL.
    :table value: (str) the value in the Key/Value pairs used to replace data in the URL.
    :param context: Expects rest
    """
    #Count is used to iterate over the context.rest list along with the row for loop.
    rest_count = 0
    
    #For each row in context.table.
    for row in context.table:
        table_key=row['key']
        table_value=row['value']
        r = requests.put(str(context.rest[rest_count]), data = {table_key:table_value})

        assert r.status_code == 201, 'POST REST request for "{}" Failed!'.format(context.rest[rest_count])
        
        rest_count += 1


@then('all DELETE Requests are successfully executed against all GET Requests')
def then_all_delete_requests_are_successfully_executed_against_all_get_requests(context):
    """
    As the name applies, DELETE APIs are used to delete resources (identified by the 
    Request-URI). All REST requests in context.rest will be deleted. 
    
    :param context: Expects rest.
    """
    for site in context.rest:
        r = requests.delete(site)
        
        '''
        A successful response of DELETE requests SHOULD be HTTP response code 200 (OK) if 
        the response includes an entity describing the status, 202 (Accepted) if the action 
        has been queued, or 204 (No Content) if the action has been performed but the 
        response does not include an entity.
        '''
        assert r.status_code == 202 or 200, 'DELETE REST request for "{}" Failed!'.format(site)
