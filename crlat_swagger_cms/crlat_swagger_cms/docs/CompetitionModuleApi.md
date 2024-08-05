# swagger_client.CompetitionModuleApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**competition_module_by_id**](CompetitionModuleApi.md#competition_module_by_id) | **DELETE** /competition/{compId}/tab/{tabId}/subTab/{subTabId}/module/{moduleId} | CompetitionModuleById
[**competition_module_by_id_0**](CompetitionModuleApi.md#competition_module_by_id_0) | **DELETE** /competition/{compId}/tab/{tabId}/module/{moduleId} | CompetitionModuleById
[**find_all_competition_module**](CompetitionModuleApi.md#find_all_competition_module) | **GET** /competitionModule | findAll
[**find_competition_expand_competition_module**](CompetitionModuleApi.md#find_competition_expand_competition_module) | **GET** /competition/{compId}/tab/{tabId}/subTab/{subTabId}/module/{moduleId} | findOne
[**find_competition_expand_competition_module_0**](CompetitionModuleApi.md#find_competition_expand_competition_module_0) | **GET** /competition/{compId}/tab/{tabId}/module/{moduleId} | findOne
[**find_one_competition_module**](CompetitionModuleApi.md#find_one_competition_module) | **GET** /competitionModule/{id} | findOne
[**order**](CompetitionModuleApi.md#order) | **POST** /competition/{compId}/tab/{tabId}/subTab/{subTabId}/module/ordering | order
[**order_0**](CompetitionModuleApi.md#order_0) | **POST** /competition/{compId}/tab/{tabId}/module/ordering | order
[**save_competition_module**](CompetitionModuleApi.md#save_competition_module) | **POST** /competition/{compId}/tab/{tabId}/subTab/{subTabId}/module | save
[**save_competition_module_0**](CompetitionModuleApi.md#save_competition_module_0) | **POST** /competition/{compId}/tab/{tabId}/module | save
[**update_competition_module**](CompetitionModuleApi.md#update_competition_module) | **PUT** /competitionModule/{id} | update

# **competition_module_by_id**
> competition_module_by_id(comp_id, tab_id, sub_tab_id, module_id)

CompetitionModuleById

Delete a CompetitionModule

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
api_instance = swagger_client.CompetitionModuleApi(swagger_client.ApiClient(configuration))
comp_id = 'comp_id_example' # str | id of competition
tab_id = 'tab_id_example' # str | id of tab
sub_tab_id = 'sub_tab_id_example' # str | id of subtab
module_id = 'module_id_example' # str | id of module

try:
    # CompetitionModuleById
    api_instance.competition_module_by_id(comp_id, tab_id, sub_tab_id, module_id)
except ApiException as e:
    print("Exception when calling CompetitionModuleApi->competition_module_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **comp_id** | **str**| id of competition | 
 **tab_id** | **str**| id of tab | 
 **sub_tab_id** | **str**| id of subtab | 
 **module_id** | **str**| id of module | 

### Return type

void (empty response body)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **competition_module_by_id_0**
> competition_module_by_id_0(comp_id, tab_id, module_id)

CompetitionModuleById

Delete a CompetitionModule

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
api_instance = swagger_client.CompetitionModuleApi(swagger_client.ApiClient(configuration))
comp_id = 'comp_id_example' # str | id of competition
tab_id = 'tab_id_example' # str | id of tab
module_id = 'module_id_example' # str | id of module

try:
    # CompetitionModuleById
    api_instance.competition_module_by_id_0(comp_id, tab_id, module_id)
except ApiException as e:
    print("Exception when calling CompetitionModuleApi->competition_module_by_id_0: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **comp_id** | **str**| id of competition | 
 **tab_id** | **str**| id of tab | 
 **module_id** | **str**| id of module | 

### Return type

void (empty response body)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_all_competition_module**
> list[CompetitionModule] find_all_competition_module()

findAll

Retrieve all CompetitionModules

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
api_instance = swagger_client.CompetitionModuleApi(swagger_client.ApiClient(configuration))

try:
    # findAll
    api_response = api_instance.find_all_competition_module()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionModuleApi->find_all_competition_module: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[CompetitionModule]**](CompetitionModule.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_competition_expand_competition_module**
> Competition2 find_competition_expand_competition_module(comp_id, tab_id, sub_tab_id, module_id)

findOne

Searches Conpetition's CompetitionModules

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
api_instance = swagger_client.CompetitionModuleApi(swagger_client.ApiClient(configuration))
comp_id = 'comp_id_example' # str | id of competition
tab_id = 'tab_id_example' # str | id of tab
sub_tab_id = 'sub_tab_id_example' # str | id of subtab
module_id = 'module_id_example' # str | id of module

try:
    # findOne
    api_response = api_instance.find_competition_expand_competition_module(comp_id, tab_id, sub_tab_id, module_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionModuleApi->find_competition_expand_competition_module: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **comp_id** | **str**| id of competition | 
 **tab_id** | **str**| id of tab | 
 **sub_tab_id** | **str**| id of subtab | 
 **module_id** | **str**| id of module | 

### Return type

[**Competition2**](Competition2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_competition_expand_competition_module_0**
> Competition2 find_competition_expand_competition_module_0(comp_id, tab_id, module_id)

findOne

Searches Conpetition's CompetitionModules

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
api_instance = swagger_client.CompetitionModuleApi(swagger_client.ApiClient(configuration))
comp_id = 'comp_id_example' # str | id of competition
tab_id = 'tab_id_example' # str | id of tab
module_id = 'module_id_example' # str | id of module

try:
    # findOne
    api_response = api_instance.find_competition_expand_competition_module_0(comp_id, tab_id, module_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionModuleApi->find_competition_expand_competition_module_0: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **comp_id** | **str**| id of competition | 
 **tab_id** | **str**| id of tab | 
 **module_id** | **str**| id of module | 

### Return type

[**Competition2**](Competition2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one_competition_module**
> CompetitionModule2 find_one_competition_module(id)

findOne

Searches CompetitionModule by id

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
api_instance = swagger_client.CompetitionModuleApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.find_one_competition_module(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionModuleApi->find_one_competition_module: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**CompetitionModule2**](CompetitionModule2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **order**
> CompetitionModule2 order(body, comp_id, tab_id, sub_tab_id)

order

Set order for all competitionModules

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
api_instance = swagger_client.CompetitionModuleApi(swagger_client.ApiClient(configuration))
body = swagger_client.Ordering2() # Ordering2 | List of ordered ids of competitionModules
comp_id = 'comp_id_example' # str | id of competition
tab_id = 'tab_id_example' # str | id of tab
sub_tab_id = 'sub_tab_id_example' # str | id of subtab

try:
    # order
    api_response = api_instance.order(body, comp_id, tab_id, sub_tab_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionModuleApi->order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Ordering2**](Ordering2.md)| List of ordered ids of competitionModules | 
 **comp_id** | **str**| id of competition | 
 **tab_id** | **str**| id of tab | 
 **sub_tab_id** | **str**| id of subtab | 

### Return type

[**CompetitionModule2**](CompetitionModule2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **order_0**
> CompetitionModule2 order_0(body, comp_id, tab_id)

order

Set order for all competitionModules

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
api_instance = swagger_client.CompetitionModuleApi(swagger_client.ApiClient(configuration))
body = swagger_client.Ordering2() # Ordering2 | List of ordered ids of competitionModules
comp_id = 'comp_id_example' # str | id of competition
tab_id = 'tab_id_example' # str | id of tab

try:
    # order
    api_response = api_instance.order_0(body, comp_id, tab_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionModuleApi->order_0: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Ordering2**](Ordering2.md)| List of ordered ids of competitionModules | 
 **comp_id** | **str**| id of competition | 
 **tab_id** | **str**| id of tab | 

### Return type

[**CompetitionModule2**](CompetitionModule2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save_competition_module**
> CompetitionModule2 save_competition_module(body, comp_id, tab_id, sub_tab_id)

save

Add a new CompetitionModule to subTab

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
api_instance = swagger_client.CompetitionModuleApi(swagger_client.ApiClient(configuration))
body = swagger_client.CompetitionModule2() # CompetitionModule2 | CompetitionModule object that needs to be added to the storage
comp_id = 'comp_id_example' # str | id of competition
tab_id = 'tab_id_example' # str | id of tab
sub_tab_id = 'sub_tab_id_example' # str | id of subtab

try:
    # save
    api_response = api_instance.save_competition_module(body, comp_id, tab_id, sub_tab_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionModuleApi->save_competition_module: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CompetitionModule2**](CompetitionModule2.md)| CompetitionModule object that needs to be added to the storage | 
 **comp_id** | **str**| id of competition | 
 **tab_id** | **str**| id of tab | 
 **sub_tab_id** | **str**| id of subtab | 

### Return type

[**CompetitionModule2**](CompetitionModule2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save_competition_module_0**
> CompetitionModule2 save_competition_module_0(body, comp_id, tab_id)

save

Add a new CompetitionModule to Module

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
api_instance = swagger_client.CompetitionModuleApi(swagger_client.ApiClient(configuration))
body = swagger_client.CompetitionModule2() # CompetitionModule2 | CompetitionModule object that needs to be added to the storage
comp_id = 'comp_id_example' # str | id of competition
tab_id = 'tab_id_example' # str | id of tab

try:
    # save
    api_response = api_instance.save_competition_module_0(body, comp_id, tab_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionModuleApi->save_competition_module_0: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CompetitionModule2**](CompetitionModule2.md)| CompetitionModule object that needs to be added to the storage | 
 **comp_id** | **str**| id of competition | 
 **tab_id** | **str**| id of tab | 

### Return type

[**CompetitionModule2**](CompetitionModule2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_competition_module**
> CompetitionModule2 update_competition_module(body, id)

update

Update an existing CompetitionModule

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
api_instance = swagger_client.CompetitionModuleApi(swagger_client.ApiClient(configuration))
body = swagger_client.CompetitionModule2() # CompetitionModule2 | CompetitionModule object that needs to be updated in the storage
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.update_competition_module(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionModuleApi->update_competition_module: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CompetitionModule2**](CompetitionModule2.md)| CompetitionModule object that needs to be updated in the storage | 
 **id** | **str**| id of resource | 

### Return type

[**CompetitionModule2**](CompetitionModule2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

