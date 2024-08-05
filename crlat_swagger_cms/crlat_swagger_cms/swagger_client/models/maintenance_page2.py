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


class MaintenancePage2(object):
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
        'validity_period_end': 'str',
        'validity_period_start': 'str',
        'name': 'str',
        'desktop': 'bool',
        'tablet': 'bool',
        'mobile': 'bool',
        'target_uri': 'str',
        'brand': 'str',
        'filename': 'UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentsfilenameYamlFilename',
        'uri_medium': 'str',
        'uri_original': 'str'
    }

    attribute_map = {
        'id': 'id',
        'validity_period_end': 'validityPeriodEnd',
        'validity_period_start': 'validityPeriodStart',
        'name': 'name',
        'desktop': 'desktop',
        'tablet': 'tablet',
        'mobile': 'mobile',
        'target_uri': 'targetUri',
        'brand': 'brand',
        'filename': 'filename',
        'uri_medium': 'uriMedium',
        'uri_original': 'uriOriginal'
    }

    def __init__(self, id=None, validity_period_end=None, validity_period_start=None, name=None, desktop=None, tablet=None, mobile=None, target_uri=None, brand=None, filename=None, uri_medium=None, uri_original=None):  # noqa: E501
        """MaintenancePage2 - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._validity_period_end = None
        self._validity_period_start = None
        self._name = None
        self._desktop = None
        self._tablet = None
        self._mobile = None
        self._target_uri = None
        self._brand = None
        self._filename = None
        self._uri_medium = None
        self._uri_original = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if validity_period_end is not None:
            self.validity_period_end = validity_period_end
        if validity_period_start is not None:
            self.validity_period_start = validity_period_start
        if name is not None:
            self.name = name
        if desktop is not None:
            self.desktop = desktop
        if tablet is not None:
            self.tablet = tablet
        if mobile is not None:
            self.mobile = mobile
        if target_uri is not None:
            self.target_uri = target_uri
        if brand is not None:
            self.brand = brand
        if filename is not None:
            self.filename = filename
        if uri_medium is not None:
            self.uri_medium = uri_medium
        if uri_original is not None:
            self.uri_original = uri_original

    @property
    def id(self):
        """Gets the id of this MaintenancePage2.  # noqa: E501


        :return: The id of this MaintenancePage2.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this MaintenancePage2.


        :param id: The id of this MaintenancePage2.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def validity_period_end(self):
        """Gets the validity_period_end of this MaintenancePage2.  # noqa: E501


        :return: The validity_period_end of this MaintenancePage2.  # noqa: E501
        :rtype: str
        """
        return self._validity_period_end

    @validity_period_end.setter
    def validity_period_end(self, validity_period_end):
        """Sets the validity_period_end of this MaintenancePage2.


        :param validity_period_end: The validity_period_end of this MaintenancePage2.  # noqa: E501
        :type: str
        """

        self._validity_period_end = validity_period_end

    @property
    def validity_period_start(self):
        """Gets the validity_period_start of this MaintenancePage2.  # noqa: E501


        :return: The validity_period_start of this MaintenancePage2.  # noqa: E501
        :rtype: str
        """
        return self._validity_period_start

    @validity_period_start.setter
    def validity_period_start(self, validity_period_start):
        """Sets the validity_period_start of this MaintenancePage2.


        :param validity_period_start: The validity_period_start of this MaintenancePage2.  # noqa: E501
        :type: str
        """

        self._validity_period_start = validity_period_start

    @property
    def name(self):
        """Gets the name of this MaintenancePage2.  # noqa: E501


        :return: The name of this MaintenancePage2.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this MaintenancePage2.


        :param name: The name of this MaintenancePage2.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def desktop(self):
        """Gets the desktop of this MaintenancePage2.  # noqa: E501


        :return: The desktop of this MaintenancePage2.  # noqa: E501
        :rtype: bool
        """
        return self._desktop

    @desktop.setter
    def desktop(self, desktop):
        """Sets the desktop of this MaintenancePage2.


        :param desktop: The desktop of this MaintenancePage2.  # noqa: E501
        :type: bool
        """

        self._desktop = desktop

    @property
    def tablet(self):
        """Gets the tablet of this MaintenancePage2.  # noqa: E501


        :return: The tablet of this MaintenancePage2.  # noqa: E501
        :rtype: bool
        """
        return self._tablet

    @tablet.setter
    def tablet(self, tablet):
        """Sets the tablet of this MaintenancePage2.


        :param tablet: The tablet of this MaintenancePage2.  # noqa: E501
        :type: bool
        """

        self._tablet = tablet

    @property
    def mobile(self):
        """Gets the mobile of this MaintenancePage2.  # noqa: E501


        :return: The mobile of this MaintenancePage2.  # noqa: E501
        :rtype: bool
        """
        return self._mobile

    @mobile.setter
    def mobile(self, mobile):
        """Sets the mobile of this MaintenancePage2.


        :param mobile: The mobile of this MaintenancePage2.  # noqa: E501
        :type: bool
        """

        self._mobile = mobile

    @property
    def target_uri(self):
        """Gets the target_uri of this MaintenancePage2.  # noqa: E501


        :return: The target_uri of this MaintenancePage2.  # noqa: E501
        :rtype: str
        """
        return self._target_uri

    @target_uri.setter
    def target_uri(self, target_uri):
        """Sets the target_uri of this MaintenancePage2.


        :param target_uri: The target_uri of this MaintenancePage2.  # noqa: E501
        :type: str
        """

        self._target_uri = target_uri

    @property
    def brand(self):
        """Gets the brand of this MaintenancePage2.  # noqa: E501


        :return: The brand of this MaintenancePage2.  # noqa: E501
        :rtype: str
        """
        return self._brand

    @brand.setter
    def brand(self, brand):
        """Sets the brand of this MaintenancePage2.


        :param brand: The brand of this MaintenancePage2.  # noqa: E501
        :type: str
        """

        self._brand = brand

    @property
    def filename(self):
        """Gets the filename of this MaintenancePage2.  # noqa: E501


        :return: The filename of this MaintenancePage2.  # noqa: E501
        :rtype: UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentsfilenameYamlFilename
        """
        return self._filename

    @filename.setter
    def filename(self, filename):
        """Sets the filename of this MaintenancePage2.


        :param filename: The filename of this MaintenancePage2.  # noqa: E501
        :type: UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentsfilenameYamlFilename
        """

        self._filename = filename

    @property
    def uri_medium(self):
        """Gets the uri_medium of this MaintenancePage2.  # noqa: E501


        :return: The uri_medium of this MaintenancePage2.  # noqa: E501
        :rtype: str
        """
        return self._uri_medium

    @uri_medium.setter
    def uri_medium(self, uri_medium):
        """Sets the uri_medium of this MaintenancePage2.


        :param uri_medium: The uri_medium of this MaintenancePage2.  # noqa: E501
        :type: str
        """

        self._uri_medium = uri_medium

    @property
    def uri_original(self):
        """Gets the uri_original of this MaintenancePage2.  # noqa: E501


        :return: The uri_original of this MaintenancePage2.  # noqa: E501
        :rtype: str
        """
        return self._uri_original

    @uri_original.setter
    def uri_original(self, uri_original):
        """Sets the uri_original of this MaintenancePage2.


        :param uri_original: The uri_original of this MaintenancePage2.  # noqa: E501
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
        if issubclass(MaintenancePage2, dict):
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
        if not isinstance(other, MaintenancePage2):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
