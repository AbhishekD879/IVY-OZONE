# swagger_client.SportQuickLinkApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**find_one23**](SportQuickLinkApi.md#find_one23) | **GET** /sport-quick-link/{id} | findOne
[**save24**](SportQuickLinkApi.md#save24) | **POST** /sport-quick-link | save
[**sport_quick_link_by_id**](SportQuickLinkApi.md#sport_quick_link_by_id) | **DELETE** /sport-quick-link/{id} | Delete
[**sport_quick_link_find_all24**](SportQuickLinkApi.md#sport_quick_link_find_all24) | **GET** /sport-quick-link | findAll
[**sport_quick_link_read_by_brand_and_sport**](SportQuickLinkApi.md#sport_quick_link_read_by_brand_and_sport) | **GET** /sport-quick-link/brand/{brand} | findAll
[**sport_quick_link_read_by_brand_and_sport_0**](SportQuickLinkApi.md#sport_quick_link_read_by_brand_and_sport_0) | **GET** /sport-quick-link/brand/{brand}/{pageType}/{pageId} | findAll
[**update23**](SportQuickLinkApi.md#update23) | **PUT** /sport-quick-link/{id} | update

# **find_one23**
> SportQuickLink2 find_one23(id)

findOne

Searches SportQuickLink by id

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
api_instance = swagger_client.SportQuickLinkApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.find_one23(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SportQuickLinkApi->find_one23: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**SportQuickLink2**](SportQuickLink2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save24**
> SportQuickLink2 save24(body)

save

Add a new SportQuickLink

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
api_instance = swagger_client.SportQuickLinkApi(swagger_client.ApiClient(configuration))
body = swagger_client.SportQuickLink2() # SportQuickLink2 | SportQuickLink object that needs to be added to the storage

try:
    # save
    api_response = api_instance.save24(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SportQuickLinkApi->save24: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SportQuickLink2**](SportQuickLink2.md)| SportQuickLink object that needs to be added to the storage | 

### Return type

[**SportQuickLink2**](SportQuickLink2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **sport_quick_link_by_id**
> sport_quick_link_by_id(id)

Delete

Delete a SportQuickLink

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
api_instance = swagger_client.SportQuickLinkApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # Delete
    api_instance.sport_quick_link_by_id(id)
except ApiException as e:
    print("Exception when calling SportQuickLinkApi->sport_quick_link_by_id: %s\n" % e)
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

# **sport_quick_link_find_all24**
> list[SportQuickLink] sport_quick_link_find_all24()

findAll

Retrieve all SportQuickLinks

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
api_instance = swagger_client.SportQuickLinkApi(swagger_client.ApiClient(configuration))

try:
    # findAll
    api_response = api_instance.sport_quick_link_find_all24()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SportQuickLinkApi->sport_quick_link_find_all24: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[SportQuickLink]**](SportQuickLink.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **sport_quick_link_read_by_brand_and_sport**
> list[SportQuickLink2] sport_quick_link_read_by_brand_and_sport(brand)

findAll

Searches SportQuickLink by brand and sportId and sort it by sortOrder field in Asc order

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
api_instance = swagger_client.SportQuickLinkApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return

try:
    # findAll
    api_response = api_instance.sport_quick_link_read_by_brand_and_sport(brand)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SportQuickLinkApi->sport_quick_link_read_by_brand_and_sport: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 

### Return type

[**list[SportQuickLink2]**](SportQuickLink2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **sport_quick_link_read_by_brand_and_sport_0**
> list[SportQuickLink2] sport_quick_link_read_by_brand_and_sport_0(brand, page_type, page_id)

findAll

Searches SportQuickLink by brand and sort it by sortOrder field in Asc order

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
api_instance = swagger_client.SportQuickLinkApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return
page_type = 'page_type_example' # str | name of pageType
page_id = 1.2 # float | pageId to filter objects

try:
    # findAll
    api_response = api_instance.sport_quick_link_read_by_brand_and_sport_0(brand, page_type, page_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SportQuickLinkApi->sport_quick_link_read_by_brand_and_sport_0: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 
 **page_type** | **str**| name of pageType | 
 **page_id** | **float**| pageId to filter objects | 

### Return type

[**list[SportQuickLink2]**](SportQuickLink2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update23**
> SportQuickLink2 update23(body, id)

update

Update an existing SportQuickLink

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
api_instance = swagger_client.SportQuickLinkApi(swagger_client.ApiClient(configuration))
body = swagger_client.SportQuickLink2() # SportQuickLink2 | SportQuickLink object that needs to be updated in the storage
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.update23(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SportQuickLinkApi->update23: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SportQuickLink2**](SportQuickLink2.md)| SportQuickLink object that needs to be updated in the storage | 
 **id** | **str**| id of resource | 

### Return type

[**SportQuickLink2**](SportQuickLink2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

