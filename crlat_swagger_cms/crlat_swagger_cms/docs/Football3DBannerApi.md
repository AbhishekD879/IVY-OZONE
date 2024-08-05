# swagger_client.Football3DBannerApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**find_all15**](Football3DBannerApi.md#find_all15) | **GET** /football-3d-banner | findAll
[**find_one14**](Football3DBannerApi.md#find_one14) | **GET** /football-3d-banner/{id} | findOne
[**football3d_banner_by_id**](Football3DBannerApi.md#football3d_banner_by_id) | **DELETE** /football-3d-banner/{id} | Football3dBannerById
[**order**](Football3DBannerApi.md#order) | **POST** /football-3d-banner/ordering | order
[**read**](Football3DBannerApi.md#read) | **GET** /football-3d-banner/brand/{brand} | read
[**remove_image**](Football3DBannerApi.md#remove_image) | **DELETE** /football-3d-banner/{id}/image | removeImage
[**save15**](Football3DBannerApi.md#save15) | **POST** /football-3d-banner | save
[**update14**](Football3DBannerApi.md#update14) | **PUT** /football-3d-banner/{id} | update
[**upload_image**](Football3DBannerApi.md#upload_image) | **POST** /football-3d-banner/{id}/image | uploadImage

# **find_all15**
> list[Football3DBanner] find_all15()

findAll

Retrieve all Football3DBanners

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
api_instance = swagger_client.Football3DBannerApi(swagger_client.ApiClient(configuration))

try:
    # findAll
    api_response = api_instance.find_all15()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling Football3DBannerApi->find_all15: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Football3DBanner]**](Football3DBanner.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one14**
> Football3DBanner2 find_one14(id)

findOne

Searches Football3DBanner by id

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
api_instance = swagger_client.Football3DBannerApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.find_one14(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling Football3DBannerApi->find_one14: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**Football3DBanner2**](Football3DBanner2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **football3d_banner_by_id**
> football3d_banner_by_id(id)

Football3dBannerById

Delete a Football3DBanner

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
api_instance = swagger_client.Football3DBannerApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # Football3dBannerById
    api_instance.football3d_banner_by_id(id)
except ApiException as e:
    print("Exception when calling Football3DBannerApi->football3d_banner_by_id: %s\n" % e)
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

Set order for all Football3DBanner

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
api_instance = swagger_client.Football3DBannerApi(swagger_client.ApiClient(configuration))
body = swagger_client.Ordering2() # Ordering2 | List of ordered ids of Football3DBanner

try:
    # order
    api_instance.order(body)
except ApiException as e:
    print("Exception when calling Football3DBannerApi->order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Ordering2**](Ordering2.md)| List of ordered ids of Football3DBanner | 

### Return type

void (empty response body)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read**
> list[Football3DBanner2] read(brand)

read

Searches Football3DBanner by brand and sort it by sortOrder field in Asc order

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
api_instance = swagger_client.Football3DBannerApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return

try:
    # read
    api_response = api_instance.read(brand)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling Football3DBannerApi->read: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 

### Return type

[**list[Football3DBanner2]**](Football3DBanner2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_image**
> remove_image(id)

removeImage

Remove image from Football3DBanner

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
api_instance = swagger_client.Football3DBannerApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # removeImage
    api_instance.remove_image(id)
except ApiException as e:
    print("Exception when calling Football3DBannerApi->remove_image: %s\n" % e)
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

# **save15**
> Football3DBanner2 save15(body)

save

Add a new Football3DBanner

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
api_instance = swagger_client.Football3DBannerApi(swagger_client.ApiClient(configuration))
body = swagger_client.Football3DBanner2() # Football3DBanner2 | Football3DBanner object that needs to be added to the storage

try:
    # save
    api_response = api_instance.save15(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling Football3DBannerApi->save15: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Football3DBanner2**](Football3DBanner2.md)| Football3DBanner object that needs to be added to the storage | 

### Return type

[**Football3DBanner2**](Football3DBanner2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update14**
> Football3DBanner2 update14(body, id)

update

Update an existing Football3DBanner

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
api_instance = swagger_client.Football3DBannerApi(swagger_client.ApiClient(configuration))
body = swagger_client.Football3DBanner2() # Football3DBanner2 | Football3DBanner object that needs to be updated in the storage
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.update14(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling Football3DBannerApi->update14: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Football3DBanner2**](Football3DBanner2.md)| Football3DBanner object that needs to be updated in the storage | 
 **id** | **str**| id of resource | 

### Return type

[**Football3DBanner2**](Football3DBanner2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_image**
> Football3DBanner2 upload_image(id, file=file)

uploadImage

Upload new image for Football3DBanner

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
api_instance = swagger_client.Football3DBannerApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource
file = 'file_example' # str |  (optional)

try:
    # uploadImage
    api_response = api_instance.upload_image(id, file=file)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling Football3DBannerApi->upload_image: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 
 **file** | **str**|  | [optional] 

### Return type

[**Football3DBanner2**](Football3DBanner2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

