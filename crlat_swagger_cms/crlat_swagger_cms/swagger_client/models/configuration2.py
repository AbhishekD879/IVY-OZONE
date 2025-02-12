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


class Configuration2(object):
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
        'config': 'list[UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentsconfigurationItemYamlConfigurationItem]'
    }

    attribute_map = {
        'id': 'id',
        'brand': 'brand',
        'config': 'config'
    }

    def __init__(self, id=None, brand=None, config=None):  # noqa: E501
        """Configuration2 - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._brand = None
        self._config = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if brand is not None:
            self.brand = brand
        if config is not None:
            self.config = config

    @property
    def id(self):
        """Gets the id of this Configuration2.  # noqa: E501


        :return: The id of this Configuration2.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Configuration2.


        :param id: The id of this Configuration2.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def brand(self):
        """Gets the brand of this Configuration2.  # noqa: E501


        :return: The brand of this Configuration2.  # noqa: E501
        :rtype: str
        """
        return self._brand

    @brand.setter
    def brand(self, brand):
        """Sets the brand of this Configuration2.


        :param brand: The brand of this Configuration2.  # noqa: E501
        :type: str
        """

        self._brand = brand

    @property
    def config(self):
        """Gets the config of this Configuration2.  # noqa: E501


        :return: The config of this Configuration2.  # noqa: E501
        :rtype: list[UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentsconfigurationItemYamlConfigurationItem]
        """
        return self._config

    @config.setter
    def config(self, config):
        """Sets the config of this Configuration2.


        :param config: The config of this Configuration2.  # noqa: E501
        :type: list[UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentsconfigurationItemYamlConfigurationItem]
        """

        self._config = config

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
        if issubclass(Configuration2, dict):
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
        if not isinstance(other, Configuration2):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
