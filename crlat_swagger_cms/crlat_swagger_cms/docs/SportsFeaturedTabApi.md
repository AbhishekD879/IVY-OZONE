# swagger_client.SportsFeaturedTabApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_one**](SportsFeaturedTabApi.md#delete_one) | **DELETE** /sports-featured-tab/{id} | deleteOne
[**deletefea**](SportsFeaturedTabApi.md#deletefea) | **DELETE** /sports-featured-tab/{id}/module/{moduleId} | deletefea
[**find_all11**](SportsFeaturedTabApi.md#find_all11) | **GET** /sports-featured-tab | findAll
[**find_all12**](SportsFeaturedTabApi.md#find_all12) | **GET** /sports-featured-tab/{id}/module | findAll
[**find_one10**](SportsFeaturedTabApi.md#find_one10) | **GET** /sports-featured-tab/{id} | findOne
[**find_one11**](SportsFeaturedTabApi.md#find_one11) | **GET** /sports-featured-tab/{id}/module/{moduleId} | findOne
[**save11**](SportsFeaturedTabApi.md#save11) | **POST** /sports-featured-tab | save
[**save12**](SportsFeaturedTabApi.md#save12) | **POST** /sports-featured-tab/{id}/module | save
[**update10**](SportsFeaturedTabApi.md#update10) | **PUT** /sports-featured-tab/{id} | update
[**update11**](SportsFeaturedTabApi.md#update11) | **PUT** /sports-featured-tab/{id}/module/{moduleId} | update

# **delete_one**
> delete_one(id)

deleteOne

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
api_instance = swagger_client.SportsFeaturedTabApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # deleteOne
    api_instance.delete_one(id)
except ApiException as e:
    print("Exception when calling SportsFeaturedTabApi->delete_one: %s\n" % e)
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

# **deletefea**
> deletefea(id, module_id)

deletefea

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
api_instance = swagger_client.SportsFeaturedTabApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource
module_id = 'module_id_example' # str | 

try:
    # deletefea
    api_instance.deletefea(id, module_id)
except ApiException as e:
    print("Exception when calling SportsFeaturedTabApi->deletefea: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 
 **module_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_all11**
> list[SportsFeaturedTab] find_all11()

findAll

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
api_instance = swagger_client.SportsFeaturedTabApi(swagger_client.ApiClient(configuration))

try:
    # findAll
    api_response = api_instance.find_all11()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SportsFeaturedTabApi->find_all11: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[SportsFeaturedTab]**](SportsFeaturedTab.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_all12**
> list[SimpleModule] find_all12(id)

findAll

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
api_instance = swagger_client.SportsFeaturedTabApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findAll
    api_response = api_instance.find_all12(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SportsFeaturedTabApi->find_all12: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**list[SimpleModule]**](SimpleModule.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one10**
> SportsFeaturedTab2 find_one10(id)

findOne

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
api_instance = swagger_client.SportsFeaturedTabApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.find_one10(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SportsFeaturedTabApi->find_one10: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**SportsFeaturedTab2**](SportsFeaturedTab2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one11**
> SimpleModule2 find_one11(id, module_id)

findOne

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
api_instance = swagger_client.SportsFeaturedTabApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource
module_id = 'module_id_example' # str | 

try:
    # findOne
    api_response = api_instance.find_one11(id, module_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SportsFeaturedTabApi->find_one11: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 
 **module_id** | **str**|  | 

### Return type

[**SimpleModule2**](SimpleModule2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save11**
> SportsFeaturedTab2 save11(body)

save

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
api_instance = swagger_client.SportsFeaturedTabApi(swagger_client.ApiClient(configuration))
body = swagger_client.SportsFeaturedTab2() # SportsFeaturedTab2 | 

try:
    # save
    api_response = api_instance.save11(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SportsFeaturedTabApi->save11: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SportsFeaturedTab2**](SportsFeaturedTab2.md)|  | 

### Return type

[**SportsFeaturedTab2**](SportsFeaturedTab2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save12**
> SimpleModule2 save12(id, body=body)

save

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
api_instance = swagger_client.SportsFeaturedTabApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource
body = swagger_client.SimpleModule2() # SimpleModule2 |  (optional)

try:
    # save
    api_response = api_instance.save12(id, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SportsFeaturedTabApi->save12: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 
 **body** | [**SimpleModule2**](SimpleModule2.md)|  | [optional] 

### Return type

[**SimpleModule2**](SimpleModule2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update10**
> SportsFeaturedTab2 update10(body, id)

update

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
api_instance = swagger_client.SportsFeaturedTabApi(swagger_client.ApiClient(configuration))
body = swagger_client.SportsFeaturedTab2() # SportsFeaturedTab2 | 
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.update10(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SportsFeaturedTabApi->update10: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SportsFeaturedTab2**](SportsFeaturedTab2.md)|  | 
 **id** | **str**| id of resource | 

### Return type

[**SportsFeaturedTab2**](SportsFeaturedTab2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update11**
> SimpleModule2 update11(id, module_id, body=body)

update

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
api_instance = swagger_client.SportsFeaturedTabApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource
module_id = 'module_id_example' # str | 
body = swagger_client.SimpleModule2() # SimpleModule2 |  (optional)

try:
    # update
    api_response = api_instance.update11(id, module_id, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SportsFeaturedTabApi->update11: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 
 **module_id** | **str**|  | 
 **body** | [**SimpleModule2**](SimpleModule2.md)|  | [optional] 

### Return type

[**SimpleModule2**](SimpleModule2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

