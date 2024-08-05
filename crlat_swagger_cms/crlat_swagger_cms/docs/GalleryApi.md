# swagger_client.GalleryApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**find_all18**](GalleryApi.md#find_all18) | **GET** /gallery | findAll
[**find_one17**](GalleryApi.md#find_one17) | **GET** /gallery/{id} | findOne
[**gallery_by_id**](GalleryApi.md#gallery_by_id) | **DELETE** /gallery/{id} | GalleryById
[**save18**](GalleryApi.md#save18) | **POST** /gallery | save
[**update17**](GalleryApi.md#update17) | **PUT** /gallery/{id} | update

# **find_all18**
> list[Gallery] find_all18()

findAll

Retrieve all Gallerys

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
api_instance = swagger_client.GalleryApi(swagger_client.ApiClient(configuration))

try:
    # findAll
    api_response = api_instance.find_all18()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GalleryApi->find_all18: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Gallery]**](Gallery.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one17**
> Gallery2 find_one17(id)

findOne

Searches Gallery by id

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
api_instance = swagger_client.GalleryApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.find_one17(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GalleryApi->find_one17: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**Gallery2**](Gallery2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **gallery_by_id**
> gallery_by_id(id)

GalleryById

Delete a Gallery

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
api_instance = swagger_client.GalleryApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # GalleryById
    api_instance.gallery_by_id(id)
except ApiException as e:
    print("Exception when calling GalleryApi->gallery_by_id: %s\n" % e)
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

# **save18**
> Gallery2 save18(body)

save

Add a new Gallery

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
api_instance = swagger_client.GalleryApi(swagger_client.ApiClient(configuration))
body = swagger_client.Gallery2() # Gallery2 | Gallery object that needs to be added to the storage

try:
    # save
    api_response = api_instance.save18(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GalleryApi->save18: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Gallery2**](Gallery2.md)| Gallery object that needs to be added to the storage | 

### Return type

[**Gallery2**](Gallery2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update17**
> Gallery2 update17(body, id)

update

Update an existing Gallery

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
api_instance = swagger_client.GalleryApi(swagger_client.ApiClient(configuration))
body = swagger_client.Gallery2() # Gallery2 | Gallery object that needs to be updated in the storage
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.update17(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GalleryApi->update17: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Gallery2**](Gallery2.md)| Gallery object that needs to be updated in the storage | 
 **id** | **str**| id of resource | 

### Return type

[**Gallery2**](Gallery2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

