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


class SportsFeaturedTab(object):
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
        'name': 'str',
        'path': 'str',
        'category_id': 'str',
        'brand': 'str',
        'cms_modules_request_payload': 'list[UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentssimpleModuleYamlSimpleModule]',
        'disabled': 'bool'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'path': 'path',
        'category_id': 'categoryId',
        'brand': 'brand',
        'cms_modules_request_payload': 'cms_modules_request_payload',
        'disabled': 'disabled'
    }

    def __init__(self, id=None, name=None, path=None, category_id=None, brand=None, modules=None, disabled=None):  # noqa: E501
        """SportsFeaturedTab - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._name = None
        self._path = None
        self._category_id = None
        self._brand = None
        self._modules = None
        self._disabled = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if path is not None:
            self.path = path
        if category_id is not None:
            self.category_id = category_id
        if brand is not None:
            self.brand = brand
        if modules is not None:
            self.modules = modules
        if disabled is not None:
            self.disabled = disabled

    @property
    def id(self):
        """Gets the id of this SportsFeaturedTab.  # noqa: E501


        :return: The id of this SportsFeaturedTab.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this SportsFeaturedTab.


        :param id: The id of this SportsFeaturedTab.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this SportsFeaturedTab.  # noqa: E501


        :return: The name of this SportsFeaturedTab.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this SportsFeaturedTab.


        :param name: The name of this SportsFeaturedTab.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def path(self):
        """Gets the path of this SportsFeaturedTab.  # noqa: E501


        :return: The path of this SportsFeaturedTab.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this SportsFeaturedTab.


        :param path: The path of this SportsFeaturedTab.  # noqa: E501
        :type: str
        """

        self._path = path

    @property
    def category_id(self):
        """Gets the category_id of this SportsFeaturedTab.  # noqa: E501


        :return: The category_id of this SportsFeaturedTab.  # noqa: E501
        :rtype: str
        """
        return self._category_id

    @category_id.setter
    def category_id(self, category_id):
        """Sets the category_id of this SportsFeaturedTab.


        :param category_id: The category_id of this SportsFeaturedTab.  # noqa: E501
        :type: str
        """

        self._category_id = category_id

    @property
    def brand(self):
        """Gets the brand of this SportsFeaturedTab.  # noqa: E501


        :return: The brand of this SportsFeaturedTab.  # noqa: E501
        :rtype: str
        """
        return self._brand

    @brand.setter
    def brand(self, brand):
        """Sets the brand of this SportsFeaturedTab.


        :param brand: The brand of this SportsFeaturedTab.  # noqa: E501
        :type: str
        """

        self._brand = brand

    @property
    def modules(self):
        """Gets the cms_modules_request_payload of this SportsFeaturedTab.  # noqa: E501


        :return: The cms_modules_request_payload of this SportsFeaturedTab.  # noqa: E501
        :rtype: list[UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentssimpleModuleYamlSimpleModule]
        """
        return self._modules

    @modules.setter
    def modules(self, modules):
        """Sets the cms_modules_request_payload of this SportsFeaturedTab.


        :param modules: The cms_modules_request_payload of this SportsFeaturedTab.  # noqa: E501
        :type: list[UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentssimpleModuleYamlSimpleModule]
        """

        self._modules = modules

    @property
    def disabled(self):
        """Gets the disabled of this SportsFeaturedTab.  # noqa: E501


        :return: The disabled of this SportsFeaturedTab.  # noqa: E501
        :rtype: bool
        """
        return self._disabled

    @disabled.setter
    def disabled(self, disabled):
        """Sets the disabled of this SportsFeaturedTab.


        :param disabled: The disabled of this SportsFeaturedTab.  # noqa: E501
        :type: bool
        """

        self._disabled = disabled

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
        if issubclass(SportsFeaturedTab, dict):
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
        if not isinstance(other, SportsFeaturedTab):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other