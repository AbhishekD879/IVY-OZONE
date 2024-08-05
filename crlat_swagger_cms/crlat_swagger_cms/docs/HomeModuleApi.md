# swagger_client.HomeModuleApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**find_all20**](HomeModuleApi.md#find_all20) | **GET** /home-module | findAll
[**find_one19**](HomeModuleApi.md#find_one19) | **GET** /home-module/{id} | findOne
[**home_module_by_id**](HomeModuleApi.md#home_module_by_id) | **DELETE** /home-module/{id} | HomeModuleById
[**load_ss_events**](HomeModuleApi.md#load_ss_events) | **GET** /home-module/brand/{brand}/ss/event | loadSSEvents
[**read**](HomeModuleApi.md#read) | **GET** /home-module/brand/{brand} | read
[**read_by_brand_page_type_page_id**](HomeModuleApi.md#read_by_brand_page_type_page_id) | **GET** /home-module/brand/{brand}/{pageType}/{pageId} | read
[**save20**](HomeModuleApi.md#save20) | **POST** /home-module | save
[**update19**](HomeModuleApi.md#update19) | **PUT** /home-module/{id} | update

# **find_all20**
> list[HomeModule] find_all20(active=active)

findAll

Retrieve active/inactive HomeModules

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
api_instance = swagger_client.HomeModuleApi(swagger_client.ApiClient(configuration))
active = true # bool |  (optional)

try:
    # findAll
    api_response = api_instance.find_all20(active=active)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HomeModuleApi->find_all20: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **active** | **bool**|  | [optional] 

### Return type

[**list[HomeModule]**](HomeModule.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one19**
> HomeModule2 find_one19(id)

findOne

Searches HomeModule by id

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
api_instance = swagger_client.HomeModuleApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.find_one19(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HomeModuleApi->find_one19: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**HomeModule2**](HomeModule2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **home_module_by_id**
> home_module_by_id(id)

HomeModuleById

Delete a HomeModule

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
api_instance = swagger_client.HomeModuleApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # HomeModuleById
    api_instance.home_module_by_id(id)
except ApiException as e:
    print("Exception when calling HomeModuleApi->home_module_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

void (empty response body)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **load_ss_events**
> SiteServeEventDto load_ss_events(brand, selection_type, selection_id, date_from, date_to)

loadSSEvents

Returns SiteServe events by type, id and date range

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
api_instance = swagger_client.HomeModuleApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return
selection_type = 'selection_type_example' # str | Selection Type
selection_id = 1.2 # float | Selection id
date_from = '2013-10-20' # date | time in format 'yyyy-MM-dd'T'HH:mm:ssZ'
date_to = '2013-10-20' # date | time in format 'yyyy-MM-dd'T'HH:mm:ssZ'

try:
    # loadSSEvents
    api_response = api_instance.load_ss_events(brand, selection_type, selection_id, date_from, date_to)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HomeModuleApi->load_ss_events: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 
 **selection_type** | **str**| Selection Type | 
 **selection_id** | **float**| Selection id | 
 **date_from** | **date**| time in format &#x27;yyyy-MM-dd&#x27;T&#x27;HH:mm:ssZ&#x27; | 
 **date_to** | **date**| time in format &#x27;yyyy-MM-dd&#x27;T&#x27;HH:mm:ssZ&#x27; | 

### Return type

[**SiteServeEventDto**](SiteServeEventDto.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read**
> list[HomeModule2] read(brand, active=active)

read

Searches HomeModule by brand

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
api_instance = swagger_client.HomeModuleApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return
active = true # bool |  (optional)

try:
    # read
    api_response = api_instance.read(brand, active=active)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HomeModuleApi->read: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 
 **active** | **bool**|  | [optional] 

### Return type

[**list[HomeModule2]**](HomeModule2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_by_brand_page_type_page_id**
> list[HomeModule2] read_by_brand_page_type_page_id(brand, page_type, page_id)

read

Searches HomeModule by brand, pageType & pageId

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
api_instance = swagger_client.HomeModuleApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return
page_type = 'page_type_example' # str | name of pageType
page_id = 1.2 # float | pageId to filter objects

try:
    # read
    api_response = api_instance.read_by_brand_page_type_page_id(brand, page_type, page_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HomeModuleApi->read_by_brand_page_type_page_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 
 **page_type** | **str**| name of pageType | 
 **page_id** | **float**| pageId to filter objects | 

### Return type

[**list[HomeModule2]**](HomeModule2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save20**
> HomeModule2 save20(body)

save

Add a new HomeModule

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
api_instance = swagger_client.HomeModuleApi(swagger_client.ApiClient(configuration))
body = swagger_client.HomeModule2() # HomeModule2 | HomeModule object that needs to be added to the storage

try:
    # save
    api_response = api_instance.post_new_home_module(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HomeModuleApi->save20: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**HomeModule2**](HomeModule2.md)| HomeModule object that needs to be added to the storage | 

### Return type

[**HomeModule2**](HomeModule2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update19**
> HomeModule2 update19(body, id)

update

Update an existing HomeModule

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
api_instance = swagger_client.HomeModuleApi(swagger_client.ApiClient(configuration))
body = swagger_client.HomeModule2() # HomeModule2 | Part of HomeModule that needs to be updated in the storage
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.update19(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HomeModuleApi->update19: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**HomeModule2**](HomeModule2.md)| Part of HomeModule that needs to be updated in the storage | 
 **id** | **str**| id of resource | 

### Return type

[**HomeModule2**](HomeModule2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

