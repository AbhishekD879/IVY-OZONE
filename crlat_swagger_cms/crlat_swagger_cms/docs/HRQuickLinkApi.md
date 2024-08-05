# swagger_client.HRQuickLinkApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**find_all21**](HRQuickLinkApi.md#find_all21) | **GET** /hr-quick-link | findAll
[**find_one20**](HRQuickLinkApi.md#find_one20) | **GET** /hr-quick-link/{id} | findOne
[**hr_quick_link_by_id**](HRQuickLinkApi.md#hr_quick_link_by_id) | **DELETE** /hr-quick-link/{id} | HrQuickLinkById
[**order**](HRQuickLinkApi.md#order) | **POST** /hr-quick-link/ordering | order
[**read**](HRQuickLinkApi.md#read) | **GET** /hr-quick-link/brand/{brand} | read
[**remove_image_hr_quick_link**](HRQuickLinkApi.md#remove_image_hr_quick_link) | **DELETE** /hr-quick-link/{id}/image | removeImage
[**save21**](HRQuickLinkApi.md#save21) | **POST** /hr-quick-link | save
[**update20**](HRQuickLinkApi.md#update20) | **PUT** /hr-quick-link/{id} | update
[**upload_image_hr_quick_link**](HRQuickLinkApi.md#upload_image_hr_quick_link) | **POST** /hr-quick-link/{id}/image | uploadImage

# **find_all21**
> list[HRQuickLink] find_all21()

findAll

Retrieve all HRQuickLinks

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
api_instance = swagger_client.HRQuickLinkApi(swagger_client.ApiClient(configuration))

try:
    # findAll
    api_response = api_instance.find_all21()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HRQuickLinkApi->find_all21: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[HRQuickLink]**](HRQuickLink.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one20**
> HRQuickLink2 find_one20(id)

findOne

Searches HRQuickLink by id

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
api_instance = swagger_client.HRQuickLinkApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.find_one20(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HRQuickLinkApi->find_one20: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**HRQuickLink2**](HRQuickLink2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **hr_quick_link_by_id**
> hr_quick_link_by_id(id)

HrQuickLinkById

Delete a HRQuickLink

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
api_instance = swagger_client.HRQuickLinkApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # HrQuickLinkById
    api_instance.hr_quick_link_by_id(id)
except ApiException as e:
    print("Exception when calling HRQuickLinkApi->hr_quick_link_by_id: %s\n" % e)
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

Set order for all HRQuickLink

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
api_instance = swagger_client.HRQuickLinkApi(swagger_client.ApiClient(configuration))
body = swagger_client.Ordering2() # Ordering2 | List of ordered ids of HRQuickLink

try:
    # order
    api_instance.order(body)
except ApiException as e:
    print("Exception when calling HRQuickLinkApi->order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Ordering2**](Ordering2.md)| List of ordered ids of HRQuickLink | 

### Return type

void (empty response body)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read**
> list[HRQuickLink2] read(brand)

read

Searches HRQuickLink by brand and sort it by sortOrder field in Asc order

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
api_instance = swagger_client.HRQuickLinkApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return

try:
    # read
    api_response = api_instance.read(brand)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HRQuickLinkApi->read: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 

### Return type

[**list[HRQuickLink2]**](HRQuickLink2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_image_hr_quick_link**
> remove_image_hr_quick_link(id)

removeImage

Remove image from hrQuickLink

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
api_instance = swagger_client.HRQuickLinkApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # removeImage
    api_instance.remove_image_hr_quick_link(id)
except ApiException as e:
    print("Exception when calling HRQuickLinkApi->remove_image_hr_quick_link: %s\n" % e)
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

# **save21**
> HRQuickLink2 save21(body)

save

Add a new HRQuickLink

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
api_instance = swagger_client.HRQuickLinkApi(swagger_client.ApiClient(configuration))
body = swagger_client.HRQuickLink2() # HRQuickLink2 | HRQuickLink object that needs to be added to the storage

try:
    # save
    api_response = api_instance.save21(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HRQuickLinkApi->save21: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**HRQuickLink2**](HRQuickLink2.md)| HRQuickLink object that needs to be added to the storage | 

### Return type

[**HRQuickLink2**](HRQuickLink2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update20**
> HRQuickLink2 update20(body, id)

update

Update an existing HRQuickLink

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
api_instance = swagger_client.HRQuickLinkApi(swagger_client.ApiClient(configuration))
body = swagger_client.HRQuickLink2() # HRQuickLink2 | HRQuickLink object that needs to be updated in the storage
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.update20(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HRQuickLinkApi->update20: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**HRQuickLink2**](HRQuickLink2.md)| HRQuickLink object that needs to be updated in the storage | 
 **id** | **str**| id of resource | 

### Return type

[**HRQuickLink2**](HRQuickLink2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_image_hr_quick_link**
> HRQuickLink2 upload_image_hr_quick_link(id, file=file)

uploadImage

Upload new image for hrQuickLink

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
api_instance = swagger_client.HRQuickLinkApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource
file = 'file_example' # str |  (optional)

try:
    # uploadImage
    api_response = api_instance.upload_image_hr_quick_link(id, file=file)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HRQuickLinkApi->upload_image_hr_quick_link: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 
 **file** | **str**|  | [optional] 

### Return type

[**HRQuickLink2**](HRQuickLink2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

