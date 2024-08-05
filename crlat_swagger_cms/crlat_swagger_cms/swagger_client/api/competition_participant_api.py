# coding: utf-8

"""
    Oxygen CMS REST API

    CMS Private API (Used by CMS UI)   # noqa: E501

    OpenAPI spec version: 82.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from crlat_swagger_cms.swagger_client.api_client import ApiClient


class CompetitionParticipantApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def competition_participant(self, participant_id, **kwargs):  # noqa: E501
        """uploadImage  # noqa: E501

        Upload new image for CompetitionParticipant  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.competition_participant(participant_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str participant_id: id of participant (required)
        :param str file:
        :param str file_type: fileType of image
        :return: CompetitionParticipant2
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.competition_participant_with_http_info(participant_id, **kwargs)  # noqa: E501
        else:
            (data) = self.competition_participant_with_http_info(participant_id, **kwargs)  # noqa: E501
            return data

    def competition_participant_with_http_info(self, participant_id, **kwargs):  # noqa: E501
        """uploadImage  # noqa: E501

        Upload new image for CompetitionParticipant  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.competition_participant_with_http_info(participant_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str participant_id: id of participant (required)
        :param str file:
        :param str file_type: fileType of image
        :return: CompetitionParticipant2
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['participant_id', 'file', 'file_type']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method competition_participant" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'participant_id' is set
        if ('participant_id' not in params or
                params['participant_id'] is None):
            raise ValueError("Missing the required parameter `participant_id` when calling `competition_participant`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'participant_id' in params:
            path_params['participantId'] = params['participant_id']  # noqa: E501

        query_params = []
        if 'file_type' in params:
            query_params.append(('fileType', params['file_type']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'file' in params:
            form_params.append(('file', params['file']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/participant/{participantId}/image', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CompetitionParticipant2',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def competition_participant_by_id(self, comp_id, participant_id, **kwargs):  # noqa: E501
        """CompetitionParticipantById  # noqa: E501

        Delete a CompetitionParticipant  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.competition_participant_by_id(comp_id, participant_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str comp_id: id of competition (required)
        :param str participant_id: id of participant (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.competition_participant_by_id_with_http_info(comp_id, participant_id, **kwargs)  # noqa: E501
        else:
            (data) = self.competition_participant_by_id_with_http_info(comp_id, participant_id, **kwargs)  # noqa: E501
            return data

    def competition_participant_by_id_with_http_info(self, comp_id, participant_id, **kwargs):  # noqa: E501
        """CompetitionParticipantById  # noqa: E501

        Delete a CompetitionParticipant  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.competition_participant_by_id_with_http_info(comp_id, participant_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str comp_id: id of competition (required)
        :param str participant_id: id of participant (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['comp_id', 'participant_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method competition_participant_by_id" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'comp_id' is set
        if ('comp_id' not in params or
                params['comp_id'] is None):
            raise ValueError("Missing the required parameter `comp_id` when calling `competition_participant_by_id`")  # noqa: E501
        # verify the required parameter 'participant_id' is set
        if ('participant_id' not in params or
                params['participant_id'] is None):
            raise ValueError("Missing the required parameter `participant_id` when calling `competition_participant_by_id`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'comp_id' in params:
            path_params['compId'] = params['comp_id']  # noqa: E501
        if 'participant_id' in params:
            path_params['participantId'] = params['participant_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/competition/{compId}/participant/{participantId}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def find_all_competition_participant(self, **kwargs):  # noqa: E501
        """findAll  # noqa: E501

        Retrieve all CompetitionParticipant  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_all_competition_participant(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: list[CompetitionParticipant2]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.find_all_competition_participant_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.find_all_competition_participant_with_http_info(**kwargs)  # noqa: E501
            return data

    def find_all_competition_participant_with_http_info(self, **kwargs):  # noqa: E501
        """findAll  # noqa: E501

        Retrieve all CompetitionParticipant  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_all_competition_participant_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: list[CompetitionParticipant2]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method find_all_competition_participant" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/participant', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[CompetitionParticipant2]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def find_competition_expand_competition_participant(self, comp_id, participant_id, **kwargs):  # noqa: E501
        """findOne  # noqa: E501

        Searches Conpetition's CompetitionParticipant  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_competition_expand_competition_participant(comp_id, participant_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str comp_id: id of competition (required)
        :param str participant_id: id of participant (required)
        :return: Competition2
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.find_competition_expand_competition_participant_with_http_info(comp_id, participant_id, **kwargs)  # noqa: E501
        else:
            (data) = self.find_competition_expand_competition_participant_with_http_info(comp_id, participant_id, **kwargs)  # noqa: E501
            return data

    def find_competition_expand_competition_participant_with_http_info(self, comp_id, participant_id, **kwargs):  # noqa: E501
        """findOne  # noqa: E501

        Searches Conpetition's CompetitionParticipant  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_competition_expand_competition_participant_with_http_info(comp_id, participant_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str comp_id: id of competition (required)
        :param str participant_id: id of participant (required)
        :return: Competition2
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['comp_id', 'participant_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method find_competition_expand_competition_participant" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'comp_id' is set
        if ('comp_id' not in params or
                params['comp_id'] is None):
            raise ValueError("Missing the required parameter `comp_id` when calling `find_competition_expand_competition_participant`")  # noqa: E501
        # verify the required parameter 'participant_id' is set
        if ('participant_id' not in params or
                params['participant_id'] is None):
            raise ValueError("Missing the required parameter `participant_id` when calling `find_competition_expand_competition_participant`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'comp_id' in params:
            path_params['compId'] = params['comp_id']  # noqa: E501
        if 'participant_id' in params:
            path_params['participantId'] = params['participant_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/competition/{compId}/participant/{participantId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Competition2',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def find_one_competition_participant(self, participant_id, **kwargs):  # noqa: E501
        """findOne  # noqa: E501

        Searches CompetitionParticipant by id  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_one_competition_participant(participant_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str participant_id: id of participant (required)
        :return: CompetitionParticipant2
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.find_one_competition_participant_with_http_info(participant_id, **kwargs)  # noqa: E501
        else:
            (data) = self.find_one_competition_participant_with_http_info(participant_id, **kwargs)  # noqa: E501
            return data

    def find_one_competition_participant_with_http_info(self, participant_id, **kwargs):  # noqa: E501
        """findOne  # noqa: E501

        Searches CompetitionParticipant by id  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_one_competition_participant_with_http_info(participant_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str participant_id: id of participant (required)
        :return: CompetitionParticipant2
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['participant_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method find_one_competition_participant" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'participant_id' is set
        if ('participant_id' not in params or
                params['participant_id'] is None):
            raise ValueError("Missing the required parameter `participant_id` when calling `find_one_competition_participant`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'participant_id' in params:
            path_params['participantId'] = params['participant_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/participant/{participantId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CompetitionParticipant2',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def remove_image(self, participant_id, **kwargs):  # noqa: E501
        """removeImage  # noqa: E501

        Remove image from CompetitionParticipant  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.remove_image(participant_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str participant_id: id of participant (required)
        :param str file_type: fileType of image
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.remove_image_with_http_info(participant_id, **kwargs)  # noqa: E501
        else:
            (data) = self.remove_image_with_http_info(participant_id, **kwargs)  # noqa: E501
            return data

    def remove_image_with_http_info(self, participant_id, **kwargs):  # noqa: E501
        """removeImage  # noqa: E501

        Remove image from CompetitionParticipant  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.remove_image_with_http_info(participant_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str participant_id: id of participant (required)
        :param str file_type: fileType of image
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['participant_id', 'file_type']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method remove_image" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'participant_id' is set
        if ('participant_id' not in params or
                params['participant_id'] is None):
            raise ValueError("Missing the required parameter `participant_id` when calling `remove_image`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'participant_id' in params:
            path_params['participantId'] = params['participant_id']  # noqa: E501

        query_params = []
        if 'file_type' in params:
            query_params.append(('fileType', params['file_type']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/participant/{participantId}/image', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def save_competition_participant(self, body, comp_id, **kwargs):  # noqa: E501
        """save  # noqa: E501

        Add a new CompetitionParticipant  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.save_competition_participant(body, comp_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CompetitionParticipant body: CompetitionParticipant object that needs to be added to the storage (required)
        :param str comp_id: id of competition (required)
        :return: CompetitionParticipant2
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.save_competition_participant_with_http_info(body, comp_id, **kwargs)  # noqa: E501
        else:
            (data) = self.save_competition_participant_with_http_info(body, comp_id, **kwargs)  # noqa: E501
            return data

    def save_competition_participant_with_http_info(self, body, comp_id, **kwargs):  # noqa: E501
        """save  # noqa: E501

        Add a new CompetitionParticipant  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.save_competition_participant_with_http_info(body, comp_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CompetitionParticipant body: CompetitionParticipant object that needs to be added to the storage (required)
        :param str comp_id: id of competition (required)
        :return: CompetitionParticipant2
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'comp_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method save_competition_participant" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `save_competition_participant`")  # noqa: E501
        # verify the required parameter 'comp_id' is set
        if ('comp_id' not in params or
                params['comp_id'] is None):
            raise ValueError("Missing the required parameter `comp_id` when calling `save_competition_participant`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'comp_id' in params:
            path_params['compId'] = params['comp_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/competition/{compId}/participant', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CompetitionParticipant2',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_competition_participant(self, body, participant_id, **kwargs):  # noqa: E501
        """update  # noqa: E501

        Update an existing CompetitionParticipant  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_competition_participant(body, participant_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CompetitionParticipant2 body: CompetitionParticipant object that needs to be updated in the storage (required)
        :param str participant_id: id of participant (required)
        :return: CompetitionParticipant2
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.update_competition_participant_with_http_info(body, participant_id, **kwargs)  # noqa: E501
        else:
            (data) = self.update_competition_participant_with_http_info(body, participant_id, **kwargs)  # noqa: E501
            return data

    def update_competition_participant_with_http_info(self, body, participant_id, **kwargs):  # noqa: E501
        """update  # noqa: E501

        Update an existing CompetitionParticipant  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_competition_participant_with_http_info(body, participant_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CompetitionParticipant2 body: CompetitionParticipant object that needs to be updated in the storage (required)
        :param str participant_id: id of participant (required)
        :return: CompetitionParticipant2
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'participant_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_competition_participant" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `update_competition_participant`")  # noqa: E501
        # verify the required parameter 'participant_id' is set
        if ('participant_id' not in params or
                params['participant_id'] is None):
            raise ValueError("Missing the required parameter `participant_id` when calling `update_competition_participant`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'participant_id' in params:
            path_params['participantId'] = params['participant_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/participant/{participantId}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CompetitionParticipant2',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)