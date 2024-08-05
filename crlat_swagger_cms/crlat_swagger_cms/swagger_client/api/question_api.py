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


class QuestionApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def find_one48(self, quiz_id, question_id, **kwargs):  # noqa: E501
        """findOne  # noqa: E501

        Searches Question by id  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_one48(quiz_id, question_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str quiz_id: id to find quiz (required)
        :param str question_id: id to find question (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = False
        if kwargs.get('async_req'):
            return self.find_one48_with_http_info(quiz_id, question_id, **kwargs)  # noqa: E501
        else:
            (data) = self.find_one48_with_http_info(quiz_id, question_id, **kwargs)  # noqa: E501
            return data

    def find_one48_with_http_info(self, quiz_id, question_id, **kwargs):  # noqa: E501
        """findOne  # noqa: E501

        Searches Question by id  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.find_one48_with_http_info(quiz_id, question_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str quiz_id: id to find quiz (required)
        :param str question_id: id to find question (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['quiz_id', 'question_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method find_one48" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'quiz_id' is set
        if ('quiz_id' not in params or
                params['quiz_id'] is None):
            raise ValueError("Missing the required parameter `quiz_id` when calling `find_one48`")  # noqa: E501
        # verify the required parameter 'question_id' is set
        if ('question_id' not in params or
                params['question_id'] is None):
            raise ValueError("Missing the required parameter `question_id` when calling `find_one48`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'quiz_id' in params:
            path_params['quizId'] = params['quiz_id']  # noqa: E501
        if 'question_id' in params:
            path_params['questionId'] = params['question_id']  # noqa: E501

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
            '/question-engine/question/{quizId}/{questionId}', 'GET',
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