# swagger_client.ConnectMenuApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**connect_menu_by_id**](ConnectMenuApi.md#connect_menu_by_id) | **DELETE** /connect-menu/{id} | ConnectMenuById
[**find_all7**](ConnectMenuApi.md#find_all7) | **GET** /connect-menu | findAll
[**find_one6**](ConnectMenuApi.md#find_one6) | **GET** /connect-menu/{id} | findOne
[**order**](ConnectMenuApi.md#order) | **POST** /connect-menu/ordering | order
[**read**](ConnectMenuApi.md#read) | **GET** /connect-menu/brand/{brand} | read
[**remove_image_connect_menu**](ConnectMenuApi.md#remove_image_connect_menu) | **DELETE** /connect-menu/{id}/image | removeImage
[**save7**](ConnectMenuApi.md#save7) | **POST** /connect-menu | save
[**update6**](ConnectMenuApi.md#update6) | **PUT** /connect-menu/{id} | update
[**upload_image_connect_menu**](ConnectMenuApi.md#upload_image_connect_menu) | **POST** /connect-menu/{id}/image | uploadImage

# **connect_menu_by_id**
> connect_menu_by_id(id)

ConnectMenuById

Delete a ConnectMenu

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
api_instance = swagger_client.ConnectMenuApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # ConnectMenuById
    api_instance.connect_menu_by_id(id)
except ApiException as e:
    print("Exception when calling ConnectMenuApi->connect_menu_by_id: %s\n" % e)
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

# **find_all7**
> list[ConnectMenu] find_all7()

findAll

Retrieve all ConnectMenus

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
api_instance = swagger_client.ConnectMenuApi(swagger_client.ApiClient(configuration))

try:
    # findAll
    api_response = api_instance.find_all7()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectMenuApi->find_all7: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[ConnectMenu]**](ConnectMenu.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one6**
> ConnectMenu2 find_one6(id)

findOne

Searches ConnectMenu by id

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
api_instance = swagger_client.ConnectMenuApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.find_one6(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectMenuApi->find_one6: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**ConnectMenu2**](ConnectMenu2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **order**
> order(body)

order

Set order for all ConnectMenu

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
api_instance = swagger_client.ConnectMenuApi(swagger_client.ApiClient(configuration))
body = swagger_client.Ordering2() # Ordering2 | List of ordered ids of ConnectMenu

try:
    # order
    api_instance.order(body)
except ApiException as e:
    print("Exception when calling ConnectMenuApi->order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Ordering2**](Ordering2.md)| List of ordered ids of ConnectMenu | 

### Return type

void (empty response body)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read**
> list[ConnectMenu2] read(brand)

read

Searches ConnectMenu by brand and sort it by sortOrder field in Asc order

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
api_instance = swagger_client.ConnectMenuApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return

try:
    # read
    api_response = api_instance.read(brand)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectMenuApi->read: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 

### Return type

[**list[ConnectMenu2]**](ConnectMenu2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_image_connect_menu**
> remove_image_connect_menu(id)

removeImage

Remove image from ConnectMenu

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
api_instance = swagger_client.ConnectMenuApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # removeImage
    api_instance.remove_image_connect_menu(id)
except ApiException as e:
    print("Exception when calling ConnectMenuApi->remove_image_connect_menu: %s\n" % e)
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

# **save7**
> ConnectMenu2 save7(body)

save

Add a new ConnectMenu

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
api_instance = swagger_client.ConnectMenuApi(swagger_client.ApiClient(configuration))
body = swagger_client.ConnectMenu2() # ConnectMenu2 | ConnectMenu object that needs to be added to the storage

try:
    # save
    api_response = api_instance.save7(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectMenuApi->save7: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConnectMenu2**](ConnectMenu2.md)| ConnectMenu object that needs to be added to the storage | 

### Return type

[**ConnectMenu2**](ConnectMenu2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update6**
> ConnectMenu2 update6(body, id)

update

Update an existing ConnectMenu

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
api_instance = swagger_client.ConnectMenuApi(swagger_client.ApiClient(configuration))
body = swagger_client.ConnectMenu2() # ConnectMenu2 | ConnectMenu object that needs to be updated in the storage
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.update6(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectMenuApi->update6: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConnectMenu2**](ConnectMenu2.md)| ConnectMenu object that needs to be updated in the storage | 
 **id** | **str**| id of resource | 

### Return type

[**ConnectMenu2**](ConnectMenu2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_image_connect_menu**
> ConnectMenu2 upload_image_connect_menu(id, file=file)

uploadImage

Upload new image for connectMenu

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
api_instance = swagger_client.ConnectMenuApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource
file = 'file_example' # str |  (optional)

try:
    # uploadImage
    api_response = api_instance.upload_image_connect_menu(id, file=file)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectMenuApi->upload_image_connect_menu: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 
 **file** | **str**|  | [optional] 

### Return type

[**ConnectMenu2**](ConnectMenu2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

