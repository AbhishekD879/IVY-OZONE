# swagger_client.FooterLogoApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**find_all16**](FooterLogoApi.md#find_all16) | **GET** /footer-logo | findAll
[**find_one15**](FooterLogoApi.md#find_one15) | **GET** /footer-logo/{id} | findOne
[**footer_logo_by_id**](FooterLogoApi.md#footer_logo_by_id) | **DELETE** /footer-logo/{id} | FooterLogoById
[**order**](FooterLogoApi.md#order) | **POST** /footer-logo/ordering | order
[**read**](FooterLogoApi.md#read) | **GET** /footer-logo/brand/{brand} | read
[**remove_image_footer_logo**](FooterLogoApi.md#remove_image_footer_logo) | **DELETE** /footer-logo/{id}/image | removeImage
[**save16**](FooterLogoApi.md#save16) | **POST** /footer-logo | save
[**update15**](FooterLogoApi.md#update15) | **PUT** /footer-logo/{id} | update
[**upload_image_footer_logo**](FooterLogoApi.md#upload_image_footer_logo) | **POST** /footer-logo/{id}/image | uploadImage

# **find_all16**
> list[FooterLogo] find_all16()

findAll

Retrieve all FooterLogos

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
api_instance = swagger_client.FooterLogoApi(swagger_client.ApiClient(configuration))

try:
    # findAll
    api_response = api_instance.find_all16()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FooterLogoApi->find_all16: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[FooterLogo]**](FooterLogo.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one15**
> FooterLogo2 find_one15(id)

findOne

Searches FooterLogo by id

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
api_instance = swagger_client.FooterLogoApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.find_one15(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FooterLogoApi->find_one15: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**FooterLogo2**](FooterLogo2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **footer_logo_by_id**
> footer_logo_by_id(id)

FooterLogoById

Delete a FooterLogo

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
api_instance = swagger_client.FooterLogoApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # FooterLogoById
    api_instance.footer_logo_by_id(id)
except ApiException as e:
    print("Exception when calling FooterLogoApi->footer_logo_by_id: %s\n" % e)
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

Set order for all FooterLogo

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
api_instance = swagger_client.FooterLogoApi(swagger_client.ApiClient(configuration))
body = swagger_client.Ordering2() # Ordering2 | List of ordered ids of FooterLogo

try:
    # order
    api_instance.order(body)
except ApiException as e:
    print("Exception when calling FooterLogoApi->order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Ordering2**](Ordering2.md)| List of ordered ids of FooterLogo | 

### Return type

void (empty response body)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read**
> list[FooterLogo2] read(brand)

read

Searches FooterLogo by brand and sort it by sortOrder field in Asc order

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
api_instance = swagger_client.FooterLogoApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return

try:
    # read
    api_response = api_instance.read(brand)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FooterLogoApi->read: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 

### Return type

[**list[FooterLogo2]**](FooterLogo2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_image_footer_logo**
> remove_image_footer_logo(id, file_type=file_type)

removeImage

Remove image from footerLogo

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
api_instance = swagger_client.FooterLogoApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource
file_type = ['file_type_example'] # list[str] | type of file to delete (optional)

try:
    # removeImage
    api_instance.remove_image_footer_logo(id, file_type=file_type)
except ApiException as e:
    print("Exception when calling FooterLogoApi->remove_image_footer_logo: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 
 **file_type** | [**list[str]**](str.md)| type of file to delete | [optional] 

### Return type

void (empty response body)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save16**
> FooterLogo2 save16(body)

save

Add a new FooterLogo

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
api_instance = swagger_client.FooterLogoApi(swagger_client.ApiClient(configuration))
body = swagger_client.FooterLogo2() # FooterLogo2 | FooterLogo object that needs to be added to the storage

try:
    # save
    api_response = api_instance.save16(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FooterLogoApi->save16: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FooterLogo2**](FooterLogo2.md)| FooterLogo object that needs to be added to the storage | 

### Return type

[**FooterLogo2**](FooterLogo2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update15**
> FooterLogo2 update15(body, id)

update

Update an existing FooterLogo

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
api_instance = swagger_client.FooterLogoApi(swagger_client.ApiClient(configuration))
body = swagger_client.FooterLogo2() # FooterLogo2 | FooterLogo object that needs to be updated in the storage
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.update15(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FooterLogoApi->update15: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FooterLogo2**](FooterLogo2.md)| FooterLogo object that needs to be updated in the storage | 
 **id** | **str**| id of resource | 

### Return type

[**FooterLogo2**](FooterLogo2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_image_footer_logo**
> FooterLogo2 upload_image_footer_logo(id, file=file, file_type=file_type)

uploadImage

Upload new image for footerLogo

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
api_instance = swagger_client.FooterLogoApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource
file = 'file_example' # str |  (optional)
file_type = ['file_type_example'] # list[str] | type of file to delete (optional)

try:
    # uploadImage
    api_response = api_instance.upload_image_footer_logo(id, file=file, file_type=file_type)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FooterLogoApi->upload_image_footer_logo: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 
 **file** | **str**|  | [optional] 
 **file_type** | [**list[str]**](str.md)| type of file to delete | [optional] 

### Return type

[**FooterLogo2**](FooterLogo2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

