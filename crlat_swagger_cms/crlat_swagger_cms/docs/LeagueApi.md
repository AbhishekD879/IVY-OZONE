# swagger_client.LeagueApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**find_all22**](LeagueApi.md#find_all22) | **GET** /league | findAll
[**find_one21**](LeagueApi.md#find_one21) | **GET** /league/{id} | findOne
[**league_by_id**](LeagueApi.md#league_by_id) | **DELETE** /league/{id} | LeagueById
[**order**](LeagueApi.md#order) | **POST** /league/ordering | order
[**read**](LeagueApi.md#read) | **GET** /league/brand/{brand} | read
[**save22**](LeagueApi.md#save22) | **POST** /league | save
[**update21**](LeagueApi.md#update21) | **PUT** /league/{id} | update

# **find_all22**
> list[League] find_all22()

findAll

Retrieve all Leagues

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
api_instance = swagger_client.LeagueApi(swagger_client.ApiClient(configuration))

try:
    # findAll
    api_response = api_instance.find_all22()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LeagueApi->find_all22: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[League]**](League.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one21**
> League2 find_one21(id)

findOne

Searches League by id

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
api_instance = swagger_client.LeagueApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.find_one21(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LeagueApi->find_one21: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**League2**](League2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **league_by_id**
> league_by_id(id)

LeagueById

Delete a League

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
api_instance = swagger_client.LeagueApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # LeagueById
    api_instance.league_by_id(id)
except ApiException as e:
    print("Exception when calling LeagueApi->league_by_id: %s\n" % e)
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

Set order for all League

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
api_instance = swagger_client.LeagueApi(swagger_client.ApiClient(configuration))
body = swagger_client.Ordering2() # Ordering2 | List of ordered ids of League

try:
    # order
    api_instance.order(body)
except ApiException as e:
    print("Exception when calling LeagueApi->order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Ordering2**](Ordering2.md)| List of ordered ids of League | 

### Return type

void (empty response body)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read**
> list[League2] read(brand)

read

Searches League by brand and sort it by sortOrder field in Asc order

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
api_instance = swagger_client.LeagueApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return

try:
    # read
    api_response = api_instance.read(brand)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LeagueApi->read: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 

### Return type

[**list[League2]**](League2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save22**
> League2 save22(body)

save

Add a new League

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
api_instance = swagger_client.LeagueApi(swagger_client.ApiClient(configuration))
body = swagger_client.League2() # League2 | League object that needs to be added to the storage

try:
    # save
    api_response = api_instance.save22(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LeagueApi->save22: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**League2**](League2.md)| League object that needs to be added to the storage | 

### Return type

[**League2**](League2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update21**
> League2 update21(body, id)

update

Update an existing League

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
api_instance = swagger_client.LeagueApi(swagger_client.ApiClient(configuration))
body = swagger_client.League2() # League2 | League object that needs to be updated in the storage
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.update21(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LeagueApi->update21: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**League2**](League2.md)| League object that needs to be updated in the storage | 
 **id** | **str**| id of resource | 

### Return type

[**League2**](League2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

