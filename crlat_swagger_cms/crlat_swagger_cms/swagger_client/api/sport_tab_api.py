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


class SportTabApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def find_one_sport_tab(self, id, **kwargs):  # noqa: E501
        """findOne  # noqa: E501

        Searches SportTab by id  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_one_sport_tab(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: id of resource (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.find_one_sport_tab_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.find_one_sport_tab_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def find_one_sport_tab_with_http_info(self, id, **kwargs):  # noqa: E501
        """findOne  # noqa: E501

        Searches SportTab by id  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_one_sport_tab_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: id of resource (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method find_one_sport_tab" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `find_one_sport_tab`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

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
            '/sport-tab/{id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='object',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def order_sport_tab(self, body, **kwargs):  # noqa: E501
        """order  # noqa: E501

        Set order for SportTabs  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.order_sport_tab(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object body: List of ordered ids of SportTabs (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.order_sport_tab_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.order_sport_tab_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def order_sport_tab_with_http_info(self, body, **kwargs):  # noqa: E501
        """order  # noqa: E501

        Set order for SportTabs  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.order_sport_tab_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object body: List of ordered ids of SportTabs (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method order_sport_tab" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `order_sport_tab`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/sport-tab/ordering', 'POST',
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

    def read(self, brand, sport_id, **kwargs):  # noqa: E501
        """read  # noqa: E501

        Searches SportTab by brand and siteserve sport id in Asc order  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read(brand, sport_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str brand: name of brand to return (required)
        :param str sport_id: id of resource (required)
        :return: list[object]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.read_with_http_info(brand, sport_id, **kwargs)  # noqa: E501
        else:
            (data) = self.read_with_http_info(brand, sport_id, **kwargs)  # noqa: E501
            return data

    def read_with_http_info(self, brand, sport_id, **kwargs):  # noqa: E501
        """read  # noqa: E501

        Searches SportTab by brand and siteserve sport id in Asc order  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read_with_http_info(brand, sport_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str brand: name of brand to return (required)
        :param str sport_id: id of resource (required)
        :return: list[object]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['brand', 'sport_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method read" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'brand' is set
        if ('brand' not in params or
                params['brand'] is None):
            raise ValueError("Missing the required parameter `brand` when calling `read`")  # noqa: E501
        # verify the required parameter 'sport_id' is set
        if ('sport_id' not in params or
                params['sport_id'] is None):
            raise ValueError("Missing the required parameter `sport_id` when calling `read`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'brand' in params:
            path_params['brand'] = params['brand']  # noqa: E501
        if 'sport_id' in params:
            path_params['sportId'] = params['sport_id']  # noqa: E501

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
            '/sport-tab/brand/{brand}/sport/{sportId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[object]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_sport_tab(self, body, id, **kwargs):  # noqa: E501
        """update  # noqa: E501

        Update an existing SportTab  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_sport_tab(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object body: SportTab object that needs to be updated in the storage (required)
        :param str id: id of resource (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.update_sport_tab_with_http_info(body, id, **kwargs)  # noqa: E501
        else:
            (data) = self.update_sport_tab_with_http_info(body, id, **kwargs)  # noqa: E501
            return data

    def update_sport_tab_with_http_info(self, body, id, **kwargs):  # noqa: E501
        """update  # noqa: E501

        Update an existing SportTab  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_sport_tab_with_http_info(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object body: SportTab object that needs to be updated in the storage (required)
        :param str id: id of resource (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_sport_tab" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `update_sport_tab`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `update_sport_tab`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

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
            '/sport-tab/{id}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='object',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
