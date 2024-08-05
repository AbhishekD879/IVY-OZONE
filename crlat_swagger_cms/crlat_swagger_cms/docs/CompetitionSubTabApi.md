# swagger_client.CompetitionSubTabApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**competition_sub_tab_by_id**](CompetitionSubTabApi.md#competition_sub_tab_by_id) | **DELETE** /competition/{compId}/tab/{tabId}/subTab/{subTabId} | CompetitionSubTabById
[**find_all_competition_sub_tab**](CompetitionSubTabApi.md#find_all_competition_sub_tab) | **GET** /competitionSubTab | findAll
[**find_competition_expand_competition_sub_tab**](CompetitionSubTabApi.md#find_competition_expand_competition_sub_tab) | **GET** /competition/{compId}/tab/{tabId}/subTab/{subTabId} | findOne
[**find_one_competition_sub_tab**](CompetitionSubTabApi.md#find_one_competition_sub_tab) | **GET** /competitionSubTab/{id} | findOne
[**order**](CompetitionSubTabApi.md#order) | **POST** /competition/{compId}/tab/{tabId}/subTab/ordering | order
[**save_competition_sub_tab**](CompetitionSubTabApi.md#save_competition_sub_tab) | **POST** /competition/{compId}/tab/{tabId}/subTab | save
[**update_competition_sub_tab**](CompetitionSubTabApi.md#update_competition_sub_tab) | **PUT** /competitionSubTab/{id} | update

# **competition_sub_tab_by_id**
> competition_sub_tab_by_id(comp_id, tab_id, sub_tab_id)

CompetitionSubTabById

Delete a CompetitionSubTab

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
api_instance = swagger_client.CompetitionSubTabApi(swagger_client.ApiClient(configuration))
comp_id = 'comp_id_example' # str | id of competition
tab_id = 'tab_id_example' # str | id of tab
sub_tab_id = 'sub_tab_id_example' # str | id of subtab

try:
    # CompetitionSubTabById
    api_instance.competition_sub_tab_by_id(comp_id, tab_id, sub_tab_id)
except ApiException as e:
    print("Exception when calling CompetitionSubTabApi->competition_sub_tab_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **comp_id** | **str**| id of competition | 
 **tab_id** | **str**| id of tab | 
 **sub_tab_id** | **str**| id of subtab | 

### Return type

void (empty response body)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_all_competition_sub_tab**
> list[CompetitionSubTab] find_all_competition_sub_tab()

findAll

Retrieve all CompetitionSubTabs

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
api_instance = swagger_client.CompetitionSubTabApi(swagger_client.ApiClient(configuration))

try:
    # findAll
    api_response = api_instance.find_all_competition_sub_tab()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionSubTabApi->find_all_competition_sub_tab: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[CompetitionSubTab]**](CompetitionSubTab.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_competition_expand_competition_sub_tab**
> Competition2 find_competition_expand_competition_sub_tab(comp_id, tab_id, sub_tab_id)

findOne

Searches Conpetition's CompetitionSubTabs

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
api_instance = swagger_client.CompetitionSubTabApi(swagger_client.ApiClient(configuration))
comp_id = 'comp_id_example' # str | id of competition
tab_id = 'tab_id_example' # str | id of tab
sub_tab_id = 'sub_tab_id_example' # str | id of subtab

try:
    # findOne
    api_response = api_instance.find_competition_expand_competition_sub_tab(comp_id, tab_id, sub_tab_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionSubTabApi->find_competition_expand_competition_sub_tab: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **comp_id** | **str**| id of competition | 
 **tab_id** | **str**| id of tab | 
 **sub_tab_id** | **str**| id of subtab | 

### Return type

[**Competition2**](Competition2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one_competition_sub_tab**
> CompetitionSubTab2 find_one_competition_sub_tab(id)

findOne

Searches CompetitionSubTab by id

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
api_instance = swagger_client.CompetitionSubTabApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.find_one_competition_sub_tab(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionSubTabApi->find_one_competition_sub_tab: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**CompetitionSubTab2**](CompetitionSubTab2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **order**
> CompetitionSubTab2 order(body, comp_id, tab_id)

order

Set order for all competitionSubTabs

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
api_instance = swagger_client.CompetitionSubTabApi(swagger_client.ApiClient(configuration))
body = swagger_client.Ordering2() # Ordering2 | List of ordered ids of competitionSubTabs
comp_id = 'comp_id_example' # str | id of competition
tab_id = 'tab_id_example' # str | id of tab

try:
    # order
    api_response = api_instance.order(body, comp_id, tab_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionSubTabApi->order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Ordering2**](Ordering2.md)| List of ordered ids of competitionSubTabs | 
 **comp_id** | **str**| id of competition | 
 **tab_id** | **str**| id of tab | 

### Return type

[**CompetitionSubTab2**](CompetitionSubTab2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save_competition_sub_tab**
> CompetitionSubTab2 save_competition_sub_tab(body, comp_id, tab_id)

save

Add a new CompetitionSubTab

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
api_instance = swagger_client.CompetitionSubTabApi(swagger_client.ApiClient(configuration))
body = swagger_client.CompetitionSubTab2() # CompetitionSubTab2 | CompetitionSubTab object that needs to be added to the storage
comp_id = 'comp_id_example' # str | id of competition
tab_id = 'tab_id_example' # str | id of tab

try:
    # save
    api_response = api_instance.save_competition_sub_tab(body, comp_id, tab_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionSubTabApi->save_competition_sub_tab: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CompetitionSubTab2**](CompetitionSubTab2.md)| CompetitionSubTab object that needs to be added to the storage | 
 **comp_id** | **str**| id of competition | 
 **tab_id** | **str**| id of tab | 

### Return type

[**CompetitionSubTab2**](CompetitionSubTab2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_competition_sub_tab**
> CompetitionSubTab2 update_competition_sub_tab(body, id)

update

Update an existing CompetitionSubTab

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
api_instance = swagger_client.CompetitionSubTabApi(swagger_client.ApiClient(configuration))
body = swagger_client.CompetitionSubTab2() # CompetitionSubTab2 | CompetitionSubTab object that needs to be updated in the storage
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.update_competition_sub_tab(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionSubTabApi->update_competition_sub_tab: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CompetitionSubTab2**](CompetitionSubTab2.md)| CompetitionSubTab object that needs to be updated in the storage | 
 **id** | **str**| id of resource | 

### Return type

[**CompetitionSubTab2**](CompetitionSubTab2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

