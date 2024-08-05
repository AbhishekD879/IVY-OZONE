# swagger_client.BankingMenuApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**detele_banking_menu_by_id**](BankingMenuApi.md#detele_banking_menu_by_id) | **DELETE** /banking-menu/{id} | BankingMenuById
[**find_all_banking_menu**](BankingMenuApi.md#find_all_banking_menu) | **GET** /banking-menu | findAll
[**find_one_banking_menu**](BankingMenuApi.md#find_one_banking_menu) | **GET** /banking-menu/{id} | findOne
[**order**](BankingMenuApi.md#order) | **POST** /banking-menu/ordering | order
[**read**](BankingMenuApi.md#read) | **GET** /banking-menu/brand/{brand} | read
[**remove_image_banking_menu**](BankingMenuApi.md#remove_image_banking_menu) | **DELETE** /banking-menu/{id}/image | removeImage
[**save_banking_menu**](BankingMenuApi.md#save_banking_menu) | **POST** /banking-menu | save
[**update_banking_menu**](BankingMenuApi.md#update_banking_menu) | **PUT** /banking-menu/{id} | update
[**upload_image_banking_menu**](BankingMenuApi.md#upload_image_banking_menu) | **POST** /banking-menu/{id}/image | uploadImage

# **detele_banking_menu_by_id**
> detele_banking_menu_by_id(id)

BankingMenuById

Delete a BankingMenu

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
api_instance = swagger_client.BankingMenuApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # BankingMenuById
    api_instance.detele_banking_menu_by_id(id)
except ApiException as e:
    print("Exception when calling BankingMenuApi->detele_banking_menu_by_id: %s\n" % e)
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

# **find_all_banking_menu**
> list[BankingMenu] find_all_banking_menu()

findAll

Retrieve all BankingMenus

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
api_instance = swagger_client.BankingMenuApi(swagger_client.ApiClient(configuration))

try:
    # findAll
    api_response = api_instance.find_all_banking_menu()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BankingMenuApi->find_all_banking_menu: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[BankingMenu]**](BankingMenu.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one_banking_menu**
> BankingMenu2 find_one_banking_menu(id)

findOne

Searches BankingMenu by id

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
api_instance = swagger_client.BankingMenuApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.find_one_banking_menu(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BankingMenuApi->find_one_banking_menu: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**BankingMenu2**](BankingMenu2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **order**
> order(body)

order

Set order for all BankingMenu

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
api_instance = swagger_client.BankingMenuApi(swagger_client.ApiClient(configuration))
body = swagger_client.Ordering2() # Ordering2 | List of ordered ids of BankingMenu

try:
    # order
    api_instance.order(body)
except ApiException as e:
    print("Exception when calling BankingMenuApi->order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Ordering2**](Ordering2.md)| List of ordered ids of BankingMenu | 

### Return type

void (empty response body)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read**
> list[BankingMenu2] read(brand)

read

Searches BankingMenu by brand and sort it by sortOrder field in Asc order

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
api_instance = swagger_client.BankingMenuApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return

try:
    # read
    api_response = api_instance.read(brand)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BankingMenuApi->read: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 

### Return type

[**list[BankingMenu2]**](BankingMenu2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_image_banking_menu**
> remove_image_banking_menu(id, file_type=file_type)

removeImage

Remove image from bankingMenu

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
api_instance = swagger_client.BankingMenuApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource
file_type = ['file_type_example'] # list[str] | type of file to delete (optional)

try:
    # removeImage
    api_instance.remove_image_banking_menu(id, file_type=file_type)
except ApiException as e:
    print("Exception when calling BankingMenuApi->remove_image_banking_menu: %s\n" % e)
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

# **save_banking_menu**
> BankingMenu2 save_banking_menu(body)

save

Add a new BankingMenu

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
api_instance = swagger_client.BankingMenuApi(swagger_client.ApiClient(configuration))
body = swagger_client.BankingMenu2() # BankingMenu2 | BankingMenu object that needs to be added to the storage

try:
    # save
    api_response = api_instance.save_banking_menu(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BankingMenuApi->save_banking_menu: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**BankingMenu2**](BankingMenu2.md)| BankingMenu object that needs to be added to the storage | 

### Return type

[**BankingMenu2**](BankingMenu2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_banking_menu**
> BankingMenu2 update_banking_menu(body, id)

update

Update an existing BankingMenu

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
api_instance = swagger_client.BankingMenuApi(swagger_client.ApiClient(configuration))
body = swagger_client.BankingMenu2() # BankingMenu2 | BankingMenu object that needs to be updated in the storage
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.update_banking_menu(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BankingMenuApi->update_banking_menu: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**BankingMenu2**](BankingMenu2.md)| BankingMenu object that needs to be updated in the storage | 
 **id** | **str**| id of resource | 

### Return type

[**BankingMenu2**](BankingMenu2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_image_banking_menu**
> BankingMenu2 upload_image_banking_menu(id, file=file, file_type=file_type)

uploadImage

Upload new image for BankingMenu

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
api_instance = swagger_client.BankingMenuApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource
file = 'file_example' # str |  (optional)
file_type = ['file_type_example'] # list[str] | type of file to delete (optional)

try:
    # uploadImage
    api_response = api_instance.upload_image_banking_menu(id, file=file, file_type=file_type)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BankingMenuApi->upload_image_banking_menu: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 
 **file** | **str**|  | [optional] 
 **file_type** | [**list[str]**](str.md)| type of file to delete | [optional] 

### Return type

[**BankingMenu2**](BankingMenu2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

