# coding: utf-8

"""
    Api Documentation

    Api Documentation  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six


class CompetitionModuleDto(object):
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
        'max_display': 'int',
        'name': 'str',
        'type': 'str',
        'view_type': 'str'
    }

    attribute_map = {
        'id': 'id',
        'max_display': 'maxDisplay',
        'name': 'name',
        'type': 'type',
        'view_type': 'viewType'
    }

    def __init__(self, id=None, max_display=None, name=None, type=None, view_type=None):  # noqa: E501
        """CompetitionModuleDto - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._max_display = None
        self._name = None
        self._type = None
        self._view_type = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if max_display is not None:
            self.max_display = max_display
        if name is not None:
            self.name = name
        if type is not None:
            self.type = type
        if view_type is not None:
            self.view_type = view_type

    @property
    def id(self):
        """Gets the id of this CompetitionModuleDto.  # noqa: E501


        :return: The id of this CompetitionModuleDto.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this CompetitionModuleDto.


        :param id: The id of this CompetitionModuleDto.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def max_display(self):
        """Gets the max_display of this CompetitionModuleDto.  # noqa: E501


        :return: The max_display of this CompetitionModuleDto.  # noqa: E501
        :rtype: int
        """
        return self._max_display

    @max_display.setter
    def max_display(self, max_display):
        """Sets the max_display of this CompetitionModuleDto.


        :param max_display: The max_display of this CompetitionModuleDto.  # noqa: E501
        :type: int
        """

        self._max_display = max_display

    @property
    def name(self):
        """Gets the name of this CompetitionModuleDto.  # noqa: E501


        :return: The name of this CompetitionModuleDto.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CompetitionModuleDto.


        :param name: The name of this CompetitionModuleDto.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def type(self):
        """Gets the type of this CompetitionModuleDto.  # noqa: E501


        :return: The type of this CompetitionModuleDto.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this CompetitionModuleDto.


        :param type: The type of this CompetitionModuleDto.  # noqa: E501
        :type: str
        """
        allowed_values = ["AEM", "NEXT_EVENTS", "NEXT_EVENTS_INDIVIDUAL", "PROMOTIONS", "OUTRIGHTS", "SPECIALS", "SPECIALS_OVERVIEW", "GROUP_WIDGET", "GROUP_ALL", "GROUP_INDIVIDUAL", "RESULTS", "KNOCKOUTS"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def view_type(self):
        """Gets the view_type of this CompetitionModuleDto.  # noqa: E501


        :return: The view_type of this CompetitionModuleDto.  # noqa: E501
        :rtype: str
        """
        return self._view_type

    @view_type.setter
    def view_type(self, view_type):
        """Sets the view_type of this CompetitionModuleDto.


        :param view_type: The view_type of this CompetitionModuleDto.  # noqa: E501
        :type: str
        """
        allowed_values = ["LIST", "GRID", "CARD"]  # noqa: E501
        if view_type not in allowed_values:
            raise ValueError(
                "Invalid value for `view_type` ({0}), must be one of {1}"  # noqa: E501
                .format(view_type, allowed_values)
            )

        self._view_type = view_type

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
        if issubclass(CompetitionModuleDto, dict):
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
        if not isinstance(other, CompetitionModuleDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
