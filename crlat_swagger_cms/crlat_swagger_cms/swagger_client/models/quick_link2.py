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


class QuickLink2(object):
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
        'sort_order': 'float',
        'validity_period_end': 'str',
        'validity_period_start': 'str',
        'target': 'str',
        'body': 'str',
        'title': 'str',
        'disabled': 'bool',
        'lang': 'str',
        'brand': 'str',
        'link_type': 'str',
        'race_type': 'str',
        'filename': 'UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentsfilenameYamlFilename',
        'uri_medium': 'str'
    }

    attribute_map = {
        'id': 'id',
        'sort_order': 'sortOrder',
        'validity_period_end': 'validityPeriodEnd',
        'validity_period_start': 'validityPeriodStart',
        'target': 'target',
        'body': 'body',
        'title': 'title',
        'disabled': 'disabled',
        'lang': 'lang',
        'brand': 'brand',
        'link_type': 'linkType',
        'race_type': 'raceType',
        'filename': 'filename',
        'uri_medium': 'uriMedium'
    }

    def __init__(self, id=None, sort_order=None, validity_period_end=None, validity_period_start=None, target=None, body=None, title=None, disabled=None, lang=None, brand=None, link_type=None, race_type=None, filename=None, uri_medium=None):  # noqa: E501
        """QuickLink2 - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._sort_order = None
        self._validity_period_end = None
        self._validity_period_start = None
        self._target = None
        self._body = None
        self._title = None
        self._disabled = None
        self._lang = None
        self._brand = None
        self._link_type = None
        self._race_type = None
        self._filename = None
        self._uri_medium = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if sort_order is not None:
            self.sort_order = sort_order
        if validity_period_end is not None:
            self.validity_period_end = validity_period_end
        if validity_period_start is not None:
            self.validity_period_start = validity_period_start
        if target is not None:
            self.target = target
        if body is not None:
            self.body = body
        if title is not None:
            self.title = title
        if disabled is not None:
            self.disabled = disabled
        if lang is not None:
            self.lang = lang
        if brand is not None:
            self.brand = brand
        if link_type is not None:
            self.link_type = link_type
        if race_type is not None:
            self.race_type = race_type
        if filename is not None:
            self.filename = filename
        if uri_medium is not None:
            self.uri_medium = uri_medium

    @property
    def id(self):
        """Gets the id of this QuickLink2.  # noqa: E501


        :return: The id of this QuickLink2.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this QuickLink2.


        :param id: The id of this QuickLink2.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def sort_order(self):
        """Gets the sort_order of this QuickLink2.  # noqa: E501


        :return: The sort_order of this QuickLink2.  # noqa: E501
        :rtype: float
        """
        return self._sort_order

    @sort_order.setter
    def sort_order(self, sort_order):
        """Sets the sort_order of this QuickLink2.


        :param sort_order: The sort_order of this QuickLink2.  # noqa: E501
        :type: float
        """

        self._sort_order = sort_order

    @property
    def validity_period_end(self):
        """Gets the validity_period_end of this QuickLink2.  # noqa: E501


        :return: The validity_period_end of this QuickLink2.  # noqa: E501
        :rtype: str
        """
        return self._validity_period_end

    @validity_period_end.setter
    def validity_period_end(self, validity_period_end):
        """Sets the validity_period_end of this QuickLink2.


        :param validity_period_end: The validity_period_end of this QuickLink2.  # noqa: E501
        :type: str
        """

        self._validity_period_end = validity_period_end

    @property
    def validity_period_start(self):
        """Gets the validity_period_start of this QuickLink2.  # noqa: E501


        :return: The validity_period_start of this QuickLink2.  # noqa: E501
        :rtype: str
        """
        return self._validity_period_start

    @validity_period_start.setter
    def validity_period_start(self, validity_period_start):
        """Sets the validity_period_start of this QuickLink2.


        :param validity_period_start: The validity_period_start of this QuickLink2.  # noqa: E501
        :type: str
        """

        self._validity_period_start = validity_period_start

    @property
    def target(self):
        """Gets the target of this QuickLink2.  # noqa: E501


        :return: The target of this QuickLink2.  # noqa: E501
        :rtype: str
        """
        return self._target

    @target.setter
    def target(self, target):
        """Sets the target of this QuickLink2.


        :param target: The target of this QuickLink2.  # noqa: E501
        :type: str
        """

        self._target = target

    @property
    def body(self):
        """Gets the body of this QuickLink2.  # noqa: E501


        :return: The body of this QuickLink2.  # noqa: E501
        :rtype: str
        """
        return self._body

    @body.setter
    def body(self, body):
        """Sets the body of this QuickLink2.


        :param body: The body of this QuickLink2.  # noqa: E501
        :type: str
        """

        self._body = body

    @property
    def title(self):
        """Gets the title of this QuickLink2.  # noqa: E501


        :return: The title of this QuickLink2.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this QuickLink2.


        :param title: The title of this QuickLink2.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def disabled(self):
        """Gets the disabled of this QuickLink2.  # noqa: E501


        :return: The disabled of this QuickLink2.  # noqa: E501
        :rtype: bool
        """
        return self._disabled

    @disabled.setter
    def disabled(self, disabled):
        """Sets the disabled of this QuickLink2.


        :param disabled: The disabled of this QuickLink2.  # noqa: E501
        :type: bool
        """

        self._disabled = disabled

    @property
    def lang(self):
        """Gets the lang of this QuickLink2.  # noqa: E501


        :return: The lang of this QuickLink2.  # noqa: E501
        :rtype: str
        """
        return self._lang

    @lang.setter
    def lang(self, lang):
        """Sets the lang of this QuickLink2.


        :param lang: The lang of this QuickLink2.  # noqa: E501
        :type: str
        """

        self._lang = lang

    @property
    def brand(self):
        """Gets the brand of this QuickLink2.  # noqa: E501


        :return: The brand of this QuickLink2.  # noqa: E501
        :rtype: str
        """
        return self._brand

    @brand.setter
    def brand(self, brand):
        """Sets the brand of this QuickLink2.


        :param brand: The brand of this QuickLink2.  # noqa: E501
        :type: str
        """

        self._brand = brand

    @property
    def link_type(self):
        """Gets the link_type of this QuickLink2.  # noqa: E501


        :return: The link_type of this QuickLink2.  # noqa: E501
        :rtype: str
        """
        return self._link_type

    @link_type.setter
    def link_type(self, link_type):
        """Sets the link_type of this QuickLink2.


        :param link_type: The link_type of this QuickLink2.  # noqa: E501
        :type: str
        """

        self._link_type = link_type

    @property
    def race_type(self):
        """Gets the race_type of this QuickLink2.  # noqa: E501


        :return: The race_type of this QuickLink2.  # noqa: E501
        :rtype: str
        """
        return self._race_type

    @race_type.setter
    def race_type(self, race_type):
        """Sets the race_type of this QuickLink2.


        :param race_type: The race_type of this QuickLink2.  # noqa: E501
        :type: str
        """

        self._race_type = race_type

    @property
    def filename(self):
        """Gets the filename of this QuickLink2.  # noqa: E501


        :return: The filename of this QuickLink2.  # noqa: E501
        :rtype: UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentsfilenameYamlFilename
        """
        return self._filename

    @filename.setter
    def filename(self, filename):
        """Sets the filename of this QuickLink2.


        :param filename: The filename of this QuickLink2.  # noqa: E501
        :type: UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentsfilenameYamlFilename
        """

        self._filename = filename

    @property
    def uri_medium(self):
        """Gets the uri_medium of this QuickLink2.  # noqa: E501


        :return: The uri_medium of this QuickLink2.  # noqa: E501
        :rtype: str
        """
        return self._uri_medium

    @uri_medium.setter
    def uri_medium(self, uri_medium):
        """Sets the uri_medium of this QuickLink2.


        :param uri_medium: The uri_medium of this QuickLink2.  # noqa: E501
        :type: str
        """

        self._uri_medium = uri_medium

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
        if issubclass(QuickLink2, dict):
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
        if not isinstance(other, QuickLink2):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
