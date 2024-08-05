# swagger_client.BetReceiptBannerTabletApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**bet_receipt_banner_tablet_by_id**](BetReceiptBannerTabletApi.md#bet_receipt_banner_tablet_by_id) | **DELETE** /bet-receipt-banner-tablet/{id} | BetReceiptBannerTabletById
[**find_all3**](BetReceiptBannerTabletApi.md#find_all3) | **GET** /bet-receipt-banner-tablet | findAll
[**find_one3**](BetReceiptBannerTabletApi.md#find_one3) | **GET** /bet-receipt-banner-tablet/{id} | findOne
[**order**](BetReceiptBannerTabletApi.md#order) | **POST** /bet-receipt-banner-tablet/ordering | order
[**read**](BetReceiptBannerTabletApi.md#read) | **GET** /bet-receipt-banner-tablet/brand/{brand} | read
[**remove_image**](BetReceiptBannerTabletApi.md#remove_image) | **DELETE** /bet-receipt-banner-tablet/{id}/image | removeImage
[**save3**](BetReceiptBannerTabletApi.md#save3) | **POST** /bet-receipt-banner-tablet | save
[**update3**](BetReceiptBannerTabletApi.md#update3) | **PUT** /bet-receipt-banner-tablet/{id} | update
[**upload_image**](BetReceiptBannerTabletApi.md#upload_image) | **POST** /bet-receipt-banner-tablet/{id}/image | uploadImage

# **bet_receipt_banner_tablet_by_id**
> bet_receipt_banner_tablet_by_id(id)

BetReceiptBannerTabletById

Delete a BetReceiptBannerTablet

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
api_instance = swagger_client.BetReceiptBannerTabletApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # BetReceiptBannerTabletById
    api_instance.bet_receipt_banner_tablet_by_id(id)
except ApiException as e:
    print("Exception when calling BetReceiptBannerTabletApi->bet_receipt_banner_tablet_by_id: %s\n" % e)
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

# **find_all3**
> list[BetReceiptBannerTablet] find_all3()

findAll

Retrieve all BetReceiptBannerTablets

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
api_instance = swagger_client.BetReceiptBannerTabletApi(swagger_client.ApiClient(configuration))

try:
    # findAll
    api_response = api_instance.find_all3()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BetReceiptBannerTabletApi->find_all3: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[BetReceiptBannerTablet]**](BetReceiptBannerTablet.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one3**
> BetReceiptBannerTablet2 find_one3(id)

findOne

Searches BetReceiptBannerTablet by id

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
api_instance = swagger_client.BetReceiptBannerTabletApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.find_one3(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BetReceiptBannerTabletApi->find_one3: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**BetReceiptBannerTablet2**](BetReceiptBannerTablet2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **order**
> BetReceiptBannerTablet2 order(body)

order

Set order for all BetReceiptBannerTablet

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
api_instance = swagger_client.BetReceiptBannerTabletApi(swagger_client.ApiClient(configuration))
body = swagger_client.Ordering2() # Ordering2 | List of ordered ids of BetReceiptBannerTablet

try:
    # order
    api_response = api_instance.order(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BetReceiptBannerTabletApi->order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Ordering2**](Ordering2.md)| List of ordered ids of BetReceiptBannerTablet | 

### Return type

[**BetReceiptBannerTablet2**](BetReceiptBannerTablet2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read**
> list[BetReceiptBannerTablet2] read(brand)

read

Searches BetReceiptBannerTablet by brand and sort it by sortOrder field in Asc order

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
api_instance = swagger_client.BetReceiptBannerTabletApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return

try:
    # read
    api_response = api_instance.read(brand)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BetReceiptBannerTabletApi->read: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 

### Return type

[**list[BetReceiptBannerTablet2]**](BetReceiptBannerTablet2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_image**
> remove_image(id)

removeImage

Remove image from BetReceiptBannerTablet

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
api_instance = swagger_client.BetReceiptBannerTabletApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # removeImage
    api_instance.remove_image(id)
except ApiException as e:
    print("Exception when calling BetReceiptBannerTabletApi->remove_image: %s\n" % e)
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

# **save3**
> BetReceiptBannerTablet2 save3(body)

save

Add a new BetReceiptBannerTablet

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
api_instance = swagger_client.BetReceiptBannerTabletApi(swagger_client.ApiClient(configuration))
body = swagger_client.BetReceiptBannerTablet2() # BetReceiptBannerTablet2 | BetReceiptBannerTablet object that needs to be added to the storage

try:
    # save
    api_response = api_instance.save3(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BetReceiptBannerTabletApi->save3: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**BetReceiptBannerTablet2**](BetReceiptBannerTablet2.md)| BetReceiptBannerTablet object that needs to be added to the storage | 

### Return type

[**BetReceiptBannerTablet2**](BetReceiptBannerTablet2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update3**
> BetReceiptBannerTablet2 update3(body, id)

update

Update an existing BetReceiptBannerTablet

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
api_instance = swagger_client.BetReceiptBannerTabletApi(swagger_client.ApiClient(configuration))
body = swagger_client.BetReceiptBannerTablet2() # BetReceiptBannerTablet2 | BetReceiptBannerTablet object that needs to be updated in the storage
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.update3(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BetReceiptBannerTabletApi->update3: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**BetReceiptBannerTablet2**](BetReceiptBannerTablet2.md)| BetReceiptBannerTablet object that needs to be updated in the storage | 
 **id** | **str**| id of resource | 

### Return type

[**BetReceiptBannerTablet2**](BetReceiptBannerTablet2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_image**
> BetReceiptBannerTablet2 upload_image(id, file=file)

uploadImage

Upload new image for BetReceiptBannerTablet

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
api_instance = swagger_client.BetReceiptBannerTabletApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource
file = 'file_example' # str |  (optional)

try:
    # uploadImage
    api_response = api_instance.upload_image(id, file=file)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BetReceiptBannerTabletApi->upload_image: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 
 **file** | **str**|  | [optional] 

### Return type

[**BetReceiptBannerTablet2**](BetReceiptBannerTablet2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

