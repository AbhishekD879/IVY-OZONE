# swagger_client.NavigationPointApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**find_all_navigation_point**](NavigationPointApi.md#find_all_navigation_point) | **GET** /navigation-points | findAll
[**find_one_navigation_point**](NavigationPointApi.md#find_one_navigation_point) | **GET** /navigation-points/{id} | findOne
[**navigation_point_by_id**](NavigationPointApi.md#navigation_point_by_id) | **DELETE** /navigation-points/{id} | NavigationPointById
[**read_navigation_point**](NavigationPointApi.md#read_navigation_point) | **GET** /navigation-points/brand/{brand} | read
[**save_navigation_point**](NavigationPointApi.md#save_navigation_point) | **POST** /navigation-points | save
[**update_navigation_point**](NavigationPointApi.md#update_navigation_point) | **PUT** /navigation-points/{id} | update

# **find_all_navigation_point**
> list[NavigationPoint] find_all_navigation_point()

findAll

Retrieve all NavigationPoints

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
api_instance = swagger_client.NavigationPointApi(swagger_client.ApiClient(configuration))

try:
    # findAll
    api_response = api_instance.find_all_navigation_point()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NavigationPointApi->find_all_navigation_point: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[NavigationPoint]**](NavigationPoint.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one_navigation_point**
> NavigationPoint2 find_one_navigation_point(id)

findOne

Searches NavigationPoint by id

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
api_instance = swagger_client.NavigationPointApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.find_one_navigation_point(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NavigationPointApi->find_one_navigation_point: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**NavigationPoint2**](NavigationPoint2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **navigation_point_by_id**
> navigation_point_by_id(id)

NavigationPointById

Delete a NavigationPoint

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
api_instance = swagger_client.NavigationPointApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # NavigationPointById
    api_instance.navigation_point_by_id(id)
except ApiException as e:
    print("Exception when calling NavigationPointApi->navigation_point_by_id: %s\n" % e)
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

# **read_navigation_point**
> list[NavigationPoint2] read_navigation_point(brand)

read

Searches NavigationPoint by brand

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
api_instance = swagger_client.NavigationPointApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return

try:
    # read
    api_response = api_instance.read_navigation_point(brand)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NavigationPointApi->read_navigation_point: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 

### Return type

[**list[NavigationPoint2]**](NavigationPoint2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save_navigation_point**
> NavigationPoint2 save_navigation_point(body)

save

Add a new NavigationPoint

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
api_instance = swagger_client.NavigationPointApi(swagger_client.ApiClient(configuration))
body = swagger_client.NavigationPoint2() # NavigationPoint2 | NavigationPoint object that needs to be added to the storage

try:
    # save
    api_response = api_instance.save_navigation_point(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NavigationPointApi->save_navigation_point: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**NavigationPoint2**](NavigationPoint2.md)| NavigationPoint object that needs to be added to the storage | 

### Return type

[**NavigationPoint2**](NavigationPoint2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_navigation_point**
> NavigationPoint2 update_navigation_point(body, id)

update

Update an existing NavigationPoint

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
api_instance = swagger_client.NavigationPointApi(swagger_client.ApiClient(configuration))
body = swagger_client.NavigationPoint2() # NavigationPoint2 | NavigationPoint object that needs to be updated in the storage
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.update_navigation_point(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NavigationPointApi->update_navigation_point: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**NavigationPoint2**](NavigationPoint2.md)| NavigationPoint object that needs to be updated in the storage | 
 **id** | **str**| id of resource | 

### Return type

[**NavigationPoint2**](NavigationPoint2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

