# swagger_client.ModuleRibbonTabApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**find_all26**](ModuleRibbonTabApi.md#find_all26) | **GET** /module-ribbon-tab | findAll
[**find_one25**](ModuleRibbonTabApi.md#find_one25) | **GET** /module-ribbon-tab/{id} | findOne
[**module_ribbon_tab_by_id**](ModuleRibbonTabApi.md#module_ribbon_tab_by_id) | **DELETE** /module-ribbon-tab/{id} | ModuleRibbonTabById
[**order**](ModuleRibbonTabApi.md#order) | **POST** /module-ribbon-tab/ordering | order
[**read**](ModuleRibbonTabApi.md#read) | **GET** /module-ribbon-tab/brand/{brand} | read
[**save26**](ModuleRibbonTabApi.md#save26) | **POST** /module-ribbon-tab | save
[**update25**](ModuleRibbonTabApi.md#update25) | **PUT** /module-ribbon-tab/{id} | update

# **find_all26**
> list[ModuleRibbonTab] find_all26()

findAll

Retrieve all ModuleRibbonTabs

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
api_instance = swagger_client.ModuleRibbonTabApi(swagger_client.ApiClient(configuration))

try:
    # findAll
    api_response = api_instance.find_all26()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModuleRibbonTabApi->find_all26: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[ModuleRibbonTab]**](ModuleRibbonTab.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one25**
> ModuleRibbonTab2 find_one25(id)

findOne

Searches ModuleRibbonTab by id

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
api_instance = swagger_client.ModuleRibbonTabApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.find_one25(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModuleRibbonTabApi->find_one25: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**ModuleRibbonTab2**](ModuleRibbonTab2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **module_ribbon_tab_by_id**
> module_ribbon_tab_by_id(id)

ModuleRibbonTabById

Delete a ModuleRibbonTab

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
api_instance = swagger_client.ModuleRibbonTabApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # ModuleRibbonTabById
    api_instance.module_ribbon_tab_by_id(id)
except ApiException as e:
    print("Exception when calling ModuleRibbonTabApi->module_ribbon_tab_by_id: %s\n" % e)
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

# **order**
> order(body)

order

Set order for all ModuleRibbonTab

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
api_instance = swagger_client.ModuleRibbonTabApi(swagger_client.ApiClient(configuration))
body = swagger_client.Ordering2() # Ordering2 | List of ordered ids of ModuleRibbonTabs

try:
    # order
    api_instance.order(body)
except ApiException as e:
    print("Exception when calling ModuleRibbonTabApi->order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Ordering2**](Ordering2.md)| List of ordered ids of ModuleRibbonTabs | 

### Return type

void (empty response body)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read**
> list[ModuleRibbonTab2] read(brand)

read

Searches ModuleRibbonTab by brand and sort it by sortOrder field in Asc order

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
api_instance = swagger_client.ModuleRibbonTabApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return

try:
    # read
    api_response = api_instance.read(brand)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModuleRibbonTabApi->read: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 

### Return type

[**list[ModuleRibbonTab2]**](ModuleRibbonTab2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save26**
> ModuleRibbonTab2 save26(body)

save

Add a new ModuleRibbonTab

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
api_instance = swagger_client.ModuleRibbonTabApi(swagger_client.ApiClient(configuration))
body = swagger_client.ModuleRibbonTab2() # ModuleRibbonTab2 | ModuleRibbonTab object that needs to be added to the storage

try:
    # save
    api_response = api_instance.save26(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModuleRibbonTabApi->save26: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ModuleRibbonTab2**](ModuleRibbonTab2.md)| ModuleRibbonTab object that needs to be added to the storage | 

### Return type

[**ModuleRibbonTab2**](ModuleRibbonTab2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update25**
> ModuleRibbonTab2 update25(body, id)

update

Update an existing ModuleRibbonTab

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
api_instance = swagger_client.ModuleRibbonTabApi(swagger_client.ApiClient(configuration))
body = swagger_client.ModuleRibbonTab2() # ModuleRibbonTab2 | ModuleRibbonTab object that needs to be updated in the storage
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.update25(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModuleRibbonTabApi->update25: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ModuleRibbonTab2**](ModuleRibbonTab2.md)| ModuleRibbonTab object that needs to be updated in the storage | 
 **id** | **str**| id of resource | 

### Return type

[**ModuleRibbonTab2**](ModuleRibbonTab2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

