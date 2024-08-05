# swagger_client.HeaderSubMenuApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**find_all19**](HeaderSubMenuApi.md#find_all19) | **GET** /header-submenu | findAll
[**find_one18**](HeaderSubMenuApi.md#find_one18) | **GET** /header-submenu/{id} | findOne
[**header_sub_menu_by_id**](HeaderSubMenuApi.md#header_sub_menu_by_id) | **DELETE** /header-submenu/{id} | HeaderSubMenuById
[**order**](HeaderSubMenuApi.md#order) | **POST** /header-submenu/ordering | order
[**read**](HeaderSubMenuApi.md#read) | **GET** /header-submenu/brand/{brand} | read
[**save19**](HeaderSubMenuApi.md#save19) | **POST** /header-submenu | save
[**update18**](HeaderSubMenuApi.md#update18) | **PUT** /header-submenu/{id} | update

# **find_all19**
> list[HeaderSubMenu] find_all19()

findAll

Retrieve all HeaderSubMenus

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
api_instance = swagger_client.HeaderSubMenuApi(swagger_client.ApiClient(configuration))

try:
    # findAll
    api_response = api_instance.find_all19()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HeaderSubMenuApi->find_all19: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[HeaderSubMenu]**](HeaderSubMenu.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one18**
> HeaderSubMenu2 find_one18(id)

findOne

Searches HeaderSubMenu by id

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
api_instance = swagger_client.HeaderSubMenuApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.find_one18(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HeaderSubMenuApi->find_one18: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**HeaderSubMenu2**](HeaderSubMenu2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **header_sub_menu_by_id**
> header_sub_menu_by_id(id)

HeaderSubMenuById

Delete a HeaderSubMenu

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
api_instance = swagger_client.HeaderSubMenuApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # HeaderSubMenuById
    api_instance.header_sub_menu_by_id(id)
except ApiException as e:
    print("Exception when calling HeaderSubMenuApi->header_sub_menu_by_id: %s\n" % e)
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

Set order for all HeaderSubMenu

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
api_instance = swagger_client.HeaderSubMenuApi(swagger_client.ApiClient(configuration))
body = swagger_client.Ordering2() # Ordering2 | List of ordered ids of HeaderSubMenu

try:
    # order
    api_instance.order(body)
except ApiException as e:
    print("Exception when calling HeaderSubMenuApi->order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Ordering2**](Ordering2.md)| List of ordered ids of HeaderSubMenu | 

### Return type

void (empty response body)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read**
> list[HeaderSubMenu2] read(brand)

read

Searches HeaderSubMenu by brand and sort it by sortOrder field in Asc order

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
api_instance = swagger_client.HeaderSubMenuApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return

try:
    # read
    api_response = api_instance.read(brand)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HeaderSubMenuApi->read: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 

### Return type

[**list[HeaderSubMenu2]**](HeaderSubMenu2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save19**
> HeaderSubMenu2 save19(body)

save

Add a new HeaderSubMenu

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
api_instance = swagger_client.HeaderSubMenuApi(swagger_client.ApiClient(configuration))
body = swagger_client.HeaderSubMenu2() # HeaderSubMenu2 | HeaderSubMenu object that needs to be added to the storage

try:
    # save
    api_response = api_instance.save19(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HeaderSubMenuApi->save19: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**HeaderSubMenu2**](HeaderSubMenu2.md)| HeaderSubMenu object that needs to be added to the storage | 

### Return type

[**HeaderSubMenu2**](HeaderSubMenu2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update18**
> HeaderSubMenu2 update18(body, id)

update

Update an existing HeaderSubMenu

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
api_instance = swagger_client.HeaderSubMenuApi(swagger_client.ApiClient(configuration))
body = swagger_client.HeaderSubMenu2() # HeaderSubMenu2 | HeaderSubMenu object that needs to be updated in the storage
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.update18(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HeaderSubMenuApi->update18: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**HeaderSubMenu2**](HeaderSubMenu2.md)| HeaderSubMenu object that needs to be updated in the storage | 
 **id** | **str**| id of resource | 

### Return type

[**HeaderSubMenu2**](HeaderSubMenu2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

