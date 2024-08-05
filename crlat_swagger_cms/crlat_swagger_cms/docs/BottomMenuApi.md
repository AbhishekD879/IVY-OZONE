# swagger_client.BottomMenuApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**bottom_menu_by_id**](BottomMenuApi.md#bottom_menu_by_id) | **DELETE** /bottom-menu/{id} | BottomMenuById
[**find_all4**](BottomMenuApi.md#find_all4) | **GET** /bottom-menu | findAll
[**find_one4**](BottomMenuApi.md#find_one4) | **GET** /bottom-menu/{id} | findOne
[**order**](BottomMenuApi.md#order) | **POST** /bottom-menu/ordering | order
[**read**](BottomMenuApi.md#read) | **GET** /bottom-menu/brand/{brand} | read
[**save4**](BottomMenuApi.md#save4) | **POST** /bottom-menu | save
[**update4**](BottomMenuApi.md#update4) | **PUT** /bottom-menu/{id} | update

# **bottom_menu_by_id**
> bottom_menu_by_id(id)

BottomMenuById

Delete a BottomMenu

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
api_instance = swagger_client.BottomMenuApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # BottomMenuById
    api_instance.bottom_menu_by_id(id)
except ApiException as e:
    print("Exception when calling BottomMenuApi->bottom_menu_by_id: %s\n" % e)
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

# **find_all4**
> list[BottomMenu] find_all4()

findAll

Retrieve all BottomMenus

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
api_instance = swagger_client.BottomMenuApi(swagger_client.ApiClient(configuration))

try:
    # findAll
    api_response = api_instance.find_all4()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BottomMenuApi->find_all4: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[BottomMenu]**](BottomMenu.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one4**
> BottomMenu2 find_one4(id)

findOne

Searches BottomMenu by id

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
api_instance = swagger_client.BottomMenuApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.find_one4(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BottomMenuApi->find_one4: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**BottomMenu2**](BottomMenu2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **order**
> order(body)

order

Set order for all BottomMenu

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
api_instance = swagger_client.BottomMenuApi(swagger_client.ApiClient(configuration))
body = swagger_client.Ordering2() # Ordering2 | List of ordered ids of BottomMenu

try:
    # order
    api_instance.order(body)
except ApiException as e:
    print("Exception when calling BottomMenuApi->order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Ordering2**](Ordering2.md)| List of ordered ids of BottomMenu | 

### Return type

void (empty response body)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read**
> list[BottomMenu2] read(brand)

read

Searches BottomMenu by brand and sort it by sortOrder field in Asc order

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
api_instance = swagger_client.BottomMenuApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return

try:
    # read
    api_response = api_instance.read(brand)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BottomMenuApi->read: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 

### Return type

[**list[BottomMenu2]**](BottomMenu2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save4**
> BottomMenu2 save4(body)

save

Add a new BottomMenu

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
api_instance = swagger_client.BottomMenuApi(swagger_client.ApiClient(configuration))
body = swagger_client.BottomMenu2() # BottomMenu2 | BottomMenu object that needs to be added to the storage

try:
    # save
    api_response = api_instance.save4(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BottomMenuApi->save4: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**BottomMenu2**](BottomMenu2.md)| BottomMenu object that needs to be added to the storage | 

### Return type

[**BottomMenu2**](BottomMenu2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update4**
> BottomMenu2 update4(body, id)

update

Update an existing BottomMenu

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
api_instance = swagger_client.BottomMenuApi(swagger_client.ApiClient(configuration))
body = swagger_client.BottomMenu2() # BottomMenu2 | BottomMenu object that needs to be updated in the storage
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.update4(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BottomMenuApi->update4: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**BottomMenu2**](BottomMenu2.md)| BottomMenu object that needs to be updated in the storage | 
 **id** | **str**| id of resource | 

### Return type

[**BottomMenu2**](BottomMenu2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

