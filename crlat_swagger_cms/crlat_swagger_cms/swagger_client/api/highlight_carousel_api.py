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


class HighlightCarouselApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def delete_highlight_carousel_by_id(self, id, **kwargs):  # noqa: E501
        """delete  # noqa: E501

        Delete a HighlightCarousel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_highlight_carousel_by_id(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: id of resource (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.delete_highlight_carousel_by_id_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_highlight_carousel_by_id_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def delete_highlight_carousel_by_id_with_http_info(self, id, **kwargs):  # noqa: E501
        """delete  # noqa: E501

        Delete a HighlightCarousel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_highlight_carousel_by_id_with_http_info(id, async_req=True)
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
                    " to method delete_highlight_carousel_by_id" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `delete_highlight_carousel_by_id`")  # noqa: E501

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
            '/highlight-carousel/{id}', 'DELETE',
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

    def find_all_highlight_carousels(self, **kwargs):  # noqa: E501
        """findAll  # noqa: E501

        Retrieve all HighlightCarousels  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_all_highlight_carousels(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: list[object]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.find_all_highlight_carousels_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.find_all_highlight_carousels_with_http_info(**kwargs)  # noqa: E501
            return data

    def find_all_highlight_carousels_with_http_info(self, **kwargs):  # noqa: E501
        """findAll  # noqa: E501

        Retrieve all HighlightCarousels  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_all_highlight_carousels_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: list[object]
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
                    " to method find_all_highlight_carousels" % key
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
            '/highlight-carousel', 'GET',
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

    def find_all_highlight_carousels_by_brand_and_sport(self, brand, page_type, page_id, **kwargs):  # noqa: E501
        """findAllByBrandAndSport  # noqa: E501

        Searches HighlightCarousel by brand and sort it by sortOrder field in Asc order  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_all_highlight_carousels_by_brand_and_sport(brand, page_type, page_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str brand: name of brand to return (required)
        :param str page_type: name of pageType (required)
        :param float page_id: pageId to filter objects (required)
        :return: list[object]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.find_all_highlight_carousels_by_brand_and_sport_with_http_info(brand, page_type, page_id, **kwargs)  # noqa: E501
        else:
            (data) = self.find_all_highlight_carousels_by_brand_and_sport_with_http_info(brand, page_type, page_id, **kwargs)  # noqa: E501
            return data

    def find_all_highlight_carousels_by_brand_and_sport_with_http_info(self, brand, page_type, page_id, **kwargs):  # noqa: E501
        """findAllByBrandAndSport  # noqa: E501

        Searches HighlightCarousel by brand and sort it by sortOrder field in Asc order  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_all_highlight_carousels_by_brand_and_sport_with_http_info(brand, page_type, page_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str brand: name of brand to return (required)
        :param str page_type: name of pageType (required)
        :param float page_id: pageId to filter objects (required)
        :return: list[object]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['brand', 'page_type', 'page_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method find_all_highlight_carousels_by_brand_and_sport" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'brand' is set
        if ('brand' not in params or
                params['brand'] is None):
            raise ValueError("Missing the required parameter `brand` when calling `find_all_highlight_carousels_by_brand_and_sport`")  # noqa: E501
        # verify the required parameter 'page_type' is set
        if ('page_type' not in params or
                params['page_type'] is None):
            raise ValueError("Missing the required parameter `page_type` when calling `find_all_highlight_carousels_by_brand_and_sport`")  # noqa: E501
        # verify the required parameter 'page_id' is set
        if ('page_id' not in params or
                params['page_id'] is None):
            raise ValueError("Missing the required parameter `page_id` when calling `find_all_highlight_carousels_by_brand_and_sport`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'brand' in params:
            path_params['brand'] = params['brand']  # noqa: E501
        if 'page_type' in params:
            path_params['pageType'] = params['page_type']  # noqa: E501
        if 'page_id' in params:
            path_params['pageId'] = params['page_id']  # noqa: E501

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
            '/highlight-carousel/brand/{brand}/{pageType}/{pageId}', 'GET',
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

    def order(self, body, **kwargs):  # noqa: E501
        """order  # noqa: E501

        Set order for all HighlightCarousels  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.order(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object body: List of ordered ids of HighlightCarousels (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.order_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.order_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def order_with_http_info(self, body, **kwargs):  # noqa: E501
        """order  # noqa: E501

        Set order for all HighlightCarousels  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.order_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object body: List of ordered ids of HighlightCarousels (required)
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
                    " to method order" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `order`")  # noqa: E501

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
            '/highlight-carousel/ordering', 'POST',
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

    def read_all_highlight_carousels(self, brand, **kwargs):  # noqa: E501
        """findAllHighlightCarousels  # noqa: E501

        Searches HighlightCarousels by brand and sort it by sortOrder field in Asc order  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read_all_highlight_carousels(brand, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str brand: name of brand to return (required)
        :return: list[object]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.read_all_highlight_carousels_with_http_info(brand, **kwargs)  # noqa: E501
        else:
            (data) = self.read_all_highlight_carousels_with_http_info(brand, **kwargs)  # noqa: E501
            return data

    def read_all_highlight_carousels_with_http_info(self, brand, **kwargs):  # noqa: E501
        """findAllHighlightCarousels  # noqa: E501

        Searches HighlightCarousels by brand and sort it by sortOrder field in Asc order  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read_all_highlight_carousels_with_http_info(brand, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str brand: name of brand to return (required)
        :return: list[object]
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
                    " to method read_all_highlight_carousels" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'brand' is set
        if ('brand' not in params or
                params['brand'] is None):
            raise ValueError("Missing the required parameter `brand` when calling `read_all_highlight_carousels`")  # noqa: E501

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
            '/highlight-carousel/brand/{brand}', 'GET',
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

    def read_highlight_carousel(self, id, **kwargs):  # noqa: E501
        """read  # noqa: E501

        Get the coupon segment by Id  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read_highlight_carousel(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: id of resource (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.read_highlight_carousel_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.read_highlight_carousel_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def read_highlight_carousel_with_http_info(self, id, **kwargs):  # noqa: E501
        """read  # noqa: E501

        Get the coupon segment by Id  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read_highlight_carousel_with_http_info(id, async_req=True)
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
                    " to method read_highlight_carousel" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `read_highlight_carousel`")  # noqa: E501

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
            '/highlight-carousel/{id}', 'GET',
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

    def remove_image_highlight_carousel(self, id, **kwargs):  # noqa: E501
        """removeSvgImage  # noqa: E501

        Remove svg image from HighlightCarousel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.remove_image_highlight_carousel(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: id of resource (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.remove_image_highlight_carousel_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.remove_image_highlight_carousel_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def remove_image_highlight_carousel_with_http_info(self, id, **kwargs):  # noqa: E501
        """removeSvgImage  # noqa: E501

        Remove svg image from HighlightCarousel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.remove_image_highlight_carousel_with_http_info(id, async_req=True)
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
                    " to method remove_image_highlight_carousel" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `remove_image_highlight_carousel`")  # noqa: E501

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
            '/highlight-carousel/{id}/image', 'DELETE',
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

    def save_highlight_carousel(self, body, **kwargs):  # noqa: E501
        """save  # noqa: E501

        Add a new HighlightCarousel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.save_highlight_carousel(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object body: HighlightCarousel object that needs to be added to the storage (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.save_highlight_carousel_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.save_highlight_carousel_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def save_highlight_carousel_with_http_info(self, body, **kwargs):  # noqa: E501
        """save  # noqa: E501

        Add a new HighlightCarousel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.save_highlight_carousel_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object body: HighlightCarousel object that needs to be added to the storage (required)
        :return: object
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
                    " to method save_highlight_carousel" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `save_highlight_carousel`")  # noqa: E501

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
            '/highlight-carousel', 'POST',
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

    def update_highlight_carousel(self, body, id, **kwargs):  # noqa: E501
        """update  # noqa: E501

        Update an existing HighlightCarousel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_highlight_carousel(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object body: HighlightCarousel object that needs to be updated in the storage (required)
        :param str id: id of resource (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.update_highlight_carousel_with_http_info(body, id, **kwargs)  # noqa: E501
        else:
            (data) = self.update_highlight_carousel_with_http_info(body, id, **kwargs)  # noqa: E501
            return data

    def update_highlight_carousel_with_http_info(self, body, id, **kwargs):  # noqa: E501
        """update  # noqa: E501

        Update an existing HighlightCarousel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_highlight_carousel_with_http_info(body, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object body: HighlightCarousel object that needs to be updated in the storage (required)
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
                    " to method update_highlight_carousel" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `update_highlight_carousel`")  # noqa: E501
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `update_highlight_carousel`")  # noqa: E501

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
            '/highlight-carousel/{id}', 'PUT',
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

    def upload_image_highlight_carousel(self, id, **kwargs):  # noqa: E501
        """uploadSvgImage  # noqa: E501

        Upload new svg image for HighlightCarousel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.upload_image_highlight_carousel(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: id of resource (required)
        :param str file:
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.upload_image_highlight_carousel_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.upload_image_highlight_carousel_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def upload_image_highlight_carousel_with_http_info(self, id, **kwargs):  # noqa: E501
        """uploadSvgImage  # noqa: E501

        Upload new svg image for HighlightCarousel  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.upload_image_highlight_carousel_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: id of resource (required)
        :param str file:
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'file']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method upload_image_highlight_carousel" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `upload_image_highlight_carousel`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []

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
            '/highlight-carousel/{id}/image', 'POST',
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