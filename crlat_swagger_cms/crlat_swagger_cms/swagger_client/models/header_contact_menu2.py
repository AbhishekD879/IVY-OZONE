# coding: utf-8

"""
    Oxygen CMS REST API

    CMS Private API (Used by CMS UI)   # noqa: E501

    OpenAPI spec version: 82.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six


class HeaderContactMenu2(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'str',
        'brand': 'str',
        'disabled': 'bool',
        'in_app': 'bool',
        'lang': 'str',
        'link_title': 'str',
        'link_title_brand': 'str',
        'sort_order': 'float',
        'target_uri': 'str',
        'label': 'str',
        'auth_required': 'bool',
        'system_id': 'float',
        'start_url': 'str'
    }

    attribute_map = {
        'id': 'id',
        'brand': 'brand',
        'disabled': 'disabled',
        'in_app': 'inApp',
        'lang': 'lang',
        'link_title': 'linkTitle',
        'link_title_brand': 'linkTitleBrand',
        'sort_order': 'sortOrder',
        'target_uri': 'targetUri',
        'label': 'label',
        'auth_required': 'authRequired',
        'system_id': 'systemID',
        'start_url': 'startUrl'
    }

    def __init__(self, id=None, brand=None, disabled=None, in_app=None, lang=None, link_title=None, link_title_brand=None, sort_order=None, target_uri=None, label=None, auth_required=None, system_id=None, start_url=None):  # noqa: E501
        """HeaderContactMenu2 - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._brand = None
        self._disabled = None
        self._in_app = None
        self._lang = None
        self._link_title = None
        self._link_title_brand = None
        self._sort_order = None
        self._target_uri = None
        self._label = None
        self._auth_required = None
        self._system_id = None
        self._start_url = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if brand is not None:
            self.brand = brand
        if disabled is not None:
            self.disabled = disabled
        if in_app is not None:
            self.in_app = in_app
        if lang is not None:
            self.lang = lang
        if link_title is not None:
            self.link_title = link_title
        if link_title_brand is not None:
            self.link_title_brand = link_title_brand
        if sort_order is not None:
            self.sort_order = sort_order
        if target_uri is not None:
            self.target_uri = target_uri
        if label is not None:
            self.label = label
        if auth_required is not None:
            self.auth_required = auth_required
        if system_id is not None:
            self.system_id = system_id
        if start_url is not None:
            self.start_url = start_url

    @property
    def id(self):
        """Gets the id of this HeaderContactMenu2.  # noqa: E501


        :return: The id of this HeaderContactMenu2.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this HeaderContactMenu2.


        :param id: The id of this HeaderContactMenu2.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def brand(self):
        """Gets the brand of this HeaderContactMenu2.  # noqa: E501


        :return: The brand of this HeaderContactMenu2.  # noqa: E501
        :rtype: str
        """
        return self._brand

    @brand.setter
    def brand(self, brand):
        """Sets the brand of this HeaderContactMenu2.


        :param brand: The brand of this HeaderContactMenu2.  # noqa: E501
        :type: str
        """

        self._brand = brand

    @property
    def disabled(self):
        """Gets the disabled of this HeaderContactMenu2.  # noqa: E501


        :return: The disabled of this HeaderContactMenu2.  # noqa: E501
        :rtype: bool
        """
        return self._disabled

    @disabled.setter
    def disabled(self, disabled):
        """Sets the disabled of this HeaderContactMenu2.


        :param disabled: The disabled of this HeaderContactMenu2.  # noqa: E501
        :type: bool
        """

        self._disabled = disabled

    @property
    def in_app(self):
        """Gets the in_app of this HeaderContactMenu2.  # noqa: E501


        :return: The in_app of this HeaderContactMenu2.  # noqa: E501
        :rtype: bool
        """
        return self._in_app

    @in_app.setter
    def in_app(self, in_app):
        """Sets the in_app of this HeaderContactMenu2.


        :param in_app: The in_app of this HeaderContactMenu2.  # noqa: E501
        :type: bool
        """

        self._in_app = in_app

    @property
    def lang(self):
        """Gets the lang of this HeaderContactMenu2.  # noqa: E501


        :return: The lang of this HeaderContactMenu2.  # noqa: E501
        :rtype: str
        """
        return self._lang

    @lang.setter
    def lang(self, lang):
        """Sets the lang of this HeaderContactMenu2.


        :param lang: The lang of this HeaderContactMenu2.  # noqa: E501
        :type: str
        """

        self._lang = lang

    @property
    def link_title(self):
        """Gets the link_title of this HeaderContactMenu2.  # noqa: E501


        :return: The link_title of this HeaderContactMenu2.  # noqa: E501
        :rtype: str
        """
        return self._link_title

    @link_title.setter
    def link_title(self, link_title):
        """Sets the link_title of this HeaderContactMenu2.


        :param link_title: The link_title of this HeaderContactMenu2.  # noqa: E501
        :type: str
        """

        self._link_title = link_title

    @property
    def link_title_brand(self):
        """Gets the link_title_brand of this HeaderContactMenu2.  # noqa: E501


        :return: The link_title_brand of this HeaderContactMenu2.  # noqa: E501
        :rtype: str
        """
        return self._link_title_brand

    @link_title_brand.setter
    def link_title_brand(self, link_title_brand):
        """Sets the link_title_brand of this HeaderContactMenu2.


        :param link_title_brand: The link_title_brand of this HeaderContactMenu2.  # noqa: E501
        :type: str
        """

        self._link_title_brand = link_title_brand

    @property
    def sort_order(self):
        """Gets the sort_order of this HeaderContactMenu2.  # noqa: E501


        :return: The sort_order of this HeaderContactMenu2.  # noqa: E501
        :rtype: float
        """
        return self._sort_order

    @sort_order.setter
    def sort_order(self, sort_order):
        """Sets the sort_order of this HeaderContactMenu2.


        :param sort_order: The sort_order of this HeaderContactMenu2.  # noqa: E501
        :type: float
        """

        self._sort_order = sort_order

    @property
    def target_uri(self):
        """Gets the target_uri of this HeaderContactMenu2.  # noqa: E501


        :return: The target_uri of this HeaderContactMenu2.  # noqa: E501
        :rtype: str
        """
        return self._target_uri

    @target_uri.setter
    def target_uri(self, target_uri):
        """Sets the target_uri of this HeaderContactMenu2.


        :param target_uri: The target_uri of this HeaderContactMenu2.  # noqa: E501
        :type: str
        """

        self._target_uri = target_uri

    @property
    def label(self):
        """Gets the label of this HeaderContactMenu2.  # noqa: E501


        :return: The label of this HeaderContactMenu2.  # noqa: E501
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this HeaderContactMenu2.


        :param label: The label of this HeaderContactMenu2.  # noqa: E501
        :type: str
        """

        self._label = label

    @property
    def auth_required(self):
        """Gets the auth_required of this HeaderContactMenu2.  # noqa: E501


        :return: The auth_required of this HeaderContactMenu2.  # noqa: E501
        :rtype: bool
        """
        return self._auth_required

    @auth_required.setter
    def auth_required(self, auth_required):
        """Sets the auth_required of this HeaderContactMenu2.


        :param auth_required: The auth_required of this HeaderContactMenu2.  # noqa: E501
        :type: bool
        """

        self._auth_required = auth_required

    @property
    def system_id(self):
        """Gets the system_id of this HeaderContactMenu2.  # noqa: E501


        :return: The system_id of this HeaderContactMenu2.  # noqa: E501
        :rtype: float
        """
        return self._system_id

    @system_id.setter
    def system_id(self, system_id):
        """Sets the system_id of this HeaderContactMenu2.


        :param system_id: The system_id of this HeaderContactMenu2.  # noqa: E501
        :type: float
        """

        self._system_id = system_id

    @property
    def start_url(self):
        """Gets the start_url of this HeaderContactMenu2.  # noqa: E501


        :return: The start_url of this HeaderContactMenu2.  # noqa: E501
        :rtype: str
        """
        return self._start_url

    @start_url.setter
    def start_url(self, start_url):
        """Sets the start_url of this HeaderContactMenu2.


        :param start_url: The start_url of this HeaderContactMenu2.  # noqa: E501
        :type: str
        """

        self._start_url = start_url

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(HeaderContactMenu2, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, HeaderContactMenu2):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
