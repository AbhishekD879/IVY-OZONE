# swagger_client.CompetitionApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**competition_by_id**](CompetitionApi.md#competition_by_id) | **DELETE** /competition/{id} | CompetitionById
[**find_all_brand_competition**](CompetitionApi.md#find_all_brand_competition) | **GET** /competition/brand/{brand} | findAllByBrand
[**find_all_competition**](CompetitionApi.md#find_all_competition) | **GET** /competition | findAll
[**find_one_competition**](CompetitionApi.md#find_one_competition) | **GET** /competition/{id} | findOne
[**find_site_serve_event_by_id**](CompetitionApi.md#find_site_serve_event_by_id) | **GET** /competition/brand/{brand}/ss/event | FindSiteServeEventById
[**find_site_serve_event_by_market_id**](CompetitionApi.md#find_site_serve_event_by_market_id) | **GET** /competition/brand/{brand}/ss/market/{marketId}/event | FindSiteServeEventByMarketId
[**find_site_serve_knockout_event_by_id**](CompetitionApi.md#find_site_serve_knockout_event_by_id) | **GET** /competition/brand/{brand}/ss/knockout/event | FindSiteServeKnockoutEventById
[**find_site_serve_market_by_id**](CompetitionApi.md#find_site_serve_market_by_id) | **GET** /competition/brand/{brand}/ss/market/{marketId} | FindSiteServeMarketById
[**find_site_serve_type_by_id**](CompetitionApi.md#find_site_serve_type_by_id) | **GET** /competition/brand/{brand}/ss/type | FindSiteServeTypeById
[**save_competition**](CompetitionApi.md#save_competition) | **POST** /competition | save
[**stats_center_groups**](CompetitionApi.md#stats_center_groups) | **GET** /competition/{compId}/stats/groups | StatsCenterGroups
[**update_competition**](CompetitionApi.md#update_competition) | **PUT** /competition/{id} | update

# **competition_by_id**
> competition_by_id(id)

CompetitionById

Delete a Competition

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
api_instance = swagger_client.CompetitionApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # CompetitionById
    api_instance.competition_by_id(id)
except ApiException as e:
    print("Exception when calling CompetitionApi->competition_by_id: %s\n" % e)
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

# **find_all_brand_competition**
> list[Competition2] find_all_brand_competition(brand)

findAllByBrand

Retrieve all Competitions for brand

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
api_instance = swagger_client.CompetitionApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return

try:
    # findAllByBrand
    api_response = api_instance.find_all_brand_competition(brand)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionApi->find_all_brand_competition: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 

### Return type

[**list[Competition2]**](Competition2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_all_competition**
> list[Competition] find_all_competition()

findAll

Retrieve all Competitions

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
api_instance = swagger_client.CompetitionApi(swagger_client.ApiClient(configuration))

try:
    # findAll
    api_response = api_instance.find_all_competition()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionApi->find_all_competition: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Competition]**](Competition.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one_competition**
> Competition2 find_one_competition(id)

findOne

Searches Competition by id

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
api_instance = swagger_client.CompetitionApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | id of resource

try:
    # findOne
    api_response = api_instance.find_one_competition(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionApi->find_one_competition: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| id of resource | 

### Return type

[**Competition2**](Competition2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_site_serve_event_by_id**
> SiteServeEventValidationResultDto2 find_site_serve_event_by_id(brand, event_ids, only_specials=only_specials)

FindSiteServeEventById

Searches SiteServeEvent by id

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
api_instance = swagger_client.CompetitionApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return
event_ids = 'event_ids_example' # str | comma separated SiteServe event ids
only_specials = true # bool | If true, the endpoint returns only the special events (optional)

try:
    # FindSiteServeEventById
    api_response = api_instance.find_site_serve_event_by_id(brand, event_ids, only_specials=only_specials)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionApi->find_site_serve_event_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 
 **event_ids** | **str**| comma separated SiteServe event ids | 
 **only_specials** | **bool**| If true, the endpoint returns only the special events | [optional] 

### Return type

[**SiteServeEventValidationResultDto2**](SiteServeEventValidationResultDto2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_site_serve_event_by_market_id**
> SiteServeEventValidationResultDto find_site_serve_event_by_market_id(brand, market_id)

FindSiteServeEventByMarketId

Searches SiteServeEvent by marketId

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
api_instance = swagger_client.CompetitionApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return
market_id = 'market_id_example' # str | SiteServe market id

try:
    # FindSiteServeEventByMarketId
    api_response = api_instance.find_site_serve_event_by_market_id(brand, market_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionApi->find_site_serve_event_by_market_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 
 **market_id** | **str**| SiteServe market id | 

### Return type

[**SiteServeEventValidationResultDto**](SiteServeEventValidationResultDto.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_site_serve_knockout_event_by_id**
> list[SiteServeKnockoutEventDto] find_site_serve_knockout_event_by_id(brand, event_id)

FindSiteServeKnockoutEventById

Searches FindSiteServeKnockoutEventById by id

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
api_instance = swagger_client.CompetitionApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return
event_id = 'event_id_example' # str | site serve event id

try:
    # FindSiteServeKnockoutEventById
    api_response = api_instance.find_site_serve_knockout_event_by_id(brand, event_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionApi->find_site_serve_knockout_event_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 
 **event_id** | **str**| site serve event id | 

### Return type

[**list[SiteServeKnockoutEventDto]**](SiteServeKnockoutEventDto.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_site_serve_market_by_id**
> SiteServeMarketDto find_site_serve_market_by_id(brand, market_id)

FindSiteServeMarketById

Searches SiteServeMarket by id

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
api_instance = swagger_client.CompetitionApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return
market_id = 'market_id_example' # str | SiteServe market id

try:
    # FindSiteServeMarketById
    api_response = api_instance.find_site_serve_market_by_id(brand, market_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionApi->find_site_serve_market_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 
 **market_id** | **str**| SiteServe market id | 

### Return type

[**SiteServeMarketDto**](SiteServeMarketDto.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_site_serve_type_by_id**
> SiteServeEventValidationResultDto2 find_site_serve_type_by_id(brand, type_ids, only_specials=only_specials)

FindSiteServeTypeById

Searches SiteServeEvents by type id

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
api_instance = swagger_client.CompetitionApi(swagger_client.ApiClient(configuration))
brand = 'brand_example' # str | name of brand to return
type_ids = 'type_ids_example' # str | comma separated SiteServe type ids
only_specials = true # bool | If true, the endpoint returns only the special events (optional)

try:
    # FindSiteServeTypeById
    api_response = api_instance.find_site_serve_type_by_id(brand, type_ids, only_specials=only_specials)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionApi->find_site_serve_type_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **brand** | **str**| name of brand to return | 
 **type_ids** | **str**| comma separated SiteServe type ids | 
 **only_specials** | **bool**| If true, the endpoint returns only the special events | [optional] 

### Return type

[**SiteServeEventValidationResultDto2**](SiteServeEventValidationResultDto2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save_competition**
> Competition2 save_competition(body)

save

Add a new Competition

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
api_instance = swagger_client.CompetitionApi(swagger_client.ApiClient(configuration))
body = swagger_client.Competition2() # Competition2 | Competition object that needs to be added to the storage

try:
    # save
    api_response = api_instance.save_competition(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionApi->save_competition: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Competition2**](Competition2.md)| Competition object that needs to be added to the storage | 

### Return type

[**Competition2**](Competition2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stats_center_groups**
> StatsCompetitionSeason stats_center_groups(comp_id)

StatsCenterGroups

Searches stats center competitions

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
api_instance = swagger_client.CompetitionApi(swagger_client.ApiClient(configuration))
comp_id = 'comp_id_example' # str | id of competition

try:
    # StatsCenterGroups
    api_response = api_instance.stats_center_groups(comp_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionApi->stats_center_groups: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **comp_id** | **str**| id of competition | 

### Return type

[**StatsCompetitionSeason**](StatsCompetitionSeason.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_competition**
> Competition2 update_competition(body, id)

update

Update an existing Competition

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
api_instance = swagger_client.CompetitionApi(swagger_client.ApiClient(configuration))
body = swagger_client.Competition2() # Competition2 | Competition object that needs to be updated in the storage
id = 'id_example' # str | id of resource

try:
    # update
    api_response = api_instance.update_competition(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionApi->update_competition: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Competition2**](Competition2.md)| Competition object that needs to be updated in the storage | 
 **id** | **str**| id of resource | 

### Return type

[**Competition2**](Competition2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

