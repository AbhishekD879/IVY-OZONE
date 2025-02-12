# coding: utf-8

"""
    Oxygen CMS Public REST API

    This page contains only public GET request available on cms_api_tests. All models & requests have been taken from bma-cms_api_tests project.   # noqa: E501

    OpenAPI spec version: 82.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from crlat_swagger_cms.swagger_client.api_client import ApiClient


class PublicCompetitionApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def find_all_brand_competitions(self, brand, **kwargs):  # noqa: E501
        """findAllCompetitionsByBrand  # noqa: E501

        Retrieve all competitions for brand  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_all_brand_competitions(brand, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str brand: name of brand to return (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.find_all_brand_competitions_with_http_info(brand, **kwargs)  # noqa: E501
        else:
            (data) = self.find_all_brand_competitions_with_http_info(brand, **kwargs)  # noqa: E501
            return data

    def find_all_brand_competitions_with_http_info(self, brand, **kwargs):  # noqa: E501
        """findAllCompetitionsByBrand  # noqa: E501

        Retrieve all competitions for brand  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_all_brand_competitions_with_http_info(brand, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str brand: name of brand to return (required)
        :return: object
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
                    " to method find_all_brand_competitions" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'brand' is set
        if ('brand' not in params or
                params['brand'] is None):
            raise ValueError("Missing the required parameter `brand` when calling `find_all_brand_competitions`")  # noqa: E501

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
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/{brand}/competition', 'GET',
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

    def find_by_uri(self, brand, uri, **kwargs):  # noqa: E501
        """findByUri  # noqa: E501

        Retrieve competition by ur  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_by_uri(brand, uri, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str brand: name of brand to return (required)
        :param str uri: uri of competiotion to return (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.find_by_uri_with_http_info(brand, uri, **kwargs)  # noqa: E501
        else:
            (data) = self.find_by_uri_with_http_info(brand, uri, **kwargs)  # noqa: E501
            return data

    def find_by_uri_with_http_info(self, brand, uri, **kwargs):  # noqa: E501
        """findByUri  # noqa: E501

        Retrieve competition by ur  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_by_uri_with_http_info(brand, uri, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str brand: name of brand to return (required)
        :param str uri: uri of competiotion to return (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['brand', 'uri']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method find_by_uri" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'brand' is set
        if ('brand' not in params or
                params['brand'] is None):
            raise ValueError("Missing the required parameter `brand` when calling `find_by_uri`")  # noqa: E501
        # verify the required parameter 'uri' is set
        if ('uri' not in params or
                params['uri'] is None):
            raise ValueError("Missing the required parameter `uri` when calling `find_by_uri`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'brand' in params:
            path_params['brand'] = params['brand']  # noqa: E501
        if 'uri' in params:
            path_params['uri'] = params['uri']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/{brand}/competition/{uri}', 'GET',
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

    def find_competition_module_by_id(self, id, **kwargs):  # noqa: E501
        """findCompetitionModuleById  # noqa: E501

        Retrieve CompetitionModule by id  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_competition_module_by_id(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: id of CompetitionModule to return (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.find_competition_module_by_id_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.find_competition_module_by_id_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def find_competition_module_by_id_with_http_info(self, id, **kwargs):  # noqa: E501
        """findCompetitionModuleById  # noqa: E501

        Retrieve CompetitionModule by id  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_competition_module_by_id_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: id of CompetitionModule to return (required)
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
                    " to method find_competition_module_by_id" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `find_competition_module_by_id`")  # noqa: E501

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
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/competition/module/{id}', 'GET',
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

    def find_sub_tab_by_id(self, id, **kwargs):  # noqa: E501
        """findCompetiotionSubTabById  # noqa: E501

        Retrieve Subtab by id  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_sub_tab_by_id(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: id of competiotionSubTab to return (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.find_sub_tab_by_id_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.find_sub_tab_by_id_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def find_sub_tab_by_id_with_http_info(self, id, **kwargs):  # noqa: E501
        """findCompetiotionSubTabById  # noqa: E501

        Retrieve Subtab by id  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_sub_tab_by_id_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: id of competiotionSubTab to return (required)
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
                    " to method find_sub_tab_by_id" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `find_sub_tab_by_id`")  # noqa: E501

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
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/competition/subtab/{id}', 'GET',
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

    def find_tab_by_id(self, id, **kwargs):  # noqa: E501
        """findCompetiotionTabById  # noqa: E501

        Retrieve tab by id  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_tab_by_id(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: id of competiotionTab to return (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.find_tab_by_id_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.find_tab_by_id_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def find_tab_by_id_with_http_info(self, id, **kwargs):  # noqa: E501
        """findCompetiotionTabById  # noqa: E501

        Retrieve tab by id  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_tab_by_id_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: id of competiotionTab to return (required)
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
                    " to method find_tab_by_id" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `find_tab_by_id`")  # noqa: E501

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
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/competition/tab/{id}', 'GET',
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
