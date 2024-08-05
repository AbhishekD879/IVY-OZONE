# swagger_client.HeaderContactMenuApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**header_contact_menu_delete_by_id**](HeaderContactMenuApi.md#header_contact_menu_delete_by_id) | **DELETE** /header-contact-menu/{id} | HeaderContactMenuById
[**header_contact_menu_find_all**](HeaderContactMenuApi.md#header_contact_menu_find_all) | **GET** /header-contact-menu | findAll
[**header_contact_menu_find_one**](HeaderContactMenuApi.md#header_contact_menu_find_one) | **GET** /header-contact-menu/{id} | findOne
[**header_contact_menu_order**](HeaderContactMenuApi.md#header_contact_menu_order) | **POST** /header-contact-menu/ordering | order
[**header_contact_menu_read**](HeaderContactMenuApi.md#header_contact_menu_read) | **GET** /header-contact-menu/brand/{brand} | read
[**header_contact_menu_save**](HeaderContactMenuApi.md#header_contact_menu_save) | **POST** /header-contact-menu | save
[**header_contact_menu_update**](HeaderContactMenuApi.md#header_contact_menu_update) | **PUT** /header-contact-menu/{id} | update

# **header_contact_menu_delete_by_id**
> header_contact_menu_delete_by_id(id)

HeaderContactMenuById

Delete a HeaderContactMenu

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
api_instance = swagger_client.HeaderContactMenuApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # HeaderContactMenuById
    api_instance.header_contact_menu_delete_by_id(id)
except ApiException as e:
    print("Exception when calling HeaderContactMenuApi->header_contact_menu_delete_by_id: %s\n" % e)
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

# **header_contact_menu_find_all**
> list[HeaderContactMenu] header_contact_menu_find_all()

findAll

Retrieve all HeaderContactMenus

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
api_instance = swagger_client.HeaderContactMenuApi(swagger_client.ApiClient(configuration))

try:
    # findAll
    api_response = api_instance.header_contact_menu_find_all()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HeaderContactMenuApi->header_contact_menu_find_all: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[HeaderContactMenu]**](HeaderContactMenu.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **header_contact_menu_find_one**
> HeaderContactMenu2 header_contact_menu_find_one(id)

findOne

Searches HeaderContactMenu by id

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
api_instance = swagger_client.HeaderContactMenuApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.header_contact_menu_find_one(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HeaderContactMenuApi->header_contact_menu_find_one: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**HeaderContactMenu2**](HeaderContactMenu2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **header_contact_menu_order**
> header_contact_menu_order(body)

order

Set order for all HeaderContactMenu

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
api_instance = swagger_client.HeaderContactMenuApi(swagger_client.ApiClient(configuration))
body = swagger_client.Ordering2() # Ordering2 | List of ordered ids of HeaderContactMenu

try:
    # order
    api_instance.header_contact_menu_order(body)
except ApiException as e:
    print("Exception when calling HeaderContactMenuApi->header_contact_menu_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Ordering2**](Ordering2.md)| List of ordered ids of HeaderContactMenu | 

### Return type

void (empty response body)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **header_contact_menu_read**
> list[HeaderContactMenu2] header_contact_menu_read(brand)

read

Searches HeaderContactMenu by brand and sort it by sortOrder field in Asc order

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
api_instance = swagger_client.HeaderContactMenuApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return

try:
    # read
    api_response = api_instance.header_contact_menu_read(brand)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HeaderContactMenuApi->header_contact_menu_read: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 

### Return type

[**list[HeaderContactMenu2]**](HeaderContactMenu2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **header_contact_menu_save**
> HeaderContactMenu2 header_contact_menu_save(body)

save

Add a new HeaderContactMenu

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
api_instance = swagger_client.HeaderContactMenuApi(swagger_client.ApiClient(configuration))
body = swagger_client.HeaderContactMenu2() # HeaderContactMenu2 | HeaderContactMenu object that needs to be added to the storage

try:
    # save
    api_response = api_instance.header_contact_menu_save(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HeaderContactMenuApi->header_contact_menu_save: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**HeaderContactMenu2**](HeaderContactMenu2.md)| HeaderContactMenu object that needs to be added to the storage | 

### Return type

[**HeaderContactMenu2**](HeaderContactMenu2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **header_contact_menu_update**
> HeaderContactMenu2 header_contact_menu_update(body, id)

update

Update an existing HeaderContactMenu

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
api_instance = swagger_client.HeaderContactMenuApi(swagger_client.ApiClient(configuration))
body = swagger_client.HeaderContactMenu2() # HeaderContactMenu2 | HeaderContactMenu object that needs to be updated in the storage
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.header_contact_menu_update(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HeaderContactMenuApi->header_contact_menu_update: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**HeaderContactMenu2**](HeaderContactMenu2.md)| HeaderContactMenu object that needs to be updated in the storage | 
 **id** | **str**| id of resource | 

### Return type

[**HeaderContactMenu2**](HeaderContactMenu2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

