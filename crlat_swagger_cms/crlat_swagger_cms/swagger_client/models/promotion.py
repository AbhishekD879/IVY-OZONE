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


class Promotion(object):
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
        'promotion_id': 'str',
        'open_bet_id': 'str',
        'title_brand': 'str',
        'sort_order': 'float',
        'height_medium': 'float',
        'width_medium': 'float',
        'uri_medium': 'str',
        'html_markup': 'str',
        'promotion_text': 'str',
        'request_id': 'str',
        'vip_levels_input': 'str',
        'validity_period_end': 'str',
        'validity_period_start': 'str',
        'short_description': 'str',
        'promo_key': 'str',
        'title': 'str',
        'vip_levels': 'list[float]',
        'lang': 'str',
        'brand': 'str',
        'category_id': 'list[str]',
        'competition_id': 'list[str]',
        'show_to_customer': 'str',
        'disabled': 'bool',
        'description': 'str',
        'filename': 'UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentsfilenameYamlFilename',
        'is_signposting_promotion': 'bool',
        'overlay_bet_now_url': 'str'
    }

    attribute_map = {
        'id': 'id',
        'promotion_id': 'promotionId',
        'open_bet_id': 'openBetId',
        'title_brand': 'title_brand',
        'sort_order': 'sortOrder',
        'height_medium': 'heightMedium',
        'width_medium': 'widthMedium',
        'uri_medium': 'uriMedium',
        'html_markup': 'htmlMarkup',
        'promotion_text': 'promotionText',
        'request_id': 'requestId',
        'vip_levels_input': 'vipLevelsInput',
        'validity_period_end': 'validityPeriodEnd',
        'validity_period_start': 'validityPeriodStart',
        'short_description': 'shortDescription',
        'promo_key': 'promoKey',
        'title': 'title',
        'vip_levels': 'vipLevels',
        'lang': 'lang',
        'brand': 'brand',
        'category_id': 'categoryId',
        'competition_id': 'competitionId',
        'show_to_customer': 'showToCustomer',
        'disabled': 'disabled',
        'description': 'description',
        'filename': 'filename',
        'is_signposting_promotion': 'isSignpostingPromotion',
        'overlay_bet_now_url': 'overlayBetNowUrl'
    }

    def __init__(self, id=None, promotion_id=None, open_bet_id=None, title_brand=None, sort_order=None, height_medium=None, width_medium=None, uri_medium=None, html_markup=None, promotion_text=None, request_id=None, vip_levels_input=None, validity_period_end=None, validity_period_start=None, short_description=None, promo_key=None, title=None, vip_levels=None, lang=None, brand=None, category_id=None, competition_id=None, show_to_customer=None, disabled=None, description=None, filename=None, is_signposting_promotion=None, overlay_bet_now_url=None):  # noqa: E501
        """Promotion - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._promotion_id = None
        self._open_bet_id = None
        self._title_brand = None
        self._sort_order = None
        self._height_medium = None
        self._width_medium = None
        self._uri_medium = None
        self._html_markup = None
        self._promotion_text = None
        self._request_id = None
        self._vip_levels_input = None
        self._validity_period_end = None
        self._validity_period_start = None
        self._short_description = None
        self._promo_key = None
        self._title = None
        self._vip_levels = None
        self._lang = None
        self._brand = None
        self._category_id = None
        self._competition_id = None
        self._show_to_customer = None
        self._disabled = None
        self._description = None
        self._filename = None
        self._is_signposting_promotion = None
        self._overlay_bet_now_url = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if promotion_id is not None:
            self.promotion_id = promotion_id
        if open_bet_id is not None:
            self.open_bet_id = open_bet_id
        if title_brand is not None:
            self.title_brand = title_brand
        if sort_order is not None:
            self.sort_order = sort_order
        if height_medium is not None:
            self.height_medium = height_medium
        if width_medium is not None:
            self.width_medium = width_medium
        if uri_medium is not None:
            self.uri_medium = uri_medium
        if html_markup is not None:
            self.html_markup = html_markup
        if promotion_text is not None:
            self.promotion_text = promotion_text
        if request_id is not None:
            self.request_id = request_id
        if vip_levels_input is not None:
            self.vip_levels_input = vip_levels_input
        if validity_period_end is not None:
            self.validity_period_end = validity_period_end
        if validity_period_start is not None:
            self.validity_period_start = validity_period_start
        if short_description is not None:
            self.short_description = short_description
        if promo_key is not None:
            self.promo_key = promo_key
        if title is not None:
            self.title = title
        if vip_levels is not None:
            self.vip_levels = vip_levels
        if lang is not None:
            self.lang = lang
        if brand is not None:
            self.brand = brand
        if category_id is not None:
            self.category_id = category_id
        if competition_id is not None:
            self.competition_id = competition_id
        if show_to_customer is not None:
            self.show_to_customer = show_to_customer
        if disabled is not None:
            self.disabled = disabled
        if description is not None:
            self.description = description
        if filename is not None:
            self.filename = filename
        if is_signposting_promotion is not None:
            self.is_signposting_promotion = is_signposting_promotion
        if overlay_bet_now_url is not None:
            self.overlay_bet_now_url = overlay_bet_now_url

    @property
    def id(self):
        """Gets the id of this Promotion.  # noqa: E501


        :return: The id of this Promotion.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Promotion.


        :param id: The id of this Promotion.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def promotion_id(self):
        """Gets the promotion_id of this Promotion.  # noqa: E501


        :return: The promotion_id of this Promotion.  # noqa: E501
        :rtype: str
        """
        return self._promotion_id

    @promotion_id.setter
    def promotion_id(self, promotion_id):
        """Sets the promotion_id of this Promotion.


        :param promotion_id: The promotion_id of this Promotion.  # noqa: E501
        :type: str
        """

        self._promotion_id = promotion_id

    @property
    def open_bet_id(self):
        """Gets the open_bet_id of this Promotion.  # noqa: E501


        :return: The open_bet_id of this Promotion.  # noqa: E501
        :rtype: str
        """
        return self._open_bet_id

    @open_bet_id.setter
    def open_bet_id(self, open_bet_id):
        """Sets the open_bet_id of this Promotion.


        :param open_bet_id: The open_bet_id of this Promotion.  # noqa: E501
        :type: str
        """

        self._open_bet_id = open_bet_id

    @property
    def title_brand(self):
        """Gets the title_brand of this Promotion.  # noqa: E501


        :return: The title_brand of this Promotion.  # noqa: E501
        :rtype: str
        """
        return self._title_brand

    @title_brand.setter
    def title_brand(self, title_brand):
        """Sets the title_brand of this Promotion.


        :param title_brand: The title_brand of this Promotion.  # noqa: E501
        :type: str
        """

        self._title_brand = title_brand

    @property
    def sort_order(self):
        """Gets the sort_order of this Promotion.  # noqa: E501


        :return: The sort_order of this Promotion.  # noqa: E501
        :rtype: float
        """
        return self._sort_order

    @sort_order.setter
    def sort_order(self, sort_order):
        """Sets the sort_order of this Promotion.


        :param sort_order: The sort_order of this Promotion.  # noqa: E501
        :type: float
        """

        self._sort_order = sort_order

    @property
    def height_medium(self):
        """Gets the height_medium of this Promotion.  # noqa: E501


        :return: The height_medium of this Promotion.  # noqa: E501
        :rtype: float
        """
        return self._height_medium

    @height_medium.setter
    def height_medium(self, height_medium):
        """Sets the height_medium of this Promotion.


        :param height_medium: The height_medium of this Promotion.  # noqa: E501
        :type: float
        """

        self._height_medium = height_medium

    @property
    def width_medium(self):
        """Gets the width_medium of this Promotion.  # noqa: E501


        :return: The width_medium of this Promotion.  # noqa: E501
        :rtype: float
        """
        return self._width_medium

    @width_medium.setter
    def width_medium(self, width_medium):
        """Sets the width_medium of this Promotion.


        :param width_medium: The width_medium of this Promotion.  # noqa: E501
        :type: float
        """

        self._width_medium = width_medium

    @property
    def uri_medium(self):
        """Gets the uri_medium of this Promotion.  # noqa: E501


        :return: The uri_medium of this Promotion.  # noqa: E501
        :rtype: str
        """
        return self._uri_medium

    @uri_medium.setter
    def uri_medium(self, uri_medium):
        """Sets the uri_medium of this Promotion.


        :param uri_medium: The uri_medium of this Promotion.  # noqa: E501
        :type: str
        """

        self._uri_medium = uri_medium

    @property
    def html_markup(self):
        """Gets the html_markup of this Promotion.  # noqa: E501


        :return: The html_markup of this Promotion.  # noqa: E501
        :rtype: str
        """
        return self._html_markup

    @html_markup.setter
    def html_markup(self, html_markup):
        """Sets the html_markup of this Promotion.


        :param html_markup: The html_markup of this Promotion.  # noqa: E501
        :type: str
        """

        self._html_markup = html_markup

    @property
    def promotion_text(self):
        """Gets the promotion_text of this Promotion.  # noqa: E501


        :return: The promotion_text of this Promotion.  # noqa: E501
        :rtype: str
        """
        return self._promotion_text

    @promotion_text.setter
    def promotion_text(self, promotion_text):
        """Sets the promotion_text of this Promotion.


        :param promotion_text: The promotion_text of this Promotion.  # noqa: E501
        :type: str
        """

        self._promotion_text = promotion_text

    @property
    def request_id(self):
        """Gets the request_id of this Promotion.  # noqa: E501


        :return: The request_id of this Promotion.  # noqa: E501
        :rtype: str
        """
        return self._request_id

    @request_id.setter
    def request_id(self, request_id):
        """Sets the request_id of this Promotion.


        :param request_id: The request_id of this Promotion.  # noqa: E501
        :type: str
        """

        self._request_id = request_id

    @property
    def vip_levels_input(self):
        """Gets the vip_levels_input of this Promotion.  # noqa: E501


        :return: The vip_levels_input of this Promotion.  # noqa: E501
        :rtype: str
        """
        return self._vip_levels_input

    @vip_levels_input.setter
    def vip_levels_input(self, vip_levels_input):
        """Sets the vip_levels_input of this Promotion.


        :param vip_levels_input: The vip_levels_input of this Promotion.  # noqa: E501
        :type: str
        """

        self._vip_levels_input = vip_levels_input

    @property
    def validity_period_end(self):
        """Gets the validity_period_end of this Promotion.  # noqa: E501


        :return: The validity_period_end of this Promotion.  # noqa: E501
        :rtype: str
        """
        return self._validity_period_end

    @validity_period_end.setter
    def validity_period_end(self, validity_period_end):
        """Sets the validity_period_end of this Promotion.


        :param validity_period_end: The validity_period_end of this Promotion.  # noqa: E501
        :type: str
        """

        self._validity_period_end = validity_period_end

    @property
    def validity_period_start(self):
        """Gets the validity_period_start of this Promotion.  # noqa: E501


        :return: The validity_period_start of this Promotion.  # noqa: E501
        :rtype: str
        """
        return self._validity_period_start

    @validity_period_start.setter
    def validity_period_start(self, validity_period_start):
        """Sets the validity_period_start of this Promotion.


        :param validity_period_start: The validity_period_start of this Promotion.  # noqa: E501
        :type: str
        """

        self._validity_period_start = validity_period_start

    @property
    def short_description(self):
        """Gets the short_description of this Promotion.  # noqa: E501


        :return: The short_description of this Promotion.  # noqa: E501
        :rtype: str
        """
        return self._short_description

    @short_description.setter
    def short_description(self, short_description):
        """Sets the short_description of this Promotion.


        :param short_description: The short_description of this Promotion.  # noqa: E501
        :type: str
        """

        self._short_description = short_description

    @property
    def promo_key(self):
        """Gets the promo_key of this Promotion.  # noqa: E501


        :return: The promo_key of this Promotion.  # noqa: E501
        :rtype: str
        """
        return self._promo_key

    @promo_key.setter
    def promo_key(self, promo_key):
        """Sets the promo_key of this Promotion.


        :param promo_key: The promo_key of this Promotion.  # noqa: E501
        :type: str
        """

        self._promo_key = promo_key

    @property
    def title(self):
        """Gets the title of this Promotion.  # noqa: E501


        :return: The title of this Promotion.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this Promotion.


        :param title: The title of this Promotion.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def vip_levels(self):
        """Gets the vip_levels of this Promotion.  # noqa: E501


        :return: The vip_levels of this Promotion.  # noqa: E501
        :rtype: list[float]
        """
        return self._vip_levels

    @vip_levels.setter
    def vip_levels(self, vip_levels):
        """Sets the vip_levels of this Promotion.


        :param vip_levels: The vip_levels of this Promotion.  # noqa: E501
        :type: list[float]
        """

        self._vip_levels = vip_levels

    @property
    def lang(self):
        """Gets the lang of this Promotion.  # noqa: E501


        :return: The lang of this Promotion.  # noqa: E501
        :rtype: str
        """
        return self._lang

    @lang.setter
    def lang(self, lang):
        """Sets the lang of this Promotion.


        :param lang: The lang of this Promotion.  # noqa: E501
        :type: str
        """

        self._lang = lang

    @property
    def brand(self):
        """Gets the brand of this Promotion.  # noqa: E501


        :return: The brand of this Promotion.  # noqa: E501
        :rtype: str
        """
        return self._brand

    @brand.setter
    def brand(self, brand):
        """Sets the brand of this Promotion.


        :param brand: The brand of this Promotion.  # noqa: E501
        :type: str
        """

        self._brand = brand

    @property
    def category_id(self):
        """Gets the category_id of this Promotion.  # noqa: E501


        :return: The category_id of this Promotion.  # noqa: E501
        :rtype: list[str]
        """
        return self._category_id

    @category_id.setter
    def category_id(self, category_id):
        """Sets the category_id of this Promotion.


        :param category_id: The category_id of this Promotion.  # noqa: E501
        :type: list[str]
        """

        self._category_id = category_id

    @property
    def competition_id(self):
        """Gets the competition_id of this Promotion.  # noqa: E501


        :return: The competition_id of this Promotion.  # noqa: E501
        :rtype: list[str]
        """
        return self._competition_id

    @competition_id.setter
    def competition_id(self, competition_id):
        """Sets the competition_id of this Promotion.


        :param competition_id: The competition_id of this Promotion.  # noqa: E501
        :type: list[str]
        """

        self._competition_id = competition_id

    @property
    def show_to_customer(self):
        """Gets the show_to_customer of this Promotion.  # noqa: E501


        :return: The show_to_customer of this Promotion.  # noqa: E501
        :rtype: str
        """
        return self._show_to_customer

    @show_to_customer.setter
    def show_to_customer(self, show_to_customer):
        """Sets the show_to_customer of this Promotion.


        :param show_to_customer: The show_to_customer of this Promotion.  # noqa: E501
        :type: str
        """

        self._show_to_customer = show_to_customer

    @property
    def disabled(self):
        """Gets the disabled of this Promotion.  # noqa: E501


        :return: The disabled of this Promotion.  # noqa: E501
        :rtype: bool
        """
        return self._disabled

    @disabled.setter
    def disabled(self, disabled):
        """Sets the disabled of this Promotion.


        :param disabled: The disabled of this Promotion.  # noqa: E501
        :type: bool
        """

        self._disabled = disabled

    @property
    def description(self):
        """Gets the description of this Promotion.  # noqa: E501


        :return: The description of this Promotion.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Promotion.


        :param description: The description of this Promotion.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def filename(self):
        """Gets the filename of this Promotion.  # noqa: E501


        :return: The filename of this Promotion.  # noqa: E501
        :rtype: UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentsfilenameYamlFilename
        """
        return self._filename

    @filename.setter
    def filename(self, filename):
        """Sets the filename of this Promotion.


        :param filename: The filename of this Promotion.  # noqa: E501
        :type: UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentsfilenameYamlFilename
        """

        self._filename = filename

    @property
    def is_signposting_promotion(self):
        """Gets the is_signposting_promotion of this Promotion.  # noqa: E501


        :return: The is_signposting_promotion of this Promotion.  # noqa: E501
        :rtype: bool
        """
        return self._is_signposting_promotion

    @is_signposting_promotion.setter
    def is_signposting_promotion(self, is_signposting_promotion):
        """Sets the is_signposting_promotion of this Promotion.


        :param is_signposting_promotion: The is_signposting_promotion of this Promotion.  # noqa: E501
        :type: bool
        """

        self._is_signposting_promotion = is_signposting_promotion

    @property
    def overlay_bet_now_url(self):
        """Gets the overlay_bet_now_url of this Promotion.  # noqa: E501


        :return: The overlay_bet_now_url of this Promotion.  # noqa: E501
        :rtype: str
        """
        return self._overlay_bet_now_url

    @overlay_bet_now_url.setter
    def overlay_bet_now_url(self, overlay_bet_now_url):
        """Sets the overlay_bet_now_url of this Promotion.


        :param overlay_bet_now_url: The overlay_bet_now_url of this Promotion.  # noqa: E501
        :type: str
        """

        self._overlay_bet_now_url = overlay_bet_now_url

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
        if issubclass(Promotion, dict):
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
        if not isinstance(other, Promotion):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other