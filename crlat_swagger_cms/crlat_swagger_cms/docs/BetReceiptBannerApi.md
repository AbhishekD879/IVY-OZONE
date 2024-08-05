# swagger_client.BetReceiptBannerApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**bet_receipt_banner_by_id**](BetReceiptBannerApi.md#bet_receipt_banner_by_id) | **DELETE** /bet-receipt-banner/{id} | BetReceiptBannerById
[**find_all2**](BetReceiptBannerApi.md#find_all2) | **GET** /bet-receipt-banner | findAll
[**find_one2**](BetReceiptBannerApi.md#find_one2) | **GET** /bet-receipt-banner/{id} | findOne
[**order**](BetReceiptBannerApi.md#order) | **POST** /bet-receipt-banner/ordering | order
[**read**](BetReceiptBannerApi.md#read) | **GET** /bet-receipt-banner/brand/{brand} | read
[**remove_image**](BetReceiptBannerApi.md#remove_image) | **DELETE** /bet-receipt-banner/{id}/image | removeImage
[**save2**](BetReceiptBannerApi.md#save2) | **POST** /bet-receipt-banner | save
[**update2**](BetReceiptBannerApi.md#update2) | **PUT** /bet-receipt-banner/{id} | update
[**upload_image**](BetReceiptBannerApi.md#upload_image) | **POST** /bet-receipt-banner/{id}/image | uploadImage

# **bet_receipt_banner_by_id**
> bet_receipt_banner_by_id(id)

BetReceiptBannerById

Delete a BetReceiptBanner

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
api_instance = swagger_client.BetReceiptBannerApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # BetReceiptBannerById
    api_instance.bet_receipt_banner_by_id(id)
except ApiException as e:
    print("Exception when calling BetReceiptBannerApi->bet_receipt_banner_by_id: %s\n" % e)
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

# **find_all2**
> list[BetReceiptBanner] find_all2()

findAll

Retrieve all BetReceiptBanners

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
api_instance = swagger_client.BetReceiptBannerApi(swagger_client.ApiClient(configuration))

try:
    # findAll
    api_response = api_instance.find_all2()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BetReceiptBannerApi->find_all2: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[BetReceiptBanner]**](BetReceiptBanner.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one2**
> BetReceiptBanner2 find_one2(id)

findOne

Searches BetReceiptBanner by id

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
api_instance = swagger_client.BetReceiptBannerApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.find_one2(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BetReceiptBannerApi->find_one2: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**BetReceiptBanner2**](BetReceiptBanner2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **order**
> order(body)

order

Set order for all BetReceiptBanner

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
api_instance = swagger_client.BetReceiptBannerApi(swagger_client.ApiClient(configuration))
body = swagger_client.Ordering2() # Ordering2 | List of ordered ids of BetReceiptBanner

try:
    # order
    api_instance.order(body)
except ApiException as e:
    print("Exception when calling BetReceiptBannerApi->order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Ordering2**](Ordering2.md)| List of ordered ids of BetReceiptBanner | 

### Return type

void (empty response body)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read**
> list[BetReceiptBanner2] read(brand)

read

Searches BetReceiptBanner by brand and sort it by sortOrder field in Asc order

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
api_instance = swagger_client.BetReceiptBannerApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return

try:
    # read
    api_response = api_instance.read(brand)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BetReceiptBannerApi->read: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 

### Return type

[**list[BetReceiptBanner2]**](BetReceiptBanner2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_image**
> remove_image(id)

removeImage

Remove image from BetReceiptBanner

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
api_instance = swagger_client.BetReceiptBannerApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # removeImage
    api_instance.remove_image(id)
except ApiException as e:
    print("Exception when calling BetReceiptBannerApi->remove_image: %s\n" % e)
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

# **save2**
> BetReceiptBanner2 save2(body)

save

Add a new BetReceiptBanner

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
api_instance = swagger_client.BetReceiptBannerApi(swagger_client.ApiClient(configuration))
body = swagger_client.BetReceiptBanner2() # BetReceiptBanner2 | BetReceiptBanner object that needs to be added to the storage

try:
    # save
    api_response = api_instance.save2(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BetReceiptBannerApi->save2: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**BetReceiptBanner2**](BetReceiptBanner2.md)| BetReceiptBanner object that needs to be added to the storage | 

### Return type

[**BetReceiptBanner2**](BetReceiptBanner2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update2**
> BetReceiptBanner2 update2(body, id)

update

Update an existing BetReceiptBanner

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
api_instance = swagger_client.BetReceiptBannerApi(swagger_client.ApiClient(configuration))
body = swagger_client.BetReceiptBanner2() # BetReceiptBanner2 | BetReceiptBanner object that needs to be updated in the storage
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.update2(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BetReceiptBannerApi->update2: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**BetReceiptBanner2**](BetReceiptBanner2.md)| BetReceiptBanner object that needs to be updated in the storage | 
 **id** | **str**| id of resource | 

### Return type

[**BetReceiptBanner2**](BetReceiptBanner2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_image**
> BetReceiptBanner2 upload_image(id, file=file)

uploadImage

Upload new image for BetReceiptBanner

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
api_instance = swagger_client.BetReceiptBannerApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource
file = 'file_example' # str |  (optional)

try:
    # uploadImage
    api_response = api_instance.upload_image(id, file=file)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BetReceiptBannerApi->upload_image: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 
 **file** | **str**|  | [optional] 

### Return type

[**BetReceiptBanner2**](BetReceiptBanner2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

