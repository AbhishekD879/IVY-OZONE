# swagger_client.SportOlympicSportsApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_files_for_olympic_sport**](SportOlympicSportsApi.md#delete_files_for_olympic_sport) | **DELETE** /sports/{id}/files | deleteFile(s)
[**find_all35**](SportOlympicSportsApi.md#find_all35) | **GET** /sports | findAll
[**find_one34**](SportOlympicSportsApi.md#find_one34) | **GET** /sports/{id} | findOne
[**order**](SportOlympicSportsApi.md#order) | **POST** /sports/ordering | order
[**read**](SportOlympicSportsApi.md#read) | **GET** /sports/brand/{brand} | read
[**save35**](SportOlympicSportsApi.md#save35) | **POST** /sports | save
[**sport_by_id**](SportOlympicSportsApi.md#sport_by_id) | **DELETE** /sports/{id} | SportById
[**update34**](SportOlympicSportsApi.md#update34) | **PUT** /sports/{id} | update
[**upload_files_for_olympic_sports**](SportOlympicSportsApi.md#upload_files_for_olympic_sports) | **POST** /sports/{id}/files | uploadFiles

# **delete_files_for_olympic_sport**
> delete_files_for_olympic_sport(id, file_type)

deleteFile(s)

Delete file(s)

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
api_instance = swagger_client.SportOlympicSportsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource
file_type = ['file_type_example'] # list[str] | one or more type of file(s) to delete

try:
    # deleteFile(s)
    api_instance.delete_files_for_olympic_sport(id, file_type)
except ApiException as e:
    print("Exception when calling SportOlympicSportsApi->delete_files_for_olympic_sport: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 
 **file_type** | [**list[str]**](str.md)| one or more type of file(s) to delete | 

### Return type

void (empty response body)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_all35**
> list[Sport] find_all35(brand, name=name)

findAll

Retrieve all Sports

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
api_instance = swagger_client.SportOlympicSportsApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return
name = 'name_example' # str | sport name (optional)

try:
    # findAll
    api_response = api_instance.find_all35(brand, name=name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SportOlympicSportsApi->find_all35: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 
 **name** | **str**| sport name | [optional] 

### Return type

[**list[Sport]**](Sport.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one34**
> Sport2 find_one34(id)

findOne

Searches Sport by id

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
api_instance = swagger_client.SportOlympicSportsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.find_one34(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SportOlympicSportsApi->find_one34: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**Sport2**](Sport2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **order**
> order(body)

order

Set order for Sports

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
api_instance = swagger_client.SportOlympicSportsApi(swagger_client.ApiClient(configuration))
body = swagger_client.Ordering2() # Ordering2 | List of ordered ids of Sports

try:
    # order
    api_instance.order(body)
except ApiException as e:
    print("Exception when calling SportOlympicSportsApi->order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Ordering2**](Ordering2.md)| List of ordered ids of Sports | 

### Return type

void (empty response body)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read**
> list[Sport2] read(brand)

read

Searches Sport by brand and sort it by sortOrder field in Asc order

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
api_instance = swagger_client.SportOlympicSportsApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return

try:
    # read
    api_response = api_instance.read(brand)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SportOlympicSportsApi->read: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 

### Return type

[**list[Sport2]**](Sport2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save35**
> Sport2 save35(body)

save

Add a new Sport

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
api_instance = swagger_client.SportOlympicSportsApi(swagger_client.ApiClient(configuration))
body = swagger_client.Sport2() # Sport2 | Sport object that needs to be added to the storage

try:
    # save
    api_response = api_instance.save35(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SportOlympicSportsApi->save35: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Sport2**](Sport2.md)| Sport object that needs to be added to the storage | 

### Return type

[**Sport2**](Sport2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **sport_by_id**
> sport_by_id(id)

SportById

Delete a Sport

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
api_instance = swagger_client.SportOlympicSportsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # SportById
    api_instance.sport_by_id(id)
except ApiException as e:
    print("Exception when calling SportOlympicSportsApi->sport_by_id: %s\n" % e)
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

# **update34**
> Sport2 update34(body, id)

update

Update an existing Sport

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
api_instance = swagger_client.SportOlympicSportsApi(swagger_client.ApiClient(configuration))
body = swagger_client.Sport2() # Sport2 | Sport object that needs to be updated in the storage
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.update34(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SportOlympicSportsApi->update34: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Sport2**](Sport2.md)| Sport object that needs to be updated in the storage | 
 **id** | **str**| id of resource | 

### Return type

[**Sport2**](Sport2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_files_for_olympic_sports**
> Promotion2 upload_files_for_olympic_sports(id, image_file=image_file, icon=icon, svg_icon=svg_icon)

uploadFiles

Upload files

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
api_instance = swagger_client.SportOlympicSportsApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource
image_file = 'image_file_example' # str |  (optional)
icon = 'icon_example' # str |  (optional)
svg_icon = 'svg_icon_example' # str |  (optional)

try:
    # uploadFiles
    api_response = api_instance.upload_files_for_olympic_sports(id, image_file=image_file, icon=icon, svg_icon=svg_icon)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SportOlympicSportsApi->upload_files_for_olympic_sports: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 
 **image_file** | **str**|  | [optional] 
 **icon** | **str**|  | [optional] 
 **svg_icon** | **str**|  | [optional] 

### Return type

[**Promotion2**](Promotion2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

