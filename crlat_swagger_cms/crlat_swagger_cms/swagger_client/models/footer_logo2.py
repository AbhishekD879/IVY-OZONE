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


class FooterLogo2(object):
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
        'title': 'str',
        'target': 'str',
        'disabled': 'bool',
        'lang': 'str',
        'brand': 'str',
        'svg': 'str',
        'svg_id': 'str',
        'svg_filename': 'UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentssvgFilenameYamlSvgFilename',
        'filename': 'UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentsfilenameYamlFilename',
        'uri_medium': 'str',
        'uri_original': 'str'
    }

    attribute_map = {
        'id': 'id',
        'sort_order': 'sortOrder',
        'title': 'title',
        'target': 'target',
        'disabled': 'disabled',
        'lang': 'lang',
        'brand': 'brand',
        'svg': 'svg',
        'svg_id': 'svgId',
        'svg_filename': 'svgFilename',
        'filename': 'filename',
        'uri_medium': 'uriMedium',
        'uri_original': 'uriOriginal'
    }

    def __init__(self, id=None, sort_order=None, title=None, target=None, disabled=None, lang=None, brand=None, svg=None, svg_id=None, svg_filename=None, filename=None, uri_medium=None, uri_original=None):  # noqa: E501
        """FooterLogo2 - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._sort_order = None
        self._title = None
        self._target = None
        self._disabled = None
        self._lang = None
        self._brand = None
        self._svg = None
        self._svg_id = None
        self._svg_filename = None
        self._filename = None
        self._uri_medium = None
        self._uri_original = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if sort_order is not None:
            self.sort_order = sort_order
        if title is not None:
            self.title = title
        if target is not None:
            self.target = target
        if disabled is not None:
            self.disabled = disabled
        if lang is not None:
            self.lang = lang
        if brand is not None:
            self.brand = brand
        if svg is not None:
            self.svg = svg
        if svg_id is not None:
            self.svg_id = svg_id
        if svg_filename is not None:
            self.svg_filename = svg_filename
        if filename is not None:
            self.filename = filename
        if uri_medium is not None:
            self.uri_medium = uri_medium
        if uri_original is not None:
            self.uri_original = uri_original

    @property
    def id(self):
        """Gets the id of this FooterLogo2.  # noqa: E501


        :return: The id of this FooterLogo2.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this FooterLogo2.


        :param id: The id of this FooterLogo2.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def sort_order(self):
        """Gets the sort_order of this FooterLogo2.  # noqa: E501


        :return: The sort_order of this FooterLogo2.  # noqa: E501
        :rtype: float
        """
        return self._sort_order

    @sort_order.setter
    def sort_order(self, sort_order):
        """Sets the sort_order of this FooterLogo2.


        :param sort_order: The sort_order of this FooterLogo2.  # noqa: E501
        :type: float
        """

        self._sort_order = sort_order

    @property
    def title(self):
        """Gets the title of this FooterLogo2.  # noqa: E501


        :return: The title of this FooterLogo2.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this FooterLogo2.


        :param title: The title of this FooterLogo2.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def target(self):
        """Gets the target of this FooterLogo2.  # noqa: E501


        :return: The target of this FooterLogo2.  # noqa: E501
        :rtype: str
        """
        return self._target

    @target.setter
    def target(self, target):
        """Sets the target of this FooterLogo2.


        :param target: The target of this FooterLogo2.  # noqa: E501
        :type: str
        """

        self._target = target

    @property
    def disabled(self):
        """Gets the disabled of this FooterLogo2.  # noqa: E501


        :return: The disabled of this FooterLogo2.  # noqa: E501
        :rtype: bool
        """
        return self._disabled

    @disabled.setter
    def disabled(self, disabled):
        """Sets the disabled of this FooterLogo2.


        :param disabled: The disabled of this FooterLogo2.  # noqa: E501
        :type: bool
        """

        self._disabled = disabled

    @property
    def lang(self):
        """Gets the lang of this FooterLogo2.  # noqa: E501


        :return: The lang of this FooterLogo2.  # noqa: E501
        :rtype: str
        """
        return self._lang

    @lang.setter
    def lang(self, lang):
        """Sets the lang of this FooterLogo2.


        :param lang: The lang of this FooterLogo2.  # noqa: E501
        :type: str
        """

        self._lang = lang

    @property
    def brand(self):
        """Gets the brand of this FooterLogo2.  # noqa: E501


        :return: The brand of this FooterLogo2.  # noqa: E501
        :rtype: str
        """
        return self._brand

    @brand.setter
    def brand(self, brand):
        """Sets the brand of this FooterLogo2.


        :param brand: The brand of this FooterLogo2.  # noqa: E501
        :type: str
        """

        self._brand = brand

    @property
    def svg(self):
        """Gets the svg of this FooterLogo2.  # noqa: E501


        :return: The svg of this FooterLogo2.  # noqa: E501
        :rtype: str
        """
        return self._svg

    @svg.setter
    def svg(self, svg):
        """Sets the svg of this FooterLogo2.


        :param svg: The svg of this FooterLogo2.  # noqa: E501
        :type: str
        """

        self._svg = svg

    @property
    def svg_id(self):
        """Gets the svg_id of this FooterLogo2.  # noqa: E501


        :return: The svg_id of this FooterLogo2.  # noqa: E501
        :rtype: str
        """
        return self._svg_id

    @svg_id.setter
    def svg_id(self, svg_id):
        """Sets the svg_id of this FooterLogo2.


        :param svg_id: The svg_id of this FooterLogo2.  # noqa: E501
        :type: str
        """

        self._svg_id = svg_id

    @property
    def svg_filename(self):
        """Gets the svg_filename of this FooterLogo2.  # noqa: E501


        :return: The svg_filename of this FooterLogo2.  # noqa: E501
        :rtype: UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentssvgFilenameYamlSvgFilename
        """
        return self._svg_filename

    @svg_filename.setter
    def svg_filename(self, svg_filename):
        """Sets the svg_filename of this FooterLogo2.


        :param svg_filename: The svg_filename of this FooterLogo2.  # noqa: E501
        :type: UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentssvgFilenameYamlSvgFilename
        """

        self._svg_filename = svg_filename

    @property
    def filename(self):
        """Gets the filename of this FooterLogo2.  # noqa: E501


        :return: The filename of this FooterLogo2.  # noqa: E501
        :rtype: UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentsfilenameYamlFilename
        """
        return self._filename

    @filename.setter
    def filename(self, filename):
        """Sets the filename of this FooterLogo2.


        :param filename: The filename of this FooterLogo2.  # noqa: E501
        :type: UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentsfilenameYamlFilename
        """

        self._filename = filename

    @property
    def uri_medium(self):
        """Gets the uri_medium of this FooterLogo2.  # noqa: E501


        :return: The uri_medium of this FooterLogo2.  # noqa: E501
        :rtype: str
        """
        return self._uri_medium

    @uri_medium.setter
    def uri_medium(self, uri_medium):
        """Sets the uri_medium of this FooterLogo2.


        :param uri_medium: The uri_medium of this FooterLogo2.  # noqa: E501
        :type: str
        """

        self._uri_medium = uri_medium

    @property
    def uri_original(self):
        """Gets the uri_original of this FooterLogo2.  # noqa: E501


        :return: The uri_original of this FooterLogo2.  # noqa: E501
        :rtype: str
        """
        return self._uri_original

    @uri_original.setter
    def uri_original(self, uri_original):
        """Sets the uri_original of this FooterLogo2.


        :param uri_original: The uri_original of this FooterLogo2.  # noqa: E501
        :type: str
        """

        self._uri_original = uri_original

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
        if issubclass(FooterLogo2, dict):
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
        if not isinstance(other, FooterLogo2):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other