# swagger_client.HeaderMenuApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**find_all19**](HeaderMenuApi.md#find_all19) | **GET** /header-menu | findAll
[**find_one18**](HeaderMenuApi.md#find_one18) | **GET** /header-menu/{id} | findOne
[**header_menu_by_id**](HeaderMenuApi.md#header_menu_by_id) | **DELETE** /header-menu/{id} | HeaderMenuById
[**order**](HeaderMenuApi.md#order) | **POST** /header-menu/ordering | order
[**read**](HeaderMenuApi.md#read) | **GET** /header-menu/brand/{brand} | read
[**save19**](HeaderMenuApi.md#save19) | **POST** /header-menu | save
[**update18**](HeaderMenuApi.md#update18) | **PUT** /header-menu/{id} | update

# **find_all19**
> list[HeaderMenu] find_all19()

findAll

Retrieve all HeaderMenus

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
api_instance = swagger_client.HeaderMenuApi(swagger_client.ApiClient(configuration))

try:
    # findAll
    api_response = api_instance.find_all19()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HeaderMenuApi->find_all19: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[HeaderMenu]**](HeaderMenu.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one18**
> HeaderMenu2 find_one18(id)

findOne

Searches HeaderMenu by id

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
api_instance = swagger_client.HeaderMenuApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.find_one18(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HeaderMenuApi->find_one18: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**HeaderMenu2**](HeaderMenu2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **header_menu_by_id**
> header_menu_by_id(id)

HeaderMenuById

Delete a HeaderMenu

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
api_instance = swagger_client.HeaderMenuApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # HeaderMenuById
    api_instance.header_menu_by_id(id)
except ApiException as e:
    print("Exception when calling HeaderMenuApi->header_menu_by_id: %s\n" % e)
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

Set order for all HeaderMenu

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
api_instance = swagger_client.HeaderMenuApi(swagger_client.ApiClient(configuration))
body = swagger_client.Ordering2() # Ordering2 | List of ordered ids of HeaderMenu

try:
    # order
    api_instance.order(body)
except ApiException as e:
    print("Exception when calling HeaderMenuApi->order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Ordering2**](Ordering2.md)| List of ordered ids of HeaderMenu | 

### Return type

void (empty response body)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read**
> list[HeaderMenu2] read(brand)

read

Searches HeaderMenu by brand and sort it by sortOrder field in Asc order

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
api_instance = swagger_client.HeaderMenuApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return

try:
    # read
    api_response = api_instance.read(brand)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HeaderMenuApi->read: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 

### Return type

[**list[HeaderMenu2]**](HeaderMenu2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save19**
> HeaderMenu2 save19(body)

save

Add a new HeaderMenu

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
api_instance = swagger_client.HeaderMenuApi(swagger_client.ApiClient(configuration))
body = swagger_client.HeaderMenu2() # HeaderMenu2 | HeaderMenu object that needs to be added to the storage

try:
    # save
    api_response = api_instance.save19(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HeaderMenuApi->save19: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**HeaderMenu2**](HeaderMenu2.md)| HeaderMenu object that needs to be added to the storage | 

### Return type

[**HeaderMenu2**](HeaderMenu2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update18**
> HeaderMenu2 update18(body, id)

update

Update an existing HeaderMenu

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
api_instance = swagger_client.HeaderMenuApi(swagger_client.ApiClient(configuration))
body = swagger_client.HeaderMenu2() # HeaderMenu2 | HeaderMenu object that needs to be updated in the storage
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.update18(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HeaderMenuApi->update18: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**HeaderMenu2**](HeaderMenu2.md)| HeaderMenu object that needs to be updated in the storage | 
 **id** | **str**| id of resource | 

### Return type

[**HeaderMenu2**](HeaderMenu2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

