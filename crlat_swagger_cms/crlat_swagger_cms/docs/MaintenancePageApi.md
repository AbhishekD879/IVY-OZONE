# swagger_client.MaintenancePageApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**find_all25**](MaintenancePageApi.md#find_all25) | **GET** /maintenance-page | findAll
[**find_one24**](MaintenancePageApi.md#find_one24) | **GET** /maintenance-page/{id} | findOne
[**maintenance_page_by_id**](MaintenancePageApi.md#maintenance_page_by_id) | **DELETE** /maintenance-page/{id} | MaintenancePageById
[**read**](MaintenancePageApi.md#read) | **GET** /maintenance-page/brand/{brand} | read
[**remove_image**](MaintenancePageApi.md#remove_image) | **DELETE** /maintenance-page/{id}/image | removeImage
[**save25**](MaintenancePageApi.md#save25) | **POST** /maintenance-page | save
[**update24**](MaintenancePageApi.md#update24) | **PUT** /maintenance-page/{id} | update
[**upload_image**](MaintenancePageApi.md#upload_image) | **POST** /maintenance-page/{id}/image | uploadImage

# **find_all25**
> list[MaintenancePage] find_all25()

findAll

Retrieve all MaintenancePages

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
api_instance = swagger_client.MaintenancePageApi(swagger_client.ApiClient(configuration))

try:
    # findAll
    api_response = api_instance.find_all25()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MaintenancePageApi->find_all25: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[MaintenancePage]**](MaintenancePage.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one24**
> MaintenancePage2 find_one24(id)

findOne

Searches MaintenancePage by id

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
api_instance = swagger_client.MaintenancePageApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.find_one24(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MaintenancePageApi->find_one24: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**MaintenancePage2**](MaintenancePage2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **maintenance_page_by_id**
> maintenance_page_by_id(id)

MaintenancePageById

Delete a MaintenancePage

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
api_instance = swagger_client.MaintenancePageApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # MaintenancePageById
    api_instance.maintenance_page_by_id(id)
except ApiException as e:
    print("Exception when calling MaintenancePageApi->maintenance_page_by_id: %s\n" % e)
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

# **read**
> list[MaintenancePage2] read(brand)

read

Searches MaintenancePage by brand and sort it by sortOrder field in Asc order

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
api_instance = swagger_client.MaintenancePageApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return

try:
    # read
    api_response = api_instance.read(brand)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MaintenancePageApi->read: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 

### Return type

[**list[MaintenancePage2]**](MaintenancePage2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_image**
> remove_image(id)

removeImage

Remove image from MaintenancePage

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
api_instance = swagger_client.MaintenancePageApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # removeImage
    api_instance.remove_image(id)
except ApiException as e:
    print("Exception when calling MaintenancePageApi->remove_image: %s\n" % e)
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

# **save25**
> MaintenancePage2 save25(body)

save

Add a new MaintenancePage

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
api_instance = swagger_client.MaintenancePageApi(swagger_client.ApiClient(configuration))
body = swagger_client.MaintenancePage2() # MaintenancePage2 | MaintenancePage object that needs to be added to the storage

try:
    # save
    api_response = api_instance.save25(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MaintenancePageApi->save25: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**MaintenancePage2**](MaintenancePage2.md)| MaintenancePage object that needs to be added to the storage | 

### Return type

[**MaintenancePage2**](MaintenancePage2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update24**
> MaintenancePage2 update24(body, id)

update

Update an existing MaintenancePage

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
api_instance = swagger_client.MaintenancePageApi(swagger_client.ApiClient(configuration))
body = swagger_client.MaintenancePage2() # MaintenancePage2 | MaintenancePage object that needs to be updated in the storage
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.update24(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MaintenancePageApi->update24: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**MaintenancePage2**](MaintenancePage2.md)| MaintenancePage object that needs to be updated in the storage | 
 **id** | **str**| id of resource | 

### Return type

[**MaintenancePage2**](MaintenancePage2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_image**
> MaintenancePage2 upload_image(id, file=file)

uploadImage

Upload new image for MaintenancePage

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
api_instance = swagger_client.MaintenancePageApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource
file = 'file_example' # str |  (optional)

try:
    # uploadImage
    api_response = api_instance.upload_image(id, file=file)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MaintenancePageApi->upload_image: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 
 **file** | **str**|  | [optional] 

### Return type

[**MaintenancePage2**](MaintenancePage2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

