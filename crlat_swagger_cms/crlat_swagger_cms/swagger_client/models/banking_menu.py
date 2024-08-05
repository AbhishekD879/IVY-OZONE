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


class BankingMenu(object):
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
        'collection_type': 'str',
        'disabled': 'bool',
        'filename': 'UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentssvgFilenameYamlSvgFilename',
        'height_medium': 'float',
        'height_small': 'float',
        'icon_aligment': 'str',
        'in_app': 'bool',
        'lang': 'str',
        'link_title': 'str',
        'link_title_brand': 'str',
        'menu_item_view': 'str',
        'path': 'str',
        'section': 'str',
        'show_item_for': 'str',
        'sort_order': 'float',
        'sprite_class': 'str',
        'target_uri': 'str',
        'type': 'str',
        'uri_medium': 'str',
        'uri_small': 'str',
        'width_medium': 'float',
        'width_small': 'float',
        'show_only_on_ios': 'bool',
        'show_only_on_android': 'bool',
        'height_large': 'float',
        'width_large': 'float',
        'svg': 'str',
        'svg_filename': 'UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentsfilenameYamlFilename',
        'svg_id': 'str',
        'qa': 'str',
        'uri_large': 'str',
        'auth_required': 'bool',
        'system_id': 'float',
        'start_url': 'str',
        'sub_header': 'str'
    }

    attribute_map = {
        'id': 'id',
        'brand': 'brand',
        'collection_type': 'collectionType',
        'disabled': 'disabled',
        'filename': 'filename',
        'height_medium': 'heightMedium',
        'height_small': 'heightSmall',
        'icon_aligment': 'iconAligment',
        'in_app': 'inApp',
        'lang': 'lang',
        'link_title': 'linkTitle',
        'link_title_brand': 'linkTitle_brand',
        'menu_item_view': 'menuItemView',
        'path': 'path',
        'section': 'section',
        'show_item_for': 'showItemFor',
        'sort_order': 'sortOrder',
        'sprite_class': 'spriteClass',
        'target_uri': 'targetUri',
        'type': 'type',
        'uri_medium': 'uriMedium',
        'uri_small': 'uriSmall',
        'width_medium': 'widthMedium',
        'width_small': 'widthSmall',
        'show_only_on_ios': 'showOnlyOnIOS',
        'show_only_on_android': 'showOnlyOnAndroid',
        'height_large': 'heightLarge',
        'width_large': 'widthLarge',
        'svg': 'svg',
        'svg_filename': 'svgFilename',
        'svg_id': 'svgId',
        'qa': 'qa',
        'uri_large': 'uriLarge',
        'auth_required': 'authRequired',
        'system_id': 'systemID',
        'start_url': 'startUrl',
        'sub_header': 'subHeader'
    }

    def __init__(self, id=None, brand=None, collection_type=None, disabled=None, filename=None, height_medium=None, height_small=None, icon_aligment=None, in_app=None, lang=None, link_title=None, link_title_brand=None, menu_item_view=None, path=None, section=None, show_item_for=None, sort_order=None, sprite_class=None, target_uri=None, type=None, uri_medium=None, uri_small=None, width_medium=None, width_small=None, show_only_on_ios=None, show_only_on_android=None, height_large=None, width_large=None, svg=None, svg_filename=None, svg_id=None, qa=None, uri_large=None, auth_required=None, system_id=None, start_url=None, sub_header=None):  # noqa: E501
        """BankingMenu - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._brand = None
        self._collection_type = None
        self._disabled = None
        self._filename = None
        self._height_medium = None
        self._height_small = None
        self._icon_aligment = None
        self._in_app = None
        self._lang = None
        self._link_title = None
        self._link_title_brand = None
        self._menu_item_view = None
        self._path = None
        self._section = None
        self._show_item_for = None
        self._sort_order = None
        self._sprite_class = None
        self._target_uri = None
        self._type = None
        self._uri_medium = None
        self._uri_small = None
        self._width_medium = None
        self._width_small = None
        self._show_only_on_ios = None
        self._show_only_on_android = None
        self._height_large = None
        self._width_large = None
        self._svg = None
        self._svg_filename = None
        self._svg_id = None
        self._qa = None
        self._uri_large = None
        self._auth_required = None
        self._system_id = None
        self._start_url = None
        self._sub_header = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if brand is not None:
            self.brand = brand
        if collection_type is not None:
            self.collection_type = collection_type
        if disabled is not None:
            self.disabled = disabled
        if filename is not None:
            self.filename = filename
        if height_medium is not None:
            self.height_medium = height_medium
        if height_small is not None:
            self.height_small = height_small
        if icon_aligment is not None:
            self.icon_aligment = icon_aligment
        if in_app is not None:
            self.in_app = in_app
        if lang is not None:
            self.lang = lang
        if link_title is not None:
            self.link_title = link_title
        if link_title_brand is not None:
            self.link_title_brand = link_title_brand
        if menu_item_view is not None:
            self.menu_item_view = menu_item_view
        if path is not None:
            self.path = path
        if section is not None:
            self.section = section
        if show_item_for is not None:
            self.show_item_for = show_item_for
        if sort_order is not None:
            self.sort_order = sort_order
        if sprite_class is not None:
            self.sprite_class = sprite_class
        if target_uri is not None:
            self.target_uri = target_uri
        if type is not None:
            self.type = type
        if uri_medium is not None:
            self.uri_medium = uri_medium
        if uri_small is not None:
            self.uri_small = uri_small
        if width_medium is not None:
            self.width_medium = width_medium
        if width_small is not None:
            self.width_small = width_small
        if show_only_on_ios is not None:
            self.show_only_on_ios = show_only_on_ios
        if show_only_on_android is not None:
            self.show_only_on_android = show_only_on_android
        if height_large is not None:
            self.height_large = height_large
        if width_large is not None:
            self.width_large = width_large
        if svg is not None:
            self.svg = svg
        if svg_filename is not None:
            self.svg_filename = svg_filename
        if svg_id is not None:
            self.svg_id = svg_id
        if qa is not None:
            self.qa = qa
        if uri_large is not None:
            self.uri_large = uri_large
        if auth_required is not None:
            self.auth_required = auth_required
        if system_id is not None:
            self.system_id = system_id
        if start_url is not None:
            self.start_url = start_url
        if sub_header is not None:
            self.sub_header = sub_header

    @property
    def id(self):
        """Gets the id of this BankingMenu.  # noqa: E501


        :return: The id of this BankingMenu.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this BankingMenu.


        :param id: The id of this BankingMenu.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def brand(self):
        """Gets the brand of this BankingMenu.  # noqa: E501


        :return: The brand of this BankingMenu.  # noqa: E501
        :rtype: str
        """
        return self._brand

    @brand.setter
    def brand(self, brand):
        """Sets the brand of this BankingMenu.


        :param brand: The brand of this BankingMenu.  # noqa: E501
        :type: str
        """

        self._brand = brand

    @property
    def collection_type(self):
        """Gets the collection_type of this BankingMenu.  # noqa: E501


        :return: The collection_type of this BankingMenu.  # noqa: E501
        :rtype: str
        """
        return self._collection_type

    @collection_type.setter
    def collection_type(self, collection_type):
        """Sets the collection_type of this BankingMenu.


        :param collection_type: The collection_type of this BankingMenu.  # noqa: E501
        :type: str
        """

        self._collection_type = collection_type

    @property
    def disabled(self):
        """Gets the disabled of this BankingMenu.  # noqa: E501


        :return: The disabled of this BankingMenu.  # noqa: E501
        :rtype: bool
        """
        return self._disabled

    @disabled.setter
    def disabled(self, disabled):
        """Sets the disabled of this BankingMenu.


        :param disabled: The disabled of this BankingMenu.  # noqa: E501
        :type: bool
        """

        self._disabled = disabled

    @property
    def filename(self):
        """Gets the filename of this BankingMenu.  # noqa: E501


        :return: The filename of this BankingMenu.  # noqa: E501
        :rtype: UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentssvgFilenameYamlSvgFilename
        """
        return self._filename

    @filename.setter
    def filename(self, filename):
        """Sets the filename of this BankingMenu.


        :param filename: The filename of this BankingMenu.  # noqa: E501
        :type: UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentssvgFilenameYamlSvgFilename
        """

        self._filename = filename

    @property
    def height_medium(self):
        """Gets the height_medium of this BankingMenu.  # noqa: E501


        :return: The height_medium of this BankingMenu.  # noqa: E501
        :rtype: float
        """
        return self._height_medium

    @height_medium.setter
    def height_medium(self, height_medium):
        """Sets the height_medium of this BankingMenu.


        :param height_medium: The height_medium of this BankingMenu.  # noqa: E501
        :type: float
        """

        self._height_medium = height_medium

    @property
    def height_small(self):
        """Gets the height_small of this BankingMenu.  # noqa: E501


        :return: The height_small of this BankingMenu.  # noqa: E501
        :rtype: float
        """
        return self._height_small

    @height_small.setter
    def height_small(self, height_small):
        """Sets the height_small of this BankingMenu.


        :param height_small: The height_small of this BankingMenu.  # noqa: E501
        :type: float
        """

        self._height_small = height_small

    @property
    def icon_aligment(self):
        """Gets the icon_aligment of this BankingMenu.  # noqa: E501


        :return: The icon_aligment of this BankingMenu.  # noqa: E501
        :rtype: str
        """
        return self._icon_aligment

    @icon_aligment.setter
    def icon_aligment(self, icon_aligment):
        """Sets the icon_aligment of this BankingMenu.


        :param icon_aligment: The icon_aligment of this BankingMenu.  # noqa: E501
        :type: str
        """

        self._icon_aligment = icon_aligment

    @property
    def in_app(self):
        """Gets the in_app of this BankingMenu.  # noqa: E501


        :return: The in_app of this BankingMenu.  # noqa: E501
        :rtype: bool
        """
        return self._in_app

    @in_app.setter
    def in_app(self, in_app):
        """Sets the in_app of this BankingMenu.


        :param in_app: The in_app of this BankingMenu.  # noqa: E501
        :type: bool
        """

        self._in_app = in_app

    @property
    def lang(self):
        """Gets the lang of this BankingMenu.  # noqa: E501


        :return: The lang of this BankingMenu.  # noqa: E501
        :rtype: str
        """
        return self._lang

    @lang.setter
    def lang(self, lang):
        """Sets the lang of this BankingMenu.


        :param lang: The lang of this BankingMenu.  # noqa: E501
        :type: str
        """

        self._lang = lang

    @property
    def link_title(self):
        """Gets the link_title of this BankingMenu.  # noqa: E501


        :return: The link_title of this BankingMenu.  # noqa: E501
        :rtype: str
        """
        return self._link_title

    @link_title.setter
    def link_title(self, link_title):
        """Sets the link_title of this BankingMenu.


        :param link_title: The link_title of this BankingMenu.  # noqa: E501
        :type: str
        """

        self._link_title = link_title

    @property
    def link_title_brand(self):
        """Gets the link_title_brand of this BankingMenu.  # noqa: E501


        :return: The link_title_brand of this BankingMenu.  # noqa: E501
        :rtype: str
        """
        return self._link_title_brand

    @link_title_brand.setter
    def link_title_brand(self, link_title_brand):
        """Sets the link_title_brand of this BankingMenu.


        :param link_title_brand: The link_title_brand of this BankingMenu.  # noqa: E501
        :type: str
        """

        self._link_title_brand = link_title_brand

    @property
    def menu_item_view(self):
        """Gets the menu_item_view of this BankingMenu.  # noqa: E501


        :return: The menu_item_view of this BankingMenu.  # noqa: E501
        :rtype: str
        """
        return self._menu_item_view

    @menu_item_view.setter
    def menu_item_view(self, menu_item_view):
        """Sets the menu_item_view of this BankingMenu.


        :param menu_item_view: The menu_item_view of this BankingMenu.  # noqa: E501
        :type: str
        """

        self._menu_item_view = menu_item_view

    @property
    def path(self):
        """Gets the path of this BankingMenu.  # noqa: E501


        :return: The path of this BankingMenu.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this BankingMenu.


        :param path: The path of this BankingMenu.  # noqa: E501
        :type: str
        """

        self._path = path

    @property
    def section(self):
        """Gets the section of this BankingMenu.  # noqa: E501


        :return: The section of this BankingMenu.  # noqa: E501
        :rtype: str
        """
        return self._section

    @section.setter
    def section(self, section):
        """Sets the section of this BankingMenu.


        :param section: The section of this BankingMenu.  # noqa: E501
        :type: str
        """

        self._section = section

    @property
    def show_item_for(self):
        """Gets the show_item_for of this BankingMenu.  # noqa: E501


        :return: The show_item_for of this BankingMenu.  # noqa: E501
        :rtype: str
        """
        return self._show_item_for

    @show_item_for.setter
    def show_item_for(self, show_item_for):
        """Sets the show_item_for of this BankingMenu.


        :param show_item_for: The show_item_for of this BankingMenu.  # noqa: E501
        :type: str
        """

        self._show_item_for = show_item_for

    @property
    def sort_order(self):
        """Gets the sort_order of this BankingMenu.  # noqa: E501


        :return: The sort_order of this BankingMenu.  # noqa: E501
        :rtype: float
        """
        return self._sort_order

    @sort_order.setter
    def sort_order(self, sort_order):
        """Sets the sort_order of this BankingMenu.


        :param sort_order: The sort_order of this BankingMenu.  # noqa: E501
        :type: float
        """

        self._sort_order = sort_order

    @property
    def sprite_class(self):
        """Gets the sprite_class of this BankingMenu.  # noqa: E501


        :return: The sprite_class of this BankingMenu.  # noqa: E501
        :rtype: str
        """
        return self._sprite_class

    @sprite_class.setter
    def sprite_class(self, sprite_class):
        """Sets the sprite_class of this BankingMenu.


        :param sprite_class: The sprite_class of this BankingMenu.  # noqa: E501
        :type: str
        """

        self._sprite_class = sprite_class

    @property
    def target_uri(self):
        """Gets the target_uri of this BankingMenu.  # noqa: E501


        :return: The target_uri of this BankingMenu.  # noqa: E501
        :rtype: str
        """
        return self._target_uri

    @target_uri.setter
    def target_uri(self, target_uri):
        """Sets the target_uri of this BankingMenu.


        :param target_uri: The target_uri of this BankingMenu.  # noqa: E501
        :type: str
        """

        self._target_uri = target_uri

    @property
    def type(self):
        """Gets the type of this BankingMenu.  # noqa: E501


        :return: The type of this BankingMenu.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this BankingMenu.


        :param type: The type of this BankingMenu.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def uri_medium(self):
        """Gets the uri_medium of this BankingMenu.  # noqa: E501


        :return: The uri_medium of this BankingMenu.  # noqa: E501
        :rtype: str
        """
        return self._uri_medium

    @uri_medium.setter
    def uri_medium(self, uri_medium):
        """Sets the uri_medium of this BankingMenu.


        :param uri_medium: The uri_medium of this BankingMenu.  # noqa: E501
        :type: str
        """

        self._uri_medium = uri_medium

    @property
    def uri_small(self):
        """Gets the uri_small of this BankingMenu.  # noqa: E501


        :return: The uri_small of this BankingMenu.  # noqa: E501
        :rtype: str
        """
        return self._uri_small

    @uri_small.setter
    def uri_small(self, uri_small):
        """Sets the uri_small of this BankingMenu.


        :param uri_small: The uri_small of this BankingMenu.  # noqa: E501
        :type: str
        """

        self._uri_small = uri_small

    @property
    def width_medium(self):
        """Gets the width_medium of this BankingMenu.  # noqa: E501


        :return: The width_medium of this BankingMenu.  # noqa: E501
        :rtype: float
        """
        return self._width_medium

    @width_medium.setter
    def width_medium(self, width_medium):
        """Sets the width_medium of this BankingMenu.


        :param width_medium: The width_medium of this BankingMenu.  # noqa: E501
        :type: float
        """

        self._width_medium = width_medium

    @property
    def width_small(self):
        """Gets the width_small of this BankingMenu.  # noqa: E501


        :return: The width_small of this BankingMenu.  # noqa: E501
        :rtype: float
        """
        return self._width_small

    @width_small.setter
    def width_small(self, width_small):
        """Sets the width_small of this BankingMenu.


        :param width_small: The width_small of this BankingMenu.  # noqa: E501
        :type: float
        """

        self._width_small = width_small

    @property
    def show_only_on_ios(self):
        """Gets the show_only_on_ios of this BankingMenu.  # noqa: E501


        :return: The show_only_on_ios of this BankingMenu.  # noqa: E501
        :rtype: bool
        """
        return self._show_only_on_ios

    @show_only_on_ios.setter
    def show_only_on_ios(self, show_only_on_ios):
        """Sets the show_only_on_ios of this BankingMenu.


        :param show_only_on_ios: The show_only_on_ios of this BankingMenu.  # noqa: E501
        :type: bool
        """

        self._show_only_on_ios = show_only_on_ios

    @property
    def show_only_on_android(self):
        """Gets the show_only_on_android of this BankingMenu.  # noqa: E501


        :return: The show_only_on_android of this BankingMenu.  # noqa: E501
        :rtype: bool
        """
        return self._show_only_on_android

    @show_only_on_android.setter
    def show_only_on_android(self, show_only_on_android):
        """Sets the show_only_on_android of this BankingMenu.


        :param show_only_on_android: The show_only_on_android of this BankingMenu.  # noqa: E501
        :type: bool
        """

        self._show_only_on_android = show_only_on_android

    @property
    def height_large(self):
        """Gets the height_large of this BankingMenu.  # noqa: E501


        :return: The height_large of this BankingMenu.  # noqa: E501
        :rtype: float
        """
        return self._height_large

    @height_large.setter
    def height_large(self, height_large):
        """Sets the height_large of this BankingMenu.


        :param height_large: The height_large of this BankingMenu.  # noqa: E501
        :type: float
        """

        self._height_large = height_large

    @property
    def width_large(self):
        """Gets the width_large of this BankingMenu.  # noqa: E501


        :return: The width_large of this BankingMenu.  # noqa: E501
        :rtype: float
        """
        return self._width_large

    @width_large.setter
    def width_large(self, width_large):
        """Sets the width_large of this BankingMenu.


        :param width_large: The width_large of this BankingMenu.  # noqa: E501
        :type: float
        """

        self._width_large = width_large

    @property
    def svg(self):
        """Gets the svg of this BankingMenu.  # noqa: E501


        :return: The svg of this BankingMenu.  # noqa: E501
        :rtype: str
        """
        return self._svg

    @svg.setter
    def svg(self, svg):
        """Sets the svg of this BankingMenu.


        :param svg: The svg of this BankingMenu.  # noqa: E501
        :type: str
        """

        self._svg = svg

    @property
    def svg_filename(self):
        """Gets the svg_filename of this BankingMenu.  # noqa: E501


        :return: The svg_filename of this BankingMenu.  # noqa: E501
        :rtype: UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentsfilenameYamlFilename
        """
        return self._svg_filename

    @svg_filename.setter
    def svg_filename(self, svg_filename):
        """Sets the svg_filename of this BankingMenu.


        :param svg_filename: The svg_filename of this BankingMenu.  # noqa: E501
        :type: UsersbmakarIdeaProjectsoxygenCmsApisrcmainresourcesstaticprivatecomponentsfilenameYamlFilename
        """

        self._svg_filename = svg_filename

    @property
    def svg_id(self):
        """Gets the svg_id of this BankingMenu.  # noqa: E501


        :return: The svg_id of this BankingMenu.  # noqa: E501
        :rtype: str
        """
        return self._svg_id

    @svg_id.setter
    def svg_id(self, svg_id):
        """Sets the svg_id of this BankingMenu.


        :param svg_id: The svg_id of this BankingMenu.  # noqa: E501
        :type: str
        """

        self._svg_id = svg_id

    @property
    def qa(self):
        """Gets the qa of this BankingMenu.  # noqa: E501


        :return: The qa of this BankingMenu.  # noqa: E501
        :rtype: str
        """
        return self._qa

    @qa.setter
    def qa(self, qa):
        """Sets the qa of this BankingMenu.


        :param qa: The qa of this BankingMenu.  # noqa: E501
        :type: str
        """

        self._qa = qa

    @property
    def uri_large(self):
        """Gets the uri_large of this BankingMenu.  # noqa: E501


        :return: The uri_large of this BankingMenu.  # noqa: E501
        :rtype: str
        """
        return self._uri_large

    @uri_large.setter
    def uri_large(self, uri_large):
        """Sets the uri_large of this BankingMenu.


        :param uri_large: The uri_large of this BankingMenu.  # noqa: E501
        :type: str
        """

        self._uri_large = uri_large

    @property
    def auth_required(self):
        """Gets the auth_required of this BankingMenu.  # noqa: E501


        :return: The auth_required of this BankingMenu.  # noqa: E501
        :rtype: bool
        """
        return self._auth_required

    @auth_required.setter
    def auth_required(self, auth_required):
        """Sets the auth_required of this BankingMenu.


        :param auth_required: The auth_required of this BankingMenu.  # noqa: E501
        :type: bool
        """

        self._auth_required = auth_required

    @property
    def system_id(self):
        """Gets the system_id of this BankingMenu.  # noqa: E501


        :return: The system_id of this BankingMenu.  # noqa: E501
        :rtype: float
        """
        return self._system_id

    @system_id.setter
    def system_id(self, system_id):
        """Sets the system_id of this BankingMenu.


        :param system_id: The system_id of this BankingMenu.  # noqa: E501
        :type: float
        """

        self._system_id = system_id

    @property
    def start_url(self):
        """Gets the start_url of this BankingMenu.  # noqa: E501


        :return: The start_url of this BankingMenu.  # noqa: E501
        :rtype: str
        """
        return self._start_url

    @start_url.setter
    def start_url(self, start_url):
        """Sets the start_url of this BankingMenu.


        :param start_url: The start_url of this BankingMenu.  # noqa: E501
        :type: str
        """

        self._start_url = start_url

    @property
    def sub_header(self):
        """Gets the sub_header of this BankingMenu.  # noqa: E501


        :return: The sub_header of this BankingMenu.  # noqa: E501
        :rtype: str
        """
        return self._sub_header

    @sub_header.setter
    def sub_header(self, sub_header):
        """Sets the sub_header of this BankingMenu.


        :param sub_header: The sub_header of this BankingMenu.  # noqa: E501
        :type: str
        """

        self._sub_header = sub_header

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
        if issubclass(BankingMenu, dict):
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
        if not isinstance(other, BankingMenu):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
