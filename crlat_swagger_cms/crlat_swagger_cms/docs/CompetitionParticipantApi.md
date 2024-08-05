# swagger_client.CompetitionParticipantApi

All URIs are relative to */v1/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**competition_participant**](CompetitionParticipantApi.md#competition_participant) | **POST** /participant/{participantId}/image | uploadImage
[**competition_participant_by_id**](CompetitionParticipantApi.md#competition_participant_by_id) | **DELETE** /competition/{compId}/participant/{participantId} | CompetitionParticipantById
[**find_all_competition_participant**](CompetitionParticipantApi.md#find_all_competition_participant) | **GET** /participant | findAll
[**find_competition_expand_competition_participant**](CompetitionParticipantApi.md#find_competition_expand_competition_participant) | **GET** /competition/{compId}/participant/{participantId} | findOne
[**find_one_competition_participant**](CompetitionParticipantApi.md#find_one_competition_participant) | **GET** /participant/{participantId} | findOne
[**remove_image**](CompetitionParticipantApi.md#remove_image) | **DELETE** /participant/{participantId}/image | removeImage
[**save_competition_participant**](CompetitionParticipantApi.md#save_competition_participant) | **POST** /competition/{compId}/participant | save
[**update_competition_participant**](CompetitionParticipantApi.md#update_competition_participant) | **PUT** /participant/{participantId} | update

# **competition_participant**
> CompetitionParticipant2 competition_participant(participant_id, file=file, file_type=file_type)

uploadImage

Upload new image for CompetitionParticipant

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
api_instance = swagger_client.CompetitionParticipantApi(swagger_client.ApiClient(configuration))
participant_id = 'participant_id_example' # str | id of participant
file = 'file_example' # str |  (optional)
file_type = 'file_type_example' # str | fileType of image (optional)

try:
    # uploadImage
    api_response = api_instance.competition_participant(participant_id, file=file, file_type=file_type)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionParticipantApi->competition_participant: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **participant_id** | **str**| id of participant | 
 **file** | **str**|  | [optional] 
 **file_type** | **str**| fileType of image | [optional] 

### Return type

[**CompetitionParticipant2**](CompetitionParticipant2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **competition_participant_by_id**
> competition_participant_by_id(comp_id, participant_id)

CompetitionParticipantById

Delete a CompetitionParticipant

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
api_instance = swagger_client.CompetitionParticipantApi(swagger_client.ApiClient(configuration))
comp_id = 'comp_id_example' # str | id of competition
participant_id = 'participant_id_example' # str | id of participant

try:
    # CompetitionParticipantById
    api_instance.competition_participant_by_id(comp_id, participant_id)
except ApiException as e:
    print("Exception when calling CompetitionParticipantApi->competition_participant_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **comp_id** | **str**| id of competition | 
 **participant_id** | **str**| id of participant | 

### Return type

void (empty response body)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_all_competition_participant**
> list[CompetitionParticipant2] find_all_competition_participant()

findAll

Retrieve all CompetitionParticipant

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
api_instance = swagger_client.CompetitionParticipantApi(swagger_client.ApiClient(configuration))

try:
    # findAll
    api_response = api_instance.find_all_competition_participant()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionParticipantApi->find_all_competition_participant: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[CompetitionParticipant2]**](CompetitionParticipant2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_competition_expand_competition_participant**
> Competition2 find_competition_expand_competition_participant(comp_id, participant_id)

findOne

Searches Conpetition's CompetitionParticipant

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
api_instance = swagger_client.CompetitionParticipantApi(swagger_client.ApiClient(configuration))
comp_id = 'comp_id_example' # str | id of competition
participant_id = 'participant_id_example' # str | id of participant

try:
    # findOne
    api_response = api_instance.find_competition_expand_competition_participant(comp_id, participant_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionParticipantApi->find_competition_expand_competition_participant: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **comp_id** | **str**| id of competition | 
 **participant_id** | **str**| id of participant | 

### Return type

[**Competition2**](Competition2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_one_competition_participant**
> CompetitionParticipant2 find_one_competition_participant(participant_id)

findOne

Searches CompetitionParticipant by id

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
api_instance = swagger_client.CompetitionParticipantApi(swagger_client.ApiClient(configuration))
participant_id = 'participant_id_example' # str | id of participant

try:
    # findOne
    api_response = api_instance.find_one_competition_participant(participant_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionParticipantApi->find_one_competition_participant: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **participant_id** | **str**| id of participant | 

### Return type

[**CompetitionParticipant2**](CompetitionParticipant2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_image**
> remove_image(participant_id, file_type=file_type)

removeImage

Remove image from CompetitionParticipant

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
api_instance = swagger_client.CompetitionParticipantApi(swagger_client.ApiClient(configuration))
participant_id = 'participant_id_example' # str | id of participant
file_type = 'file_type_example' # str | fileType of image (optional)

try:
    # removeImage
    api_instance.remove_image(participant_id, file_type=file_type)
except ApiException as e:
    print("Exception when calling CompetitionParticipantApi->remove_image: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **participant_id** | **str**| id of participant | 
 **file_type** | **str**| fileType of image | [optional] 

### Return type

void (empty response body)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save_competition_participant**
> CompetitionParticipant2 save_competition_participant(body, comp_id)

save

Add a new CompetitionParticipant

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
api_instance = swagger_client.CompetitionParticipantApi(swagger_client.ApiClient(configuration))
body = swagger_client.CompetitionParticipant() # CompetitionParticipant | CompetitionParticipant object that needs to be added to the storage
comp_id = 'comp_id_example' # str | id of competition

try:
    # save
    api_response = api_instance.save_competition_participant(body, comp_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionParticipantApi->save_competition_participant: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CompetitionParticipant**](CompetitionParticipant.md)| CompetitionParticipant object that needs to be added to the storage | 
 **comp_id** | **str**| id of competition | 

### Return type

[**CompetitionParticipant2**](CompetitionParticipant2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_competition_participant**
> CompetitionParticipant2 update_competition_participant(body, participant_id)

update

Update an existing CompetitionParticipant

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
api_instance = swagger_client.CompetitionParticipantApi(swagger_client.ApiClient(configuration))
body = swagger_client.CompetitionParticipant2() # CompetitionParticipant2 | CompetitionParticipant object that needs to be updated in the storage
participant_id = 'participant_id_example' # str | id of participant

try:
    # update
    api_response = api_instance.update_competition_participant(body, participant_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CompetitionParticipantApi->update_competition_participant: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CompetitionParticipant2**](CompetitionParticipant2.md)| CompetitionParticipant object that needs to be updated in the storage | 
 **participant_id** | **str**| id of participant | 

### Return type

[**CompetitionParticipant2**](CompetitionParticipant2.md)

### Authorization

[Authorization](../README.md#Authorization)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

