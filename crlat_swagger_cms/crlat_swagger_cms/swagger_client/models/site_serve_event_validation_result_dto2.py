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


class SiteServeEventValidationResultDto2(object):
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
        'valid': 'list[UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentscompetitionSiteServeDataYamlSiteServeMinimalEventDto]',
        'invalid': 'list[str]'
    }

    attribute_map = {
        'valid': 'valid',
        'invalid': 'invalid'
    }

    def __init__(self, valid=None, invalid=None):  # noqa: E501
        """SiteServeEventValidationResultDto2 - a model defined in Swagger"""  # noqa: E501
        self._valid = None
        self._invalid = None
        self.discriminator = None
        if valid is not None:
            self.valid = valid
        if invalid is not None:
            self.invalid = invalid

    @property
    def valid(self):
        """Gets the valid of this SiteServeEventValidationResultDto2.  # noqa: E501


        :return: The valid of this SiteServeEventValidationResultDto2.  # noqa: E501
        :rtype: list[UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentscompetitionSiteServeDataYamlSiteServeMinimalEventDto]
        """
        return self._valid

    @valid.setter
    def valid(self, valid):
        """Sets the valid of this SiteServeEventValidationResultDto2.


        :param valid: The valid of this SiteServeEventValidationResultDto2.  # noqa: E501
        :type: list[UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentscompetitionSiteServeDataYamlSiteServeMinimalEventDto]
        """

        self._valid = valid

    @property
    def invalid(self):
        """Gets the invalid of this SiteServeEventValidationResultDto2.  # noqa: E501


        :return: The invalid of this SiteServeEventValidationResultDto2.  # noqa: E501
        :rtype: list[str]
        """
        return self._invalid

    @invalid.setter
    def invalid(self, invalid):
        """Sets the invalid of this SiteServeEventValidationResultDto2.


        :param invalid: The invalid of this SiteServeEventValidationResultDto2.  # noqa: E501
        :type: list[str]
        """

        self._invalid = invalid

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
        if issubclass(SiteServeEventValidationResultDto2, dict):
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
        if not isinstance(other, SiteServeEventValidationResultDto2):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
