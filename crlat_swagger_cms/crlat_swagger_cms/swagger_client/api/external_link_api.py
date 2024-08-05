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


class ExternalLinkApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def external_link_by_id(self, id, **kwargs):  # noqa: E501
        """ExternalLinkById  # noqa: E501

        Delete a ExternalLink  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.external_link_by_id(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: id of resource (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.external_link_by_id_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.external_link_by_id_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def external_link_by_id_with_http_info(self, id, **kwargs):  # noqa: E501
        """ExternalLinkById  # noqa: E501

        Delete a ExternalLink  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.external_link_by_id_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: id of resource (required)
        :return: None
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
                    " to method external_link_by_id" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `external_link_by_id`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/external-link/{id}', 'DELETE',
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

    def external_links_by_brand(self, brand, **kwargs):  # noqa: E501
        """find ExternalLink by brand  # noqa: E501

        Searches ExternalLinks by brand  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.external_links_by_brand(brand, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str brand: name of brand to return (required)
        :return: list[ExternalLink2]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.external_links_by_brand_with_http_info(brand, **kwargs)  # noqa: E501
        else:
            (data) = self.external_links_by_brand_with_http_info(brand, **kwargs)  # noqa: E501
            return data

    def external_links_by_brand_with_http_info(self, brand, **kwargs):  # noqa: E501
        """find ExternalLink by brand  # noqa: E501

        Searches ExternalLinks by brand  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.external_links_by_brand_with_http_info(brand, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str brand: name of brand to return (required)
        :return: list[ExternalLink2]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['brand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method external_links_by_brand" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'brand' is set
        if ('brand' not in params or
                params['brand'] is None):
            raise ValueError("Missing the required parameter `brand` when calling `external_links_by_brand`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'brand' in params:
            path_params['brand'] = params['brand']  # noqa: E501

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
            '/external-link/brand/{brand}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[ExternalLink2]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def find_all6(self, **kwargs):  # noqa: E501
        """findAll  # noqa: E501

        Retrieve all ExternalLinks  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_all6(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: list[ExternalLink]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.find_all6_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.find_all6_with_http_info(**kwargs)  # noqa: E501
            return data

    def find_all6_with_http_info(self, **kwargs):  # noqa: E501
        """findAll  # noqa: E501

        Retrieve all ExternalLinks  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_all6_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: list[ExternalLink]
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
                    " to method find_all6" % key
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
            '/external-link', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[ExternalLink]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def find_one6(self, id, **kwargs):  # noqa: E501
        """findOne  # noqa: E501

        Searches ExternalLink by id  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_one6(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: id of resource (required)
        :return: ExternalLink2
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.find_one6_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.find_one6_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def find_one6_with_http_info(self, id, **kwargs):  # noqa: E501
        """findOne  # noqa: E501

        Searches ExternalLink by id  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_one6_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: id of resource (required)
        :return: ExternalLink2
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
                    " to method find_one6" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `find_one6`")  # noqa: E501

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
            '/external-link/{id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ExternalLink2',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def save6(self, body, **kwargs):  # noqa: E501
        """save  # noqa: E501

        Add a new ExternalLink  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.save6(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ExternalLink2 body: ExternalLink object that needs to be added to the storage (required)
        :return: ExternalLink2
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.save6_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.save6_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def save6_with_http_info(self, body, **kwargs):  # noqa: E501
        """save  # noqa: E501

        Add a new ExternalLink  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.save6_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ExternalLink2 body: ExternalLink object that needs to be added to the storage (required)
        :return: ExternalLink2
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
                    " to method save6" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `save6`")  # noqa: E501

        collection_formats = {}

        path_params = {}

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
            '/external-link', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ExternalLink2',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update6(self, body, id, **kwargs):  # noqa: E501
        """update  # noqa: E501

        Update an existing ExternalLink  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update6(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ExternalLink2 body: ExternalLink object that needs to be updated in the storage (required)
        :param str id: id of resource (required)
        :return: ExternalLink2
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.update6_with_http_info(body, id, **kwargs)  # noqa: E501
        else:
            (data) = self.update6_with_http_info(body, id, **kwargs)  # noqa: E501
            return data

    def update6_with_http_info(self, body, id, **kwargs):  # noqa: E501
        """update  # noqa: E501

        Update an existing ExternalLink  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update6_with_http_info(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ExternalLink2 body: ExternalLink object that needs to be updated in the storage (required)
        :param str id: id of resource (required)
        :return: ExternalLink2
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
                    " to method update6" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `update6`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `update6`")  # noqa: E501

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
            '/external-link/{id}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ExternalLink2',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)