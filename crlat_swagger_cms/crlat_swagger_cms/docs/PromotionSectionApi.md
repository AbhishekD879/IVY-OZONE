# swagger_client.PromotionSectionApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**find_all30**](PromotionSectionApi.md#find_all30) | **GET** /promotion/brand/{brand}/section | findAll
[**find_one29**](PromotionSectionApi.md#find_one29) | **GET** /promotion/brand/{brand}/section/{id} | findOne
[**promotion_section_by_id**](PromotionSectionApi.md#promotion_section_by_id) | **DELETE** /promotion/brand/{brand}/section/{id} | PromotionSectionById
[**save30**](PromotionSectionApi.md#save30) | **POST** /promotion/brand/{brand}/section | save
[**update29**](PromotionSectionApi.md#update29) | **PUT** /promotion/brand/{brand}/section/{id} | update

# **find_all30**
> list[PromotionSection2] find_all30(brand)

findAll

Retrieve all Promotions Sections by brand

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
api_instance = swagger_client.PromotionSectionApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return

try:
    # findAll
    api_response = api_instance.find_all30(brand)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PromotionSectionApi->find_all30: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 

### Return type

[**list[PromotionSection2]**](PromotionSection2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one29**
> PromotionSection find_one29(id, brand)

findOne

Searches Promotion Section by id

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
api_instance = swagger_client.PromotionSectionApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource
brand = 'brand_example' # str | name of brand to return

try:
    # findOne
    api_response = api_instance.find_one29(id, brand)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PromotionSectionApi->find_one29: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 
 **brand** | **str**| name of brand to return | 

### Return type

[**PromotionSection**](PromotionSection.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **promotion_section_by_id**
> promotion_section_by_id(id, brand)

PromotionSectionById

Delete a Promotion Section

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
api_instance = swagger_client.PromotionSectionApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource
brand = 'brand_example' # str | name of brand to return

try:
    # PromotionSectionById
    api_instance.promotion_section_by_id(id, brand)
except ApiException as e:
    print("Exception when calling PromotionSectionApi->promotion_section_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 
 **brand** | **str**| name of brand to return | 

### Return type

void (empty response body)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save30**
> PromotionSection2 save30(body, brand)

save

Add a new PromotionSection

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
api_instance = swagger_client.PromotionSectionApi(swagger_client.ApiClient(configuration))
body = swagger_client.Promotion2() # Promotion2 | Promotion object that needs to be added to the storage
brand = 'brand_example' # str | name of brand to return

try:
    # save
    api_response = api_instance.save30(body, brand)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PromotionSectionApi->save30: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Promotion2**](Promotion2.md)| Promotion object that needs to be added to the storage | 
 **brand** | **str**| name of brand to return | 

### Return type

[**PromotionSection2**](PromotionSection2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update29**
> Promotion2 update29(body, id, brand)

update

Update an existing Promotion Section

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
api_instance = swagger_client.PromotionSectionApi(swagger_client.ApiClient(configuration))
body = swagger_client.Promotion2() # Promotion2 | Promotion Section object that needs to be updated in the storage
id = 'id_example' # str | id of resource
brand = 'brand_example' # str | name of brand to return

try:
    # update
    api_response = api_instance.update29(body, id, brand)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PromotionSectionApi->update29: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Promotion2**](Promotion2.md)| Promotion Section object that needs to be updated in the storage | 
 **id** | **str**| id of resource | 
 **brand** | **str**| name of brand to return | 

### Return type

[**Promotion2**](Promotion2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

