# swagger_client.FeaturedEventsTypeApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**featured_events_type_by_id**](FeaturedEventsTypeApi.md#featured_events_type_by_id) | **DELETE** /featured-events-type/{id} | FeaturedEventsTypeById
[**find_all13**](FeaturedEventsTypeApi.md#find_all13) | **GET** /featured-events-type | findAll
[**find_one12**](FeaturedEventsTypeApi.md#find_one12) | **GET** /featured-events-type/{id} | findOne
[**read**](FeaturedEventsTypeApi.md#read) | **GET** /featured-events-type/brand/{brand} | read
[**save13**](FeaturedEventsTypeApi.md#save13) | **POST** /featured-events-type | save
[**update12**](FeaturedEventsTypeApi.md#update12) | **PUT** /featured-events-type/{id} | update

# **featured_events_type_by_id**
> featured_events_type_by_id(id)

FeaturedEventsTypeById

Delete a FeaturedEventsType

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
api_instance = swagger_client.FeaturedEventsTypeApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # FeaturedEventsTypeById
    api_instance.featured_events_type_by_id(id)
except ApiException as e:
    print("Exception when calling FeaturedEventsTypeApi->featured_events_type_by_id: %s\n" % e)
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

# **find_all13**
> list[FeaturedEventsType] find_all13()

findAll

Retrieve all FeaturedEventsTypes

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
api_instance = swagger_client.FeaturedEventsTypeApi(swagger_client.ApiClient(configuration))

try:
    # findAll
    api_response = api_instance.find_all13()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FeaturedEventsTypeApi->find_all13: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[FeaturedEventsType]**](FeaturedEventsType.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one12**
> FeaturedEventsType2 find_one12(id)

findOne

Searches FeaturedEventsType by id

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
api_instance = swagger_client.FeaturedEventsTypeApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.find_one12(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FeaturedEventsTypeApi->find_one12: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**FeaturedEventsType2**](FeaturedEventsType2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read**
> list[FeaturedEventsType2] read(brand)

read

Searches FeaturedEventsType by brand and sort it by sortOrder field in Asc order

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
api_instance = swagger_client.FeaturedEventsTypeApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return

try:
    # read
    api_response = api_instance.read(brand)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FeaturedEventsTypeApi->read: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 

### Return type

[**list[FeaturedEventsType2]**](FeaturedEventsType2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save13**
> FeaturedEventsType2 save13(body)

save

Add a new FeaturedEventsType

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
api_instance = swagger_client.FeaturedEventsTypeApi(swagger_client.ApiClient(configuration))
body = swagger_client.FeaturedEventsType2() # FeaturedEventsType2 | FeaturedEventsType object that needs to be added to the storage

try:
    # save
    api_response = api_instance.save13(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FeaturedEventsTypeApi->save13: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FeaturedEventsType2**](FeaturedEventsType2.md)| FeaturedEventsType object that needs to be added to the storage | 

### Return type

[**FeaturedEventsType2**](FeaturedEventsType2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update12**
> FeaturedEventsType2 update12(body, id)

update

Update an existing FeaturedEventsType

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
api_instance = swagger_client.FeaturedEventsTypeApi(swagger_client.ApiClient(configuration))
body = swagger_client.FeaturedEventsType2() # FeaturedEventsType2 | FeaturedEventsType object that needs to be updated in the storage
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.update12(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FeaturedEventsTypeApi->update12: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FeaturedEventsType2**](FeaturedEventsType2.md)| FeaturedEventsType object that needs to be updated in the storage | 
 **id** | **str**| id of resource | 

### Return type

[**FeaturedEventsType2**](FeaturedEventsType2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

