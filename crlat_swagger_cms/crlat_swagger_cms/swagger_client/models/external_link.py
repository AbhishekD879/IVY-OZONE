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


class ExternalLink(object):
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
        'url': 'str',
        'brand': 'str',
        'target': 'str'
    }

    attribute_map = {
        'url': 'url',
        'brand': 'brand',
        'target': 'target'
    }

    def __init__(self, url=None, brand=None, target='NEW'):  # noqa: E501
        """ExternalLink - a model defined in Swagger"""  # noqa: E501
        self._url = None
        self._brand = None
        self._target = None
        self.discriminator = None
        if url is not None:
            self.url = url
        if brand is not None:
            self.brand = brand
        if target is not None:
            self.target = target

    @property
    def url(self):
        """Gets the url of this ExternalLink.  # noqa: E501


        :return: The url of this ExternalLink.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this ExternalLink.


        :param url: The url of this ExternalLink.  # noqa: E501
        :type: str
        """

        self._url = url

    @property
    def brand(self):
        """Gets the brand of this ExternalLink.  # noqa: E501


        :return: The brand of this ExternalLink.  # noqa: E501
        :rtype: str
        """
        return self._brand

    @brand.setter
    def brand(self, brand):
        """Sets the brand of this ExternalLink.


        :param brand: The brand of this ExternalLink.  # noqa: E501
        :type: str
        """

        self._brand = brand

    @property
    def target(self):
        """Gets the target of this ExternalLink.  # noqa: E501


        :return: The target of this ExternalLink.  # noqa: E501
        :rtype: str
        """
        return self._target

    @target.setter
    def target(self, target):
        """Sets the target of this ExternalLink.


        :param target: The target of this ExternalLink.  # noqa: E501
        :type: str
        """
        allowed_values = ["NEW", "CURRENT"]  # noqa: E501
        if target not in allowed_values:
            raise ValueError(
                "Invalid value for `target` ({0}), must be one of {1}"  # noqa: E501
                .format(target, allowed_values)
            )

        self._target = target

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
        if issubclass(ExternalLink, dict):
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
        if not isinstance(other, ExternalLink):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other