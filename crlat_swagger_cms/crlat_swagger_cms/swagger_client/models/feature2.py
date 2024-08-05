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


class Feature2(object):
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
        'title_brand': 'str',
        'sort_order': 'float',
        'height_medium': 'float',
        'width_medium': 'float',
        'uri_medium': 'str',
        'validity_period_end': 'str',
        'validity_period_start': 'str',
        'short_description': 'str',
        'title': 'str',
        'vip_levels': 'list[float]',
        'lang': 'str',
        'brand': 'str',
        'show_to_customer': 'str',
        'disabled': 'bool',
        'description': 'str',
        'filename': 'UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentsfilenameYamlFilename'
    }

    attribute_map = {
        'id': 'id',
        'title_brand': 'title_brand',
        'sort_order': 'sortOrder',
        'height_medium': 'heightMedium',
        'width_medium': 'widthMedium',
        'uri_medium': 'uriMedium',
        'validity_period_end': 'validityPeriodEnd',
        'validity_period_start': 'validityPeriodStart',
        'short_description': 'shortDescription',
        'title': 'title',
        'vip_levels': 'vipLevels',
        'lang': 'lang',
        'brand': 'brand',
        'show_to_customer': 'showToCustomer',
        'disabled': 'disabled',
        'description': 'description',
        'filename': 'filename'
    }

    def __init__(self, id=None, title_brand=None, sort_order=None, height_medium=None, width_medium=None, uri_medium=None, validity_period_end=None, validity_period_start=None, short_description=None, title=None, vip_levels=None, lang=None, brand=None, show_to_customer=None, disabled=None, description=None, filename=None):  # noqa: E501
        """Feature2 - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._title_brand = None
        self._sort_order = None
        self._height_medium = None
        self._width_medium = None
        self._uri_medium = None
        self._validity_period_end = None
        self._validity_period_start = None
        self._short_description = None
        self._title = None
        self._vip_levels = None
        self._lang = None
        self._brand = None
        self._show_to_customer = None
        self._disabled = None
        self._description = None
        self._filename = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if title_brand is not None:
            self.title_brand = title_brand
        if sort_order is not None:
            self.sort_order = sort_order
        if height_medium is not None:
            self.height_medium = height_medium
        if width_medium is not None:
            self.width_medium = width_medium
        if uri_medium is not None:
            self.uri_medium = uri_medium
        if validity_period_end is not None:
            self.validity_period_end = validity_period_end
        if validity_period_start is not None:
            self.validity_period_start = validity_period_start
        if short_description is not None:
            self.short_description = short_description
        if title is not None:
            self.title = title
        if vip_levels is not None:
            self.vip_levels = vip_levels
        if lang is not None:
            self.lang = lang
        if brand is not None:
            self.brand = brand
        if show_to_customer is not None:
            self.show_to_customer = show_to_customer
        if disabled is not None:
            self.disabled = disabled
        if description is not None:
            self.description = description
        if filename is not None:
            self.filename = filename

    @property
    def id(self):
        """Gets the id of this Feature2.  # noqa: E501


        :return: The id of this Feature2.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Feature2.


        :param id: The id of this Feature2.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def title_brand(self):
        """Gets the title_brand of this Feature2.  # noqa: E501


        :return: The title_brand of this Feature2.  # noqa: E501
        :rtype: str
        """
        return self._title_brand

    @title_brand.setter
    def title_brand(self, title_brand):
        """Sets the title_brand of this Feature2.


        :param title_brand: The title_brand of this Feature2.  # noqa: E501
        :type: str
        """

        self._title_brand = title_brand

    @property
    def sort_order(self):
        """Gets the sort_order of this Feature2.  # noqa: E501


        :return: The sort_order of this Feature2.  # noqa: E501
        :rtype: float
        """
        return self._sort_order

    @sort_order.setter
    def sort_order(self, sort_order):
        """Sets the sort_order of this Feature2.


        :param sort_order: The sort_order of this Feature2.  # noqa: E501
        :type: float
        """

        self._sort_order = sort_order

    @property
    def height_medium(self):
        """Gets the height_medium of this Feature2.  # noqa: E501


        :return: The height_medium of this Feature2.  # noqa: E501
        :rtype: float
        """
        return self._height_medium

    @height_medium.setter
    def height_medium(self, height_medium):
        """Sets the height_medium of this Feature2.


        :param height_medium: The height_medium of this Feature2.  # noqa: E501
        :type: float
        """

        self._height_medium = height_medium

    @property
    def width_medium(self):
        """Gets the width_medium of this Feature2.  # noqa: E501


        :return: The width_medium of this Feature2.  # noqa: E501
        :rtype: float
        """
        return self._width_medium

    @width_medium.setter
    def width_medium(self, width_medium):
        """Sets the width_medium of this Feature2.


        :param width_medium: The width_medium of this Feature2.  # noqa: E501
        :type: float
        """

        self._width_medium = width_medium

    @property
    def uri_medium(self):
        """Gets the uri_medium of this Feature2.  # noqa: E501


        :return: The uri_medium of this Feature2.  # noqa: E501
        :rtype: str
        """
        return self._uri_medium

    @uri_medium.setter
    def uri_medium(self, uri_medium):
        """Sets the uri_medium of this Feature2.


        :param uri_medium: The uri_medium of this Feature2.  # noqa: E501
        :type: str
        """

        self._uri_medium = uri_medium

    @property
    def validity_period_end(self):
        """Gets the validity_period_end of this Feature2.  # noqa: E501


        :return: The validity_period_end of this Feature2.  # noqa: E501
        :rtype: str
        """
        return self._validity_period_end

    @validity_period_end.setter
    def validity_period_end(self, validity_period_end):
        """Sets the validity_period_end of this Feature2.


        :param validity_period_end: The validity_period_end of this Feature2.  # noqa: E501
        :type: str
        """

        self._validity_period_end = validity_period_end

    @property
    def validity_period_start(self):
        """Gets the validity_period_start of this Feature2.  # noqa: E501


        :return: The validity_period_start of this Feature2.  # noqa: E501
        :rtype: str
        """
        return self._validity_period_start

    @validity_period_start.setter
    def validity_period_start(self, validity_period_start):
        """Sets the validity_period_start of this Feature2.


        :param validity_period_start: The validity_period_start of this Feature2.  # noqa: E501
        :type: str
        """

        self._validity_period_start = validity_period_start

    @property
    def short_description(self):
        """Gets the short_description of this Feature2.  # noqa: E501


        :return: The short_description of this Feature2.  # noqa: E501
        :rtype: str
        """
        return self._short_description

    @short_description.setter
    def short_description(self, short_description):
        """Sets the short_description of this Feature2.


        :param short_description: The short_description of this Feature2.  # noqa: E501
        :type: str
        """

        self._short_description = short_description

    @property
    def title(self):
        """Gets the title of this Feature2.  # noqa: E501


        :return: The title of this Feature2.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this Feature2.


        :param title: The title of this Feature2.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def vip_levels(self):
        """Gets the vip_levels of this Feature2.  # noqa: E501


        :return: The vip_levels of this Feature2.  # noqa: E501
        :rtype: list[float]
        """
        return self._vip_levels

    @vip_levels.setter
    def vip_levels(self, vip_levels):
        """Sets the vip_levels of this Feature2.


        :param vip_levels: The vip_levels of this Feature2.  # noqa: E501
        :type: list[float]
        """

        self._vip_levels = vip_levels

    @property
    def lang(self):
        """Gets the lang of this Feature2.  # noqa: E501


        :return: The lang of this Feature2.  # noqa: E501
        :rtype: str
        """
        return self._lang

    @lang.setter
    def lang(self, lang):
        """Sets the lang of this Feature2.


        :param lang: The lang of this Feature2.  # noqa: E501
        :type: str
        """

        self._lang = lang

    @property
    def brand(self):
        """Gets the brand of this Feature2.  # noqa: E501


        :return: The brand of this Feature2.  # noqa: E501
        :rtype: str
        """
        return self._brand

    @brand.setter
    def brand(self, brand):
        """Sets the brand of this Feature2.


        :param brand: The brand of this Feature2.  # noqa: E501
        :type: str
        """

        self._brand = brand

    @property
    def show_to_customer(self):
        """Gets the show_to_customer of this Feature2.  # noqa: E501


        :return: The show_to_customer of this Feature2.  # noqa: E501
        :rtype: str
        """
        return self._show_to_customer

    @show_to_customer.setter
    def show_to_customer(self, show_to_customer):
        """Sets the show_to_customer of this Feature2.


        :param show_to_customer: The show_to_customer of this Feature2.  # noqa: E501
        :type: str
        """

        self._show_to_customer = show_to_customer

    @property
    def disabled(self):
        """Gets the disabled of this Feature2.  # noqa: E501


        :return: The disabled of this Feature2.  # noqa: E501
        :rtype: bool
        """
        return self._disabled

    @disabled.setter
    def disabled(self, disabled):
        """Sets the disabled of this Feature2.


        :param disabled: The disabled of this Feature2.  # noqa: E501
        :type: bool
        """

        self._disabled = disabled

    @property
    def description(self):
        """Gets the description of this Feature2.  # noqa: E501


        :return: The description of this Feature2.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Feature2.


        :param description: The description of this Feature2.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def filename(self):
        """Gets the filename of this Feature2.  # noqa: E501


        :return: The filename of this Feature2.  # noqa: E501
        :rtype: UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentsfilenameYamlFilename
        """
        return self._filename

    @filename.setter
    def filename(self, filename):
        """Sets the filename of this Feature2.


        :param filename: The filename of this Feature2.  # noqa: E501
        :type: UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentsfilenameYamlFilename
        """

        self._filename = filename

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
        if issubclass(Feature2, dict):
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
        if not isinstance(other, Feature2):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
