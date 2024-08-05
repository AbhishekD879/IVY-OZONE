# swagger_client.DashboardApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**dashboard**](DashboardApi.md#dashboard) | **DELETE** /dashboard/{id} | Dashboard
[**find_all_offset_limit**](DashboardApi.md#find_all_offset_limit) | **GET** /dashboard | findAllOffsetLimit
[**find_one8**](DashboardApi.md#find_one8) | **GET** /dashboard/{id} | findOne
[**read**](DashboardApi.md#read) | **GET** /dashboard/brand/{brand} | read
[**read_0**](DashboardApi.md#read_0) | **GET** /dashboard/brand/{brand}?date&#x3D;{date} | read
[**save9**](DashboardApi.md#save9) | **POST** /dashboard | save
[**update8**](DashboardApi.md#update8) | **PUT** /dashboard/{id} | update

# **dashboard**
> dashboard(id)

Dashboard

Delete a Dashboard

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
api_instance = swagger_client.DashboardApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # Dashboard
    api_instance.dashboard(id)
except ApiException as e:
    print("Exception when calling DashboardApi->dashboard: %s\n" % e)
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

# **find_all_offset_limit**
> list[Dashboard] find_all_offset_limit(offset=offset, limit=limit)

findAllOffsetLimit

Retrieve all Dashboards with offset & limit provided

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
api_instance = swagger_client.DashboardApi(swagger_client.ApiClient(configuration))
offset = 56 # int |  (optional)
limit = 56 # int |  (optional)

try:
    # findAllOffsetLimit
    api_response = api_instance.find_all_offset_limit(offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DashboardApi->find_all_offset_limit: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **offset** | **int**|  | [optional] 
 **limit** | **int**|  | [optional] 

### Return type

[**list[Dashboard]**](Dashboard.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one8**
> Dashboard2 find_one8(id)

findOne

Searches Dashboard by id

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
api_instance = swagger_client.DashboardApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.find_one8(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DashboardApi->find_one8: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**Dashboard2**](Dashboard2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read**
> list[Dashboard2] read(brand)

read

Searches Dashboard by brand

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
api_instance = swagger_client.DashboardApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return

try:
    # read
    api_response = api_instance.read(brand)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DashboardApi->read: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 

### Return type

[**list[Dashboard2]**](Dashboard2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_0**
> list[Dashboard2] read_0(brand, _date=_date)

read

Searches Dashboard by brand and date

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
api_instance = swagger_client.DashboardApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return
_date = '2013-10-20' # date | date in format 'yyyy-MM-dd' (optional)

try:
    # read
    api_response = api_instance.read_0(brand, _date=_date)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DashboardApi->read_0: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 
 **_date** | **date**| date in format &#x27;yyyy-MM-dd&#x27; | [optional] 

### Return type

[**list[Dashboard2]**](Dashboard2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save9**
> Dashboard2 save9(body)

save

Add a new Dashboard

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
api_instance = swagger_client.DashboardApi(swagger_client.ApiClient(configuration))
body = swagger_client.Dashboard2() # Dashboard2 | Dashboard object that needs to be added to the storage

try:
    # save
    api_response = api_instance.save9(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DashboardApi->save9: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Dashboard2**](Dashboard2.md)| Dashboard object that needs to be added to the storage | 

### Return type

[**Dashboard2**](Dashboard2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update8**
> Dashboard2 update8(body, id)

update

Update an existing Dashboard

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
api_instance = swagger_client.DashboardApi(swagger_client.ApiClient(configuration))
body = swagger_client.Dashboard2() # Dashboard2 | Dashboard object that needs to be updated in the storage
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.update8(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DashboardApi->update8: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Dashboard2**](Dashboard2.md)| Dashboard object that needs to be updated in the storage | 
 **id** | **str**| id of resource | 

### Return type

[**Dashboard2**](Dashboard2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

