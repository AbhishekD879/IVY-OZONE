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


class FooterMenu2(object):
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
        'desktop': 'bool',
        'disabled': 'bool',
        'filename': 'UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentssvgFilenameYamlSvgFilename',
        'height_medium': 'float',
        'height_small': 'float',
        'image_title': 'str',
        'image_title_brand': 'str',
        'in_app': 'bool',
        'lang': 'str',
        'link_title': 'str',
        'link_title_brand': 'str',
        'mobile': 'bool',
        'path': 'str',
        'show_item_for': 'str',
        'sort_order': 'float',
        'sprite_class': 'str',
        'svg': 'str',
        'svg_filename': 'UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentssvgFilenameYamlSvgFilename',
        'svg_id': 'str',
        'tablet': 'bool',
        'target_uri': 'str',
        'uri_medium': 'str',
        'uri_small': 'str',
        'width_medium': 'float',
        'width_small': 'float',
        'collection_type': 'str',
        'item_type': 'str',
        'height_large': 'float',
        'width_large': 'float',
        'uri_large': 'str',
        'auth_required': 'bool',
        'system_id': 'float'
    }

    attribute_map = {
        'id': 'id',
        'brand': 'brand',
        'desktop': 'desktop',
        'disabled': 'disabled',
        'filename': 'filename',
        'height_medium': 'heightMedium',
        'height_small': 'heightSmall',
        'image_title': 'imageTitle',
        'image_title_brand': 'imageTitle_brand',
        'in_app': 'inApp',
        'lang': 'lang',
        'link_title': 'linkTitle',
        'link_title_brand': 'linkTitle_brand',
        'mobile': 'mobile',
        'path': 'path',
        'show_item_for': 'showItemFor',
        'sort_order': 'sortOrder',
        'sprite_class': 'spriteClass',
        'svg': 'svg',
        'svg_filename': 'svgFilename',
        'svg_id': 'svgId',
        'tablet': 'tablet',
        'target_uri': 'targetUri',
        'uri_medium': 'uriMedium',
        'uri_small': 'uriSmall',
        'width_medium': 'widthMedium',
        'width_small': 'widthSmall',
        'collection_type': 'collectionType',
        'item_type': 'itemType',
        'height_large': 'heightLarge',
        'width_large': 'widthLarge',
        'uri_large': 'uriLarge',
        'auth_required': 'authRequired',
        'system_id': 'systemID'
    }

    def __init__(self, id=None, brand=None, desktop=None, disabled=None, filename=None, height_medium=None, height_small=None, image_title=None, image_title_brand=None, in_app=None, lang=None, link_title=None, link_title_brand=None, mobile=None, path=None, show_item_for=None, sort_order=None, sprite_class=None, svg=None, svg_filename=None, svg_id=None, tablet=None, target_uri=None, uri_medium=None, uri_small=None, width_medium=None, width_small=None, collection_type=None, item_type=None, height_large=None, width_large=None, uri_large=None, auth_required=None, system_id=None):  # noqa: E501
        """FooterMenu2 - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._brand = None
        self._desktop = None
        self._disabled = None
        self._filename = None
        self._height_medium = None
        self._height_small = None
        self._image_title = None
        self._image_title_brand = None
        self._in_app = None
        self._lang = None
        self._link_title = None
        self._link_title_brand = None
        self._mobile = None
        self._path = None
        self._show_item_for = None
        self._sort_order = None
        self._sprite_class = None
        self._svg = None
        self._svg_filename = None
        self._svg_id = None
        self._tablet = None
        self._target_uri = None
        self._uri_medium = None
        self._uri_small = None
        self._width_medium = None
        self._width_small = None
        self._collection_type = None
        self._item_type = None
        self._height_large = None
        self._width_large = None
        self._uri_large = None
        self._auth_required = None
        self._system_id = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if brand is not None:
            self.brand = brand
        if desktop is not None:
            self.desktop = desktop
        if disabled is not None:
            self.disabled = disabled
        if filename is not None:
            self.filename = filename
        if height_medium is not None:
            self.height_medium = height_medium
        if height_small is not None:
            self.height_small = height_small
        if image_title is not None:
            self.image_title = image_title
        if image_title_brand is not None:
            self.image_title_brand = image_title_brand
        if in_app is not None:
            self.in_app = in_app
        if lang is not None:
            self.lang = lang
        if link_title is not None:
            self.link_title = link_title
        if link_title_brand is not None:
            self.link_title_brand = link_title_brand
        if mobile is not None:
            self.mobile = mobile
        if path is not None:
            self.path = path
        if show_item_for is not None:
            self.show_item_for = show_item_for
        if sort_order is not None:
            self.sort_order = sort_order
        if sprite_class is not None:
            self.sprite_class = sprite_class
        if svg is not None:
            self.svg = svg
        if svg_filename is not None:
            self.svg_filename = svg_filename
        if svg_id is not None:
            self.svg_id = svg_id
        if tablet is not None:
            self.tablet = tablet
        if target_uri is not None:
            self.target_uri = target_uri
        if uri_medium is not None:
            self.uri_medium = uri_medium
        if uri_small is not None:
            self.uri_small = uri_small
        if width_medium is not None:
            self.width_medium = width_medium
        if width_small is not None:
            self.width_small = width_small
        if collection_type is not None:
            self.collection_type = collection_type
        if item_type is not None:
            self.item_type = item_type
        if height_large is not None:
            self.height_large = height_large
        if width_large is not None:
            self.width_large = width_large
        if uri_large is not None:
            self.uri_large = uri_large
        if auth_required is not None:
            self.auth_required = auth_required
        if system_id is not None:
            self.system_id = system_id

    @property
    def id(self):
        """Gets the id of this FooterMenu2.  # noqa: E501


        :return: The id of this FooterMenu2.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this FooterMenu2.


        :param id: The id of this FooterMenu2.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def brand(self):
        """Gets the brand of this FooterMenu2.  # noqa: E501


        :return: The brand of this FooterMenu2.  # noqa: E501
        :rtype: str
        """
        return self._brand

    @brand.setter
    def brand(self, brand):
        """Sets the brand of this FooterMenu2.


        :param brand: The brand of this FooterMenu2.  # noqa: E501
        :type: str
        """

        self._brand = brand

    @property
    def desktop(self):
        """Gets the desktop of this FooterMenu2.  # noqa: E501


        :return: The desktop of this FooterMenu2.  # noqa: E501
        :rtype: bool
        """
        return self._desktop

    @desktop.setter
    def desktop(self, desktop):
        """Sets the desktop of this FooterMenu2.


        :param desktop: The desktop of this FooterMenu2.  # noqa: E501
        :type: bool
        """

        self._desktop = desktop

    @property
    def disabled(self):
        """Gets the disabled of this FooterMenu2.  # noqa: E501


        :return: The disabled of this FooterMenu2.  # noqa: E501
        :rtype: bool
        """
        return self._disabled

    @disabled.setter
    def disabled(self, disabled):
        """Sets the disabled of this FooterMenu2.


        :param disabled: The disabled of this FooterMenu2.  # noqa: E501
        :type: bool
        """

        self._disabled = disabled

    @property
    def filename(self):
        """Gets the filename of this FooterMenu2.  # noqa: E501


        :return: The filename of this FooterMenu2.  # noqa: E501
        :rtype: UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentssvgFilenameYamlSvgFilename
        """
        return self._filename

    @filename.setter
    def filename(self, filename):
        """Sets the filename of this FooterMenu2.


        :param filename: The filename of this FooterMenu2.  # noqa: E501
        :type: UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentssvgFilenameYamlSvgFilename
        """

        self._filename = filename

    @property
    def height_medium(self):
        """Gets the height_medium of this FooterMenu2.  # noqa: E501


        :return: The height_medium of this FooterMenu2.  # noqa: E501
        :rtype: float
        """
        return self._height_medium

    @height_medium.setter
    def height_medium(self, height_medium):
        """Sets the height_medium of this FooterMenu2.


        :param height_medium: The height_medium of this FooterMenu2.  # noqa: E501
        :type: float
        """

        self._height_medium = height_medium

    @property
    def height_small(self):
        """Gets the height_small of this FooterMenu2.  # noqa: E501


        :return: The height_small of this FooterMenu2.  # noqa: E501
        :rtype: float
        """
        return self._height_small

    @height_small.setter
    def height_small(self, height_small):
        """Sets the height_small of this FooterMenu2.


        :param height_small: The height_small of this FooterMenu2.  # noqa: E501
        :type: float
        """

        self._height_small = height_small

    @property
    def image_title(self):
        """Gets the image_title of this FooterMenu2.  # noqa: E501


        :return: The image_title of this FooterMenu2.  # noqa: E501
        :rtype: str
        """
        return self._image_title

    @image_title.setter
    def image_title(self, image_title):
        """Sets the image_title of this FooterMenu2.


        :param image_title: The image_title of this FooterMenu2.  # noqa: E501
        :type: str
        """

        self._image_title = image_title

    @property
    def image_title_brand(self):
        """Gets the image_title_brand of this FooterMenu2.  # noqa: E501


        :return: The image_title_brand of this FooterMenu2.  # noqa: E501
        :rtype: str
        """
        return self._image_title_brand

    @image_title_brand.setter
    def image_title_brand(self, image_title_brand):
        """Sets the image_title_brand of this FooterMenu2.


        :param image_title_brand: The image_title_brand of this FooterMenu2.  # noqa: E501
        :type: str
        """

        self._image_title_brand = image_title_brand

    @property
    def in_app(self):
        """Gets the in_app of this FooterMenu2.  # noqa: E501


        :return: The in_app of this FooterMenu2.  # noqa: E501
        :rtype: bool
        """
        return self._in_app

    @in_app.setter
    def in_app(self, in_app):
        """Sets the in_app of this FooterMenu2.


        :param in_app: The in_app of this FooterMenu2.  # noqa: E501
        :type: bool
        """

        self._in_app = in_app

    @property
    def lang(self):
        """Gets the lang of this FooterMenu2.  # noqa: E501


        :return: The lang of this FooterMenu2.  # noqa: E501
        :rtype: str
        """
        return self._lang

    @lang.setter
    def lang(self, lang):
        """Sets the lang of this FooterMenu2.


        :param lang: The lang of this FooterMenu2.  # noqa: E501
        :type: str
        """

        self._lang = lang

    @property
    def link_title(self):
        """Gets the link_title of this FooterMenu2.  # noqa: E501


        :return: The link_title of this FooterMenu2.  # noqa: E501
        :rtype: str
        """
        return self._link_title

    @link_title.setter
    def link_title(self, link_title):
        """Sets the link_title of this FooterMenu2.


        :param link_title: The link_title of this FooterMenu2.  # noqa: E501
        :type: str
        """

        self._link_title = link_title

    @property
    def link_title_brand(self):
        """Gets the link_title_brand of this FooterMenu2.  # noqa: E501


        :return: The link_title_brand of this FooterMenu2.  # noqa: E501
        :rtype: str
        """
        return self._link_title_brand

    @link_title_brand.setter
    def link_title_brand(self, link_title_brand):
        """Sets the link_title_brand of this FooterMenu2.


        :param link_title_brand: The link_title_brand of this FooterMenu2.  # noqa: E501
        :type: str
        """

        self._link_title_brand = link_title_brand

    @property
    def mobile(self):
        """Gets the mobile of this FooterMenu2.  # noqa: E501


        :return: The mobile of this FooterMenu2.  # noqa: E501
        :rtype: bool
        """
        return self._mobile

    @mobile.setter
    def mobile(self, mobile):
        """Sets the mobile of this FooterMenu2.


        :param mobile: The mobile of this FooterMenu2.  # noqa: E501
        :type: bool
        """

        self._mobile = mobile

    @property
    def path(self):
        """Gets the path of this FooterMenu2.  # noqa: E501


        :return: The path of this FooterMenu2.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this FooterMenu2.


        :param path: The path of this FooterMenu2.  # noqa: E501
        :type: str
        """

        self._path = path

    @property
    def show_item_for(self):
        """Gets the show_item_for of this FooterMenu2.  # noqa: E501


        :return: The show_item_for of this FooterMenu2.  # noqa: E501
        :rtype: str
        """
        return self._show_item_for

    @show_item_for.setter
    def show_item_for(self, show_item_for):
        """Sets the show_item_for of this FooterMenu2.


        :param show_item_for: The show_item_for of this FooterMenu2.  # noqa: E501
        :type: str
        """

        self._show_item_for = show_item_for

    @property
    def sort_order(self):
        """Gets the sort_order of this FooterMenu2.  # noqa: E501


        :return: The sort_order of this FooterMenu2.  # noqa: E501
        :rtype: float
        """
        return self._sort_order

    @sort_order.setter
    def sort_order(self, sort_order):
        """Sets the sort_order of this FooterMenu2.


        :param sort_order: The sort_order of this FooterMenu2.  # noqa: E501
        :type: float
        """

        self._sort_order = sort_order

    @property
    def sprite_class(self):
        """Gets the sprite_class of this FooterMenu2.  # noqa: E501


        :return: The sprite_class of this FooterMenu2.  # noqa: E501
        :rtype: str
        """
        return self._sprite_class

    @sprite_class.setter
    def sprite_class(self, sprite_class):
        """Sets the sprite_class of this FooterMenu2.


        :param sprite_class: The sprite_class of this FooterMenu2.  # noqa: E501
        :type: str
        """

        self._sprite_class = sprite_class

    @property
    def svg(self):
        """Gets the svg of this FooterMenu2.  # noqa: E501


        :return: The svg of this FooterMenu2.  # noqa: E501
        :rtype: str
        """
        return self._svg

    @svg.setter
    def svg(self, svg):
        """Sets the svg of this FooterMenu2.


        :param svg: The svg of this FooterMenu2.  # noqa: E501
        :type: str
        """

        self._svg = svg

    @property
    def svg_filename(self):
        """Gets the svg_filename of this FooterMenu2.  # noqa: E501


        :return: The svg_filename of this FooterMenu2.  # noqa: E501
        :rtype: UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentssvgFilenameYamlSvgFilename
        """
        return self._svg_filename

    @svg_filename.setter
    def svg_filename(self, svg_filename):
        """Sets the svg_filename of this FooterMenu2.


        :param svg_filename: The svg_filename of this FooterMenu2.  # noqa: E501
        :type: UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentssvgFilenameYamlSvgFilename
        """

        self._svg_filename = svg_filename

    @property
    def svg_id(self):
        """Gets the svg_id of this FooterMenu2.  # noqa: E501


        :return: The svg_id of this FooterMenu2.  # noqa: E501
        :rtype: str
        """
        return self._svg_id

    @svg_id.setter
    def svg_id(self, svg_id):
        """Sets the svg_id of this FooterMenu2.


        :param svg_id: The svg_id of this FooterMenu2.  # noqa: E501
        :type: str
        """

        self._svg_id = svg_id

    @property
    def tablet(self):
        """Gets the tablet of this FooterMenu2.  # noqa: E501


        :return: The tablet of this FooterMenu2.  # noqa: E501
        :rtype: bool
        """
        return self._tablet

    @tablet.setter
    def tablet(self, tablet):
        """Sets the tablet of this FooterMenu2.


        :param tablet: The tablet of this FooterMenu2.  # noqa: E501
        :type: bool
        """

        self._tablet = tablet

    @property
    def target_uri(self):
        """Gets the target_uri of this FooterMenu2.  # noqa: E501


        :return: The target_uri of this FooterMenu2.  # noqa: E501
        :rtype: str
        """
        return self._target_uri

    @target_uri.setter
    def target_uri(self, target_uri):
        """Sets the target_uri of this FooterMenu2.


        :param target_uri: The target_uri of this FooterMenu2.  # noqa: E501
        :type: str
        """

        self._target_uri = target_uri

    @property
    def uri_medium(self):
        """Gets the uri_medium of this FooterMenu2.  # noqa: E501


        :return: The uri_medium of this FooterMenu2.  # noqa: E501
        :rtype: str
        """
        return self._uri_medium

    @uri_medium.setter
    def uri_medium(self, uri_medium):
        """Sets the uri_medium of this FooterMenu2.


        :param uri_medium: The uri_medium of this FooterMenu2.  # noqa: E501
        :type: str
        """

        self._uri_medium = uri_medium

    @property
    def uri_small(self):
        """Gets the uri_small of this FooterMenu2.  # noqa: E501


        :return: The uri_small of this FooterMenu2.  # noqa: E501
        :rtype: str
        """
        return self._uri_small

    @uri_small.setter
    def uri_small(self, uri_small):
        """Sets the uri_small of this FooterMenu2.


        :param uri_small: The uri_small of this FooterMenu2.  # noqa: E501
        :type: str
        """

        self._uri_small = uri_small

    @property
    def width_medium(self):
        """Gets the width_medium of this FooterMenu2.  # noqa: E501


        :return: The width_medium of this FooterMenu2.  # noqa: E501
        :rtype: float
        """
        return self._width_medium

    @width_medium.setter
    def width_medium(self, width_medium):
        """Sets the width_medium of this FooterMenu2.


        :param width_medium: The width_medium of this FooterMenu2.  # noqa: E501
        :type: float
        """

        self._width_medium = width_medium

    @property
    def width_small(self):
        """Gets the width_small of this FooterMenu2.  # noqa: E501


        :return: The width_small of this FooterMenu2.  # noqa: E501
        :rtype: float
        """
        return self._width_small

    @width_small.setter
    def width_small(self, width_small):
        """Sets the width_small of this FooterMenu2.


        :param width_small: The width_small of this FooterMenu2.  # noqa: E501
        :type: float
        """

        self._width_small = width_small

    @property
    def collection_type(self):
        """Gets the collection_type of this FooterMenu2.  # noqa: E501


        :return: The collection_type of this FooterMenu2.  # noqa: E501
        :rtype: str
        """
        return self._collection_type

    @collection_type.setter
    def collection_type(self, collection_type):
        """Sets the collection_type of this FooterMenu2.


        :param collection_type: The collection_type of this FooterMenu2.  # noqa: E501
        :type: str
        """

        self._collection_type = collection_type

    @property
    def item_type(self):
        """Gets the item_type of this FooterMenu2.  # noqa: E501


        :return: The item_type of this FooterMenu2.  # noqa: E501
        :rtype: str
        """
        return self._item_type

    @item_type.setter
    def item_type(self, item_type):
        """Sets the item_type of this FooterMenu2.


        :param item_type: The item_type of this FooterMenu2.  # noqa: E501
        :type: str
        """

        self._item_type = item_type

    @property
    def height_large(self):
        """Gets the height_large of this FooterMenu2.  # noqa: E501


        :return: The height_large of this FooterMenu2.  # noqa: E501
        :rtype: float
        """
        return self._height_large

    @height_large.setter
    def height_large(self, height_large):
        """Sets the height_large of this FooterMenu2.


        :param height_large: The height_large of this FooterMenu2.  # noqa: E501
        :type: float
        """

        self._height_large = height_large

    @property
    def width_large(self):
        """Gets the width_large of this FooterMenu2.  # noqa: E501


        :return: The width_large of this FooterMenu2.  # noqa: E501
        :rtype: float
        """
        return self._width_large

    @width_large.setter
    def width_large(self, width_large):
        """Sets the width_large of this FooterMenu2.


        :param width_large: The width_large of this FooterMenu2.  # noqa: E501
        :type: float
        """

        self._width_large = width_large

    @property
    def uri_large(self):
        """Gets the uri_large of this FooterMenu2.  # noqa: E501


        :return: The uri_large of this FooterMenu2.  # noqa: E501
        :rtype: str
        """
        return self._uri_large

    @uri_large.setter
    def uri_large(self, uri_large):
        """Sets the uri_large of this FooterMenu2.


        :param uri_large: The uri_large of this FooterMenu2.  # noqa: E501
        :type: str
        """

        self._uri_large = uri_large

    @property
    def auth_required(self):
        """Gets the auth_required of this FooterMenu2.  # noqa: E501


        :return: The auth_required of this FooterMenu2.  # noqa: E501
        :rtype: bool
        """
        return self._auth_required

    @auth_required.setter
    def auth_required(self, auth_required):
        """Sets the auth_required of this FooterMenu2.


        :param auth_required: The auth_required of this FooterMenu2.  # noqa: E501
        :type: bool
        """

        self._auth_required = auth_required

    @property
    def system_id(self):
        """Gets the system_id of this FooterMenu2.  # noqa: E501


        :return: The system_id of this FooterMenu2.  # noqa: E501
        :rtype: float
        """
        return self._system_id

    @system_id.setter
    def system_id(self, system_id):
        """Sets the system_id of this FooterMenu2.


        :param system_id: The system_id of this FooterMenu2.  # noqa: E501
        :type: float
        """

        self._system_id = system_id

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
        if issubclass(FooterMenu2, dict):
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
        if not isinstance(other, FooterMenu2):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
