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


class Dashboard2(object):
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
        'estimated_time': 'str',
        'status': 'str',
        'purge_id': 'str',
        'progress_uri': 'str',
        'support_id': 'str',
        'type': 'str',
        'domains': 'str',
        'current_time': 'str',
        'brand': 'str'
    }

    attribute_map = {
        'id': 'id',
        'estimated_time': 'estimatedTime',
        'status': 'status',
        'purge_id': 'purgeID',
        'progress_uri': 'progressURI',
        'support_id': 'supportID',
        'type': 'type',
        'domains': 'domains',
        'current_time': 'currentTime',
        'brand': 'brand'
    }

    def __init__(self, id=None, estimated_time=None, status=None, purge_id=None, progress_uri=None, support_id=None, type=None, domains=None, current_time=None, brand=None):  # noqa: E501
        """Dashboard2 - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._estimated_time = None
        self._status = None
        self._purge_id = None
        self._progress_uri = None
        self._support_id = None
        self._type = None
        self._domains = None
        self._current_time = None
        self._brand = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if estimated_time is not None:
            self.estimated_time = estimated_time
        if status is not None:
            self.status = status
        if purge_id is not None:
            self.purge_id = purge_id
        if progress_uri is not None:
            self.progress_uri = progress_uri
        if support_id is not None:
            self.support_id = support_id
        if type is not None:
            self.type = type
        if domains is not None:
            self.domains = domains
        if current_time is not None:
            self.current_time = current_time
        if brand is not None:
            self.brand = brand

    @property
    def id(self):
        """Gets the id of this Dashboard2.  # noqa: E501


        :return: The id of this Dashboard2.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Dashboard2.


        :param id: The id of this Dashboard2.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def estimated_time(self):
        """Gets the estimated_time of this Dashboard2.  # noqa: E501


        :return: The estimated_time of this Dashboard2.  # noqa: E501
        :rtype: str
        """
        return self._estimated_time

    @estimated_time.setter
    def estimated_time(self, estimated_time):
        """Sets the estimated_time of this Dashboard2.


        :param estimated_time: The estimated_time of this Dashboard2.  # noqa: E501
        :type: str
        """

        self._estimated_time = estimated_time

    @property
    def status(self):
        """Gets the status of this Dashboard2.  # noqa: E501


        :return: The status of this Dashboard2.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Dashboard2.


        :param status: The status of this Dashboard2.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def purge_id(self):
        """Gets the purge_id of this Dashboard2.  # noqa: E501


        :return: The purge_id of this Dashboard2.  # noqa: E501
        :rtype: str
        """
        return self._purge_id

    @purge_id.setter
    def purge_id(self, purge_id):
        """Sets the purge_id of this Dashboard2.


        :param purge_id: The purge_id of this Dashboard2.  # noqa: E501
        :type: str
        """

        self._purge_id = purge_id

    @property
    def progress_uri(self):
        """Gets the progress_uri of this Dashboard2.  # noqa: E501


        :return: The progress_uri of this Dashboard2.  # noqa: E501
        :rtype: str
        """
        return self._progress_uri

    @progress_uri.setter
    def progress_uri(self, progress_uri):
        """Sets the progress_uri of this Dashboard2.


        :param progress_uri: The progress_uri of this Dashboard2.  # noqa: E501
        :type: str
        """

        self._progress_uri = progress_uri

    @property
    def support_id(self):
        """Gets the support_id of this Dashboard2.  # noqa: E501


        :return: The support_id of this Dashboard2.  # noqa: E501
        :rtype: str
        """
        return self._support_id

    @support_id.setter
    def support_id(self, support_id):
        """Sets the support_id of this Dashboard2.


        :param support_id: The support_id of this Dashboard2.  # noqa: E501
        :type: str
        """

        self._support_id = support_id

    @property
    def type(self):
        """Gets the type of this Dashboard2.  # noqa: E501


        :return: The type of this Dashboard2.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Dashboard2.


        :param type: The type of this Dashboard2.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def domains(self):
        """Gets the domains of this Dashboard2.  # noqa: E501


        :return: The domains of this Dashboard2.  # noqa: E501
        :rtype: str
        """
        return self._domains

    @domains.setter
    def domains(self, domains):
        """Sets the domains of this Dashboard2.


        :param domains: The domains of this Dashboard2.  # noqa: E501
        :type: str
        """

        self._domains = domains

    @property
    def current_time(self):
        """Gets the current_time of this Dashboard2.  # noqa: E501


        :return: The current_time of this Dashboard2.  # noqa: E501
        :rtype: str
        """
        return self._current_time

    @current_time.setter
    def current_time(self, current_time):
        """Sets the current_time of this Dashboard2.


        :param current_time: The current_time of this Dashboard2.  # noqa: E501
        :type: str
        """

        self._current_time = current_time

    @property
    def brand(self):
        """Gets the brand of this Dashboard2.  # noqa: E501


        :return: The brand of this Dashboard2.  # noqa: E501
        :rtype: str
        """
        return self._brand

    @brand.setter
    def brand(self, brand):
        """Sets the brand of this Dashboard2.


        :param brand: The brand of this Dashboard2.  # noqa: E501
        :type: str
        """

        self._brand = brand

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
        if issubclass(Dashboard2, dict):
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
        if not isinstance(other, Dashboard2):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
