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


class PublicSportsFeaturedTabApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def sports_featured_tab_by_brand_and_path(self, brand, path, **kwargs):  # noqa: E501
        """SportsFeaturedTabByBrandAndPath  # noqa: E501

        Retrieve featured tab data for brand by path (sport)  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sports_featured_tab_by_brand_and_path(brand, path, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str brand: name of brand to return (required)
        :param str path: path to get feature tab data by (usually sport name) (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.sports_featured_tab_by_brand_and_path_with_http_info(brand, path, **kwargs)  # noqa: E501
        else:
            (data) = self.sports_featured_tab_by_brand_and_path_with_http_info(brand, path, **kwargs)  # noqa: E501
            return data

    def sports_featured_tab_by_brand_and_path_with_http_info(self, brand, path, **kwargs):  # noqa: E501
        """SportsFeaturedTabByBrandAndPath  # noqa: E501

        Retrieve featured tab data for brand by path (sport)  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sports_featured_tab_by_brand_and_path_with_http_info(brand, path, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str brand: name of brand to return (required)
        :param str path: path to get feature tab data by (usually sport name) (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['brand', 'path']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method sports_featured_tab_by_brand_and_path" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'brand' is set
        if ('brand' not in params or
                params['brand'] is None):
            raise ValueError("Missing the required parameter `brand` when calling `sports_featured_tab_by_brand_and_path`")  # noqa: E501
        # verify the required parameter 'path' is set
        if ('path' not in params or
                params['path'] is None):
            raise ValueError("Missing the required parameter `path` when calling `sports_featured_tab_by_brand_and_path`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'brand' in params:
            path_params['brand'] = params['brand']  # noqa: E501
        if 'path' in params:
            path_params['path'] = params['path']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/{brand}/sports-featured-tab/{path}', 'GET',
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