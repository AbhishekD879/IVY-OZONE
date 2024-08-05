# swagger_client.CompetitionTabApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**competition_tab_by_id**](CompetitionTabApi.md#competition_tab_by_id) | **DELETE** /competition/{compId}/tab/{tabId} | CompetitionTabById
[**find_all_competition_tab**](CompetitionTabApi.md#find_all_competition_tab) | **GET** /competitionTab | findAll
[**find_competition_expand_competition_tab**](CompetitionTabApi.md#find_competition_expand_competition_tab) | **GET** /competition/{compId}/tab/{tabId} | findOne
[**find_one_competition_tab**](CompetitionTabApi.md#find_one_competition_tab) | **GET** /competitionTab/{id} | findOne
[**order**](CompetitionTabApi.md#order) | **POST** /competition/{compId}/tab/ordering | order
[**save_competition_tab**](CompetitionTabApi.md#save_competition_tab) | **POST** /competition/{id}/tab | save
[**update_competition_tab**](CompetitionTabApi.md#update_competition_tab) | **PUT** /competitionTab/{id} | update

# **competition_tab_by_id**
> competition_tab_by_id(comp_id, tab_id)

CompetitionTabById

Delete a CompetitionTab

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: Authorization
configuration = swagger_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.CompetitionTabApi(swagger_client.ApiClient(configuration))
comp_id = 'comp_id_example' # str | id of competition
tab_id = 'tab_id_example' # str | id of tab

try:
    # CompetitionTabById
    api_instance.competition_tab_by_id(comp_id, tab_id)
except ApiException as e:
    print("Exception when calling CompetitionTabApi->competition_tab_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **comp_id** | **str**| id of competition | 
 **tab_id** | **str**| id of tab | 

### Return type

void (empty response body)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_all_competition_tab**
> list[CompetitionTab] find_all_competition_tab()

findAll

Retrieve all CompetitionTabs

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: Authorization
configuration = swagger_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.CompetitionTabApi(swagger_client.ApiClient(configuration))

try:
    # findAll
    api_response = api_instance.find_all_competition_tab()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionTabApi->find_all_competition_tab: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[CompetitionTab]**](CompetitionTab.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_competition_expand_competition_tab**
> Competition2 find_competition_expand_competition_tab(comp_id, tab_id)

findOne

Searches Conpetition's CompetitionTabs

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: Authorization
configuration = swagger_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.CompetitionTabApi(swagger_client.ApiClient(configuration))
comp_id = 'comp_id_example' # str | id of competition
tab_id = 'tab_id_example' # str | id of tab

try:
    # findOne
    api_response = api_instance.find_competition_expand_competition_tab(comp_id, tab_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionTabApi->find_competition_expand_competition_tab: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **comp_id** | **str**| id of competition | 
 **tab_id** | **str**| id of tab | 

### Return type

[**Competition2**](Competition2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one_competition_tab**
> CompetitionTab2 find_one_competition_tab(id)

findOne

Searches CompetitionTab by id

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: Authorization
configuration = swagger_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.CompetitionTabApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.find_one_competition_tab(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionTabApi->find_one_competition_tab: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**CompetitionTab2**](CompetitionTab2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **order**
> CompetitionTab2 order(body, comp_id)

order

Set order for all competitionTabs

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: Authorization
configuration = swagger_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.CompetitionTabApi(swagger_client.ApiClient(configuration))
body = swagger_client.Ordering2() # Ordering2 | List of ordered ids of competitionTabs
comp_id = 'comp_id_example' # str | id of competition

try:
    # order
    api_response = api_instance.order(body, comp_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionTabApi->order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Ordering2**](Ordering2.md)| List of ordered ids of competitionTabs | 
 **comp_id** | **str**| id of competition | 

### Return type

[**CompetitionTab2**](CompetitionTab2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save_competition_tab**
> CompetitionTab2 save_competition_tab(body, id)

save

Add a new CompetitionTab

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: Authorization
configuration = swagger_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.CompetitionTabApi(swagger_client.ApiClient(configuration))
body = swagger_client.CompetitionTab2() # CompetitionTab2 | CompetitionTab object that needs to be added to the storage
id = 'id_example' # str | id of resource

try:
    # save
    api_response = api_instance.save_competition_tab(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionTabApi->save_competition_tab: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CompetitionTab2**](CompetitionTab2.md)| CompetitionTab object that needs to be added to the storage | 
 **id** | **str**| id of resource | 

### Return type

[**CompetitionTab2**](CompetitionTab2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_competition_tab**
> CompetitionTab2 update_competition_tab(body, id)

update

Update an existing CompetitionTab

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: Authorization
configuration = swagger_client.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.CompetitionTabApi(swagger_client.ApiClient(configuration))
body = swagger_client.CompetitionTab2() # CompetitionTab2 | CompetitionTab object that needs to be updated in the storage
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.update_competition_tab(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionTabApi->update_competition_tab: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CompetitionTab2**](CompetitionTab2.md)| CompetitionTab object that needs to be updated in the storage | 
 **id** | **str**| id of resource | 

### Return type

[**CompetitionTab2**](CompetitionTab2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

