# swagger_client.BannerApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**banner_by_id**](BannerApi.md#banner_by_id) | **DELETE** /banner/{id} | BannerById
[**find_all**](BannerApi.md#find_all) | **GET** /banner | findAll
[**find_one**](BannerApi.md#find_one) | **GET** /banner/{id} | findOne
[**order**](BannerApi.md#order) | **POST** /banner/ordering | order
[**read**](BannerApi.md#read) | **GET** /banner/brand/{brand} | read
[**remove_banner_image**](BannerApi.md#remove_banner_image) | **GET** /banner/removeImage/{bannerId} | removeBannerImage
[**save**](BannerApi.md#save) | **POST** /banner | save
[**update**](BannerApi.md#update) | **PUT** /banner/{id} | update
[**upload_banner_image**](BannerApi.md#upload_banner_image) | **POST** /banner/uploadImage/{bannerId} | uploadBannerImage

# **banner_by_id**
> banner_by_id(id)

BannerById

Delete a Banner

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
api_instance = swagger_client.BannerApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # BannerById
    api_instance.banner_by_id(id)
except ApiException as e:
    print("Exception when calling BannerApi->banner_by_id: %s\n" % e)
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

# **find_all**
> list[Banner] find_all()

findAll

Retrieve all Banners

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
api_instance = swagger_client.BannerApi(swagger_client.ApiClient(configuration))

try:
    # findAll
    api_response = api_instance.find_all()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BannerApi->find_all: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Banner]**](Banner.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one**
> Banner2 find_one(id)

findOne

Searches Banner by id

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
api_instance = swagger_client.BannerApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.find_one(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BannerApi->find_one: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**Banner2**](Banner2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **order**
> order(body)

order

Set order for all Banner

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
api_instance = swagger_client.BannerApi(swagger_client.ApiClient(configuration))
body = swagger_client.Ordering() # Ordering | List of ordered ids of Banner

try:
    # order
    api_instance.order(body)
except ApiException as e:
    print("Exception when calling BannerApi->order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Ordering**](Ordering.md)| List of ordered ids of Banner | 

### Return type

void (empty response body)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read**
> list[Banner2] read(brand)

read

Searches Banner by brand and sort it by sortOrder field in Asc order

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
api_instance = swagger_client.BannerApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return

try:
    # read
    api_response = api_instance.read(brand)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BannerApi->read: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 

### Return type

[**list[Banner2]**](Banner2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_banner_image**
> Banner2 remove_banner_image(banner_id, desktop_image=desktop_image)

removeBannerImage

Remove image from Banner

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
api_instance = swagger_client.BannerApi(swagger_client.ApiClient(configuration))
banner_id = 'banner_id_example' # str | 
desktop_image = true # bool | flag that marks which image to remove - medium & small or desktop (optional)

try:
    # removeBannerImage
    api_response = api_instance.remove_banner_image(banner_id, desktop_image=desktop_image)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BannerApi->remove_banner_image: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **banner_id** | **str**|  | 
 **desktop_image** | **bool**| flag that marks which image to remove - medium &amp; small or desktop | [optional] 

### Return type

[**Banner2**](Banner2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save**
> Banner2 save(body)

save

Add a new Banner

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
api_instance = swagger_client.BannerApi(swagger_client.ApiClient(configuration))
body = swagger_client.Banner2() # Banner2 | Banner object that needs to be added to the storage

try:
    # save
    api_response = api_instance.save(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BannerApi->save: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Banner2**](Banner2.md)| Banner object that needs to be added to the storage | 

### Return type

[**Banner2**](Banner2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update**
> Banner2 update(body, id)

update

Update an existing Banner

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
api_instance = swagger_client.BannerApi(swagger_client.ApiClient(configuration))
body = swagger_client.Banner2() # Banner2 | Banner object that needs to be updated in the storage
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.update(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BannerApi->update: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Banner2**](Banner2.md)| Banner object that needs to be updated in the storage | 
 **id** | **str**| id of resource | 

### Return type

[**Banner2**](Banner2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_banner_image**
> Banner2 upload_banner_image(banner_id, file=file, desktop_image=desktop_image)

uploadBannerImage

Upload new image for banner

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
api_instance = swagger_client.BannerApi(swagger_client.ApiClient(configuration))
banner_id = 'banner_id_example' # str | 
file = 'file_example' # str |  (optional)
desktop_image = true # bool | flag that marks if the image provided will go to small & medium folders, or only in desktop (optional)

try:
    # uploadBannerImage
    api_response = api_instance.upload_banner_image(banner_id, file=file, desktop_image=desktop_image)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BannerApi->upload_banner_image: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **banner_id** | **str**|  | 
 **file** | **str**|  | [optional] 
 **desktop_image** | **bool**| flag that marks if the image provided will go to small &amp; medium folders, or only in desktop | [optional] 

### Return type

[**Banner2**](Banner2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

