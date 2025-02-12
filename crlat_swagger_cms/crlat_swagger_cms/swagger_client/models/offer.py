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


class Offer(object):
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
        'module': 'str',
        'vip_levels_input': 'str',
        'target_uri': 'str',
        'display_to': 'str',
        'display_from': 'str',
        'name': 'str',
        'vip_levels': 'list[float]',
        'brand': 'str',
        'disabled': 'bool',
        'show_offer_to': 'str',
        'show_offer_on': 'str',
        'use_direct_image_url': 'bool',
        'direct_image_url': 'str',
        'image': 'UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentsfilenameYamlFilename',
        'image_uri': 'str'
    }

    attribute_map = {
        'id': 'id',
        'sort_order': 'sortOrder',
        'module': 'module',
        'vip_levels_input': 'vipLevelsInput',
        'target_uri': 'targetUri',
        'display_to': 'displayTo',
        'display_from': 'displayFrom',
        'name': 'name',
        'vip_levels': 'vipLevels',
        'brand': 'brand',
        'disabled': 'disabled',
        'show_offer_to': 'showOfferTo',
        'show_offer_on': 'showOfferOn',
        'use_direct_image_url': 'useDirectImageUrl',
        'direct_image_url': 'directImageUrl',
        'image': 'image',
        'image_uri': 'imageUri'
    }

    def __init__(self, id=None, sort_order=None, module=None, vip_levels_input=None, target_uri=None, display_to=None, display_from=None, name=None, vip_levels=None, brand=None, disabled=None, show_offer_to=None, show_offer_on=None, use_direct_image_url=None, direct_image_url=None, image=None, image_uri=None):  # noqa: E501
        """Offer - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._sort_order = None
        self._module = None
        self._vip_levels_input = None
        self._target_uri = None
        self._display_to = None
        self._display_from = None
        self._name = None
        self._vip_levels = None
        self._brand = None
        self._disabled = None
        self._show_offer_to = None
        self._show_offer_on = None
        self._use_direct_image_url = None
        self._direct_image_url = None
        self._image = None
        self._image_uri = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if sort_order is not None:
            self.sort_order = sort_order
        if module is not None:
            self.module = module
        if vip_levels_input is not None:
            self.vip_levels_input = vip_levels_input
        if target_uri is not None:
            self.target_uri = target_uri
        if display_to is not None:
            self.display_to = display_to
        if display_from is not None:
            self.display_from = display_from
        if name is not None:
            self.name = name
        if vip_levels is not None:
            self.vip_levels = vip_levels
        if brand is not None:
            self.brand = brand
        if disabled is not None:
            self.disabled = disabled
        if show_offer_to is not None:
            self.show_offer_to = show_offer_to
        if show_offer_on is not None:
            self.show_offer_on = show_offer_on
        if use_direct_image_url is not None:
            self.use_direct_image_url = use_direct_image_url
        if direct_image_url is not None:
            self.direct_image_url = direct_image_url
        if image is not None:
            self.image = image
        if image_uri is not None:
            self.image_uri = image_uri

    @property
    def id(self):
        """Gets the id of this Offer.  # noqa: E501


        :return: The id of this Offer.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Offer.


        :param id: The id of this Offer.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def sort_order(self):
        """Gets the sort_order of this Offer.  # noqa: E501


        :return: The sort_order of this Offer.  # noqa: E501
        :rtype: float
        """
        return self._sort_order

    @sort_order.setter
    def sort_order(self, sort_order):
        """Sets the sort_order of this Offer.


        :param sort_order: The sort_order of this Offer.  # noqa: E501
        :type: float
        """

        self._sort_order = sort_order

    @property
    def module(self):
        """Gets the module of this Offer.  # noqa: E501


        :return: The module of this Offer.  # noqa: E501
        :rtype: str
        """
        return self._module

    @module.setter
    def module(self, module):
        """Sets the module of this Offer.


        :param module: The module of this Offer.  # noqa: E501
        :type: str
        """

        self._module = module

    @property
    def vip_levels_input(self):
        """Gets the vip_levels_input of this Offer.  # noqa: E501


        :return: The vip_levels_input of this Offer.  # noqa: E501
        :rtype: str
        """
        return self._vip_levels_input

    @vip_levels_input.setter
    def vip_levels_input(self, vip_levels_input):
        """Sets the vip_levels_input of this Offer.


        :param vip_levels_input: The vip_levels_input of this Offer.  # noqa: E501
        :type: str
        """

        self._vip_levels_input = vip_levels_input

    @property
    def target_uri(self):
        """Gets the target_uri of this Offer.  # noqa: E501


        :return: The target_uri of this Offer.  # noqa: E501
        :rtype: str
        """
        return self._target_uri

    @target_uri.setter
    def target_uri(self, target_uri):
        """Sets the target_uri of this Offer.


        :param target_uri: The target_uri of this Offer.  # noqa: E501
        :type: str
        """

        self._target_uri = target_uri

    @property
    def display_to(self):
        """Gets the display_to of this Offer.  # noqa: E501


        :return: The display_to of this Offer.  # noqa: E501
        :rtype: str
        """
        return self._display_to

    @display_to.setter
    def display_to(self, display_to):
        """Sets the display_to of this Offer.


        :param display_to: The display_to of this Offer.  # noqa: E501
        :type: str
        """

        self._display_to = display_to

    @property
    def display_from(self):
        """Gets the display_from of this Offer.  # noqa: E501


        :return: The display_from of this Offer.  # noqa: E501
        :rtype: str
        """
        return self._display_from

    @display_from.setter
    def display_from(self, display_from):
        """Sets the display_from of this Offer.


        :param display_from: The display_from of this Offer.  # noqa: E501
        :type: str
        """

        self._display_from = display_from

    @property
    def name(self):
        """Gets the name of this Offer.  # noqa: E501


        :return: The name of this Offer.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Offer.


        :param name: The name of this Offer.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def vip_levels(self):
        """Gets the vip_levels of this Offer.  # noqa: E501


        :return: The vip_levels of this Offer.  # noqa: E501
        :rtype: list[float]
        """
        return self._vip_levels

    @vip_levels.setter
    def vip_levels(self, vip_levels):
        """Sets the vip_levels of this Offer.


        :param vip_levels: The vip_levels of this Offer.  # noqa: E501
        :type: list[float]
        """

        self._vip_levels = vip_levels

    @property
    def brand(self):
        """Gets the brand of this Offer.  # noqa: E501


        :return: The brand of this Offer.  # noqa: E501
        :rtype: str
        """
        return self._brand

    @brand.setter
    def brand(self, brand):
        """Sets the brand of this Offer.


        :param brand: The brand of this Offer.  # noqa: E501
        :type: str
        """

        self._brand = brand

    @property
    def disabled(self):
        """Gets the disabled of this Offer.  # noqa: E501


        :return: The disabled of this Offer.  # noqa: E501
        :rtype: bool
        """
        return self._disabled

    @disabled.setter
    def disabled(self, disabled):
        """Sets the disabled of this Offer.


        :param disabled: The disabled of this Offer.  # noqa: E501
        :type: bool
        """

        self._disabled = disabled

    @property
    def show_offer_to(self):
        """Gets the show_offer_to of this Offer.  # noqa: E501


        :return: The show_offer_to of this Offer.  # noqa: E501
        :rtype: str
        """
        return self._show_offer_to

    @show_offer_to.setter
    def show_offer_to(self, show_offer_to):
        """Sets the show_offer_to of this Offer.


        :param show_offer_to: The show_offer_to of this Offer.  # noqa: E501
        :type: str
        """

        self._show_offer_to = show_offer_to

    @property
    def show_offer_on(self):
        """Gets the show_offer_on of this Offer.  # noqa: E501


        :return: The show_offer_on of this Offer.  # noqa: E501
        :rtype: str
        """
        return self._show_offer_on

    @show_offer_on.setter
    def show_offer_on(self, show_offer_on):
        """Sets the show_offer_on of this Offer.


        :param show_offer_on: The show_offer_on of this Offer.  # noqa: E501
        :type: str
        """

        self._show_offer_on = show_offer_on

    @property
    def use_direct_image_url(self):
        """Gets the use_direct_image_url of this Offer.  # noqa: E501


        :return: The use_direct_image_url of this Offer.  # noqa: E501
        :rtype: bool
        """
        return self._use_direct_image_url

    @use_direct_image_url.setter
    def use_direct_image_url(self, use_direct_image_url):
        """Sets the use_direct_image_url of this Offer.


        :param use_direct_image_url: The use_direct_image_url of this Offer.  # noqa: E501
        :type: bool
        """

        self._use_direct_image_url = use_direct_image_url

    @property
    def direct_image_url(self):
        """Gets the direct_image_url of this Offer.  # noqa: E501


        :return: The direct_image_url of this Offer.  # noqa: E501
        :rtype: str
        """
        return self._direct_image_url

    @direct_image_url.setter
    def direct_image_url(self, direct_image_url):
        """Sets the direct_image_url of this Offer.


        :param direct_image_url: The direct_image_url of this Offer.  # noqa: E501
        :type: str
        """

        self._direct_image_url = direct_image_url

    @property
    def image(self):
        """Gets the image of this Offer.  # noqa: E501


        :return: The image of this Offer.  # noqa: E501
        :rtype: UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentsfilenameYamlFilename
        """
        return self._image

    @image.setter
    def image(self, image):
        """Sets the image of this Offer.


        :param image: The image of this Offer.  # noqa: E501
        :type: UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentsfilenameYamlFilename
        """

        self._image = image

    @property
    def image_uri(self):
        """Gets the image_uri of this Offer.  # noqa: E501


        :return: The image_uri of this Offer.  # noqa: E501
        :rtype: str
        """
        return self._image_uri

    @image_uri.setter
    def image_uri(self, image_uri):
        """Sets the image_uri of this Offer.


        :param image_uri: The image_uri of this Offer.  # noqa: E501
        :type: str
        """

        self._image_uri = image_uri

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
        if issubclass(Offer, dict):
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
        if not isinstance(other, Offer):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
