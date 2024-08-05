# swagger_client.ConfigurationApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**configuration_brand_by_brand**](ConfigurationApi.md#configuration_brand_by_brand) | **DELETE** /configuration/brand/{brand} | ConfigurationBrandByBrand
[**configuration_brand_element_by_brand**](ConfigurationApi.md#configuration_brand_element_by_brand) | **DELETE** /configuration/brand/{brand}/element/{elementId} | ConfigurationBrandElementByBrand
[**create_element**](ConfigurationApi.md#create_element) | **POST** /configuration/brand/{brand}/element | createElement
[**find_all6**](ConfigurationApi.md#find_all6) | **GET** /configuration | findAll
[**find_by_brand**](ConfigurationApi.md#find_by_brand) | **GET** /configuration/brand/{brand} | findByBrand
[**save6**](ConfigurationApi.md#save6) | **POST** /configuration | save
[**update_element**](ConfigurationApi.md#update_element) | **PUT** /configuration/brand/{brand}/element/{elementId} | updateElement

# **configuration_brand_by_brand**
> configuration_brand_by_brand(brand)

ConfigurationBrandByBrand

Delete a Configuration for brand

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
api_instance = swagger_client.ConfigurationApi(swagger_client.ApiClient(configuration))
brand = swagger_client.Brand792() # Brand792 | 

try:
    # ConfigurationBrandByBrand
    api_instance.configuration_brand_by_brand(brand)
except ApiException as e:
    print("Exception when calling ConfigurationApi->configuration_brand_by_brand: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | [**Brand792**](.md)|  | 

### Return type

void (empty response body)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **configuration_brand_element_by_brand**
> configuration_brand_element_by_brand(brand, element_id)

ConfigurationBrandElementByBrand

Delete an element for Configuration

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
api_instance = swagger_client.ConfigurationApi(swagger_client.ApiClient(configuration))
brand = swagger_client.Brand792() # Brand792 | 
element_id = 'element_id_example' # str | 

try:
    # ConfigurationBrandElementByBrand
    api_instance.configuration_brand_element_by_brand(brand, element_id)
except ApiException as e:
    print("Exception when calling ConfigurationApi->configuration_brand_element_by_brand: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | [**Brand792**](.md)|  | 
 **element_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_element**
> ConfigurationItem2 create_element(body, brand)

createElement

Add an element to Configuration

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
api_instance = swagger_client.ConfigurationApi(swagger_client.ApiClient(configuration))
body = swagger_client.ConfigurationItem() # ConfigurationItem | Element object that needs to be added to Configuration entity
brand = swagger_client.Brand792() # Brand792 | 

try:
    # createElement
    api_response = api_instance.create_element(body, brand)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConfigurationApi->create_element: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConfigurationItem**](ConfigurationItem.md)| Element object that needs to be added to Configuration entity | 
 **brand** | [**Brand792**](.md)|  | 

### Return type

[**ConfigurationItem2**](ConfigurationItem2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_all6**
> list[Configuration] find_all6()

findAll

Retrieve all Configurations

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
api_instance = swagger_client.ConfigurationApi(swagger_client.ApiClient(configuration))

try:
    # findAll
    api_response = api_instance.find_all6()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConfigurationApi->find_all6: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Configuration]**](Configuration.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_by_brand**
> Configuration2 find_by_brand(brand)

findByBrand

Searches Configuration by brand name

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
api_instance = swagger_client.ConfigurationApi(swagger_client.ApiClient(configuration))
brand = swagger_client.Brand79() # Brand79 | 

try:
    # findByBrand
    api_response = api_instance.find_by_brand(brand)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConfigurationApi->find_by_brand: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | [**Brand79**](.md)|  | 

### Return type

[**Configuration2**](Configuration2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save6**
> Configuration2 save6(body)

save

Add a new Configuration

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
api_instance = swagger_client.ConfigurationApi(swagger_client.ApiClient(configuration))
body = swagger_client.Configuration2() # Configuration2 | Configuration object that needs to be added to the storage

try:
    # save
    api_response = api_instance.save6(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConfigurationApi->save6: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Configuration2**](Configuration2.md)| Configuration object that needs to be added to the storage | 

### Return type

[**Configuration2**](Configuration2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_element**
> ConfigurationItem2 update_element(body, brand, element_id)

updateElement

Update an existing element for Configuration

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
api_instance = swagger_client.ConfigurationApi(swagger_client.ApiClient(configuration))
body = swagger_client.ConfigurationItem2() # ConfigurationItem2 | Element object that needs to be updated in Configuration entity
brand = swagger_client.Brand792() # Brand792 | 
element_id = 'element_id_example' # str | 

try:
    # updateElement
    api_response = api_instance.update_element(body, brand, element_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConfigurationApi->update_element: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConfigurationItem2**](ConfigurationItem2.md)| Element object that needs to be updated in Configuration entity | 
 **brand** | [**Brand792**](.md)|  | 
 **element_id** | **str**|  | 

### Return type

[**ConfigurationItem2**](ConfigurationItem2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

