# swagger_client.AppUpdateApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**app_update_by_id**](AppUpdateApi.md#app_update_by_id) | **DELETE** /app-update/{id} | AppUpdateById
[**find_all1**](AppUpdateApi.md#find_all1) | **GET** /app-update | findAll
[**find_one1**](AppUpdateApi.md#find_one1) | **GET** /app-update/{id} | findOne
[**save1**](AppUpdateApi.md#save1) | **POST** /app-update | save
[**update1**](AppUpdateApi.md#update1) | **PUT** /app-update/{id} | update

# **app_update_by_id**
> app_update_by_id(id)

AppUpdateById

Delete a AppUpdate

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
api_instance = swagger_client.AppUpdateApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # AppUpdateById
    api_instance.app_update_by_id(id)
except ApiException as e:
    print("Exception when calling AppUpdateApi->app_update_by_id: %s\n" % e)
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

# **find_all1**
> list[AppUpdate] find_all1()

findAll

Retrieve all AppUpdates

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
api_instance = swagger_client.AppUpdateApi(swagger_client.ApiClient(configuration))

try:
    # findAll
    api_response = api_instance.find_all1()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AppUpdateApi->find_all1: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[AppUpdate]**](AppUpdate.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one1**
> AppUpdate2 find_one1(id)

findOne

Searches AppUpdate by id

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
api_instance = swagger_client.AppUpdateApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.find_one1(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AppUpdateApi->find_one1: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**AppUpdate2**](AppUpdate2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save1**
> AppUpdate2 save1(body)

save

Add a new AppUpdate

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
api_instance = swagger_client.AppUpdateApi(swagger_client.ApiClient(configuration))
body = swagger_client.AppUpdate2() # AppUpdate2 | AppUpdate object that needs to be added to the storage

try:
    # save
    api_response = api_instance.save1(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AppUpdateApi->save1: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AppUpdate2**](AppUpdate2.md)| AppUpdate object that needs to be added to the storage | 

### Return type

[**AppUpdate2**](AppUpdate2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update1**
> AppUpdate2 update1(body, id)

update

Update an existing AppUpdate

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
api_instance = swagger_client.AppUpdateApi(swagger_client.ApiClient(configuration))
body = swagger_client.AppUpdate2() # AppUpdate2 | AppUpdate object that needs to be updated in the storage
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.update1(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AppUpdateApi->update1: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AppUpdate2**](AppUpdate2.md)| AppUpdate object that needs to be updated in the storage | 
 **id** | **str**| id of resource | 

### Return type

[**AppUpdate2**](AppUpdate2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

