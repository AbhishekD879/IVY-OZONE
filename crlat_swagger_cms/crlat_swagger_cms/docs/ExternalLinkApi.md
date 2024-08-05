# swagger_client.ExternalLinkApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**external_link_by_id**](ExternalLinkApi.md#external_link_by_id) | **DELETE** /external-link/{id} | ExternalLinkById
[**external_links_by_brand**](ExternalLinkApi.md#external_links_by_brand) | **GET** /external-link/brand/{brand} | find ExternalLink by brand
[**find_all6**](ExternalLinkApi.md#find_all6) | **GET** /external-link | findAll
[**find_one6**](ExternalLinkApi.md#find_one6) | **GET** /external-link/{id} | findOne
[**save6**](ExternalLinkApi.md#save6) | **POST** /external-link | save
[**update6**](ExternalLinkApi.md#update6) | **PUT** /external-link/{id} | update

# **external_link_by_id**
> external_link_by_id(id)

ExternalLinkById

Delete a ExternalLink

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
api_instance = swagger_client.ExternalLinkApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # ExternalLinkById
    api_instance.external_link_by_id(id)
except ApiException as e:
    print("Exception when calling ExternalLinkApi->external_link_by_id: %s\n" % e)
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

# **external_links_by_brand**
> list[ExternalLink2] external_links_by_brand(brand)

find ExternalLink by brand

Searches ExternalLinks by brand

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
api_instance = swagger_client.ExternalLinkApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return

try:
    # find ExternalLink by brand
    api_response = api_instance.external_links_by_brand(brand)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExternalLinkApi->external_links_by_brand: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 

### Return type

[**list[ExternalLink2]**](ExternalLink2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_all6**
> list[ExternalLink] find_all6()

findAll

Retrieve all ExternalLinks

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
api_instance = swagger_client.ExternalLinkApi(swagger_client.ApiClient(configuration))

try:
    # findAll
    api_response = api_instance.find_all6()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExternalLinkApi->find_all6: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[ExternalLink]**](ExternalLink.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one6**
> ExternalLink2 find_one6(id)

findOne

Searches ExternalLink by id

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
api_instance = swagger_client.ExternalLinkApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.find_one6(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExternalLinkApi->find_one6: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**ExternalLink2**](ExternalLink2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save6**
> ExternalLink2 save6(body)

save

Add a new ExternalLink

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
api_instance = swagger_client.ExternalLinkApi(swagger_client.ApiClient(configuration))
body = swagger_client.ExternalLink2() # ExternalLink2 | ExternalLink object that needs to be added to the storage

try:
    # save
    api_response = api_instance.save6(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExternalLinkApi->save6: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ExternalLink2**](ExternalLink2.md)| ExternalLink object that needs to be added to the storage | 

### Return type

[**ExternalLink2**](ExternalLink2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update6**
> ExternalLink2 update6(body, id)

update

Update an existing ExternalLink

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
api_instance = swagger_client.ExternalLinkApi(swagger_client.ApiClient(configuration))
body = swagger_client.ExternalLink2() # ExternalLink2 | ExternalLink object that needs to be updated in the storage
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.update6(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExternalLinkApi->update6: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ExternalLink2**](ExternalLink2.md)| ExternalLink object that needs to be updated in the storage | 
 **id** | **str**| id of resource | 

### Return type

[**ExternalLink2**](ExternalLink2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

