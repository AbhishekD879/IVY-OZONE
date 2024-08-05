# swagger_client.SportCategoryApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**find_all34**](SportCategoryApi.md#find_all34) | **GET** /sport-category | findAll
[**find_one33**](SportCategoryApi.md#find_one33) | **GET** /sport-category/{id} | findOne
[**order**](SportCategoryApi.md#order) | **POST** /sport-category/ordering | order
[**read**](SportCategoryApi.md#read) | **GET** /sport-category/brand/{brand} | read
[**remove_image_sport_category**](SportCategoryApi.md#remove_image_sport_category) | **DELETE** /sport-category/{id}/image | removeImage
[**save34**](SportCategoryApi.md#save34) | **POST** /sport-category | save
[**sport_category_by_id**](SportCategoryApi.md#sport_category_by_id) | **DELETE** /sport-category/{id} | SportCategoryById
[**update33**](SportCategoryApi.md#update33) | **PUT** /sport-category/{id} | update
[**upload_image_sport_category**](SportCategoryApi.md#upload_image_sport_category) | **POST** /sport-category/{id}/image | uploadImage

# **find_all34**
> list[SportCategory] find_all34()

findAll

Retrieve all SportCategorys

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
api_instance = swagger_client.SportCategoryApi(swagger_client.ApiClient(configuration))

try:
    # findAll
    api_response = api_instance.find_all34()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SportCategoryApi->find_all34: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[SportCategory]**](SportCategory.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one33**
> SportCategory2 find_one33(id)

findOne

Searches SportCategory by id

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
api_instance = swagger_client.SportCategoryApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.find_one33(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SportCategoryApi->find_one33: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**SportCategory2**](SportCategory2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **order**
> order(body)

order

Set order for all SportCategory

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
api_instance = swagger_client.SportCategoryApi(swagger_client.ApiClient(configuration))
body = swagger_client.Ordering2() # Ordering2 | List of ordered ids of SportCategory

try:
    # order
    api_instance.order(body)
except ApiException as e:
    print("Exception when calling SportCategoryApi->order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Ordering2**](Ordering2.md)| List of ordered ids of SportCategory | 

### Return type

void (empty response body)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read**
> list[SportCategory2] read(brand)

read

Searches SportCategory by brand and sort it by sortOrder field in Asc order

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
api_instance = swagger_client.SportCategoryApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return

try:
    # read
    api_response = api_instance.read(brand)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SportCategoryApi->read: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 

### Return type

[**list[SportCategory2]**](SportCategory2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_image_sport_category**
> remove_image_sport_category(id, file_type=file_type)

removeImage

Remove image from sportCategory

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
api_instance = swagger_client.SportCategoryApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource
file_type = ['file_type_example'] # list[str] | type of file to delete (optional)

try:
    # removeImage
    api_instance.remove_image_sport_category(id, file_type=file_type)
except ApiException as e:
    print("Exception when calling SportCategoryApi->remove_image_sport_category: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 
 **file_type** | [**list[str]**](str.md)| type of file to delete | [optional] 

### Return type

void (empty response body)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save34**
> SportCategory2 save34(body)

save

Add a new SportCategory

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
api_instance = swagger_client.SportCategoryApi(swagger_client.ApiClient(configuration))
body = swagger_client.SportCategory2() # SportCategory2 | SportCategory object that needs to be added to the storage

try:
    # save
    api_response = api_instance.save34(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SportCategoryApi->save34: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SportCategory2**](SportCategory2.md)| SportCategory object that needs to be added to the storage | 

### Return type

[**SportCategory2**](SportCategory2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **sport_category_by_id**
> sport_category_by_id(id)

SportCategoryById

Delete a SportCategory

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
api_instance = swagger_client.SportCategoryApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # SportCategoryById
    api_instance.sport_category_by_id(id)
except ApiException as e:
    print("Exception when calling SportCategoryApi->sport_category_by_id: %s\n" % e)
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

# **update33**
> SportCategory2 update33(body, id)

update

Update an existing SportCategory

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
api_instance = swagger_client.SportCategoryApi(swagger_client.ApiClient(configuration))
body = swagger_client.SportCategory2() # SportCategory2 | SportCategory object that needs to be updated in the storage
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.update33(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SportCategoryApi->update33: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SportCategory2**](SportCategory2.md)| SportCategory object that needs to be updated in the storage | 
 **id** | **str**| id of resource | 

### Return type

[**SportCategory2**](SportCategory2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_image_sport_category**
> SportCategory2 upload_image_sport_category(id, file=file, file_type=file_type)

uploadImage

Upload new image for SportCategory

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
api_instance = swagger_client.SportCategoryApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource
file = 'file_example' # str |  (optional)
file_type = ['file_type_example'] # list[str] | type of file to delete (optional)

try:
    # uploadImage
    api_response = api_instance.upload_image_sport_category(id, file=file, file_type=file_type)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SportCategoryApi->upload_image_sport_category: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 
 **file** | **str**|  | [optional] 
 **file_type** | [**list[str]**](str.md)| type of file to delete | [optional] 

### Return type

[**SportCategory2**](SportCategory2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

