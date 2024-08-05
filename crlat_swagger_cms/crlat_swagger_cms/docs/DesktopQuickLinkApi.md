# swagger_client.DesktopQuickLinkApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**desktop_quick_link_by_id**](DesktopQuickLinkApi.md#desktop_quick_link_by_id) | **DELETE** /desktop-quick-link/{id} | DesktopQuickLinkById
[**find_all24**](DesktopQuickLinkApi.md#find_all24) | **GET** /desktop-quick-link | findAll
[**find_one23**](DesktopQuickLinkApi.md#find_one23) | **GET** /desktop-quick-link/{id} | findOne
[**order**](DesktopQuickLinkApi.md#order) | **POST** /desktop-quick-link/ordereing | order
[**read**](DesktopQuickLinkApi.md#read) | **GET** /desktop-quick-link/brand/{brand} | read
[**remove_image_desktop_quick_link**](DesktopQuickLinkApi.md#remove_image_desktop_quick_link) | **DELETE** /desktop-quick-link/{id}/image | removeImage
[**save24**](DesktopQuickLinkApi.md#save24) | **POST** /desktop-quick-link | save
[**update23**](DesktopQuickLinkApi.md#update23) | **PUT** /desktop-quick-link/{id} | update
[**upload_image_desktop_quick_link**](DesktopQuickLinkApi.md#upload_image_desktop_quick_link) | **POST** /desktop-quick-link/{id}/image | uploadImage

# **desktop_quick_link_by_id**
> desktop_quick_link_by_id(id)

DesktopQuickLinkById

Delete a DesktopQuickLink

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
api_instance = swagger_client.DesktopQuickLinkApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # DesktopQuickLinkById
    api_instance.desktop_quick_link_by_id(id)
except ApiException as e:
    print("Exception when calling DesktopQuickLinkApi->desktop_quick_link_by_id: %s\n" % e)
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

# **find_all24**
> list[DesktopQuickLink] find_all24()

findAll

Retrieve all DesktopQuickLinks

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
api_instance = swagger_client.DesktopQuickLinkApi(swagger_client.ApiClient(configuration))

try:
    # findAll
    api_response = api_instance.find_all24()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DesktopQuickLinkApi->find_all24: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[DesktopQuickLink]**](DesktopQuickLink.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one23**
> DesktopQuickLink2 find_one23(id)

findOne

Searches DesktopQuickLink by id

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
api_instance = swagger_client.DesktopQuickLinkApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.find_one23(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DesktopQuickLinkApi->find_one23: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**DesktopQuickLink2**](DesktopQuickLink2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **order**
> order(body)

order

Set order for all DesktopQuickLink

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
api_instance = swagger_client.DesktopQuickLinkApi(swagger_client.ApiClient(configuration))
body = swagger_client.Ordering2() # Ordering2 | List of ordered ids of DesktopQuickLink

try:
    # order
    api_instance.order(body)
except ApiException as e:
    print("Exception when calling DesktopQuickLinkApi->order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Ordering2**](Ordering2.md)| List of ordered ids of DesktopQuickLink | 

### Return type

void (empty response body)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read**
> list[DesktopQuickLink2] read(brand)

read

Searches DesktopQuickLink by brand and sort it by sortOrder field in Asc order

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
api_instance = swagger_client.DesktopQuickLinkApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return

try:
    # read
    api_response = api_instance.read(brand)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DesktopQuickLinkApi->read: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 

### Return type

[**list[DesktopQuickLink2]**](DesktopQuickLink2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_image_desktop_quick_link**
> remove_image_desktop_quick_link(id)

removeImage

Remove image from DesktopQuickLink

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
api_instance = swagger_client.DesktopQuickLinkApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # removeImage
    api_instance.remove_image_desktop_quick_link(id)
except ApiException as e:
    print("Exception when calling DesktopQuickLinkApi->remove_image_desktop_quick_link: %s\n" % e)
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

# **save24**
> DesktopQuickLink2 save24(body)

save

Add a new DesktopQuickLink

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
api_instance = swagger_client.DesktopQuickLinkApi(swagger_client.ApiClient(configuration))
body = swagger_client.DesktopQuickLink2() # DesktopQuickLink2 | DesktopQuickLink object that needs to be added to the storage

try:
    # save
    api_response = api_instance.save24(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DesktopQuickLinkApi->save24: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**DesktopQuickLink2**](DesktopQuickLink2.md)| DesktopQuickLink object that needs to be added to the storage | 

### Return type

[**DesktopQuickLink2**](DesktopQuickLink2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update23**
> DesktopQuickLink2 update23(body, id)

update

Update an existing DesktopQuickLink

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
api_instance = swagger_client.DesktopQuickLinkApi(swagger_client.ApiClient(configuration))
body = swagger_client.DesktopQuickLink2() # DesktopQuickLink2 | DesktopQuickLink object that needs to be updated in the storage
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.update23(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DesktopQuickLinkApi->update23: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**DesktopQuickLink2**](DesktopQuickLink2.md)| DesktopQuickLink object that needs to be updated in the storage | 
 **id** | **str**| id of resource | 

### Return type

[**DesktopQuickLink2**](DesktopQuickLink2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_image_desktop_quick_link**
> DesktopQuickLink2 upload_image_desktop_quick_link(id, file=file)

uploadImage

Upload new image for DesktopQuickLink

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
api_instance = swagger_client.DesktopQuickLinkApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource
file = 'file_example' # str |  (optional)

try:
    # uploadImage
    api_response = api_instance.upload_image_desktop_quick_link(id, file=file)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DesktopQuickLinkApi->upload_image_desktop_quick_link: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 
 **file** | **str**|  | [optional] 

### Return type

[**DesktopQuickLink2**](DesktopQuickLink2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

