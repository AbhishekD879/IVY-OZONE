import json
import logging
import re
from collections import namedtuple
from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union
from lxml.html import document_fromstring,fromstring
from lxml.etree import tostring

from faker import Faker

from crlat_core.request import InvalidResponseException
from crlat_cms_client import LOGGER_NAME
from crlat_cms_client.module_ribbon.module_ribbon_tabs import ModuleRibbonTabs
from crlat_cms_client.request import CMSAPIRequest
from crlat_cms_client.utils.date_time import get_date_time_as_string
from crlat_cms_client.utils.exceptions import CMSException
from crlat_cms_client.utils.settings import define_cms_settings
from crlat_cms_client.utils.settings import get_cms_settings
from crlat_cms_client.utils.waiters import wait_for_result

try:
    from urlparse import urljoin
except:
    from urllib.parse import urljoin

fake = Faker()


class CMSClient(object):
    def __init__(self,
                 env='dev0',
                 brand='bma'):
        define_cms_settings(env=env, brand=brand)
        self.env = env
        self.cms_settings = get_cms_settings()
        self._logger = logging.getLogger(LOGGER_NAME)
        self.brand = brand
        self.module_ribbon_tabs = ModuleRibbonTabs(brand=self.brand, env=self.env)
        self.request = CMSAPIRequest()

        # created CMS items from test. used for tearDown in voltron project
        self._created_featured_tab_modules = []
        self._created_promotions = []
        self._created_offer_module = []
        self._created_offers = []
        self._created_banners = []
        self._created_module_ribbon_tabs = []
        self._created_highlights_carousels = []
        self._created_surface_bets = []
        self._created_quick_links = []
        self._created_coupon_segment = []
        self._created_super_buttons = []
        self._created_special_super_buttons = []
        self._created_event_hubs = []
        self._created_racing_edp_markets = []
        self._created_timeline_template = []
        self._created_timeline_post = []
        self._created_five_a_side_show_down = []
        self._created_sport_category = []
        self._created_inplay_module = []
        self._created_footer_menu = []
        self._created_big_competitions = []
        self._created_rgy_modules = []
        self._created_rgy_bonus_suppression_modules = []
        self._created_desktop_quick_links = []
        self._created_question_engine_quiz = []
        self._created_seo_page = []
        self._create_byb_widget = []

        # stored cached data for reducing number of calls
        self._cached_initial_data = {'mobile': None, 'desktop': None}

        self.auto_test_quiz_name = 'Autotest_Quiz'

    image_url = 'https://i.imgur.com/FXQ6IuX.jpeg'

    # Menu items
    def get_cms_menu_items(self, menu_types: Union[List[str], str], filters: Optional[Dict] = None) -> Dict[str, List]:
        """
        Returns a dict of lists for menu items (dict).
        The dict's keys are menu types and lists contains menu items' dict.

        :param menu_types: Either 'Right Menus', 'User Menus' or 'Connect Menus'
        :param filters: Any column name as a dict, eg. {'showItemFor': ['both', 'loggedIn']}

        :Usage:
        client.get_cms_menu_items('Right Menus')
        client.get_cms_menu_items(['Right Menus'])
        client.get_cms_menu_items(['Right Menus', 'User Menus'], filters = {})
        """

        def match(item: str, filter_item: Tuple) -> bool:
            """
            Returns True if an item meets expected filter criteria
            """
            field, condition = filter_item
            if field not in item:
                return False
            value = item.get(field)
            if isinstance(condition, list):
                return value in condition
            return value == condition

        menus = {'Right Menus': 'right-menu',
                 'User Menus': 'user-menu',
                 'Connect Menus': 'connect-menu',
                 'Footer Menus': 'footer-menu'}

        filters = filters or {}

        if not menu_types:
            menu_types = menus.keys()
        else:
            if not isinstance(menu_types, list):
                menu_types = [menu_types]
        cms_menu_items = {}

        for mt in menu_types:
            try:
                path = f'{menus[mt]}/brand/{self.brand}'
            except KeyError as e:
                error = f'Cannot find menu type with given key: {e}, while getting CMS menu items!'
                self._logger.error(error)
                raise KeyError(error)
            # TODO: Please improve getting response from do_request (inc. remove make_path) re VOL-135 (in progress)
            response = self.request.get(path)
            cms_menu_items[mt] = [menu_item for menu_item in response if
                                  all([match(menu_item, f) for f in filters.items()])]
        return cms_menu_items

    def get_cms_right_menu_items(self) -> list:
        """
        Returns a list of all available Right Menu items
        :return: List of Right Menu items
        """
        path = f'right-menu/brand/{self.brand}'
        right_menu = [{k.strip(): v for k, v in elem.items()} for elem in self.request.get(path)]
        return right_menu

    def get_cms_header_menu_items(self) -> list:
        """
        Returns list of available Header Menu items.
        :return:
        """
        path = 'header-menu/brand/%s' % self.brand
        return self.request.get(path)

    def get_header_submenus(self) -> list:
        """
        Returns list of available Header Sub Menu items.
        :return: List of Sub Menu items
        """
        path = 'header-submenu/brand/%s' % self.brand
        return self.request.get(path)

    def create_header_submenu(self, name=None, target_url=None):
        path = 'header-submenu'
        payload = {
            "id": "",
            "brand": self.brand,
            "disabled": False,
            "inApp": True,
            "linkTitle": name,
            "targetUri": target_url
        }
        data = json.dumps(payload)
        return self.request.post(path, data=data)

    def get_header_submenu(self, header_submenu_id: str):
        """
        Get the header sub menu with the given header_submenu_id
        Args:
            header_submenu_id (str): The unique identifier of the header submenu to update.
        Returns:
            dict: A dictionary representing the response of the given header submenu id.
        """
        path = f'header-submenu/{header_submenu_id}'
        return self.request.get(path)

    def update_header_submenu(self, header_submenu_id: str, **kwargs):
        """
        Update a header submenu with the specified header_submenu_id using the provided data.
        Args:
            header_submenu_id (str): The unique identifier of the header submenu to update.
            **kwargs: Additional keyword arguments to specify the updated fields of the header submenu.
        Parameters:
              - **kwargs (dict): Keyword arguments to specify the updated fields. You can provide
                values for the following fields:
              - targetUri (str): The url of the header submenu.
              - disabled (bool): Indicates whether the header submenu is disabled.
              - inApp (bool): Indicates whether the header submenu is in App.
              - linkTitle (str): The title of the Header submenu.
        Returns:
            dict: A dictionary representing the response from the update request contains all response of header submenu.
        """
        header_submenu_data = self.get_header_submenu(header_submenu_id=header_submenu_id)
        path = f'header-submenu/{header_submenu_id}'
        for key in header_submenu_data.keys():
            if key in kwargs:
                header_submenu_data[key] = kwargs[key]
        data = json.dumps(header_submenu_data)
        responce = self.request.put(path, data=data)
        return responce

    def delete_header_submenu(self, id=None):
        path = f'header-submenu/{id}'
        self.request.delete(path, parse_response=False)

    def is_item_enabled(self, items: list, item_name: str) -> bool:
        """
        Get status of ['disabled'] key for specified item, and remove specified item from collection

        :param items: List with items
        :param item_name: Item name to get status of ['disabled'] key
        :return: Status of ['disabled'] key
        """
        for item in items:
            if item['imageTitle'].strip() == item_name:
                items.remove(item)
                return item['disabled'] is False

    def get_left_menu_items(self):
        """
        Left menu (A-Z sports) consists of the following CMS items from CMS -> Sports Pages:
            - Sport Categories items, where checkboxes 'Active' and 'Show in A-Z' are enabled
            - Olympic sports items, where checkbox 'Active' is enabled
            - If there's sport item with the same name for Sport Categories and Olympic sports:
                - If item in Sport Categories has checkbox 'Active' enabled, but 'Show in A-Z' is disabled,
                    availability of item depends on the Olympic sports 'Active' checkbox:
                        - Olympic sports enabled 'Active' checkbox means that item will be enabled for Left Menu
                        - Olympic sports disabled 'Active' checkbox means that item won't be enabled for Left Menu

        :return: List with left menu items names ['Diving', 'Football', ...] sorted by alphabetical ascending
        """
        initial_data = self.get_initial_data(device_type='desktop')
        sport_categories_items = initial_data['sportCategories']
        olympic_sports_items = initial_data['sports']

        left_menu_items = []
        for sport_categories_item in sport_categories_items:
            item_name = sport_categories_item['imageTitle'].strip()
            if not sport_categories_item['disabled'] and sport_categories_item['showInAZ']:
                left_menu_items.append(item_name)
            elif not sport_categories_item['disabled']:
                if self.is_item_enabled(olympic_sports_items, item_name):
                    left_menu_items.append(item_name)

        for olympic_sports_item in olympic_sports_items:
            item_name = olympic_sports_item['imageTitle']
            if not olympic_sports_item['disabled'] and item_name not in left_menu_items:
                left_menu_items.append(item_name)

        return sorted(left_menu_items)

    # Featured

    def _load_events(self, select_event_by, id, dateFrom, dateTo):
        if self.env in ('dev0', 'dev1', 'dev2', 'tst0', 'tst1', 'stg0', 'hlv0', 'hlv2'):
            path = 'home-module/brand/%s/ss/event' % self.brand
        else:
            path = 'home-module/ss/event'
        params = (
            ('selectionType', select_event_by),
            ('selectionId', id),
            ('dateFrom', dateFrom),
            ('dateTo', dateTo),
        )
        r = wait_for_result(lambda: self.request.get(path, params=params),
                            name='Events to load from SS to CMS',
                            poll_interval=1,
                            timeout=3)
        return r

    def add_featured_tab_module(self, select_event_by: str, id: int, page_type: str = 'sport', **kwargs) -> dict:
        """
        Creates Featured tab module
        :param select_event_by: str, select type of module creation
        :param id: int, id (type, category, selection etc.)
        :param page_type: str, page type where module is configured. E.g.: 'sport', 'eventhub'
        :return: dict, object with all information about just created module (id, title, etc)
        """
        if not kwargs.get('show_all_events', None):
            maxRows = kwargs.get('max_rows', 3)
        else:
            maxRows = ''
        allowed_select_by_options = ['Type', 'RacingGrid', 'Enhanced Multiples', 'Selection', 'RaceTypeId', 'Event',
                                     'Market', 'Category', 'Class']

        if select_event_by not in allowed_select_by_options:
            raise CMSException(
                f'"{select_event_by}" is not allowed option for selecting events on Featured module, '
                f'please select one of: [{allowed_select_by_options}]')

        badge = kwargs.get('badge', 'None')
        show_expanded = kwargs.get('show_expanded', True)

        now = datetime.now()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        events_time_from_hours_delta = kwargs.get('events_time_from_hours_delta', -3)
        module_time_from_hours_delta = kwargs.get('module_time_from_hours_delta', -3)

        moduleDateFrom = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                                 hours=module_time_from_hours_delta, minutes=-1)[:-3] + 'Z'
        eventsDateFrom = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                                 hours=events_time_from_hours_delta, minutes=-1)[:-3] + 'Z'
        dateTo = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                         days=1)[:-3] + 'Z'

        events = [] if select_event_by in ['RacingGrid'] else self._load_events(select_event_by, id, eventsDateFrom, dateTo)
        # to load events from ss call and to send events to cms if we want to restrict number of events to display
        # if show all events we need to send empty string as parameter so the length can't use it
        if not kwargs.get('show_all_events', None):
            events = events[0:maxRows] if len(events) >= maxRows else events
        custom_title = kwargs.get('title')
        title = custom_title if custom_title else fake.city()
        page_id = kwargs.get('page_id', '0')
        footer_link_url = kwargs.get('footer_link_url', 'http://' + title + '.com')
        payload = {
            'badge': badge,
            'brand': self.brand,
            'data': events,
            'dataSelection': {'selectionId': id,
                              'selectionType': select_event_by},
            'displayOrder': 0,
            'eventsSelectionSettings': {'from': eventsDateFrom,
                                        'to': dateTo,
                                        'autoRefresh': kwargs.get('auto_refresh',False)},
            'footerLink': {'text': 'footer text for ' + title,
                           'url': footer_link_url},
            'id': 'null',
            'maxRows': maxRows,
            'maxSelections': 3,
            'navItem': 'Featured',
            'publishToChannels': [self.brand],
            'publishedDevices': {self.brand: {'desktop': True,
                                              'tablet': True,
                                              'mobile': True}},
            'showExpanded': show_expanded,
            'title': 'Auto ' + title + ' Module',
            'totalEvents': 0,
            'version': 0,
            'visibility': {'displayFrom': moduleDateFrom,
                           'displayTo': dateTo,
                           'enabled': True},
            "personalised": False,
            "pageId": page_id,
            "pageType": page_type,
            'inclusionList': kwargs.get('inclusionList', []),
            'universalSegment': kwargs.get('universalSegment', True),
            'exclusionList': kwargs.get('exclusionList', [])
        }
        data = json.dumps(payload)
        module = self.request.post('home-module', data=data)
        self._created_featured_tab_modules.append(module['id'])
        return module

    def delete_featured_tab_module(self, id):
        path = 'home-module/%s' % id
        self.request.delete(path, parse_response=False)

    def get_featured_tab_module(self, module_id: str) -> dict:
        """
        Method used to get Featured module info from CMS
        :param module_id: ID for existing Featured module
        :return: object with all information about just created feature module (id, title, etc)
        """
        path = f'home-module/{module_id}'
        return self.request.get(path)

    def get_feature_modules(self,segment='Universal') -> list:
        """
        Get a list of feature modules for the specified brand and segment.
        Args:
            segment (str, optional): The segment for which feature modules are requested.
                Defaults to 'Universal'.
        Returns:
            list: A list of feature modules for the specified brand and segment.
        """
        path = f'home-module/brand/{self.brand}/segment/{segment}?active=true'
        return self.request.get(path)

    def update_featured_tab_module(self, module_id: str, enabled=True, **kwargs) -> dict:
        """
        Method used to update Featured module fields in CMS
        :param module_id: ID for Featured module
        :param enabled: True/False , to make the featured module active(display)/inactive(undisplay)
        :param kwargs date_from: from date visibility of featured module
        :param kwargs date_to: to date visibility of featured module
        :param kwargs: data parameter if needed to be modified
        :return: Updated object with all information about just updated Featured module (id, title, etc)
        """
        module = self.get_featured_tab_module(module_id=module_id)
        module['visibility']['enabled'] = enabled
        module['data'] = kwargs.get('data', module['data'])
        module['visibility']['displayFrom'] = kwargs.get('date_from', module['visibility']['displayFrom'])
        module['visibility']['displayTo'] = kwargs.get('date_to', module['visibility']['displayTo'])
        module['dataSelection']['selectionId'] = kwargs.get('selection_id', module['dataSelection']['selectionId'])
        path = f'home-module/{module_id}'
        return self.request.put(path, data=json.dumps(module))

    # Promotions

    def _promo_link_html(self, link, link_name):
        """
        :param link: str: link to add
        :param link_name: str: link name
        :return: str: HTML formatted string
        """
        promotion_description = '<p><a href="{link}">{name}</a></p>'.format(link=link, name=link_name)
        return promotion_description

    def _promo_button_html(self, button_width, button_color, button_name, button_link, opt_in_button):
        """
        :param button_width: str('full' or 'half'): define button width
        :param button_color: str('blue' or 'green'): define button color
        :param button_name: str: button name
        :param button_link: str: button link to add
        :return: str: HTML formatted string
        """
        style = 'style1' if button_color == 'blue' else 'style2'
        if opt_in_button:
            opt_in_button = 'handle-opt-in'
            button_name = f'<span class="btn-label">{button_name}</span>'
        else:
            opt_in_button = ''
        promotion_description = '<p><a class="btn btn-{style} {button_width}-width {opt_in_button}" ' \
                                'href="{link}" ' \
                                'target="">{name}</a></p>'.format(style=style,
                                                                  button_width=button_width,
                                                                  opt_in_button=opt_in_button,
                                                                  link=button_link,
                                                                  name=button_name)
        return promotion_description

    def add_promotion(self, **kwargs):
        """
        :param promo_description (str or list of dicts):
         ** If str - promotion will created with text in description;
         ** If list of dicts - promotion will be created with specified in this list elements, for example:
        to create promotion with link, green full button and blue half button we should set:
        promo_description = [{'link': 'https://invictus.coral.co.uk/#/lotto', 'link_name': 'auto_test_link'},
        {'button_name': 'In-Play', 'button_link': 'https://invictus.coral.co.uk/#/in-play', 'button_width': 'full', 'button_color': 'green'},
        {'button_name': 'Home', 'button_link': 'https://invictus.coral.co.uk/#/home', 'button_width': 'half', 'button_color': 'blue'}]
         ** All elements repeatable, for example we can create promotion with few identical elements:
        promo_description =
        [{'link': 'https://invictus.coral.co.uk/#/lotto'},
        {'link': 'https://invictus.coral.co.uk/#/lotto'},
        {'button_name': 'In-Play', 'button_width': 'half', 'button_color': 'blue'},
        {'button_name': 'In-Play', 'button_width': 'half', 'button_color': 'blue'},
        {'button_name': 'In-Play', 'button_width': 'full', 'button_color': 'green'},
        {'button_name': 'Home', 'button_width': 'full', 'button_color': 'blue'}]
        :return namedtuple: created promotion info
        """
        now = datetime.now()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        date_from = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False, hours=-6,
                                            minutes=-1, days=-1)[:-3] + 'Z'
        date_to = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False, hours=-3,
                                          days=1)[:-3] + 'Z'
        parameters = {
            'id': '',
            'title_brand': '',
            'sortOrder': 0,
            'heightMedium': None,
            'widthMedium': None,
            'uriMedium': None,
            'htmlMarkup': '<p>Terms & Conditions: %s</p>' % fake.text(),
            'requestId': None,
            'vipLevelsInput': kwargs.get('vipLevelsInput', None),
            'validityPeriodStart': date_from,
            'validityPeriodEnd': date_to,
            'shortDescription': fake.sentence(),
            'promoKey': fake.md5(),
            'title': 'Auto ' + fake.city() + ' Promotion',
            'vipLevels': [
                0
            ],
            'lang': 'en',
            'brand': self.brand,
            'categoryId': kwargs.get('category_id', []),
            'showToCustomer': kwargs.get('show_to_user', 'both'),
            'disabled': False,
            'description': None,
            'directFileUrl': self.image_url,
            'useDirectFileUrl': True,
            'isSignpostingPromotion': False
        }
        promo_description_params = kwargs.get('promo_description', [])
        promotion_description = ''
        if promo_description_params and isinstance(promo_description_params, list):
            for description in promo_description_params:
                if 'link' in description:
                    link, link_name = description['link'], description.get('link_name', 'autotest_link')
                    promotion_description += self._promo_link_html(link=link, link_name=link_name)
                if 'button_name' in description:
                    button_name = description['button_name']
                    button_link = description.get('button_link', 'https://google.com')
                    button_width = description.get('button_width', 'full')
                    button_color = description.get('button_color', 'green')
                    handle_opt_in = description.get('is_it_opt_in_button', '')
                    promotion_description += self._promo_button_html(button_width=button_width,
                                                                     button_color=button_color,
                                                                     button_name=button_name,
                                                                     button_link=button_link,
                                                                     opt_in_button=handle_opt_in)
        kwargs.pop('promo_description', None)
        parameters.update(kwargs) if kwargs else parameters
        parameters['description'] = promotion_description if promotion_description else fake.text()
        data = json.dumps(parameters)
        promo = self.request.post('promotion', data=data)
        PromoParams = namedtuple('promotion_info', ['title', 'key', 'short_description', 'description', 'id'])
        promo_params = PromoParams(promo['title'], promo['promoKey'], promo['shortDescription'], promo['description'],
                                   promo['id'])
        self._logger.info('*** Added promotion {promo_params}'.format(promo_params=promo_params))
        self._created_promotions.append(promo_params.id)
        return promo_params

    def delete_promotion(self, id):
        path = 'promotion/%s' % id
        self.request.delete(path, parse_response=False)

    def get_promotions(self):
        path = 'promotion/brand/%s' % self.brand
        return self.request.get(path)

    def get_promotion_by_name(self, title: str, **kwargs):
        return list(filter(lambda promotion: promotion["title"].upper() == title.upper(), self.get_promotions()))[0]

    def get_promotion(self, promotion_id):
        path = 'promotion/%s' % promotion_id
        return self.request.get(path)

    def update_promotion(self, promotion_id, **kwargs):
        promotion = self.get_promotion(promotion_id)
        self._logger.info('*** Updating with: "%s"' % kwargs)
        promotion.update(kwargs)
        path = 'promotion/%s' % promotion_id
        data = json.dumps(promotion)
        self.request.put(path, data=data)

    # Banners

    def get_banners(self):
        path = 'banner/brand/%s' % self.brand
        return self.request.get(path)

    def get_bet_receipt_banner_name(self, league_name):
        id = self.get_league_info(league_name=league_name, info_name='banner')
        path = 'bet-receipt-banner/%s' % id
        try:
            return self.request.get(path)['name']
        except CMSException as e:
            raise CMSException('Cannot find bet receipt banner with id: "%s" for league: "%s",'
                               '\nRaised exception message:\n"%s"'
                               % (id, league_name, e.message))

    def _get_image_for_banner(self):
        required_image_parameters = ['desktopFilename', 'desktopUriMedium', 'desktopUriSmall',
                                     'filename', 'uriMedium', 'uriSmall']
        banners = self.get_banners()
        banner_ids = [banner['id'] for banner in banners]
        banner_with_image = None
        for banner_id in banner_ids:
            banner = self.get_banner(banner_id)
            if all(v is not None and v is not '' for v in
                   [banner[parameter] for parameter in required_image_parameters]):
                banner_with_image = banner
                break

        if not banner_with_image:
            raise CMSException('Cannot find available banner with image')
        image_parameters = {parameter: banner_with_image[parameter] for parameter in required_image_parameters}
        self._logger.debug('*** Found image parameters %s' % image_parameters)
        return image_parameters

    def add_banner(self, **kwargs) -> namedtuple:
        parameters = {
            'id': '',
            'alt': '',
            'brand': self.brand,
            'categoryId': '',
            'categoryName': 'default',
            'desktopFilename': {
                'filename': '',
                'originalname': '',
                'path': '',
                'size': 0,
                'filetype': ''
            },
            'desktopHeightMedium': '',
            'desktopTargetUri': '',
            'desktopUriMedium': '',
            'desktopUriSmall': '',
            'desktopWidthMedium': '',
            'disabled': False,
            'filename': {
                'filename': '',
                'originalname': '',
                'path': '',
                'size': 0,
                'filetype': 'image/jpeg'
            },
            'imageTitle': 'Auto ' + fake.city() + ' Banner',
            'imageTitle_brand': self.brand,
            'showToCustomer': 'both',
            'validityPeriodEnd': get_date_time_as_string(time_format='%Y-%m-%d', url_encode=False, days=1),
            'validityPeriodStart': get_date_time_as_string(time_format='%Y-%m-%d', url_encode=False),
            'vipLevels': [0],
            'targetUri': '',
            'vipLevelsInput': '',
            'desktopEnabled': True,
            'desktopInApp': True,
            'enabled': True
        }
        parameters.update(self._get_image_for_banner())
        parameters.update(kwargs) if kwargs else parameters
        data = json.dumps(parameters)
        banner = self.request.post('banner', data=data)
        BannerParams = namedtuple('banner_info', ['title', 'id'])
        banner_params = BannerParams(banner['imageTitle'], banner['id'])
        self._logger.info('*** Added banner {banner_params}'.format(banner_params=banner_params))
        self._created_banners.append(banner_params.id)
        return banner_params

    def get_banner(self, banner_id) -> dict:
        path = 'banner/%s' % banner_id
        return self.request.get(path)

    def update_banner(self, banner_id, **kwargs) -> dict:
        banner = self.get_banner(banner_id)
        banner.update(kwargs)
        path = 'banner/%s' % banner_id
        data = json.dumps(banner)
        return self.request.put(path, data=data)

    def upload_picture(self, banner_id):
        raise CMSException('Not working. Use _get_image_for_banner instead')

    def delete_banner(self, banner_id) -> None:
        path = 'banner/%s' % banner_id
        self.request.delete(path, parse_response=False)

    # offers

    def get_offer_modules(self) -> list:
        """
        Returns list of available Offer Modules
        :return:
        """
        path = 'offer-module/brand/%s' % self.brand
        return self.request.get(path)

    def create_offer_module(self, name='Offer Module: Auto test Offer Module', show_module_on='both') -> dict:
        """
        Create new offer module
        :param name: str: offer module name
        :param show_module_on: str: display on desktop, mobile on both device types
        :return: dict with offer details
        """
        path = f'offer-module'

        data = {
            "name": name,
            "showModuleOn": show_module_on,
            "sortOrder": 0,
            "brand": self.brand,
            "disabled": False,
        }

        data = json.dumps(data)
        offer_module = self.request.post(path, data=data)
        self._created_offer_module.append(offer_module.get('id'))
        return offer_module

    def update_offer_module(self, offer_module_id: str, name: str, **kwargs) -> None:
        """
        Update offer module
        :param name: str: updated offer module name
        :param offer_module_id: ID of offer needed to update
        """
        path = f'offer-module/{offer_module_id}'

        data = {
            "name": name,
            "showModuleOn": kwargs.get('showModuleOn', 'both'),
            "sortOrder": kwargs.get('sortOrder', 0),
            "brand": self.brand,
            "disabled": kwargs.get('disabled', False)
        }

        data = json.dumps(data)
        self.request.put(path, data=data)

    def delete_offer_modules(self, offer_module_id: str) -> None:
        """
        Method used to delete existing offer module
        :param offer_module_id: ID of offer needed to delete
        :return:
        """
        path = f'offer-module/{offer_module_id}'
        self.request.delete(path, parse_response=False)

    def get_offers(self) -> list:
        """
        Returns list of available Offers
        :return:
        """
        path = 'offer/brand/%s' % self.brand
        return self.request.get(path)

    def get_offers_for_device_type(self, device_type: str) -> list:
        """
        Returns list of available Offers
        :param device_type: device type to get offers - 'desktop', 'tablet' etc.
        :return: list of available Offers
        """
        path = get_cms_settings().config.public_api_url + 'v2/' + f'{self.brand}/offers/{device_type}'
        return self.request.get(path)

    def add_offer(self, offer_module_id, **kwargs) -> dict:
        """
        Method used to add offer into existing Offer Module
        :param offer_module_id: Id of existing Offer Module (by default – autotest module)
        :param kwargs: Any parameters needed to modify
        :return: Offer parameters
        """
        displayFrom_days = kwargs.get('displayFrom_days', 0)
        displayTo_days = kwargs.get('displayTo_days', 1)

        parameters = {
            'vipLevelsInput': kwargs.get('vipLevelsInput', ''),
            'module': offer_module_id,
            'targetUri': f'/{fake.uri_path()}',
            'displayFrom': get_date_time_as_string(time_format='%Y-%m-%dT%H:%M:%SZ', url_encode=False, days=displayFrom_days),
            'displayTo': get_date_time_as_string(time_format='%Y-%m-%dT%H:%M:%SZ', url_encode=False, days=displayTo_days),
            'name': f'Auto {fake.first_name_female()} Offer',
            'showOfferTo': kwargs.get('showOfferTo', 'both'),
            'showOfferOn': 'both',
            'id': '',
            'sortOrder': fake.random_int(min=1, max=100),
            'vipLevels': [],
            'brand': self.brand,
            'disabled': False,
            'useDirectImageUrl': True,
            'directImageUrl': self.image_url,
            'imageUri': '',
        }
        parameters.update(kwargs) if kwargs else parameters
        data = json.dumps(parameters)
        offer = self.request.post('offer', data=data)
        self._created_offers.append(offer.get('id'))
        return offer

    def update_offer(self, offer_module_id: str, offer_id:str, offer_name: str, **kwargs) -> None:
        """
        Update offer
        :param name: str: updated offer name
        :param offer_module_id: Offer module id
        :param offer_id: Offer id
        """
        displayFrom_days = kwargs.get('displayFrom_days', 0)
        displayTo_days = kwargs.get('displayTo_days', 1)

        path = f'offer/{offer_id}'

        data = {"id": offer_id,
                "module": offer_module_id,
                "targetUri": kwargs.get('targetUri', '/horse-racing'),
                "displayTo": get_date_time_as_string(time_format='%Y-%m-%dT%H:%M:%SZ', url_encode=False, days=displayTo_days),
                "displayFrom": get_date_time_as_string(time_format='%Y-%m-%dT%H:%M:%SZ', url_encode=False, days=displayFrom_days),
                "name": offer_name,
                "brand": self.brand,
                "disabled": kwargs.get('disabled', False),
                "showOfferTo": "both",
                "showOfferOn": "desktop"}

        data = json.dumps(data)
        self.request.put(path, data=data)

    def delete_offer(self, offer_id: str) -> None:
        """
        Method used to delete existing offer
        :param offer_id: ID of offer needed to delete
        :return:
        """
        path = 'offer/%s' % offer_id
        self.request.delete(path, parse_response=False)

    # widgets

    def get_widgets(self, widget_type: str = None) -> list:
        """
        Method used to get available widgets
        :param widget_type: str: widget type
        :return: List of widget's parameters
        """
        path = 'widget/brand/%s' % self.brand
        widgets = self.request.get(path)

        if widget_type:
            widgets = [widget for widget in widgets if widget['type'] == widget_type]

        return widgets

    def set_widget_ordering(self, new_order: list, moving_item):
        """
        Method allows to change widgets ordering in CMS
        :param new_order: list of sports e.g. ["5ed12f4cc9e77c0001f66909","5ecf9906c9e77c0001a0e57a","5ed12ef4c9e77c0001f66905"]
        :param moving_item: Item id e.g. '5ed12f4cc9e77c0001f66909'
        """
        data = {
            "order": new_order,
            "id": moving_item
        }
        data = json.dumps(data)
        path = f'widget/ordering'
        self.request.post(path, data=data, parse_response=False)

    def update_widget(self, widget_id, **kwargs):
        """
        Update a widget's properties based on the provided widget_id and keyword arguments.

        :param widget_id: The unique identifier of the widget to update.
        :type widget_id: int or str

        :param **kwargs: Keyword arguments for updating widget properties.
            Supported fields for update include 'title', 'columns', 'disabled', 'showExpanded',
            'showOnDesktop', 'showOnMobile', 'type', 'showFirstEvent', and 'type_brand'.

        :return: A response object containing the updated widget data.
        :rtype: dict

        This method retrieves a widget with the specified widget_id, updates its properties
        based on the provided keyword arguments, and sends a PUT request to update the widget
        on the server.

        :raises IndexError: If no widget with the specified widget_id is found in the list of widgets.
        """
        response = [widget for widget in self.get_widgets() if widget.get('id') == widget_id][0]
        path = f'widget/{widget_id}'

        fields_to_update = [
            'title', 'columns', 'disabled', 'showExpanded', 'showOnDesktop', 'showOnMobile',
            'type', 'showFirstEvent', 'type_brand'
        ]

        for field in fields_to_update:
            # Update the field with the value from kwargs if provided, otherwise use the current value.
            response[field] = kwargs.pop(field, response[field])

        # Convert the updated response to JSON data.
        data = json.dumps(response)

        # Send a PUT request to update the widget on the server.
        return self.request.put(path, data=data)

    def get_market_tabs_order(self):
        path = 'edp-market/brand/%s' % self.brand
        r = self.request.get(path)
        last_market = next((market['name'] for market in r if market['lastItem'] is True), '')
        markets_ordered = [market['name'] for market in r if market['lastItem'] is False]
        markets_ordered.append(last_market) if last_market else self._logger.info('No last market set on EDP')

        return markets_ordered

    # BYB Widget in homepage, Football SLP, BYB Mobile,Any Big Competition
    def get_byb_widget(self):
        """
        Method to get 'BYB Widget' for brand.
        :return: return Response from the API containing a list of BYB Widget Active Market Cards details
        """
        path = f'byb-widget/brand/{self.brand}'
        response = self.request.get(path)
        return response

    def get_byb_expired_market_cards(self):
        """
        Method to get 'BYB Expired Market Cards
        return: return response from the API containing a list of BYB Expired Market Cards
        """
        path = f'byb-widget-data/brand/{self.brand}/status?active=false'
        response = self.request.get(path)
        return response

    def update_byb_widget(self, **kwargs):
        """
        Method to update the BYB Widget with new attributes.

        Parameters:
        **kwargs: Arbitrary keyword arguments representing the attributes to be updated and their new values.

        Returns:
        response (dict): The response from the PUT request to update the BYB widget.
        """
        byb_response = self.get_byb_widget()
        path = f'byb-widget/{byb_response.get("id")}'
        if not byb_response:
            raise CMSException("unable to get BYB widget response")
        for attribute, value in kwargs.items():
            if attribute not in byb_response:
                raise CMSException(f'Attributes :"{attribute}" is not valid')
            byb_response[attribute] = value

        response = self.request.put(url=path, data=json.dumps(byb_response))
        return response

    def updated_byb_expired_market_cards(self,market_card_id,**kwargs):
        """
        Method to update an expired market card in the BYB Widget.

        Parameters:
        market_card_id (str): The ID of the expired market card to be updated.
        **kwargs: Arbitrary keyword arguments representing the attributes to be updated and their new values.

        Returns:
        response (dict): The response from the PUT request to update the expired market card.
        """
        byb_widget_expiry_cards = self.get_byb_expired_market_cards()

        market_response = next(
            (byb_widget_data for byb_widget_data in byb_widget_expiry_cards if byb_widget_data['id'] == market_card_id), None)
        if not market_response:
            raise CMSException(f'Unable to fetch market card response for given market id: "{market_card_id}"')

        path = f'byb-widget-data/{market_card_id}'
        for attribute, value in kwargs.items():
            if attribute not in market_response:
                raise CMSException(f'Attributes :"{attribute}" is not valid')
            market_response[attribute] = value

        response = self.request.put(url=path, data=json.dumps(market_response))
        return response

    def create_new_market_cards(self, title,event_id,market_id,locations:[],**kwargs):
        """
        Creates new market cards with the given details and sends a POST request to the specified endpoint.

        Args:
            title (str): The title of the market card.
            event_id (str): The ID of the event associated with the market card.
            market_id (str): The ID of the market associated with the market card.
            locations (list): A list of location identifiers.
            **kwargs: Additional keyword arguments:
                - date_from (str): Optional. The start date and time for the card display in ISO format.
                  Defaults to one minute before the current time.
                - date_to (str): Optional. The end date and time for the card display in ISO format.
                  Defaults to one day and ten hours from the current time.
                - sortOrder (int): Optional. The sort order of the market card. Defaults to 0.

        Returns:
        dict: The response from the POST request, which includes the ID of the created market card.
        """
        now = datetime.now()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        date_from = kwargs.get('date_from', get_date_time_as_string(date_time_obj=now, time_format=time_format,
                                                                    minutes=-1,url_encode=False)[:-3] + 'Z')
        date_to = kwargs.get('date_to', get_date_time_as_string(date_time_obj=now, time_format=time_format,
                                                                url_encode=False, days=1, hours=-10)[:-3] + 'Z')
        path = 'byb-widget-data'
        payload = {
            'id': None,
            'displayFrom': date_from,
            'displayTo': date_to,
            'title': title,
            'eventId': event_id,
            'marketId': market_id,
            'brand': self.brand,
            'locations': locations,
            "sortOrder": kwargs.get("sortOrder", 0)

        }

        response = self.request.post(url=path,data=json.dumps(payload))
        self._create_byb_widget.append(response.get('id'))
        return response

    def update_market_cards(self, market_card_id,**kwargs):
        """
        Method to update an existing market card in the BYB Widget.

        Parameters:
        market_card_id (str): The ID of the market card to be updated.
        **kwargs: Arbitrary keyword arguments representing the attributes to be updated and their new values.

        Returns:
        response (dict): The response from the PUT request to update the market card.
        """
        byb_widget = self.get_byb_widget()
        byb_widget_datas = byb_widget.get('data')

        market_response = next((byb_widget_data for byb_widget_data in byb_widget_datas if byb_widget_data['id'] == market_card_id), None)
        if not market_response:
            raise CMSException(f'Unable to fetch market card response for given market id: "{market_card_id}"')

        path = f'byb-widget-data/{market_card_id}'
        for attribute, value in kwargs.items():
            if attribute not in market_response:
                raise CMSException(f'Attributes :"{attribute}" is not valid')
            market_response[attribute] = value

        response = self.request.put(url=path, data=json.dumps(market_response))
        return response

    def set_byb_widget_ordering(self, new_order: list, moving_item):
        """
        Method allows to change byb widgets ordering in CMS
        :param new_order: list of sports e.g. ["5ed12f4cc9e77c0001f66909","5ecf9906c9e77c0001a0e57a","5ed12ef4c9e77c0001f66905"]
        :param moving_item: Item id e.g. '5ed12f4cc9e77c0001f66909'
        """
        data = {
            "order": new_order,
            "id": moving_item
        }
        data = json.dumps(data)
        path = f'byb-widget-data/ordering'
        self.request.post(path, data=data, parse_response=False)

    def delete_byb_widget(self, market_card_id):
        """
        Method to delete a 'byb widget' based on its ID.
        :params byb_widget_id: The ID of the byb widget to be deleted.
        :return: None
        """
        path = f'byb-widget-data/{market_card_id}'
        return self.request.delete(path, parse_response=False)

    # 5-A-Side
    def get_five_a_side_formations(self) -> list:
        """
        Returns list of 5-A-Side formations
        :return:
        """
        content = \
            self.request.get(url=get_cms_settings().config.public_api_url + f'{self.brand}/five-a-side-formations')
        return content

    # YourCall part

    def get_your_call_leagues(self):
        path = 'your-call-league/brand/%s' % self.brand
        r = self.request.get(path)
        return r

    def get_your_call_markets(self):
        path = 'your-call-market/brand/%s' % self.brand
        r = self.request.get(path)
        return r

    def get_build_your_bet_markets(self) -> list:
        """
        Method used to get BYB markets mapping on EDP
        :return: list of BYB market dicts
        """
        path = 'byb-market/brand/%s' % self.brand
        return self.request.get(path)

    def get_your_call_market_info(self, market_name):
        your_call_markets = self.get_your_call_markets()

        your_call_market_info = next((market_info for market_info in your_call_markets
                                      if market_name in market_info.values()),
                                     None)
        if not your_call_market_info:
            raise CMSException('Market "%s" was not found among #YourCall markets %s ' % market_name)
        return your_call_market_info

    def is_your_call_static_block_enabled(self, title='yourcall-page') -> bool:
        """
        Method to check enabled status for required
        :param title: cms title parameter for required yourcall static block
        :type title: str
        :return: is enabled state
        """
        yc_static_block = self.get_your_call_static_block_by_title(title=title, public=False)
        is_yc_static_block_enabled = yc_static_block.get('enabled')
        return is_yc_static_block_enabled

    def get_your_call_static_block_by_title(self, title, public=True) -> dict:
        """
        Method to get yourcall static block parameters
        :param title: cms title parameter for required yourcall static block
        :param public: use public api for get call and private for update
        :return: yourcall static block's parameters
        """
        if public:
            static_blocks = self.get_your_call_static_block()
        else:
            static_blocks = self._get_private_your_call_static_block()
        yc_static_block = next((static_block for static_block in static_blocks if static_block['title'] == title), None)
        if not yc_static_block:
            yc_static_blocks = [static_block['title'] for static_block in static_blocks]
            raise CMSException(f'YC Static block "{title}" was not found among {yc_static_blocks}')
        return yc_static_block

    def update_your_call_static_block(self, title, **kwargs) -> dict:
        """
        Method to update yourcall static block
        :param title: cms title parameter for required yourcall static block
        :param kwargs: parameters needed to update
        :return: Update static block parameters
        """
        yc_static_block = self.get_your_call_static_block_by_title(title=title, public=False)
        your_call_static_block_id = yc_static_block.get('id')
        yc_static_block.update(kwargs)
        path = 'your-call-static-block/%s' % your_call_static_block_id
        data = json.dumps(yc_static_block)
        return self.request.put(path, data=data)

    def _get_private_your_call_static_block(self):
        path = 'your-call-static-block/brand/%s' % self.brand
        content = self.request.get(path)
        return content

    def get_your_call_static_block(self):
        content = self.request.get(url=get_cms_settings().config.public_api_url + f'{self.brand}/yc-static-block')
        return content

    def get_your_call_league_info(self, league_name):
        your_call_leagues = self.get_your_call_leagues()

        your_call_league_info = next((league_info for league_info in your_call_leagues
                                      if league_name in league_info.values()),
                                     None)
        if not your_call_league_info:
            raise CMSException('League : "%s" was not found on YourCall Leagues page' % league_name)
        return your_call_league_info

    def horse_racing_your_call_static_block(self, htmlMarkup):
        static_blocks = self._get_private_your_call_static_block()
        block = next(block for block in static_blocks if block['title'] == 'yourcall-racing')
        path = f'your-call-static-block/{block["id"]}'
        params = {'id': block['id'],
                  'titleBrand': block['titleBrand'],
                  'title': 'yourcall-racing',
                  'lang': block['lang'],
                  'brand': block['brand'],
                  'enabled': True,
                  'htmlMarkup': htmlMarkup}
        return self.request.put(path, data=json.dumps(params))

    def your_call_league_switcher(self, **kwargs):
        league_key = kwargs.get('league_key', '5a12c99ef1de47000bcbe1a5')
        league_name = kwargs.get('league_name', 'English Premiere League')
        type_id = kwargs.get('type_id', 442)
        status = kwargs.get('status', True)
        path = 'your-call-league/%s' % league_key

        league_info = self.get_your_call_league_info(league_name=league_name)
        payload = {
            'id': league_key,
            'sortOrder': 1,
            'name': league_name,
            'lang': 'en',
            'brand': self.brand,
            'enabled': status,
            'typeId': type_id
        }

        if status != league_info['enabled']:
            self.request.put(path, data=json.dumps(payload))

    # Odds Boost

    def update_odds_boost_config(self,
                                 enabled=True,
                                 logged_in_header_text=None,
                                 logged_out_header_text=None,
                                 terms_and_conditions_text=None):
        config = self.request.get(url=get_cms_settings().config.api_url + f'odds-boost/{self.brand}')

        default_logged_in_text = config['loggedInHeaderText']
        default_logged_out_text = config['loggedOutHeaderText']
        default_terms_and_conditions_text = config['termsAndConditionsText']
        svg = config['svg']
        svg_id = config['svgId']
        svg_filename = config['svgFilename']

        logged_in_header_text = logged_in_header_text if logged_in_header_text else default_logged_in_text
        logged_out_header_text = logged_out_header_text if logged_out_header_text else default_logged_out_text
        terms_and_conditions_text = terms_and_conditions_text if terms_and_conditions_text else default_terms_and_conditions_text

        body = {
            'id': self.brand,
            'sortOrder': None,
            'enabled': enabled,
            'loggedInHeaderText': logged_in_header_text,
            'loggedOutHeaderText': logged_out_header_text,
            'lang': 'en',
            'svg': svg,
            'svgId': svg_id,
            'svg_filename': svg_filename,
            'termsAndConditionsText': terms_and_conditions_text,
            'brand': self.brand
        }
        self.request.put(url=get_cms_settings().config.api_url + f'odds-boost/{self.brand}', data=json.dumps(body))

    # System Configuration Config

    def get_config_id(self, config_name):
        """
        :param config_name: enter the config_name for which you want to get id
        :return: id of provided config_name
        """
        path = 'configuration/brand/%s' % self.brand
        response = self.request.get(path)
        for config in response['config']:
            if config['name'] == config_name:
                return config['id']
        else:
            raise Exception('Configuration name "%s" does not exists' % config_name)

    def update_yourcall_icons_tabs(self, enable_icon=True, enable_tab=True):
        id = self.get_config_id(config_name='YourCallIconsAndTabs')
        path = 'configuration/brand/%s/element/%s' % (self.brand, id)
        payload = {'id': id,
                   'name': 'YourCallIconsAndTabs',
                   'items': [{'multiselectValue': None,
                              'name': 'enableIcon',
                              'type': 'checkbox',
                              'value': enable_icon},

                             {'multiselectValue': None,
                              'name': 'enableTab',
                              'type': 'checkbox',
                              'value': enable_tab}
                             ]
                   }
        return self.request.put(path, data=json.dumps(payload))

    def add_coupon_segment(self, coupon_ids: str, **kwargs) -> dict:
        """
        :param coupon_ids: coupon ids 643, 447, check .yaml file to get ids
        :return: dict
        """
        custom_title = kwargs.get('segment_name')
        title = custom_title if custom_title else 'Auto segment' + fake.city()
        date = datetime.now()
        today_day_name = date.strftime('%A')
        path = 'coupon-segment'
        params = {
            "brand": self.brand,
            "title": title,
            "couponKeys": str(coupon_ids),
            "scheduleType": 0,
            "dayOfWeekArr": [
                {"dayName": today_day_name.upper(), "checked": True}
            ],
            "dayOfWeek": [today_day_name.upper()]
        }
        data = json.dumps(params)
        coupon_segment = self.request.post(path, data=data)
        self._created_coupon_segment.append(coupon_segment.get('id'))
        return coupon_segment

    def delete_coupon_segment(self, coupon_segment_id: str) -> None:
        """
        Delete coupon segment from CMS
        :param coupon_segment_id: specifies id of coupon segment
        """
        path = f'coupon-segment/{coupon_segment_id}'
        self.request.delete(path, parse_response=False)

    def new_coupon_badge_switcher(self, status):
        id = self.get_config_id(config_name='FootballCouponsNewBadge')
        path = 'configuration/brand/%s/element/%s' % (self.brand, id)
        payload = {
            'id': id,
            'name': 'FootballCouponsNewBadge',
            'items': [
                {
                    'multiselectValue': '',
                    'name': 'enableCouponNewBadge',
                    'type': 'checkbox',
                    'value': status
                },
                {
                    'multiselectValue': '',
                    'name': 'couponName',
                    'type': 'input',
                    'value': 'Goalscorer'}
            ]
        }
        current_state = self.get_system_configuration_item('FootballCouponsNewBadge').get('enableCouponNewBadge')
        if status != current_state:
            self.request.put(path, data=json.dumps(payload))

    # System Configuration Structure

    def get_system_configuration_structure(self):
        self._logger.warning(f'"{__name__}" is deprecated; use "get_initial_data" method')
        path = '%s/system-configuration' % self.brand
        response = self.request.get(get_cms_settings().config.public_api_url + path)
        return response

    def get_system_configuration_item(self, item: str):
        path = f'{self.brand}/system-configurations/{item}'
        try:
            return self.request.get(get_cms_settings().config.public_api_url + path)
        except InvalidResponseException:
            return {}

    def get_initial_data(self, device_type: str = 'mobile', cached: bool = False) -> dict:
        """
        Used to retrieve information needed for initial site load
        :param device_type: mobile or desktop (tablet is mobile)
        :param cached: Returns cached data if True. if False – makes new request
        :return:
        """
        path = f'{self.brand}/initial-data/{device_type}'

        if cached and self._cached_initial_data.get(device_type):
            self._logger.debug(f'*** Returning cached response for {path} on {self.env}')
            initial_data = self._cached_initial_data.get(device_type)
        else:
            initial_data = self.request.get(get_cms_settings().config.public_api_url + path)
            self._cached_initial_data[device_type] = initial_data
        return initial_data

    def update_system_configuration_structure(self, config_item: str, field_name: str, field_value):
        """
        General method for updating CMS System Structure
        :param config_item: Config item. e.g. CompetitionsFootball, NextRaces...
        :param field_name: Available config item's field
        :param field_value: Field value
        :return: Updated System Structure
        """
        system_configuration = self.get_system_configuration_structure()
        try:
            system_configuration[config_item][field_name] = field_value
        except KeyError:
            raise CMSException(f'Config item/name {config_item}/{field_name} not found in System Structure')
        path = f'structure/brand/{self.brand}'
        payload = {
            'lang': 'en',
            'brand': self.brand,
            'structure': system_configuration
        }
        request = self.request.put(path, data=json.dumps(payload))
        self._cached_initial_data = {'mobile': None, 'desktop': None}  # so new data will be returned for the next request
        return request

    # Quick links

    def create_quick_link(self, title: str, sport_id: int, page_type: str = 'sport', date_from: str = None,
                          date_to: str = None, destination: str = 'https://invictus-coral.co.uk', **kwargs: dict) -> dict:
        """
        Create Quick link for Sports and Event Hubs pages
        :param title: str, title for quick link
        :param sport_id: int, for example for homepage sport_id=0 for football sport_id=16, ID is getting from OpenBet
        :param page_type: str, page type where quick link module is configured. E.g.: 'sport', 'eventhub'
        :param date_from: str, start time at which module will be displayed. E.g.: "2019-10-25T13:20:30.633Z"
        :param date_to: str, end time at which module will be undisplayed. E.g.: "2019-10-26T13:20:30.633Z"
        :param destination: str, redirect to page
        :return: dict, created module configuration
        """
        now = datetime.now()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        if not date_from:
            date_from = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False, hours=-3,
                                                minutes=-1)[:-3] + 'Z'
        if not date_to:
            date_to = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False, hours=-3,
                                              days=1)[:-3] + 'Z'
        path = 'sport-quick-link'
        params = {
            'id': 'default',
            'sportId': sport_id,
            'pageId': sport_id,
            'pageType': page_type,
            'brand': self.brand,
            'disabled': False,
            'sortOrder': None,
            'destination': destination,
            'title': title,
            'validityPeriodEnd': date_to,
            'validityPeriodStart': date_from,
            'svg': '',
            'svgId': kwargs.get('svgId', None),
            'svgFilename': {
                'filename': '',
                'path': '',
                'size': 0,
                'filetype': ''
            },
            'inclusionList': kwargs.get('inclusionList', []),
            'universalSegment': kwargs.get('universalSegment', True),
            'exclusionList': kwargs.get('exclusionList', [])
        }
        data = json.dumps(params)
        quick_link = self.request.post(path, data=data)
        self._created_quick_links.append(quick_link.get('id'))
        return quick_link

    def get_quick_link(self, quick_link_id: str):
        """
        Retrieve a quick link resource by its unique identifier.
        Args:
            quick_link_id (str): The unique identifier of the quick link to retrieve.

        Returns:
            dict: A dictionary representing the quick link resource if found, or None if not found.
        This method sends a GET request to the 'sport-quick-link' API endpoint with the provided
        quick_link_id to fetch the corresponding quick link resource.
        """
        path = f'sport-quick-link/{quick_link_id}'
        return self.request.get(path)

    def update_quick_link(self, quick_link_id: str, **kwargs):
        """
        Update a quick link resource with the specified quick_link_id using the provided data.
        Args:
            quick_link_id (str): The unique identifier of the quick link to update.
            **kwargs: Additional keyword arguments to specify the updated fields of the quick link.
        Returns:
            dict: A dictionary representing the response from the update request.
        This method allows you to update an existing quick link resource identified by the
        quick_link_id with new data. You can specify the fields to be updated using the keyword
        arguments (**kwargs), where each argument corresponds to a specific field in the quick
        link resource.
        Parameters:
            - quick_link_id (str): The unique identifier of the quick link to update.
            - **kwargs (dict): Keyword arguments to specify the updated fields. You can provide
              values for the following fields:
              - sortOrder (int): The sorting order of the quick link.
              - pageId (str): The identifier of the associated page.
              - pageType (str): The type of the page.
              - disabled (bool): Indicates whether the quick link is disabled.
              - segmentReferences (list): A list of segment references.
              - exclusionList (list): A list of exclusions.
              - inclusionList (list): A list of inclusions.
              - fanzoneInclusions (list): A list of fanzone inclusions.
              - archivalId (str): The archival identifier.
              - universalSegment (str): The universal segment identifier.
              - message (str): A message associated with the quick link.
              - title (str): The title of the quick link.
              - destination (str): The destination URL or reference.
              - svg (str): The SVG representation.
              - svgFilename (str): The filename of the SVG.
              - svgId (str): The SVG identifier.
              - validityPeriodEnd (str): The end of the validity period.
              - validityPeriodStart (str): The start of the validity period.
              - sportId (str): The identifier of the sport associated with the quick link.
        Returns:
            dict: A dictionary representing the response from the update request contains all response of quick link.
        """
        quick_link_data = self.get_quick_link(quick_link_id=quick_link_id)
        path = f'sport-quick-link/{quick_link_id}'
        for key in quick_link_data.keys():
            if key in kwargs:
                quick_link_data[key] = kwargs[key]
        data = json.dumps(quick_link_data)
        request = self.request.put(path, data=data)
        return request

    def get_quick_links(self, sport_id: str, segment='Universal') -> list:
        """
        :param sport_id: str for example for homepage sport_id=0 for football sport_id=16, ID is getting from OpenBet
        :return: list
        """
        path = f'sport-quick-link/brand/{self.brand}/segment/{segment}/sport/{int(sport_id)}'
        response = self.request.get(path)
        filter_by_page_id = list(filter(lambda param: param['pageId'] == str(sport_id), response))
        return filter_by_page_id

    def change_quick_link_state(self, quick_link_object: dict, active: bool = True) -> None:
        """
        :param quick_link_object: dict created object with params
        :param active: True/False Quick link becomes Enabled/Disabled
        :return:
        """
        quick_link_id = quick_link_object.get('id')
        quick_link_title = quick_link_object.get('title')
        path = f'sport-quick-link/{quick_link_id}'
        quick_link_object['disabled'] = not active
        self._logger.debug(f'*** Quick link "{quick_link_title}" changed state to "{active}"')
        self.request.put(path, data=json.dumps(quick_link_object))

    def delete_quick_link(self, quick_link_id: str) -> None:
        """
        Delete quick link from CMS
        :param quick_link_id: specifies id of quick link
        """
        path = f'sport-quick-link/{quick_link_id}'
        self.request.delete(path, parse_response=False)

    def get_desktop_quick_links(self) -> list:
        """
        DESCRIPTION: Get all available Desktop quick links (Quick links) configuration info
        :return: List with all available desktop quick links configuration info
        """
        path = f'desktop-quick-link/brand/{self.brand}'
        return self.request.get(path)

    def get_desktop_quick_link(self, desktop_quick_link_id: str):
        """
        Retrieve a desktop quick link resource by its unique identifier.
        Args:
            desktop_quick_link_id (str): The unique identifier of the destop quick link to retrieve.

        Returns:
            dict: A dictionary representing the dsktop quick link resource if found, or None if not found.
        This method sends a GET request to the 'desktop-quick-link' API endpoint with the provided
        desktop_quick_link_id to fetch the corresponding desktop quick link resource.
        """
        path = f'desktop-quick-link/{desktop_quick_link_id}'
        return self.request.get(path)

    def create_desktop_quick_links(self, title: str, target_url: str , **kwargs: dict) -> dict:
        """
        Create Desktop Quick link
        :param title: str, title for quick link
        :param target: str, redirect to page
        :return: dict, created module configuration
        """
        path = 'desktop-quick-link'
        payload = {"brand": self.brand,
                   "collectionType": kwargs.get("collectionType", ""),
                   "disabled": kwargs.get("disabled", False),
                   "filename":
                       {
                           "filename": kwargs.get("filename", ""),
                           "originalfilename": kwargs.get("originalfilename", ""),
                           "path": kwargs.get("path", ""),
                           "size": kwargs.get("size", 0),
                           "filetype": kwargs.get("filetype", ""),
                       },
                   "isAtoZQuickLink": kwargs.get("isAtoZQuickLink", False),
                   "sortOrder": 0,
                   "spriteClass": kwargs.get("spriteClass", ""),
                   "target": target_url,
                   "title": title
                    }
        data = json.dumps(payload)
        response = self.request.post(path,data=data)
        self._created_desktop_quick_links.append(response.get('id'))
        return response

    def update_desktop_quick_links(self, desktop_quick_link_id: str, **kwargs):
        """
        Update a dektop quick link resource with the specified desktop_quick_link_id using the provided data.
        Args:
            desktop_quick_link_id (str): The unique identifier of the desktop quick link to update.
            **kwargs: Additional keyword arguments to specify the updated fields of the desktop quick link.
        Returns:
            dict: A dictionary representing the response from the update request.
        This method allows you to update an existing desktop quick link resource identified by the
        desktop_quick_link_id with new data. You can specify the fields to be updated using the keyword
        arguments (**kwargs), where each argument corresponds to a specific field in the desktop quick
        link resource.
        """
        response = self.get_desktop_quick_link(desktop_quick_link_id=desktop_quick_link_id)
        path = f'desktop-quick-link/{desktop_quick_link_id}'
        fields_to_update = [
            'collectionType', 'disabled', 'filename', 'isAtoZQuickLink', 'sortOrder', 'spriteClass', 'target', 'title'
        ]
        for field in fields_to_update:
            response[field] = kwargs.pop(field, response[field])
        data = json.dumps(response)
        return self.request.put(path,data=data)

    def delete_desktop_quick_lnk(self, desktop_quick_link_id: str) -> None:
        """
        Delete desktop quick link from CMS
        :param desktop_quick_link_id: specifies id of desktop quick link
        """
        path = f'desktop-quick-link/{desktop_quick_link_id}'
        self.request.delete(path, parse_response=False)

    # Super Button
    def get_mobile_super_buttons(self) -> list:
        """
        DESCRIPTION: Get all available Super Buttons (Quick links) configuration info
        :return: List with all available Super Buttons configuration info
        """
        path = 'navigation-points/brand/%s' % self.brand
        content = self.request.get(path)
        return content

    def add_mobile_super_button(self, **kwargs: dict) -> dict:
        """
        Creates Super Button
        :param kwargs: Named arguments of parameters which should be set during the creation
        :return: Supper Button configuration info
        :themes takes: theme_1, theme_2, theme_3, theme_4, theme_5, theme_6
        """
        name = kwargs.get('name', 'Auto Super ' + fake.city())
        name = name[:25]  # There is limitation for 'name' field to contain 25 characters max
        super_button_id = next((super_button['id'] for super_button in self.get_mobile_super_buttons()
                                if super_button['title'].upper() == name.upper()), None)
        if super_button_id:
            raise CMSException(f'Super button with name "{name}" is already present')
        path = 'navigation-points'

        now = datetime.utcnow()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        display_from = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False, hours=-3,
                                               minutes=-1)[:-3] + 'Z'
        display_to = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False, hours=-3,
                                             days=1)[:-3] + 'Z'

        payload = {'brand': self.brand,
                   'categoryId': kwargs.get('category_id', [1, 51, 5, 6, 16]),
                   'competitionId': kwargs.get('competition_id', ['5b9ba9f3c9e77c0001e8750a',
                                                                  '5bbb35a8c9e77c000131cd08',
                                                                  '5a7b1e20c9e77c0001258ae4',
                                                                  '5af2a6a2c9e77c0001a12a76',
                                                                  '5ba8a36cc9e77c0001900dd9']),
                   'ctaAlignment': kwargs.get('ctaAlignment','center'),
                   'description': kwargs.get('description', 'Auto Test Super Button. DO NOT EDIT/DELETE it'),
                   'enabled': kwargs.get('enabled', True),
                   'homeTabs': kwargs.get('home_tabs', ['/home/buildyourbet',
                                                        '/home/coupons',
                                                        '/home/featured',
                                                        '/home/in-play',
                                                        '/home/live-stream',
                                                        '/home/next-races',
                                                        '/home/multiples',
                                                        '/home/top-bets',
                                                        '/home/multiples']),
                   'targetUri': kwargs.get('target_uri', '/sport/football/matches'),
                   'title': name,
                   'exclusionList': kwargs.get('exclusionList', []),
                   'inclusionList': kwargs.get('inclusionList', []),
                   'message': kwargs.get('message', None),
                   'shortDescription': kwargs.get('shortDescription', ""),
                   'themes': kwargs.get('themes', 'theme_1'),
                   'universalSegment': kwargs.get('universalSegment', True),
                   'validityPeriodStart': kwargs.get('validity_period_start', display_from),
                   'validityPeriodEnd': kwargs.get('validity_period_end', display_to),
                   }
        super_button = self.request.post(path, data=json.dumps(payload))
        self._created_super_buttons.append(super_button.get('id'))
        return super_button

    def update_mobile_super_button(self, name: str, **kwargs: dict) -> dict:
        """
        DESCRIPTION: Allows to update Super Button (Quick link) based on it name
        :param name: Super Button name
        :param kwargs: Named arguments of parameters which should be updated
        :return: Updated super button configuration info
        """
        super_button = next((quick_link for quick_link in self.get_mobile_super_buttons()
                             if quick_link['title'].upper() == name.upper()), None)
        if not super_button:
            raise CMSException(f'Supper Button, "{name}", not found!')
        path = f'navigation-points/{super_button["id"]}'
        payload = {'brand': self.brand,
                   'archivalId': super_button.get('archivalId'),
                   'categoryId': kwargs.get('category_id', super_button['categoryId']),
                   'competitionId': kwargs.get('competition_id', super_button['competitionId']),
                   'competitionTabs' : kwargs.get('competitiontabs', super_button.get('competitionTabs')),
                   'ctaAlignment': kwargs.get('ctaAlignment', super_button.get('ctaAlignment')),
                   'description': kwargs.get('description', super_button['description']),
                   'enabled': kwargs.get('enabled', super_button['enabled']),
                   'homeTabs': kwargs.get('home_tabs', super_button['homeTabs']),
                   'id': super_button['id'],
                   'sortOrder': kwargs.get('sortOrder', super_button['sortOrder']),
                   'targetUri': kwargs.get('target_uri', super_button['targetUri']),
                   'title': kwargs.get('title', super_button['title']),
                   'themes': kwargs.get('themes', super_button['themes']),
                   'message': kwargs.get('message', super_button.get('message')),
                   'shortDescription': kwargs.get('shortDescription', super_button.get('shortDescription')),
                   'validityPeriodEnd': kwargs.get('validity_period_end', super_button['validityPeriodEnd']),
                   'validityPeriodStart': kwargs.get('validity_period_start', super_button['validityPeriodStart']),
                   'inclusionList': kwargs.get('inclusionList', []),
                   'segmentReferences': kwargs.get('segmentReferences', super_button.get('segmentReferences')),
                   'universalSegment': kwargs.get('universalSegment', True),
                   'exclusionList': kwargs.get('exclusionList', [])
                   }
        return self.request.put(path, data=json.dumps(payload))

    def delete_mobile_super_button(self, super_button_id: str) -> None:
        """
        Delete super button
        :param super_button_id: ID of super button to delete
        """
        super_button = next((super_button for super_button in self.get_mobile_super_buttons()
                             if super_button['id'] == super_button_id), None)
        if not super_button:
            raise CMSException(f'Supper Button not found.')
        path = f'navigation-points/{super_button["id"]}'
        self.request.delete(path, parse_response=False)

    # special super button

    def get_mobile_special_super_buttons(self) -> list:
        """
        DESCRIPTION: Get all available Special Super Buttons (Quick links) configuration info
        :return: List with all available Special Super Buttons configuration info
        """
        path = 'extra-navigation-points/brand/%s' % self.brand
        content = self.request.get(path)
        return content

    def add_mobile_special_super_button(self, **kwargs: dict) -> dict:
        """
        Creates Special Super Button
        :param kwargs: Named arguments of parameters which should be set during the creation
        :param kwargs > competitionId: we need send the list of competition ids, even if you have a single competition id you need to send it in a list
        ex:['624aae821e95733e71f6c08e','624aae821e95733e71f6c08e']
        :return:  Special Supper Button configuration info
        Euro 2020-60bdddb9f5fd565980012000
        Cheltenham Festival-61b7b0f5e3676d0321cfee7f
        Grand National-624aae821e95733e71f6c08e
        IPL-636cd6d7b5c0ff3d3a07e4a3
        World Cup-6421bbbaa330930b97a70458
        Wimbledon-6436b7abf384850eeca22a00
        Rugby World Cup-643f9c91045c09524a01f212
        Royal Ascot-643f9d30e0b542513a6cb90a
        King George VI Chase-643fa139045c09524a01f22a
        UEFA EURO-643fa4f7e0b542513a6cb924
        Womens World Cup Football-643fa635045c09524a01f249
        """
        name = kwargs.get('name', 'Auto Special Super ' + fake.city())
        name = name[:25]  # There is limitation for 'name' field to contain 25 characters max
        special_super_button_id = next((special_super_button['id'] for special_super_button in self.get_mobile_special_super_buttons()
                                if special_super_button['title'].upper() == name.upper()), None)
        if special_super_button_id:
            raise CMSException(f'Special Super button with name "{name}" is already present')
        path = 'extra-navigation-points'

        now = datetime.utcnow()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        display_from = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False, hours=-3,
                                               minutes=-1)[:-3] + 'Z'
        display_to = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False, hours=-3,
                                             days=1)[:-3] + 'Z'

        description = kwargs.get('description',  'Auto Special Super ButtonDO NOT DELETE')
        description = description[:40]  # There is limitation for 'name' field to contain 45 characters max

        payload = {'brand': self.brand,
                   'categoryId': kwargs.get('category_id', [1, 51, 5, 6, 16]),
                   'competitionId': kwargs.get('competition_id', []),
                   'description': description,
                   'enabled': kwargs.get('enabled', True),
                   'homeTabs': kwargs.get('home_tabs', ['/home/featured']),
                   'targetUri': kwargs.get('target_uri', '/sport/football/matches'),
                   'title': name,
                   'validityPeriodStart': kwargs.get('validity_period_start', display_from),
                   'validityPeriodEnd': kwargs.get('validity_period_end', display_to),
                   'featureTag': '1-2-Free'
                   }
        special_super_button = self.request.post(path, data=json.dumps(payload))
        self._created_special_super_buttons.append(special_super_button.get('id'))
        return special_super_button

    def update_mobile_special_super_button(self, name: str, **kwargs: dict) -> dict:
        """
        DESCRIPTION: Allows to update Special Super Button (Quick link) based on it name
        :param name: Special super Button name
        :param kwargs: Named arguments of parameters which should be updated
        :return: Updated special super button configuration info
        """
        special_super_button = next((quick_link for quick_link in self.get_mobile_special_super_buttons()
                             if quick_link['title'].upper() == name.upper()), None)
        if not special_super_button:
            raise CMSException(f'Special Supper Button, "{name}", not found!')
        path = f'extra-navigation-points/{special_super_button["id"]}'
        payload = {'brand': self.brand,
                   'categoryId': kwargs.get('category_id', special_super_button['categoryId']),
                   'competitionId': kwargs.get('competition_id', special_super_button['competitionId']),
                   'competitionTabs' : kwargs.get('competitiontabs', special_super_button.get('competitionTabs')),
                   'description': kwargs.get('description', special_super_button['description']),
                   'enabled': kwargs.get('enabled', special_super_button['enabled']),
                   'homeTabs': kwargs.get('home_tabs', special_super_button['homeTabs']),
                   'id': special_super_button['id'],
                   'sortOrder': kwargs.get('sortOrder', special_super_button['sortOrder']),
                   'targetUri': kwargs.get('target_uri', special_super_button['targetUri']),
                   'title': kwargs.get('title', special_super_button['title']),
                   'validityPeriodEnd': kwargs.get('validity_period_end', special_super_button['validityPeriodEnd']),
                   'validityPeriodStart': kwargs.get('validity_period_start', special_super_button['validityPeriodStart']),
                   'featureTag':  kwargs.get('featureTag', special_super_button['featureTag'])
                   }
        return self.request.put(path, data=json.dumps(payload))

    def delete_mobile_special_super_button(self, special_super_button_id: str) -> None:
        """
        Delete special super button
        :param special_super_button_id: ID of special super button to delete
        """
        special_super_button = next((special_super_button for special_super_button in self.get_mobile_special_super_buttons()
                             if special_super_button['id'] == special_super_button_id), None)
        if not special_super_button:
            raise CMSException(f'Special Supper Button not found.')
        path = f'extra-navigation-points/{special_super_button["id"]}'
        self.request.delete(path, parse_response=False)

    # Sport/Race Landing page

    def get_olympic_sport(self, sport_name):
        path = 'sports/?brand=%s' % self.brand
        r = self.request.get(path)
        sport = next((sport for sport in r if sport['ssCategoryCode'] == sport_name.replace(' ', '_').upper()), None)
        if not sport:
            raise CMSException('No data found for %s sport' % sport_name)
        return sport

    def get_fixture_header(self, sport_name):
        sport_data = self.get_olympic_sport(sport_name)
        template_type = sport_data.get('outcomesTemplateType1')
        if not template_type:
            raise CMSException('No template type found for %s sport' % sport_name)
        self._logger.debug('*** Found template type "%s" for sport "%s"' % (template_type, sport_name))
        return template_type

    def get_leagues_info(self):
        path = 'league/brand/%s' % self.brand
        return self.request.get(path)

    def get_league_info(self, league_name, info_name):
        leagues_info = self.get_leagues_info()
        league = next((league for league in leagues_info if league['name'] == league_name), None)
        if not league:
            raise CMSException(
                'League "%s" not found among leagues %s' % (league_name, [league['name'] for league in leagues_info]))
        info = league.get(info_name, '')
        if not info:
            raise CMSException(
                'League info "%s" not found among info keys %s' % (info_name, [key for key in league.keys()]))
        return info

    def get_sport_categories(self) -> list:
        """
        Returns a list of sport categories.
        :return:
        """
        path = f'sport-category/brand/{self.brand}'
        return self.request.get(path)

    def get_show_in_sports_ribbon(self) -> list:
        """
        Returns a list of sport categories.
        :return:
        """
        path = f'sport-category/brand/{self.brand}/segment/Universal'
        return self.request.get(path)

    def get_virtual_next_events_config(self) -> dict:
        """
        Getting Virtual next events configuration
        :return: dict with virtual next event config
        """
        path = f'virtual-next-event/brand/{self.brand}'
        response = self.request.get(get_cms_settings().config.api_url + path)
        return response

    def get_virtual_next_event_module(self, _id):
        """
         Getting Virtual next event module configuration
        :return: dict with virtual next event config
        """
        path = f'virtual-next-event/{_id}'
        response = self.request.get(get_cms_settings().config.api_url + path)
        return response

    def update_virtual_next_events_sport_config(self,sport_module_id,**kwargs):
        """
        Method used to update next events module fields in CMS
        :param Kwargs: ID for next events module
        :param kwargs: data parameter if needed to be modified
                    :return: Updated object with all information about just updated next events module (id, title, etc)
        """
        response = self.get_sport_module_details(_id=sport_module_id)
        path = f'virtual-next-event/{sport_module_id}'
        for key in response.keys():
            if key in kwargs:
                response[key] = kwargs[key]
        data = json.dumps(lottery_response)
        request = self.request.put(path, data=data)
        return request

    def get_carousel_sports(self) -> dict:
        """
        returns a dict of sport categories names that appears in carousel with status value
        :return:
        """
        return dict(
            (category['imageTitle'], not category['disabled']) \
            for category in self.get_sport_categories() \
            if category['showInHome'] == False
        )

    #  Connect Menu

    def get_connect_menu_items(self) -> list:
        """
        Method to get Connect menu items list
        :return: list of Connect menu items
        """
        path = 'connect-menu/brand/%s' % self.brand
        connect_menu = [{k.strip(): v for k, v in elem.items()} for elem in self.request.get(path)]
        return connect_menu

    #  Static Blocks

    def get_static_block(self, uri):
        all_static_blocks = self.request.get(f'static-block/brand/{self.brand}')
        for block in all_static_blocks:
            if block['uri'] == uri:
                return block
        raise CMSException(f'Cannot find static block by "{uri}" uri field.')

    def is_static_block_enabled(self, uri):
        return self.get_static_block(uri=uri)['enabled']

    def enable_static_block(self, uri, enable=True):
        block = self.get_static_block(uri=uri)
        path = f'static-block/{block["id"]}'
        block['enabled'] = enable
        self.request.put(path, data=json.dumps(block))

    def get_world_cup_big_competition(self, world_cup_id):
        path = 'competition/%s' % world_cup_id
        return self.request.get(path)

    # Countries

    def get_countries_settings(self):
        path = '%s/countries-settings' % self.brand
        return self.request.get(urljoin(get_cms_settings().config.public_api_url, path))

    # Surface Bets

    def get_all_surface_bets(self, ):
        path = f'surface-bet/brand/{self.brand}'
        return self.request.get(path)

    def get_surface_bet(self, surface_bet_id: str) -> dict:
        """
        Method used to get Surface Bet info from CMS
        :param surface_bet_id: ID for Surface bet
        :return: object with all information about just created Surface Bet (id, title, etc)
        """
        path = f'surface-bet/{surface_bet_id}'
        return self.request.get(path)

    def get_surface_bets_for_page(self, reference_id: (str, int), related_to: str = 'sport', segment='Universal') -> list:
        """
        Searches SurfaceBet by brand for the given page
        :param related_to: type of the related entity (e.g. 'sport', 'eventhub', 'edp')
        :param reference_id: related entity ID (e.g. sport category id, edp id)
        :return: List of available Surface Bets sorted by sortOrder field in Asc order
        """
        allowed_related_to_types = ('sport', 'eventhub', 'edp')
        if related_to not in allowed_related_to_types:
            raise CMSException(f'Related entity "{related_to}" is not is allowed list: {allowed_related_to_types}')

        path = f'surface-bet/brand/{self.brand}/segment/{segment}/{related_to}/{reference_id}'
        return self.request.get(path)

    def _get_unique_references_for_sb(self, references):
        # Initialize an empty list to store unique references
        unique_references = []

        # Initialize a set to keep track of seen reference tuples
        seen_references = set()

        # Iterate through the input references list
        for reference in references:
            # Extract the "relatedTo" and "refId" values from the dictionary
            related_to = reference.get("relatedTo")
            ref_id = reference.get("refId")

            # Create a tuple of ("relatedTo", "refId") for easy comparison
            reference_tuple = ("relatedTo", str(related_to)), ("refId", str(ref_id))

            # If the reference tuple is not in the set of seen references, add it to the unique_references list
            if reference_tuple not in seen_references:
                seen_references.add(reference_tuple)
                unique_references.append(reference)

        return unique_references

    def add_surface_bet(self, selection_id: (str, int), related_to: str = 'sport',
                        related_to_event_hub: str = 'eventhub', event_hub_id: int = None, **kwargs) -> dict:
        """
        Creates a new Surface bet entry.

        :param selection_id: (str, int)
            The selection ID for the Surface bet.
        :param related_to: str, default='sport'
            Specifies the page where the Surface bet module is configured (e.g., 'sport', 'eventhub').
        :param related_to_event_hub: str, default='eventhub'
            Specifies the EventHub page where the Surface bet module is configured.
        :param priceNum: int, optional
            Numerator part of the price. Random value between 1 and 50 if not provided.
        :param priceDen: int, optional
            Denominator part of the price. Random value between 51 and 99 if not provided.
        :param on_homepage: bool, optional
            If the bet is on the homepage.
        :param all_sports: bool, optional
            If the bet is related to all sports.
        :param categoryIDs: list, optional
            List of category IDs.
        :param eventIDs: list, optional
            List of event IDs.
        :param event_hub_id: int, optional
            single event hub index.
        :param eventHubsIndexs: list, optional
            List of event hub indices.
        :param pageId: str, optional
            ID of the page.
        :param pageType: str, default='sport'
            Type of the page.
        :param content: str, optional
            Content of the surface bet.
        :param contentHeader: str, optional
            Header content for the surface bet.
        :param title: str, optional
            Title of the surface bet.
        :param svg_icon: str, optional
            ID for the SVG icon.
        :param svg_bg_id: str, optional
            Background ID for the SVG.
        :param svg_bg_image: str, optional
            Background image path for the SVG.
        :param highlightsTabOn: bool, optional
            If highlights tab is enabled.
        :param edp_on: bool, optional
            If EDP is enabled.
        :param displayOnDesktop: bool, optional
            If the bet should be displayed on desktop.
        :param message: str, optional
            Message for the surface bet.
        :param sportId: int, optional
            Sport ID for the surface bet.
        :param inclusionList: list, optional
            List of inclusions.
        :param universalSegment: bool, default=True
            If the segment is universal.
        :param exclusionList: list, optional
            List of exclusions.
        :param segmentReferences: list, optional
            References for the segments.
        :param fanzoneInclusions: list, optional
            List of fanzone inclusions.

        :return: dict
            Object containing information about the created Surface Bet, including its ID, title, and other details.

        Note:
        - In case the Surface bet is configured only for the EventHub page, set arguments as:
          related_to='eventhub', category_id=2, where category_id is the EventHub index number.
        - In case the Surface bet is configured for both EventHub and Sport pages, set arguments as:
          related_to='sport', category_id=[0, 16, 34], related_to_event_hub='eventhub', event_hub_id=2.
        """
        now = datetime.utcnow()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        displayFrom = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False, hours=-3,
                                              minutes=-1)[:-3] + 'Z'
        displayTo = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False, hours=-3,
                                            days=1)[:-3] + 'Z'

        def ensure_list(key):
            value = kwargs.get(key)
            return [value] if value and not isinstance(value, list) else value

        categoryIDs: list = ensure_list('categoryIDs') if kwargs.get('categoryIDs') is not None else []
        eventIDs: list = ensure_list('eventIDs') if kwargs.get('eventIDs') is not None else []

        price_num = int(kwargs.get('priceNum', fake.random_int(min=1, max=50)))
        price_den = int(kwargs.get('priceDen', fake.random_int(min=51, max=99)))

        event_Hubs_Indexes: list = kwargs.get('eventHubsIndexes', [])
        if event_hub_id is not None and event_hub_id not in event_Hubs_Indexes:
            event_Hubs_Indexes.append(event_hub_id)

        references = []

        if kwargs.get('on_homepage', True):
            kwargs['highlightsTabOn'] = True
            if 0 not in categoryIDs:
                categoryIDs.append(0)
        else:
            categoryIDs = [categoryID for categoryID in categoryIDs if categoryID != 0]

        if kwargs.get('all_sports'):
            references.append({'refId': "9999", 'relatedTo': 'sport', 'enabled': True})

        references.extend([{'refId': categoryID, 'relatedTo': related_to, 'enabled': True} for categoryID in categoryIDs])
        references.extend([{'refId': event_hub, 'relatedTo': related_to_event_hub, 'enabled': True} for event_hub in
                           event_Hubs_Indexes])
        references.extend([{'enabled': True, 'refId': event_id, 'relatedTo': 'edp'} for event_id in eventIDs])
        references = self._get_unique_references_for_sb(references=references)
        data = {
            'pageId': kwargs.get('pageId'),
            'pageType': kwargs.get('pageType', 'sport'),
            'content': kwargs.get('content', fake.paragraph()),
            'contentHeader': kwargs.get('contentHeader', 'Surface Bet Header'),
            'disabled': False,
            'title': kwargs.get('title', f'Auto {fake.name_female()}'),
            'displayFrom': displayFrom,
            'displayTo': displayTo,
            'selectionId': selection_id,
            'categoryIDs': categoryIDs,
            'sortOrder': None,
            'svgId': kwargs.get('svg_icon'),
            'svgBgId': kwargs.get('svg_bg_id'),
            'svgBgImgPath': kwargs.get('svg_bg_image'),
            'price': {'priceDen': price_den, 'priceNum': price_num},
            'references': references,
            'highlightsTabOn': kwargs.get('highlightsTabOn', False),
            'edpOn': kwargs.get('edp_on', False),
            'displayOnDesktop': kwargs.get('displayOnDesktop', False),
            'brand': self.brand,
            'message': kwargs.get('message'),
            'sportId': kwargs.get('sportId'),
            'inclusionList': kwargs.get('inclusionList', []),
            'universalSegment': kwargs.get('universalSegment', True),
            'exclusionList': kwargs.get('exclusionList', []),
            'segmentReferences': kwargs.get('segmentReferences', []),
            'fanzoneInclusions': kwargs.get('fanzoneInclusions', [])
        }

        response = self.request.post('surface-bet', data=json.dumps(data))
        self._created_surface_bets.append(response.get('id'))

        return response

    def update_surface_bet(self, surface_bet_id: str, **kwargs) -> dict:
        """
        Updates the fields of a Surface bet in the CMS.

        :param surface_bet_id: str
            The ID of the Surface bet to be updated.
        :param priceNum: int, optional
            Numerator part of the price.
        :param priceDen: int, optional
            Denominator part of the price.
        :param disabled: bool, optional
            If the bet is disabled.
        :param title: str, optional
            Title of the surface bet.
        :param content: str, optional
            Content of the surface bet.
        :param contentHeader: str, optional
            Header content for the surface bet.
        :param displayFrom: str, optional
            Datetime from when to start displaying.
        :param displayTo: str, optional
            Datetime until when to display.
        :param exclusionList: list, optional
            List of exclusions.
        :param inclusionList: list, optional
            List of inclusions.
        :param fanzoneInclusions: list, optional
            List of fanzone inclusions.
        :param universalSegment: bool, optional
            If the segment is universal.
        :param svg: str, optional
            SVG data for the bet.
        :param svgId: str, optional
            ID for the SVG icon.
        :param edpOn: bool, optional
            If EDP is enabled.
        :param highlightsTabOn: bool, optional
            If highlights tab is enabled.
        :param displayOnDesktop: bool, optional
            If the bet should be displayed on desktop.
        :param on_homepage: bool, optional
            If the bet is on the homepage.
        :param all_sports: bool, optional
            If the bet is related to all sports.
        :param categoryIDs: list, optional
            List of category IDs.
        :param eventHubsIndexs: list, optional
            List of event hub indices.
        :param eventIDs: list, optional
            List of event IDs.

        :return: dict
            Updated object with all information about the updated Surface Bet (id, title, etc).
        """
        surface_bet = self.get_surface_bet(surface_bet_id=surface_bet_id)

        fields_to_update = [
            'priceNum', 'priceDen', 'disabled', 'title', 'content', 'contentHeader',
            'displayFrom', 'displayTo', 'exclusionList', 'inclusionList', 'fanzoneInclusions',
            'universalSegment', 'svg', 'svgId', 'edpOn', 'highlightsTabOn', 'displayOnDesktop',
            'segmentReferences'
        ]

        for field in fields_to_update:
            if field in ['priceNum', 'priceDen']:
                surface_bet['price'][field] = kwargs.pop(field, surface_bet['price'][field])
            else:
                surface_bet[field] = kwargs.pop(field, surface_bet[field])

        references = []

        def get_references(key, related_to):
            return [{'refId': item, 'relatedTo': related_to, 'enabled': True} for item in kwargs.pop(key, [])]

        references += get_references('categoryIDs', 'sport') or \
                        [ref for ref in surface_bet['references'] if ref['relatedTo'] == "sport"]
        references += get_references('eventHubsIndexes', 'eventhub') or \
                        [ref for ref in surface_bet['references'] if ref['relatedTo'] == "eventhub"]
        references += get_references('eventIDs', 'edp') or \
                        [ref for ref in surface_bet['references'] if ref['relatedTo'] == "edp"]

        target_object = {'refId': "0", 'relatedTo': 'sport', 'enabled': True}
        if kwargs.get('on_homepage', surface_bet['highlightsTabOn']):
            surface_bet['highlightsTabOn'] = True
            exists = any([True for ref in surface_bet['references'] if ref['relatedTo'] == "sport" and ref['refId'] == "0"])
            if not exists:
                references.append(target_object)
        else:
            surface_bet['highlightsTabOn'] = False
            exists = any([True for ref in surface_bet['references'] if ref['relatedTo'] == "sport" and ref['refId'] == "0"])
            if exists:
                references = [ref for ref in references if ref['relatedTo'] != "sport" and ref['refId'] != "0"]

        if kwargs.get('all_sports'):
            exists = any(
                [True for ref in surface_bet['references'] if ref['relatedTo'] == "sport" and ref['refId'] == "9999"])
            if not exists:
                references.append({'refId': "9999", 'relatedTo': 'sport', 'enabled': True})

        references = self._get_unique_references_for_sb(references=references)
        surface_bet['references'] = references
        path = f'surface-bet/{surface_bet_id}'
        return self.request.put(path, data=json.dumps(surface_bet))

    def delete_surface_bet(self, surface_bet_id) -> None:
        """
        Removes Surface bet
        :param surface_bet_id: specifies id of surface bet which should be removed
        """
        path = f'surface-bet/{surface_bet_id}'
        self.request.delete(path, parse_response=False)

    # Highlights Carousel

    def get_all_highlights_carousels(self, segment='Universal', page_id: int = 0) -> dict:
        """
        Gets all highlights carousels.
        :return: whole highlight carousel object
        """
        return self.request.get(f'highlight-carousel/brand/{self.brand}/segment/{segment}/sport/{page_id}')

    def create_highlights_carousel(self, title: str, events: list = [], typeId: str = None, sport_id: int = 0,
                                   page_type: str = 'sport', svgId="", **kwargs) -> dict:
        """
        Create Highlights Carousel
        :param title: str, specifies highlight carousel title
        :param events: specifies list of events ids which would be attached to the carousel, could be a list of 1 element
        :param typeId: specifies type id for events which would be attached to the carousel
        :param sport_id: specifies sport id of events which would be attached to the carousel
        :param page_type: str, page type where module is configured. E.g.: 'sport', 'eventhub'
        :return: dict, object with all information about just created highlight carousel (id, title, etc)
        Note: either events or typeId must have not None value
        """
        if not events and not typeId:
            raise CMSException('Please provide either Event IDs or Type ID')
        now = datetime.now()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        date_from = kwargs.get('date_from', get_date_time_as_string(date_time_obj=now, time_format=time_format,
                                                                    url_encode=False, hours=-10)[:-3] + 'Z')
        date_to = kwargs.get('date_to', get_date_time_as_string(date_time_obj=now, time_format=time_format,
                                                                url_encode=False, days=1, hours=-10)[:-3] + 'Z')
        limit = kwargs.get('limit', 10)
        inplay = kwargs.get('inplay', False)
        path = 'highlight-carousel'
        payload = {
            'id': None,
            'displayFrom': date_from,
            'displayTo': date_to,
            'title': title,
            'disabled': False,
            'brand': self.brand,
            'sortOrder': kwargs.get('sortOrder', None),
            'svg': '',
            'svgId': svgId,
            'displayMarketType': kwargs.get('displayMarketType', 'PrimaryMarket'),
            'svgFilename': None,
            'inPlay': inplay,
            'typeId': typeId,
            'sportId': sport_id,
            'pageId': sport_id,
            'pageType': page_type,
            'limit': limit,
            'events': events,
            'typeIds': kwargs.get('typeIds', []),
            'displayOnDesktop': kwargs.get('displayOnDesktop', False),
            'inclusionList': kwargs.get('inclusionList', []),
            'fanzoneInclusions': kwargs.get('fanzoneInclusions', []),
            'universalSegment': kwargs.get('universalSegment', True),
            'exclusionList': kwargs.get('exclusionList', [])
        }
        data = json.dumps(payload)
        response = self.request.post(path, data=data)
        self._created_highlights_carousels.append(response.get('id'))
        return response

    def delete_highlights_carousel(self, highlight_carousel_id: str) -> None:
        """
        Removes highlights carousel.
        :param highlight_carousel_id: specifies id of highlights carousel which should be removed
        """
        path = f'highlight-carousel/{highlight_carousel_id}'
        self.request.delete(path, parse_response=False)

    def change_highlights_carousel_state(self, highlight_carousel, active=True):
        """
        Makes highlights carousel active/inactive.
        :param highlight_carousel: highlights carousel object
        :param active: specifies if highlights carousel should be made inactive
        """
        path = f'highlight-carousel/{highlight_carousel["id"]}'
        highlight_carousel['disabled'] = not active
        self.request.put(path, data=json.dumps(highlight_carousel))

    def update_highlights_carousel(self, highlight_carousel, **kwargs):
        """
        Updates time range during which highlights carousel should be visible.
        :param highlight_carousel: highlights carousel object
        Note if start_time or end_time is None teh time won't be changed
        """
        path = f'highlight-carousel/{highlight_carousel["id"]}'
        if 'title' in kwargs:
            highlight_carousel['title'] = kwargs['title']
        if 'start_time' in kwargs:
            highlight_carousel['displayFrom'] = kwargs['start_time']
        if 'end_time' in kwargs:
            highlight_carousel['displayTo'] = kwargs['end_time']
        if 'limit' in kwargs:
            highlight_carousel['limit'] = kwargs['limit']
        if 'inPlay' in kwargs:
            highlight_carousel['inPlay'] = kwargs['inPlay']
        if 'svgId' in kwargs:
            highlight_carousel['svgId'] = kwargs['svgId']
        if 'disabled' in kwargs:
            highlight_carousel['disabled'] = kwargs['disabled']
        if 'displayOnDesktop' in kwargs:
            highlight_carousel['displayOnDesktop'] = kwargs['displayOnDesktop']
        if 'type_id' in kwargs:
            highlight_carousel['typeId'] = kwargs['type_id']
            highlight_carousel['events'] = None
        if 'displayMarketType' in kwargs:
            highlight_carousel['displayMarketType'] = kwargs['displayMarketType']
        else:
            if 'events' in kwargs:
                if not type(kwargs['events']) == list:
                    raise CMSException(f"{kwargs['events']} events should be a list")
                highlight_carousel['events'] = kwargs['events']
                highlight_carousel['typeId'] = None
        if 'universalSegment' in kwargs and kwargs['universalSegment'] == True:
            highlight_carousel['universalSegment'] = kwargs['universalSegment']
            highlight_carousel['inclusionList'] = []
        else:
            if 'inclusionList' in kwargs:
                if not type(kwargs['inclusionList']) == list:
                    raise CMSException(f"{kwargs['inclusionList']} inclusionList should be a list")
                highlight_carousel['inclusionList'] = kwargs['inclusionList']
                highlight_carousel['universalSegment'] = False
        self.request.put(path, data=json.dumps(highlight_carousel))

    def does_system_configuration_exist(self, device_type: str) -> bool:
        if self.get_initial_data(device_type=device_type).get('systemConfiguration') is None:
            return False
        return True

    def get_sport_module(self, sport_id: int = 0, module_type: str = 'INPLAY'):
        """
        :param sport_id: Category ID for sport from OpenBet int for example for football=16, tennis=34, homepage=0
        :param module_type: module type
        :return: list
        """
        path = f'sport-module/brand/{self.brand}/sport/{sport_id}'
        response = self.request.get(path)
        if module_type:
            filter_by_module_type = list(filter(lambda param: param['moduleType'] == module_type, response))
            return filter_by_module_type
        else:
            return response

    def get_sport_module_details(self, _id: int) -> list:
        """
        :param _id: int
        :return: list
        """
        path = f'sport-module/{_id}'
        response = self.request.get(path)
        return response

    def change_sport_module_state(self, sport_module, active=True):
        """
        Make sport module active/inactive
        :param sport_module: sport module object
        :param active: specifies if sport module should be made inactive
        """
        path = f'sport-module/{sport_module["id"]}'
        sport_module['disabled'] = not active
        self.request.put(path, data=json.dumps(sport_module))

    def delete_sport_module(self, _id: str):
        """
        Delete sport module
        :param _id: str, sport module id
        """
        path = f'sport-module/{_id}'
        self.request.delete(path, parse_response=False)

    # Recently Played games

    def update_recently_played_games(self, sport_category: int = 0, module_type: str = 'RECENTLY_PLAYED_GAMES', **kwargs):
        """
        :param sport_category: sport category id
        :param module_type: module type
        """
        recently_played_games_module = self.get_sport_module(sport_category, module_type)
        module_id = recently_played_games_module[0].get('id')
        path = f'sport-module/{module_id}'
        rpg_module_details = self.get_sport_module_details(_id=module_id)
        rpg_module_config = rpg_module_details['rpgConfig']
        fields_to_update = ['title', 'bundleUrl', 'loaderUrl', 'seeMoreLink', 'gamesAmount']
        for field in fields_to_update:
                rpg_module_config[field] = kwargs.pop(field, rpg_module_config[field])
        rpg_module_details['rpgConfig'] = rpg_module_config
        self.request.put(path, data=json.dumps(rpg_module_details))

    # In Play Module

    def get_max_number_of_inplay_event(self, sport_category: int = 0, module_type: str = 'INPLAY') -> str:
        """
        :param sport_category: sport category id
        :param module_type: module type
        :return: maximum number of displayed event on in play tab
        """
        inplay_module = self.get_sport_module(sport_category, module_type)
        module_id = inplay_module[0].get('id')
        return self.get_sport_module_details(_id=module_id)['inplayConfig']['maxEventCount']

    def update_inplay_event_count(self, event_count: int, sport_category: int = 0, module_type: str = 'INPLAY'):
        """
        :param event_count: max in play event count
        :param sport_category: sport category id
        :param module_type: module type
        """
        inplay_module = self.get_sport_module(sport_category, module_type)
        module_id = inplay_module[0].get('id')
        path = f'sport-module/{module_id}'
        parameters = self.get_sport_module_details(_id=module_id)
        parameters['inplayConfig']['maxEventCount'] = event_count
        self.request.put(path, data=json.dumps(parameters))

    def update_inplay_sport_event_count(self, sport_number: int, event_count: int):
        """
        This method set max event count value for specified sport number in in-play module
        :param sport_number: sport order number
        :param event_count: max in-play sport event count
        """
        inplay_module = self.get_sport_module()
        module_id = inplay_module[0].get('id')
        path = f'sport-module/{module_id}'
        parameters = self.get_sport_module_details(_id=module_id)
        parameters['inplayConfig']['homeInplaySports'][sport_number - 1]['eventCount'] = event_count
        self.request.put(path, data=json.dumps(parameters))

    def get_inplay_module_config(self):
        """
        This method gets "In-Play" module configuration
        :return: "inplayConfig" section
        """
        inplay_module = self.get_sport_module(module_type='INPLAY')
        module_id = inplay_module[0].get('id')
        parameters = self.get_sport_module_details(_id=module_id)
        return parameters['inplayConfig']

    def get_inplay_event_count(self):
        """
        This method gets "In-Play" module "maxEventCount"
        :return: "maxEventCount" value
        """
        parameters = self.get_inplay_module_config()
        return parameters['maxEventCount']

    def get_sport_event_count(self, sport_number: int):
        """
        This method gets "In-Play" module "eventCount" value for specified Sport number
        :param sport_number: numeric value starting from 0
        :return: "eventCount" value
        """
        if sport_number > 0:
            sport_number -= 1
        parameters = self.get_inplay_module_config()
        return parameters['homeInplaySports'][sport_number]['eventCount']

    # ACCA

    def get_acca_notification(self, offer_type: str, currency: str) -> str:
        """
        Method to get actual ACCA notification
        :param offer_type: expected offer type
        :param currency: expected currency
        :return: ACCA notification
        """
        if offer_type == 'Suggested':
            description_html = self.get_static_block(uri='acca-notification-1-en-us')['htmlMarkup']
            notification = document_fromstring(description_html).text_content().replace('\r', '').replace('\xa0', ' ')
        elif offer_type == 'Eligible':
            description_html = self.get_static_block(uri='acca-notification-3-en-us')['htmlMarkup']
            notification = document_fromstring(description_html).text_content().replace('\r', ' ')
        elif offer_type == 'SuggestedType2':
            description_html = self.get_static_block(uri='acca-notification-2-en-us')['htmlMarkup']
            notification = document_fromstring(description_html).text_content().replace('\r', '').replace('\xa0', ' ') \
                .encode('ascii', 'ignore').decode()
        else:
            raise CMSException(f'Such offer type "{offer_type}" is not valid for ACCA notifications')
        return notification.replace("[['currency']]", currency).replace("[['param1']]", '1'). \
            replace("[['param2']]", '25.00').replace('\n', ' ')

    def set_super_acca_toggle_component_status(self, super_acca_component_status: bool) -> dict:
        """
        Enable/disable superAcca option for Betslip in CMS configuration
        :param super_acca_component_status: True or False
        :return: Updated system configuration structure
        """
        self._logger.warning(f'"{__name__}" is deprecated; use "update_system_configuration_structure" method')
        path = f'structure/brand/{self.brand}'
        payload = {'lang': 'en', 'brand': self.brand, 'structure': ''}
        system_configuration = self.get_system_configuration_structure()
        betslip = self.get_system_configuration_structure().get('Betslip')
        if betslip is None or betslip.get('superAcca') is None:
            raise CMSException('Betslip not found in System Structure or superAcca not found in Betslip ')
        system_configuration['Betslip']['superAcca'] = super_acca_component_status
        payload['structure'] = system_configuration

        request = self.request.put(path, data=json.dumps(payload))
        self._cached_initial_data = {'mobile': None, 'desktop': None}  # so new data will be returned for the next request
        return request

    def set_my_acca_section_cms_status(self, ema_status: bool) -> dict:
        """
        Enable/disable EMA in CMS configuration
        :param ema_status: True or False
        :return: Updated system configuration structure
        """
        self._logger.warning(f'"{__name__}" is deprecated; use "update_system_configuration_structure" method')
        path = f'structure/brand/{self.brand}'
        payload = {'lang': 'en', 'brand': self.brand, 'structure': ''}
        system_configuration = self.get_system_configuration_structure()
        ema = system_configuration.get('EMA')
        if ema is None or ema.get('enabled') is None:
            raise CMSException('EMA or "enabled" field of EMA not found in System Structure')
        system_configuration['EMA']['enabled'] = ema_status
        payload['structure'] = system_configuration

        request = self.request.put(path, data=json.dumps(payload))
        self._cached_initial_data = {'mobile': None, 'desktop': None}  # so new data will be returned for the next request
        return request

    # Coupons

    def get_coupon_market_selector_markets(self) -> list:
        return self.request.get(url=get_cms_settings().config.public_api_url + f'{self.brand}/coupon-market-selector')

    def get_coupon_market_name_and_headers(self, market_template: str) -> namedtuple:
        """
        :param market_template: Name of market template, e.g. 'Match Betting'
        :return: Name of market on Coupon Details page, e.g. 'MATCH RESULT NEW'
        """
        market_name_and_headers = namedtuple('name_and_headers', ['market_name', 'headers'])
        cms_markets = self.get_coupon_market_selector_markets()
        market_in_cms = next(
            (cms_market for cms_market in cms_markets if cms_market['templateMarketName'] == market_template), None)
        if market_in_cms:
            market_name = market_in_cms['title']
            market_headers = market_in_cms['header'] if market_in_cms['header'] else None
            return market_name_and_headers(market_name=market_name, headers=market_headers)
        else:
            self._logger.info(f'"{market_template}" is not found in list of modified market names in CMS.')
            return market_name_and_headers(market_name=market_template, headers=None)

    # Next Races

    def next_races_price_switcher(self, show_priced_only: bool):
        """
        Method for changing status for showPricedOnly in CMS  (/system-configuration/structure)
        :param showPricedOnly: True or False
        :return: Updated showPricedOnly configuration for Next Races
        """
        self._logger.warning(f'"{__name__}" is deprecated; use "update_system_configuration_structure" method')
        path = f'structure/brand/{self.brand}'
        current_state = self.get_system_configuration_item('NextRaces').get('showPricedOnly')
        field_value = 'Yes' if show_priced_only else 'No'
        if field_value != current_state:
            payload = {'lang': 'en', 'brand': self.brand, 'structure': ''}
            system_configuration = self.get_system_configuration_structure()
            next_races = system_configuration.get('NextRaces')
            if next_races is None or next_races.get('showPricedOnly') is None:
                raise CMSException('NextRaces or "showPricedOnly" field of NextRaces not found in System Structure')
            system_configuration['NextRaces']['showPricedOnly'] = field_value
            payload['structure'] = system_configuration

            request = self.request.put(path, data=json.dumps(payload))
            self._cached_initial_data = {'mobile': None,
                                         'desktop': None}  # so new data will be returned for the next request
            return request

    def set_next_races_toggle_component_status(self, next_races_component_status: bool) -> dict:
        """
        Enable/disable nextRacesComponentEnabled option for NextRacesToggle in CMS configuration
        :param next_races_component_status: Next Races component: True or False
        :return: Updated system configuration structure
        """
        self._logger.warning(f'"{__name__}" is deprecated; use "update_system_configuration_structure" method')
        path = f'structure/brand/{self.brand}'
        payload = {'lang': 'en', 'brand': self.brand, 'structure': ''}
        system_configuration = self.get_system_configuration_structure()
        next_race_toggle = system_configuration.get('NextRacesToggle')
        if next_race_toggle is None or next_race_toggle.get('nextRacesComponentEnabled') is None:
            raise CMSException('NextRacesToggle or "nextRacesComponentEnabled" field of NextRacesToggle not found'
                               ' in System Structure')
        system_configuration['NextRacesToggle']['nextRacesComponentEnabled'] = next_races_component_status
        payload['structure'] = system_configuration

        request = self.request.put(path, data=json.dumps(payload))
        self._cached_initial_data = {'mobile': None, 'desktop': None}  # so new data will be returned for the next request
        return request

    def set_next_races_numbers_of_event(self, number_of_event: str) -> dict:
        """
        Change numberOfEvents option for NextRaces in CMS configuration
        :param number_of_event: number of event that should be displayed on next races
        :return: Updated system configuration structure
        """
        self._logger.warning(f'"{__name__}" is deprecated; use "update_system_configuration_structure" method')
        path = f'structure/brand/{self.brand}'
        payload = {'lang': 'en', 'brand': self.brand, 'structure': ''}
        system_configuration = self.get_system_configuration_structure()
        next_races = system_configuration.get('NextRaces')
        if next_races is None or next_races.get('numberOfEvents') is None:
            raise CMSException('NextRaces or "numberOfEvents" not found in System Structure')
        system_configuration['NextRaces']['numberOfEvents'] = number_of_event
        payload['structure'] = system_configuration

        request = self.request.put(path, data=json.dumps(payload))
        self._cached_initial_data = {'mobile': None, 'desktop': None}  # so new data will be returned for the next request
        return request

    # RGY Bonus Suppression

    def get_active_feature_modules_alias_names(self):
        """
        getting all active alias quick link names and alias super button name
        """
        endpoint = f'alias-module-names/brand/{self.brand}'
        return self.request.get(endpoint)

    def get_all_rgy_modules(self):
        """
        Retrieve a list of RGY modules.

        Returns:
            list: A list of RGY modules.
        """
        endpoint = f'rgyModule/brand/{self.brand}'
        return self.request.get(endpoint)

    def get_rgy_module_with_alias(self, module_name:str):
        """
        Retrieve an RGY module by its name or alias.

        This method searches for an RGY module with the specified module name or alias name.

        Args:
            module_name (str): The module name or alias to search for.

        Returns:
            dict: The RGY module from CMS with the specified name or alias, or None if not found.
        """
        all_rgy_module = self.get_all_rgy_modules()

        for rgy_module in all_rgy_module:
            alias_module_names = [name.strip() for name in rgy_module.get('aliasModuleNames').split(',')]
            if rgy_module.get('moduleName') == module_name or module_name in alias_module_names:
                return rgy_module
        else:
            self._logger.info(f'Given rgy module with alias: {module_name} not available')
            return None

    def add_rgy_module(self, module_name: str, alias_module_names:str = '', sub_module_enabled: bool = False, sub_module_ids: list = [],**kwargs):
        """
        Add an RGY module with the specified module name and optional settings.

        Args:
            module_name (str): The name of the RGY module to add.
            alias_module_names (str): All the alias names of the RGY module to add, seperated with a comma(,).
            sub_module_enabled (bool, optional): Indicates whether sub-modules are enabled (default is False).
            sub_module_ids (list, optional): List of sub-module IDs (required if sub_module_enabled is True).

        Returns:
            dict: The created data from the API after adding the RGY module.
        """
        if sub_module_enabled and not sub_module_ids:
            raise CMSException(f'if sub module is enabled "sub_module_enabled"= {sub_module_enabled} '
                               f'then it is mandatatory to send sub-module ids "sub_module_ids"= {sub_module_ids}')

        path = 'rgyModule'
        params = {
            "aliasModuleNames": "",
            "aliasModules" :kwargs.get('aliasModules',[]),
            "brand": self.brand,
            "id": "",
            "moduleName": module_name,
            "subModuleEnabled": sub_module_enabled,
            "subModules": [],
            "subModuleIds": sub_module_ids
        }

        data = json.dumps(params)
        created_module = self.request.post(path, data=data)
        self._created_rgy_modules.append(created_module['id'])
        return created_module

    def delete_rgy_module(self, rgy_module_id):
        """
        Delete an RGY module by its ID.

        This method sends a request to remove an RGY module with the specified ID.

        Args:
            rgy_module_id (str): The ID of the RGY module to be deleted.

        Returns:
            None: No return value. The method either succeeds in deleting the module, or raises an exception if the module doesn't exist.
        """
        path = f'rgyModule/{self.brand}/{rgy_module_id}'
        return self.request.delete(path, parse_response=False)

    def get_all_rgy_bonus_suppression_module(self):
        """
        Retrieve a list of RGY Bonus Suppression modules.

        This method makes an API request to fetch a list of RGY associated with the Bonus Suppression modules configuration.

        Returns:
            list: A list of RGY Bonus Suppression modules.
        """
        path = f'rgyConfig/brand/{self.brand}'
        return self.request.get(path)

    def get_rgy_bonus_suppression_module(self, risk_level:str, reason_code:str):
        """
        Retrieve an RGY Bonus Suppression module by risk level and reason code.

        This method searches for an RGY Bonus Suppression module with the specified risk level and reason code.

        Args:
            risk_level (str): The risk level description of the module to retrieve.
            reason_code (str): The reason code description of the module to retrieve.

        Returns:
            dict: The RGY Bonus Suppression module with the specified risk level and reason code, or None if not found.
        """
        all_rgy_bonus_suppression_module = self.get_all_rgy_bonus_suppression_module()
        for rgy_bonus_suppression_module in all_rgy_bonus_suppression_module:
            if (
                    rgy_bonus_suppression_module.get('riskLevelDesc') == risk_level
                    and rgy_bonus_suppression_module.get('reasonDesc') == reason_code
            ):
                return rgy_bonus_suppression_module
        else:
            self._logger.info(f'RGY bonus suppression module with given risk level: {risk_level} and reason code: {reason_code} does not exist')
            return None

    def add_rgy_bonus_suppression_module(self, risk_level:str, reason_code:str, bonus_suppression_enabled=False, rgy_module_ids=[]):
        """
        Add an RGY Bonus Suppression module with specified settings.

        Args:
            risk_level (str): The pre-defined description of the risk level for the module.
            reason_code (str): The pre-defined description of the reason code for the module.
            bonus_suppression_enabled (bool, optional): Indicates whether bonus suppression is enabled (default is False).
            rgy_module_ids (list, optional): List of RGY module IDs (required if bonus_suppression_enabled is True).

        Returns:
            dict: The data of created RGY bonus suppression module from the API after adding that RGY Bonus Suppression module.
        """
        if bonus_suppression_enabled and not rgy_module_ids:
            raise CMSException(
                f'if bonus suppression is enabled "bonus_suppression_enabled"={bonus_suppression_enabled} '
                f'then it is mandatatory to send bonus suppression module ids "rgy_module_ids"= {rgy_module_ids}')

        path = 'rgyConfig'
        params = {
                    "brand": self.brand,
                    "id": "",
                    "moduleName": "",
                    "bonusSuppression": False,
                    "riskLevelCode": self._extract_starting_numbers(risk_level),
                    "reasonCode": self._extract_starting_numbers(reason_code),
                    "modules": [],
                    "enabled": bonus_suppression_enabled,
                    "riskLevelDesc": risk_level,
                    "reasonDesc": reason_code,
                    "moduleIds": rgy_module_ids
                }

        data = json.dumps(params)
        created_module =  self.request.post(path, data=data)
        self._created_rgy_bonus_suppression_modules.append(created_module['id'])
        return created_module

    def _extract_starting_numbers(self, input_string):
        """
        Extract and return the starting numbers from the input string.

        Args:
            input_string (str): The input string from which starting numbers are to be extracted.

        Returns:
            str: A string containing the extracted starting numbers from the input string.
        """
        # Use a regular expression to find the starting numbers in the input string
        match = re.match(r'^\d+', input_string)
        return str(match.group())

    def update_rgy_bonus_suppression_module(self, risk_level:str, reason_code:str, new_risk_level: str = '',
                                            new_reason_code: str = '', bonus_suppression_enabled: bool = False,
                                            rgy_module_ids: list = []):
        """
          Update the RGY Bonus Suppression module with new settings.

          This method updates the settings of an existing RGY Bonus Suppression module specified by its risk level and reason code.

          Args:
              risk_level (str): The pre-defined description of the risk level for the module.
              reason_code (str): The pre-defined description of the reason code for the module.
              new_risk_level (str, optional): The new risk level description (default is an empty string).
              new_reason_code (str, optional): The new reason code description (default is an empty string).
              bonus_suppression_enabled (bool, optional): Indicates whether bonus suppression is enabled (default is False).
              rgy_module_ids (list, optional): List of RGY module IDs to associate with the module (default is an empty list).

          Returns:
              dict: The response from the API after updating the RGY Bonus Suppression module.
          """
        # Get the current bonus suppression module
        response = self.get_rgy_bonus_suppression_module(risk_level=risk_level, reason_code=reason_code)
        path = f"rgyConfig/{response['id']}"

        # Update fields with new values if provided, else keep the current values
        response['riskLevelDesc'] = new_risk_level if new_risk_level else response['riskLevelDesc']
        response['riskLevelCode'] = self._extract_starting_numbers(new_risk_level) if new_risk_level else response['riskLevelCode']

        response['reasonDesc'] = new_reason_code if new_reason_code else response['reasonDesc']
        response['reasonCode'] = self._extract_starting_numbers(new_reason_code) if new_reason_code else response['reasonCode']

        response['enabled'] = bonus_suppression_enabled if bonus_suppression_enabled else response['enabled']

        # note that we do not have 'moduleIds' key in the response variable
        # Create a list of module IDs to add the 'moduleIds' field
        module_list = [module['id'] for module in response['modules']]
        if rgy_module_ids:
            module_list.extend(rgy_module_ids)
        response['moduleIds'] = module_list

        data = json.dumps(response)
        return self.request.put(path, data=data)

    def delete_rgy_bonus_suppression_module(self, rgy_bonus_suppression_module_id):
        """
        Delete an RGY bonus suppression module by its ID.

        This method sends a request to remove an RGY bonus suppression module with the specified ID.

        Args:
            rgy_bonus_suppression_module_id (str): The ID of the RGY bonus suppression module to be deleted.

        Returns:
            None: No return value. The method either succeeds in deleting the module, or raises an exception if the module doesn't exist.
        """
        path = f'rgyConfig/{self.brand}/{rgy_bonus_suppression_module_id}'
        return self.request.delete(path, parse_response=False)

    # Ladbrokes

    # One Two Free

    def get_one_two_free_static_texts(self) -> list:
        """
        Get 1-2-Free settings
        :return: list of dicts with settings
        """
        path = get_cms_settings().config.public_api_url + f'{self.brand}/one-two-free/static-texts'
        return self.request.get(path)

    def get_one_two_free_games_tab_details(self) -> list:
        """
        Get 1-2-Free settings
        :return: List of event from Cms games tab
        """
        path = get_cms_settings().config.public_api_url + f'{self.brand}/one-two-free/games'
        return self.request.get(path)

    def get_one_two_free_games(self):
        """
        Get all configured 1-2-free games
        :return: list of dicts with games settings
        """
        path = get_cms_settings().config.api_url + f'game/brand/{self.brand}'
        return self.request.get(path)

    def get_one_two_free_my_badges(self):
        """
        Get 1-2-Free My Badges data
        :return: a dict with My Badges data
        """
        path = f'badge/brand/{self.brand}'
        return self.request.get(path)

    def update_one_two_free_my_badges(self, **kwargs):
        """
        Update the data of My Badges pages associated with the Ladbrokes brand.

        :return: A response object containing the updated My Badges pages data.

        This method sends a request to the API endpoint to update and obtain data for My Badges pages.
        The response object includes the retrieved data.

        Fields that can be updated, along with their corresponding response keys and frontend CMS names, are as follows:
            - 'label' ('My Badges Label')
            - 'rulesDisplay' ('Rules Display')
            - 'lastUpdatedFlag' ('Display Last Updated Date & Time')
            - 'viewButtonLabel' ('View Button Text')
            - 'viewButton' ('Display View Button')
            - 'lbrRedirectionUrl' ('View Leaderboard Redirection URL')
            - 'lbrRedirectionLabel' ('View Leaderboard Redirection CTA')
            - 'viewLbrUrl' ('Euro Cup Preparation')
            - 'viewBadges' ('Display Badges')
        """
        response = self.get_one_two_free_my_badges()

        path = f'badge/{response["id"]}'
        for field in kwargs:
            if field in response:
                response[field] = kwargs.get(field, response[field])
            else:
                raise CMSException(f'sent field "{field}" is not available in My Badges response from CMS,'
                                   f' please refer the docstring of this method.')
        data = json.dumps(response)
        return self.request.put(path, data=data)

    def get_one_two_free_tab_name_configuration(self):
        """
        Get 1-2-Free Tab name configuration data
        :return: a dict with Tab name configuration data
        """
        path = f'otf-tab-config/brand/{self.brand}'
        return self.request.get(path)

    def update_one_two_free_tab_name_configuration(self, tab_id, **kwargs):
        """
        Update 1-2-Free Tab name configuration data
        :return: a dict with Tab name configuration data
        """
        path = f'otf-tab-config/{tab_id}'
        payload = {
            "brand": self.brand,
            "currentTabLabel": kwargs.get('currentTabLabel', "CURRENT"),
            "id": tab_id,
            "previousTabLabel": kwargs.get('previousTabLabel', "PREVIOUS")
        }
        data = json.dumps(payload)

        return self.request.put(path, data=data)

    # Question Engine

    def get_question_engine(self) -> list:
        """
        Method to get 'question-engine' for brand
        :return: list
        """
        path = f'question-engine/brand/{self.brand}'
        response = self.request.get(path)
        return response
    # big competations

    def get_big_competition(self):
        """
        Method to get 'question-engine' for brand.
        :return: Response from the API containing a list of competitions for the specified brand.
        """
        path = f'competition/brand/{self.brand}'
        response = self.request.get(path)
        return response

    def create_big_competition(self, competition_name, **kwargs):
        """
          Method to create a 'big competition' for the brand.
          :param competition_name: The name of the competition.
          :param kwargs: Additional keyword arguments.
              - background: Background information for the competition.
              - enabled: Whether the competition is enabled (default is True).
              - svg: SVG information for the competition.
              - svgBgId: SVG background ID.
              - svgFilename: Filename for the SVG.
              - title: Title for the competition (default is generated using fake data).
              - type_Id: Type ID for the competition.
          :return: Response from the API containing information about the newly created competition.
        """
        path = 'competition'
        payload = {
            'id': None,
            'background': kwargs.get('background', None),
            'brand': self.brand,
            'competitionParticipants': [],
            'competitionTabs': [],
            'enabled': kwargs.get('enabled', True),
            'name': competition_name,
            'svg': kwargs.get('svg', None),
            'svgBgId': kwargs.get('svgBgId', None),
            'svgFilename': kwargs.get('svgFilename', None),
            'title': kwargs.get('title', f'Auto+{fake.city()}'),
            'typeId': kwargs.get('type_Id'),
            'uri': '/' + competition_name.replace(' ', '-').lower()
        }
        response = self.request.post(
            url=path,
            data=json.dumps(payload)
        )
        self._created_big_competitions.append(response.get('id'))
        return response

    def delete_big_competition(self, big_competition_id):
        """
        Method to delete a 'big competition' based on its ID.
        :param big_competition_id: The ID of the big competition to be deleted.
        :return: None
        """
        path = f'competition/{big_competition_id}'
        return self.request.delete(path, parse_response=False)

    def create_tab_for_big_competition(self, tab_name, competition_id, **kwargs):
        """
           Method to create a tab for a 'big competition'.

           :param tab_name: The name of the tab to be created.
           :param competition_id: The ID of the competition for which the tab is being created.
           :param kwargs: Additional keyword arguments.
               - displayOrder: Display order for the tab (default is 0).
               - enabled: Whether the tab is enabled (default is True).
               - hasSubtabs: Whether the tab has subtabs (default is False).

           :return: Response from the API containing information about the newly created tab.
        """
        path = f'competition/{competition_id}/tab'
        payload = {
            'id': None,
            'brand': self.brand,
            'competitionModules': [],
            'competitionSubTabs': [],
            'displayOrder': kwargs.get('displayOrder', 0),
            'enabled': kwargs.get('enabled', True),
            'hasSubtabs': kwargs.get('hasSubtabs', False),
            'name': tab_name,
            'uri': '/' + tab_name.lower()
        }
        response = self.request.post(url=path, data=json.dumps(payload))
        return response

    def get_module_for_big_competition(self, competition_id, tab_id, module_id, **kwargs):
        """
           Method to get a module for a specific tab within a 'big competition'.

           :param competition_id: The ID of the competition containing the module.
           :param tab_id: The ID of the tab containing the module.
           :param module_id: The ID of the module to retrieve.
           :param kwargs: Additional keyword arguments (optional).

           :return: Response from the API containing information about the requested module.
        """
        path = f'competition/{competition_id}/tab/{tab_id}/module/{module_id}'
        response = self.request.get(url=path)
        return response

    def create_module_for_big_competation(self, competition_id, tab_id, module_name: str = None,
                                          module_type: str = None, **kwargs):
        """
        - 'AEM': AEM module.
            - 'NEXT_EVENTS': Next events module.
            - 'PROMOTIONS': Promotions module.
            - 'SURFACEBET': Surface bet module.
            - 'HIGHLIGHTS_CAROUSEL': Highlights carousel module.
           Method to create a module for a specific tab within a 'big competition'.

           :param competition_id: The ID of the competition in which the module will be created.
           :param tab_id: The ID of the tab in which the module will be created.
           :param module_name: The name of the module to be created (optional).
           :param module_type: The type of the module to be created (optional).
           :param kwargs: Additional keyword arguments.
               - categoryids: List of category IDs.
               - displayOrder: Display order for the module (default is 0).
               - enabled: Whether the module is enabled (default is True).
               - eventIds: List of event IDs.
               - areaId: Area ID for group module data (default is 0).
               - competitionId: Competition ID for group module data (default is 0).
               - numberQualifiers: Number of qualifiers for group module data (default is 0).
               - seasonId: Season ID for group module data (default is 0).
               - sportId: Sport ID for group module data (default is 0).
               - highlightCarousels: List of highlight carousel data.
               - events: List of events for knockout module data.
               - rounds: List of rounds for knockout module data.
               - markets: List of markets.
               - promoTag: Promotion tag for the module.
               - resultModuleSeasonId: Season ID for result module data (default is 0).
               - eventIds: List of event IDs for special module data.
               - linkUrl: Link URL for special module data.
               - typeIds: List of type IDs for special module data.
               - status: Status of the module.
               - surfaceBets: List of surface bets data.
               - typeId: Type ID for the module.

           :return: Response from the API containing information about the newly created module.
           """
        path = f'competition/{competition_id}/tab/{tab_id}/module'
        payload = {
            'aemPageName': None,
            'brand': self.brand,
            'categoryIDs': kwargs.get('categoryids', []),
            'displayOrder': kwargs.get('displayOrder', 0),
            'id': None,
            'enabled': kwargs.get('enabled', True),
            'eventIds': kwargs.get('eventIds', []),
            'groupModuleData': {'areaId': kwargs.get('areaId', 0),
                                'competitionId': kwargs.get('competitionId', 0),
                                'details': {},
                                'numberQualifiers': kwargs.get('numberQualifiers', 0),
                                'seasonId': kwargs.get('seasonId', 0), 'sportId': kwargs.get('sportId', 0)},
            'highlightCarousels': kwargs.get('highlightCarousels', []),
            'knockoutModuleData': {
                'events': kwargs.get('events', []),
                'rounds': kwargs.get('rounds', [])},
            'markets': kwargs.get('markets', []),
            'name': module_name,
            'promoTag': kwargs.get('promoTag', ""),
            'resultModuleSeasonId': kwargs.get('resultModuleSeasonId', 0),
            'specialModuleData': {'eventIds': kwargs.get('eventIds', []),
                                  'linkUrl': kwargs.get('linkUrl', ""), 'typeIds': kwargs.get('typeIds', [])},
            'status': kwargs.get('status', ""),
            'surfaceBets': kwargs.get('surfaceBets', []),
            'type': module_type,
            'typeId': kwargs.get('typeId', "")
        }
        response = self.request.post(url=path, data=json.dumps(payload))
        return response

    def update_surface_module_for_big_competition(self, module_id, module_name, **kwargs):
        """
         Update the data for a specific module within a 'big competition'.

         :param module_id: The ID of the module to be updated.
         :param module_name: The name of the module to be updated.
         :param kwargs: Additional keyword arguments to update module data.
             - enabled: Whether the module is enabled (default is True).
             - eventIds: List of event IDs.
             - areaId: Area ID for group module data (default is 0).
             - competitionId: Competition ID for group module data (default is 0).
             - competitionIds: List of competition IDs for group module data.
             - numberQualifiers: Number of qualifiers for group module data (default is 0).
             - seasonId: Season ID for group module data (default is 0).
             - sportId: Sport ID for group module data (default is 0).
             - highlightCarousels: List of highlight carousel data.
             - events: List of events for knockout module data.
             - rounds: List of rounds for knockout module data.
             - markets: List of markets.
             - maxDisplay: Maximum display value (default is 10).
             - resultModuleSeasonId: Season ID for result module data (default is 0).
             - eventIds: List of event IDs for special module data.
             - linkUrl: Link URL for special module data.
             - typeIds: List of type IDs for special module data.
             - typeId: Type ID for the module.
             - surfaceBets: List of surface bets data.
             - viewType: View type of the module (default is "CARD").

         :return: Response from the API containing information about the updated module.
         """
        path = f'competitionModule/{module_id}/{self.brand}'
        payload = {
            "aemPageName": None,
            "enabled": kwargs.get('enabled', True),
            "eventIds": kwargs.get("eventIds", []),
            'groupModuleData': {'areaId': kwargs.get('areaId', 0),
                                'competitionId': kwargs.get('competitionId', 0),
                                'competitionIds': kwargs.get('competitionIds', None),
                                'details': {},
                                'numberQualifiers': kwargs.get('numberQualifiers', 0),
                                'seasonId': kwargs.get('seasonId', 0), 'sportId': kwargs.get('sportId', 0)},
            "highlightCarousels": kwargs.get("highlightCarousels", []),
            "id": module_id,
            "knockoutModuleData": {
                'events': kwargs.get('events', []),
                'rounds': kwargs.get('rounds', [])},
            "markets": kwargs.get('markets', []),
            "maxDisplay": kwargs.get("maxDisplay", 10),
            "name": module_name,
            "surfaceBets": [],
            "resultModuleSeasonId": kwargs.get('resultModuleSeasonId', 0),
            "specialModuleData": {'eventIds': kwargs.get('eventIds', []),
                                  'linkUrl': kwargs.get('linkUrl', ""), 'typeIds': kwargs.get('typeIds', [])},
            "type": None,
            "typeId": kwargs.get('typeId', None),
            "viewType": kwargs.get('viewType', "CARD")
        }
        if kwargs.get('surfaceBets'):
            payload.update(
                {"surfaceBets": kwargs.get('surfaceBets'),
                 "type": "SURFACEBET"}
            )
        if kwargs.get('highlightCarousels'):
            payload.update(
                {"highlightCarousels": kwargs.get("highlightCarousels"),
                 "type": "HIGHLIGHTS_CAROUSEL"}
            )
        response = self.request.put(url=path, data=json.dumps(payload))
        return response

    def update_next_events_module_for_big_competition(self, module_id, module_name, module_type, type_id, **kwargs):
        """
         Update the data for next events module within a 'big competition'.

         :param module_id: The ID of the module to be updated.
         :param module_name: The name of the module to be updated.
         :param kwargs: Additional keyword arguments to update module data.
             - enabled: Whether the module is enabled (default is True).
             - eventIds: List of event IDs.
             - areaId: Area ID for group module data (default is 0).
             - competitionId: Competition ID for group module data (default is 0).
             - competitionIds: List of competition IDs for group module data.
             - numberQualifiers: Number of qualifiers for group module data (default is 0).
             - seasonId: Season ID for group module data (default is 0).
             - sportId: Sport ID for group module data (default is 0).
             - highlightCarousels: List of highlight carousel data.
             - events: List of events for knockout module data.
             - rounds: List of rounds for knockout module data.
             - markets: List of markets.
             - maxDisplay: Maximum display value (default is 10).
             - resultModuleSeasonId: Season ID for result module data (default is 0).
             - eventIds: List of event IDs for special module data.
             - linkUrl: Link URL for special module data.
             - typeIds: List of type IDs for special module data.
             - typeId: Type ID for the module.
             - surfaceBets: List of surface bets data.
             - viewType: View type of the module (default is "CARD").

         :return: Response from the API containing information about the updated module.
         """
        path = f'competitionModule/{module_id}/{self.brand}'
        payload = {
            "id": module_id,
            "name": module_name,
            "enabled": kwargs.get('enabled', True),
            "type": module_type if module_type else "NEXT_EVENTS",
            "markets": kwargs.get('markets', []),
            "typeId": type_id,
            "viewType": kwargs.get('viewType', "CARD"),
            "aemPageName": kwargs.get('aemPageName', None),
            "maxDisplay": kwargs.get("maxDisplay", 10),
            "groupModuleData": {
                'areaId': kwargs.get('areaId', 0),
                'competitionId': kwargs.get('competitionId', 0),
                'competitionIds': kwargs.get('competitionIds', None),
                'details': {},
                'numberQualifiers': kwargs.get('numberQualifiers', 0),
                'seasonId': kwargs.get('seasonId', 0),
                'sportId': kwargs.get('sportId', 0)
            },
            "specialModuleData": {
                'eventIds': kwargs.get('eventIds', []),
                'linkUrl': kwargs.get('linkUrl', ""),
                'typeIds': kwargs.get('typeIds', [])
            },
            "eventIds": kwargs.get("eventIds", []),
            "knockoutModuleData": {
                'events': kwargs.get('events', []),
                'rounds': kwargs.get('rounds', [])
            },
            "resultModuleSeasonId": kwargs.get('resultModuleSeasonId', 0),
            "surfaceBets": [],
            "highlightCarousels": kwargs.get("highlightCarousels", []),
        }
        response = self.request.put(url=path, data=json.dumps(payload))
        return response

    # Event hub

    def get_event_hubs(self) -> list:
        """
        Get all Event Hubs
        :return: list of dict with all configured event hubs
        """
        path = f'event-hub/brand/{self.brand}'
        response = self.request.get(path)
        return response

    def create_event_hub(self, index_number: int = 1) -> dict:
        """
        Create Event Hub
        :param index_number: int, index of event hub
        :return: dict
        """
        path = 'event-hub'
        payload = {
            'id': None,
            'createdAt': None,
            'createdBy': None,
            'updatedBy': None,
            'updatedAt': None,
            'updatedByUserName': None,
            'createdByUserName': None,
            'brand': self.brand,
            'title': f'Auto EventHub_{index_number}',
            'indexNumber': index_number,
            'disabled': False
        }
        response = self.request.post(
            url=path,
            data=json.dumps(payload)
        )
        self._created_event_hubs.append(response.get('id'))
        return response

    def get_sport_modules_for_event_hub(self, index_number: int) -> list:
        """
        Get all sport modules for event hub
        :param: index_number: int, indexNumber parameter of Event Hub
        :return: list of dict with all configured event hubs
        """
        path = f'sport-module/brand/{self.brand}/eventhub/{index_number}'
        response = self.request.get(path)
        return response

    def add_sport_module_to_event_hub(self, page_id: int = None, module_type: str = None) -> dict:
        """
        Add sports module to Event Hub
        :param page_id: int, number of created Event Hub, e.g. 2
        :param module_type: str, name of sport module
        :return: dict, sport module configuration
        """
        path = 'sport-module'
        quick_link_type = 'QUICK_LINK'
        surface_bet_type = 'SURFACE_BET'
        highlight_carousel_type = 'HIGHLIGHTS_CAROUSEL'
        featured_type = 'FEATURED'
        payload = {
            'publishedDevices': [],
            'sportId': None,
            'pageId': str(page_id),
            'pageType': 'eventhub',
            'enabled': True,
            'sortOrder': 1,
            'inplayConfig': None,
            'rpgConfig': None,
            'moduleConfig': None,
            'brand': self.brand,
            'disabled': False
        }
        if module_type is quick_link_type:
            payload.update(
                {
                    'moduleType': quick_link_type,
                    'title': 'Quick Links Module',
                }
            )
        elif module_type is surface_bet_type:
            payload.update(
                {
                    'moduleType': surface_bet_type,
                    'title': 'Surface Bet Module',
                }
            )
        elif module_type is highlight_carousel_type:
            payload.update(
                {
                    'moduleType': highlight_carousel_type,
                    'title': 'Highlights Carousel',
                }
            )
        elif module_type is featured_type:
            payload.update(
                {
                    'moduleType': featured_type,
                    'title': 'Featured events',
                }
            )
        response = self.request.post(
            url=path,
            data=json.dumps(payload)
        )
        return response

    def delete_event_hub_module(self, _id: str):
        """
        Delete Event Hub module
        :param _id: str, Event Hub module id
        """
        path = f'event-hub/{_id}'
        self.request.delete(path, parse_response=False)

    # Virtual sports

    def get_virtual_carousel_menu_items(self) -> list:
        """
        :return: list of dicts
        """
        response = self.request.get(url=get_cms_settings().config.public_api_url + f'{self.brand}/virtual-sports')
        return response

    def get_parent_virtual_sports(self) -> list:
        """
        Gets list of parent virtual sports
        :return: list of dicts
        """
        path = f'virtual-sport/brand/{self.brand}'
        response = self.request.get(path)
        return response

    def get_child_virtual_sports(self, sport_id) -> list:
        """
        Gets list of children virtual sports for parent
        :param sport_id: Parent sport id e.g. '5ed12f4cc9e77c0001f66909'
        :return: list of dicts
        """
        path = f'virtual-sport-track/sport-id/{sport_id}'
        response = self.request.get(path)
        return response

    def set_sport_category_ordering(self, new_order: list, moving_item, **kwargs):
        """
        Method allows to change sport category ordering in CMS
        :param new_order: list of sports e.g. ["5ed12f4cc9e77c0001f66909","5ecf9906c9e77c0001a0e57a","5ed12ef4c9e77c0001f66905"]
        :param moving_item: Item id e.g. '5ed12f4cc9e77c0001f66909'
        """
        data = {
            "order": new_order,
            "id": moving_item,
            "pageId": 'null',
            "pageType": 'null',
            "segmentName": kwargs.get('segmentName', 'Universal')
        }
        data = json.dumps(data)
        path = f'sport-category/ordering'
        self.request.post(path, data=data, parse_response=False)

    def set_parent_virtual_sports_ordering(self, new_order: list, moving_item):
        """
        Method allows to change virtual sports ordering in CMS
        :param new_order: list of sports e.g. ["5ed12f4cc9e77c0001f66909","5ecf9906c9e77c0001a0e57a","5ed12ef4c9e77c0001f66905"]
        :param moving_item: Item id e.g. '5ed12f4cc9e77c0001f66909'
        """
        data = {
            "order": new_order,
            "id": moving_item
        }
        data = json.dumps(data)
        path = f'virtual-sport/ordering'
        self.request.post(path, data=data, parse_response=False)

    def set_child_virtual_sports_ordering(self, new_order: list, moving_item):
        """
        Method allows to change child virtual sports ordering in CMS
        :param new_order: list of sports e.g. ["5ed12f4cc9e77c0001f66909","5ecf9906c9e77c0001a0e57a","5ed12ef4c9e77c0001f66905"]
        :param moving_item: Item id e.g. '5ed12f4cc9e77c0001f66909'
        """
        data = {
            "order": new_order,
            "id": moving_item
        }
        data = json.dumps(data)
        path = f'virtual-sport-track/ordering'
        self.request.post(path, data=data, parse_response=False)

    def set_county_panel_ordering_for_horse_racing(self, new_order: list, moving_item):
        """
         Method allows to change country panels ordering in CMS
        :param new_order: list of sports e.g.["5ce4ca43c9e77c000135fc24", "5d11ae63c9e77c0001d4f884", "5ce4ca42c9e77c0001e08fca"]
        :param moving_item: Item id e.g.'5eb9ebd9c9e77c00018cdb27'
        """
        data = {
            "order": new_order,
            "id": moving_item
        }
        data = json.dumps(data)
        path = f'sport-module/ordering'
        self.request.post(path, data=data, parse_response=False)

    def set_racing_edp_markets_ordering(self, new_order: list, moving_item):
        """
        Method allows to change racing edp markets ordering in CMS
        :param new_order: list of sports e.g. ["5ed12f4cc9e77c0001f66909","5ecf9906c9e77c0001a0e57a","5ed12ef4c9e77c0001f66905"]
        :param moving_item: Item id e.g. '5ed12f4cc9e77c0001f66909'
        """
        data = {
            "order": new_order,
            "id": moving_item
        }
        data = json.dumps(data)
        path = 'racing-edp-market/ordering'
        self.request.post(path, data=data, parse_response=False)

    @property
    def constants(self):
        if self.brand == 'bma':
            from crlat_cms_client.constants.base.constants import CmsConstants as Constants
        else:
            from crlat_cms_client.constants.ladbrokes.constants import LadbrokesCmsConstants as Constants
        return Constants

    def get_sport_config(self, category_id) -> dict:
        """
        Getting sport configuration and tabs
        :param category_id: Sport category id
        :return: dict with sport config
        """
        path = f'{self.brand}/sport-config/{category_id}'
        response = self.request.get(get_cms_settings().config.public_api_url + path)
        return response

    def verify_and_update_sport_config(self, sport_category_id: str, **kwargs):
        """
        Updating specified field values in sport configuration
        :param sport_category_id: Sport category id
        :param disp_sort_names: str ,dispSortNames values - e.g:'MR,HH,MH,WH,HL', 'MR,HH'
        :param primary_markets: str ,primaryMarkets values - e.g:'|Match Betting|,|Match Betting Head/Head|,|Total Sixes|'
        :return: updated sport config data for specified sport
        """
        sport_categories = self.get_sport_categories()
        counter = 0
        if sport_categories:
            for sport in sport_categories:
                if sport['categoryId'] == sport_category_id:
                    payload = sport
                    disp_sort = kwargs.get('disp_sort_names', '')
                    primary_markets = kwargs.get('primary_markets', '')
                    if (len(disp_sort) > 0) & (sport['dispSortNames'] != disp_sort):
                        payload['dispSortNames'] = disp_sort
                        counter += 1
                    if (len(primary_markets) > 0) & (sport['primaryMarkets'] != primary_markets):
                        payload['primaryMarkets'] = primary_markets
                        counter += 1
                    if counter > 0:
                        path = f'sport-category/{sport["id"]}'
                        response = self.request.put(get_cms_settings().config.api_url + path, data=json.dumps(payload))
                        return response
                    else:
                        self._logger.info('There is no change in payload for disp_sort & primary_market')
                        return True
            raise CMSException(f'Sport is not configured in CMS for sport category id: "{sport_category_id}"')
        else:
            raise CMSException('No Sports category information found')

    def verify_and_update_market_switcher_status(self, sport_name: str, status: bool):
        """
        Verifying market switcher status in system configuration for specified sport
        :param sport_name: Sport name e.g -'cricket','rugbyunion','americanfootball'
        :param status: bool e.g True/False for enabled/disabled
        :return: sport response
        """
        try:
            sport_status = self.get_initial_data()['systemConfiguration']['MarketSwitcher'][sport_name]
            if sport_status != status:
                response = self.update_system_configuration_structure(config_item='MarketSwitcher',
                                                                      field_name=sport_name, field_value=status)
                return response['structure']['MarketSwitcher'][sport_name]
            else:
                self._logger.info(f'The "{sport_name}" status is already "{sport_status}" in market switcher')
                return sport_status
        except Exception:
            raise CMSException(f'Sport "{sport_name}" information not found.')

    def verify_and_update_bet_filter_horse_racing_status(self, status: bool):
        """
        Verifying bet filter horse racing status in system configuration
        :param status: bool e.g True/False for enabled/disabled
        :return: bet filter response
        """
        try:
            bet_filter_status = self.get_initial_data()['systemConfiguration']['BetFilterHorseRacing']['enabled']
            if bet_filter_status != status:
                response = self.update_system_configuration_structure(config_item='BetFilterHorseRacing',
                                                                      field_name='enabled', field_value=status)
                return response['structure']['BetFilterHorseRacing']['enabled']
            else:
                self._logger.info(f'The bet filter horse racing status is already "{bet_filter_status}"')
                return bet_filter_status
        except Exception:
            raise CMSException('bet filter horse racing information not found')

    def get_markets_with_description(self):
        """
        :return: List of markets with description
        """
        path = f'racing-edp-market/brand/{self.brand}'
        return self.request.get(path)

    def create_and_update_markets_with_description(self, name, description, HR=True, GH=True, New_badge=False) -> list:
        """
        :param name: name of the market(it must match with ob template)
        :param description: description of the market
        :param HR: market description for Horse Racing to be enabled/disabled
        :param GH: market description for Greyhound Racing to be enabled/disabled
        :param New_badge: New badge to be enabled/disabled
        :return: created/updated market
        """
        markets = self.get_markets_with_description()
        for market in markets:
            if market['name'] == name:
                self._logger.warning(f'*** market "{name}" is already exists')

                # updating existing market
                path = f'racing-edp-market/{market["id"]}'
                data = {
                    "name": name,
                    "description": description,
                    "isHR": HR,
                    "isGH": GH,
                    "isNew": New_badge,
                    "brand": self.brand
                }
                data = json.dumps(data)
                return self.request.put(path, data=data)

        # creating new market if required market is not found
        path = f'racing-edp-market'
        data = {
            "name": name,
            "description": description,
            "isHR": HR,
            "isGH": GH,
            "isNew": New_badge,
            "brand": self.brand
        }
        data = json.dumps(data)
        market = self.request.post(path, data=data)
        self._created_racing_edp_markets.append(market['name'])
        return market

    def delete_markets_with_description(self, name):
        """
        :param name: market name
        """
        markets = self.get_markets_with_description()
        for market in markets:
            if market['name'] == name:
                path = f'racing-edp-market/{market["id"]}'
                self.request.delete(path, parse_response=False)
                break
        else:
            raise CMSException('Market name "%s" does not exists' % name)

    def update_secondary_market_tooltip(self, text: str=None, enabled: bool=True):
        """
        :param text: tooltip text if required
        :param enabled: tooltip to be enabled/disabled
        """
        id  = self.get_config_id(config_name='SecondaryMarketsTooltip')
        path = f'configuration/brand/{self.brand}/element/{id}'
        text = text if text else 'Look below to find additional markets'
        data = {
            "id": id,
            "name": "SecondaryMarketsTooltip",
            "overwrite": False,
            "initialDataConfig": True,
            "items": [{"name":"enabled", "type":"checkbox", "value":enabled},
                      {"name":"title", "type":"input", "value":text}]
        }
        data = json.dumps(data)
        return self.request.put(path, data=data)

    def get_sport_tab_id(self, sport_id: int, tab_name: str):
        """
        :param sport_id: int, for example for homepage sport_id=0 for football sport_id=16, ID is getting from OpenBet
        :param tab_name: str, name of the sport tab ex: Outright,matches,coupons
        """
        path = f'sport-tab/brand/{self.brand}/sport/{sport_id}'
        tabs_details_response = self.request.get(path)
        return next((tab['id'] for tab in tabs_details_response if tab['name']==tab_name), '')

    def get_sport_tab_data_by_tab_id(self, sport_tab_id):
        """
        :param sport_tab_id: tab id
        """
        path = f'sport-tab/{sport_tab_id}'
        response = self.request.get(path)
        return response

    def update_sports_tab_status(self, **kwargs):
        """
        :param sport_tab_id: tab id
        :param sport_id: category id ex. 16
        :param enabled: true/false
        """
        path = f'sport-tab/{kwargs["sport_tab_id"]}'
        response = self.request.get(path)
        for field in kwargs:
            if not (field in response) or field in ['sportId', 'id', 'name']:
                continue
            else:
                response[field] = kwargs.get(field)
        data = json.dumps(response)
        self.request.put(path, data=data)

    def get_sports_tab_data(self, sport_id: int, tab_name: str):
        """
        :param sport_id: int, for example for homepage sport_id=0 for football sport_id=16, ID is getting from OpenBet
        :param tab_name: str, name of the sport tab ex: Outright,matches,coupons
         """
        tab_id = self.get_sport_tab_id(sport_id=sport_id, tab_name=tab_name)
        path = f'sport-tab/{tab_id}'
        tabs_details_response = self.request.get(path)
        return tabs_details_response

    def get_sport_tab_status(self, tab_name: str, sport_id: int, **kwargs):
        sport_tab_id = self.get_sport_tab_id(sport_id=sport_id, tab_name=tab_name)
        path = f'sport-tab/{sport_tab_id}'
        response = self.request.get(path)
        check_events = response.get("checkEvents")
        has_events = response.get("hasEvents")
        enabled = response.get("enabled")
        if not enabled:
            return False
        if check_events is None or has_events is None:
            raise CMSException(f'check_events:{check_events} and has_events:{has_events},The paremeters are not present in response')
        if check_events and not has_events:
            return False
        return True

    def get_sport_tabs(self, sport_id: int):
        """
        :param sport_id: int, for example for homepage sport_id=0 for football sport_id=16, ID is getting from OpenBet
        """
        path = f'sport-tab/brand/{self.brand}/sport/{sport_id}'
        tabs_details_response = self.request.get(path)
        return tabs_details_response

    def set_sport_tabs_ordering(self, moving_item, new_order):
        """
        Sets the ordering of sport tabs by sending a request to the specified API endpoint.
        Parameters:
        - moving_item (str): The id of the sport tab to be moved.
        - new_order (list): list of sport tab ids.
        Returns:
        None
        """
        path = 'sport-tab/ordering'
        request_payload = {
            'id': moving_item,
            'order': new_order
        }
        request_payload = json.dumps(request_payload)
        self.request.post(path, data=request_payload, parse_response=False)

    def update_sports_event_filters(self, tab_name: str, enabled: str, sport_id: int, top_league_ids=None, test_league_ids=None,
                          invalid_league_ids=None, league_enabled=True, league_required=False, **kwargs):
        """
        :param sport_id: category id ex. 16
        :param enabled: true/false
        :param tab_name: str, name of the sport tab ex: Outright,matches,coupons
        :param top_league_ids: list of type ids
        :param test_league_ids: list of type ids
        :param invalid_league_ids: list of invalid type ids
        :param league_enabled: to enable league filter
        :param timefilter_enabled: to enable league filter
        """
        sport_tab_id = self.get_sport_tab_id(sport_id=sport_id, tab_name=tab_name)
        path = f'sport-tab/{sport_tab_id}'
        response = self.request.get(path)
        fields_to_update = [
            'checkEvents', 'displayName', 'marketsNames', 'filters', 'hasEvents', 'hidden', 'name', 'sortOrder',
            'interstitialBanners'
        ]
        for field in fields_to_update:
            if field == 'filters':
                if response.get('filters') is None or response.get('filters').get('time') is None:
                    time_filters = []
                else:
                    time_filters = [] if response.get('filters').get('time').get('values') is None else response.get(
                        'filters').get('time').get('values')
                response[field]['time']['enabled'] = kwargs.pop('timefilter_enabled', response[field]['time']['enabled'])
                response[field]['time']['values'] = kwargs.pop('event_filters_values', time_filters)
            elif field == 'interstitialBanners' and response[field]:
                response[field]['bannerPosition'] = kwargs.pop('banner_Position', response[field]['bannerPosition'])
                response[field]['ctaButtonLabel'] = kwargs.pop('ctaButton_Label', response[field]['ctaButtonLabel'])
                response[field]['redirectionUrl'] = kwargs.pop('redirection_Url', response[field]['redirectionUrl'])
                response[field]['bannerEnabled'] = kwargs.pop('banner_Enabled', response[field]['bannerEnabled'])
            else:
                response[field] = kwargs.pop(field, response[field])
        response['enabled'] = enabled
        response['id'] = sport_tab_id
        response['sportId'] = sport_id
        if league_required:
            final_league = self.set_league(response, top_league_ids, test_league_ids, invalid_league_ids)
            response['filters'].update({"league": {
                "enabled": league_enabled,
                "values": kwargs.get('league_values', final_league)
            }})
        data = json.dumps(response)
        self.request.put(path, data=data)

    def set_league(self, response,top_league_ids, test_league_ids, invalid_league_ids):
        """
        @param response: sport event timeline filter response
        @return: top league, test league, invalid league data
        """
        if response.get('filters') is None or response.get('filters').get('league') is None :
            league_values = []
        else:
            league_values = [] if response.get('filters').get('league').get('values') is None else response.get(
            'filters').get('league').get('values')
        final_league = []

        if league_values:
            for values in league_values:
                if values.get('leagueName') not in ['Top Leagues', 'Test Leagues', 'Invalid Leagues']:
                    final_league.append(values)

        final_top_leagues_id = []
        final_test_leagues_id = []
        final_invalid_leagues_id = []

        if top_league_ids:
            final_top_leagues_id.extend(top_league_ids)
            if len(league_values) != 0:
                for values in league_values:
                    if values.get('leagueName') == 'Top Leagues':
                        final_top_leagues_id.extend(values.get('leagueIds'))
                        break
        else:
            if len(league_values) != 0:
                for values in league_values:
                    if values.get('leagueName') == 'Top Leagues':
                        final_top_leagues_id.extend(values.get('leagueIds'))
                        break
        if len(final_top_leagues_id) != 0:
            top_legaue = {
                "leagueName": "Top Leagues",
                "leagueIds": list(set(final_top_leagues_id))
            }
            final_league.append(top_legaue)
        if test_league_ids:
            final_test_leagues_id.extend(test_league_ids)
            if len(league_values) != 0:
                for values in league_values:
                    if values.get('leagueName') == 'Test Leagues':
                        final_test_leagues_id.extend(values.get('leagueIds'))
                        break
        else:
            if len(league_values) != 0:
                for values in league_values:
                    if values.get('leagueName') == 'Test Leagues':
                        final_test_leagues_id.extend(values.get('leagueIds'))
                        break
        if len(final_test_leagues_id) != 0:
            test_legaue = {
                "leagueName": "Test Leagues",
                "leagueIds": list(set(final_test_leagues_id))
            }
            final_league.append(test_legaue)

        if invalid_league_ids:
            final_invalid_leagues_id.extend(invalid_league_ids)
            if len(league_values) != 0:
                for values in league_values:
                    if values.get('leagueName') == 'Invalid Leagues':
                        final_invalid_leagues_id.extend(values.get('leagueIds'))
                        break
        else:
            if len(league_values) != 0:
                for values in league_values:
                    if values.get('leagueName') == 'Invalid Leagues':
                        final_invalid_leagues_id.extend(values.get('leagueIds'))
                        break
        if len(final_invalid_leagues_id) != 0:
            invalid_legaue = {
                "leagueName": "Invalid Leagues",
                "leagueIds": list(set(final_invalid_leagues_id))
            }
            final_league.append(invalid_legaue)

        return final_league

    def update_sport_tab_config(self, tab_name: str, enabled: str, sport_id: int, **kwargs):
        """
        Method to update sport configuration. It retrieves the sport configuration data for a given sport id
        and tab name, and updates certain fields as specified.

        Args:
            tab_name (str): Name of the tab.
            enabled (str): A string indicating if the tab is enabled or not.
            sport_id (int): Identifier of the sport.
            timefilter_enabled (bool, optional): Flag to enable/disable time filter. Default is True.
            **kwargs: Arbitrary keyword arguments.

        Keyword Args:
            checkEvents (bool, optional): Indicates if events check is enabled or not.
            displayName (str, optional): Display name for the sport.
            marketsNames (str, optional): Market names associated with the sport.
            event_filters_values (list, optional): List of event filter values.
            hasEvents (bool, optional): Indicates if the sport has events or not.
            hidden (bool, optional): Indicates if the sport is hidden or not.
            name (str, optional): Name of the sport.
            sortOrder (int, optional): Order in which sport should be sorted.

        Returns:
            None
        """
        # Get the id of the sport tab using sport id and tab name
        sport_tab_id = self.get_sport_tab_id(sport_id=sport_id, tab_name=tab_name)

        # Set the path for the get request
        path = f'sport-tab/{sport_tab_id}'

        # Send a get request and store the response
        response = self.request.get(path)
        fields_to_update = [
            'checkEvents', 'displayName', 'marketsNames', 'filters', 'hasEvents', 'hidden', 'name', 'sortOrder'
        ]
        for field in fields_to_update:
            if field == 'filters':
                if response.get('filters') is None or response.get('filters').get('time') is None:
                    time_filters = []
                else:
                    time_filters = [] if response.get('filters').get('time').get('values') is None else response.get(
                        'filters').get('time').get('values')
                response[field]['time']['enabled'] = kwargs.pop('timefilter_enabled', response[field]['time']['enabled'])
                response[field]['time']['values'] = kwargs.pop('event_filters_values', time_filters)
            else:
                response[field] = kwargs.pop(field, response[field])
        response['enabled'] = enabled
        response['id'] = sport_tab_id
        response['sportId'] = sport_id

        # Convert the data into json format
        data = json.dumps(response)

        # Send a put request with the updated data
        self.request.put(path, data=data)

    def get_timeline_system_configuration(self) -> list:
        """
         Description: getting timeline feature details from timeline system config
         return:timeline feature enabled
        """
        path = f'timeline/system-config/brand/{self.brand}'
        return self.request.get(path)

    def update_timeline_system_config(self, enabled=True):
        """
        update timeline system config
        param enabled:timeline to be enabled/disabled
        """
        response = self.get_timeline_system_configuration()
        path = f'timeline/system-config/{response["id"]}'
        data = {
            "id": response['id'],
            "createdBy": None,
            "createdByUserName": None,
            "updatedBy": None,
            "updatedByUserName": None,
            "createdAt": None,
            "updatedAt": None,
            "brand": self.brand,
            "enabled": enabled,
            "pageUrls": "/*"
        }
        data = json.dumps(data)
        return self.request.put(path, data=data)

    def get_timeline_template(self) -> list:
        """
        return: list of timeline templates
        """
        path = f'timeline/template/brand/{self.brand}'
        return self.request.get(path)

    def create_timeline_template(self, template_name, text, **kwargs):
        """
        param template_name: template_name
        param text: text--str-- paragrah text
        param kwargs: isSpotlightTemplate--True-- while creating spotlight template
        param kwargs: isVerdictTemplate--True-- while creating verdict template
        param kwargs: yellowHeaderText--str--  text
        param kwargs: betPromptHeader--str--  text
        param kwargs: showLeftSideRedLine--boolean
        param kwargs: showLeftSideBlueLine--boolean
        param kwargs: showTimestamp--boolean
        param kwargs: showRedirectArrow--boolean
        param kwargs: showRacingPostLogoInHeader--boolean
        param kwargs: postHref--str-url
        return: object with all information about just created timeline template (id, title, etc)
        """
        path = f'timeline/template'
        data = {
            "id": "",
            "brand": self.brand,
            "name": template_name,
            "headerText": template_name + " header_text",
            "yellowHeaderText": kwargs.get('yellowHeaderText', "yellowHeaderText"),
            "subHeader": "",
            "isYellowSubHeaderBackground": False,
            "eventId": "",
            "selectionId": "",
            "topRightCornerImage": {
                "filename": "",
                "originalname": "",
                "path": "",
                "size": 0,
                "filetype": ""
            },
            "betPromptHeader": kwargs.get('betPromptHeader', ''),
            "text": text,
            "showLeftSideRedLine": kwargs.get('showLeftSideRedLine', False),
            "showLeftSideBlueLine": kwargs.get('showLeftSideBlueLine', False),
            "showTimestamp": kwargs.get('showTimestamp', True),
            "showRedirectArrow": kwargs.get('showRedirectArrow', False),
            "showRacingPostLogoInHeader": kwargs.get('showRacingPostLogoInHeader', False),
            "postHref": kwargs.get('postHref', ''),
            "isSpotlightTemplate": kwargs.get('isSpotlightTemplate', False),
            "isVerdictTemplate": kwargs.get('isVerdictTemplate', False)
        }
        data = json.dumps(data)
        response = self.request.post(path, data=data)
        self._created_timeline_template.append(response.get('id'))
        return response

    def update_timeline_template(self, template_id, **kwargs):
        """
        param template_id: templateid
        param template_name: templatename
        param kwargs: event_id: str
        param kwargs: selection_id: str
        param kwargs: betPromptHeader: str
        param kwargs: postHref: str, eg: url
        param kwargs: text: str, paragraph text
        param kwargs: showLeftSideRedLine--boolean
        param kwargs: showLeftSideBlueLine--boolean
        param kwargs: showTimestamp--boolean
        param kwargs: showRedirectArrow--boolean
        param kwargs: showRacingPostLogoInHeader--boolean
        param kwargs: showRedirectArrow--boolean
        param kwargs: isYellowSubHeaderBackground--boolean
        param kwargs: isSpotlightTemplate--True-- while creating spotlight template
        param kwargs: isVerdictTemplate--True-- while creating verdict template
        return:object with all information about just updated timeline template (id, title, etc)
        """
        path = f'timeline/template/{template_id}'
        timeline_template = self.get_timeline_single_template(template_id)
        data = {
            "id": template_id,
            "brand": self.brand,
            "name": kwargs.get('name',timeline_template['name'] + get_date_time_as_string(time_format='%Y-%m-%dT%H:%M:%SZ', url_encode=False)),
            "draft": False,
            "postIconSvgId": kwargs.get('postIconSvgId', ""),
            "headerIconSvgId": kwargs.get('headerIconSvgId', ""),
            "headerText": kwargs.get('headerText', timeline_template['headerText']),
            "yellowHeaderText": kwargs.get('yellowHeaderText', timeline_template['yellowHeaderText']),
            "subHeader": kwargs.get('subHeader', ""),
            "eventId": kwargs.get('eventId', ""),
            "selectionId": kwargs.get('selectionId', ""),
            "topRightCornerImage":
                {"filename": "",
                 "originalname": "",
                 "path": "",
                 "size": "0",
                 "filetype": ""
                 },
            "price": 'null',
            "betPromptHeader": kwargs.get('betPromptHeader', ""),
            "postHref": kwargs.get('postHref', ""),
            "text": kwargs.get('text', timeline_template['text']),
            "showLeftSideRedLine": kwargs.get('showLeftSideRedLine', False),
            "showLeftSideBlueLine": kwargs.get('showLeftSideBlueLine', False),
            "showTimestamp": kwargs.get('showTimestamp', True),
            "showRedirectArrow": kwargs.get('showRedirectArrow', False),
            "showRacingPostLogoInHeader": kwargs.get('showRacingPostLogoInHeader', False),
            "isYellowSubHeaderBackground": kwargs.get('isYellowSubHeaderBackground', False),
            "isSpotlightTemplate": kwargs.get('isSpotlightTemplate', False),
            "isVerdictTemplate": kwargs.get('isVerdictTemplate', False)
        }
        data = json.dumps(data)
        return self.request.put(path, data=data)

    def get_timeline_splash_page(self):
        """
        :return: retrive timeline splash data
        """
        path = f'timeline/splash-config/brand/{self.brand}'
        return self.request.get(path)

    def get_timeline_campaign(self) -> list:
        """
        :return: get List of timeline campaign
        """
        path = f'timeline/campaign/brand/{self.brand}'
        return self.request.get(path)

    def get_timeline_campaign_info(self, campaign_id):
        """
        :return: get info about campaign
        """
        path = f'timeline/campaign/{campaign_id}'
        return self.request.get(path)

    def add_timeline_campaign(self, campaign_name="auto_test_camp", **kwargs):
        """
        param campaign_name: name of campaign
        param kwargs: status-str, eg: LIVE,OPEN,CLOSED
        return: object with all information about just created timeline campaign (id etc)
        """
        path = f'timeline/campaign'
        data = {
            "id": "",
            "name": campaign_name,
            "displayFrom": get_date_time_as_string(time_format='%Y-%m-%dT%H:%M:%SZ', url_encode=False),
            "displayTo": get_date_time_as_string(time_format='%Y-%m-%dT%H:%M:%SZ', url_encode=False, days=3),
            "displayed": False,
            "highlighted": False,
            "status": kwargs.get('status', 'LIVE'),
            "messagesToDisplayCount": "50",
            "isChanged": False,
            "brand": self.brand
        }
        data = json.dumps(data)
        return self.request.post(path, data=data)

    def get_timeline_campaign_posts(self, campaign_id) -> list:
        """
         : return list of campaign posts
        """
        path = f'timeline/post/brand/{self.brand}/{campaign_id}'
        return self.request.get(path)

    def create_campaign_post(self, template_id, campaign_id, poststatus, **kwargs):
        """
        param template_id: templateid
        param template_name: templatename
        param campaign_id: campaign_id
        param postStatus: poststatus--PUBLISHED,UNPUBLISHED
        param kwargs:text-str, paragrah text
        param kwargs:yellowheadertext-str,  text
        param kwargs:subHeader-str,  text
        param kwargs:eventId-str,  text
        param kwargs:selectionId-str,  text
        param kwargs:betPromptHeader-str,  text
        param kwargs:postHref-str,  url
        return:object with all information about just created campaign post (id etc)
        """
        timeline_template = self.get_timeline_single_template(template_id)
        path = f'timeline/post'
        data = {
            "id": "",
            "name": timeline_template['name'],
            "template": {
                "id": template_id,
                "brand": self.brand,
                "name": kwargs.get('name', timeline_template['name']),
                "draft": False,
                "postIconSvgId": kwargs.get('postIconSvgId', timeline_template['postIconSvgId']),
                "headerIconSvgId": kwargs.get('headerIconSvgId', timeline_template['headerIconSvgId']),
                "headerText": kwargs.get('headerText', timeline_template['headerText']),
                "yellowHeaderText": kwargs.get('yellowHeaderText', timeline_template['yellowHeaderText']),
                "subHeader": kwargs.get('subHeader', timeline_template['subHeader']),
                "eventId": kwargs.get('eventId', timeline_template['eventId']),
                "selectionId": kwargs.get('selectionId', timeline_template['selectionId']),
                "topRightCornerImage": {
                    "filename": "",
                    "originalname": "",
                    "path": "",
                    "size": "0",
                    "filetype": ""
                },
                "price": 'null',
                "betPromptHeader": kwargs.get('betPromptHeader', timeline_template['betPromptHeader']),
                "postHref": kwargs.get('postHref', timeline_template['postHref']),
                "text": kwargs.get('text', timeline_template['text']),
                "showLeftSideRedLine": kwargs.get('showLeftSideRedLine', timeline_template['showLeftSideRedLine']),
                "showLeftSideBlueLine": kwargs.get('showLeftSideBlueLine', timeline_template['showLeftSideBlueLine']),
                "showTimestamp": kwargs.get('showTimestamp', timeline_template['showTimestamp']),
                "showRedirectArrow": kwargs.get('showRedirectArrow', timeline_template['showRedirectArrow']),
                "showRacingPostLogoInHeader": kwargs.get('showRacingPostLogoInHeader', timeline_template['showRacingPostLogoInHeader']),
                "isYellowSubHeaderBackground": kwargs.get('isYellowSubHeaderBackground', timeline_template['isYellowSubHeaderBackground']),
                "isSpotlightTemplate": kwargs.get('isSpotlightTemplate', timeline_template['isSpotlightTemplate']),
                "isVerdictTemplate": kwargs.get('isVerdictTemplate', timeline_template['isVerdictTemplate'])
            },
            "pinned": False,
            "campaignId": campaign_id,
            "postStatus": "DRAFT",
            "isChanged": False,
            "brand": self.brand
        }
        data = json.dumps(data)
        response = self.request.post(path, data=data)
        self.update_campaign_post(response.get('id'), poststatus, **kwargs)
        self._created_timeline_post.append(response.get('id'))
        return response

    def update_campaign_post(self,post_id, poststatus, **kwargs):
        """
        param post_id: postid
        param template_id: templateid
        param template_name: templatename
        param campaign_id: campaignid
        param poststatus: str- PUBLISHED,UNPUBLISHED
        param kwargs: event_id: str
        param kwargs: selection_id: str
        param kwargs: betPromptHeader: str
        param kwargs: postHref: str, eg: url
        param kwargs: text: str, paragraph text
        param kwargs: yellowHeaderText: str
        param kwargs: betPromptHeader: str
        param kwargs: postHref: str, eg: url
        param kwargs: text: str, paragraph text
        param kwargs: showLeftSideRedLine--boolean
        param kwargs: showLeftSideBlueLine--boolean
        param kwargs: showTimestamp--boolean
        param kwargs: showRedirectArrow--boolean
        param kwargs: showRacingPostLogoInHeader--boolean
        param kwargs: showRedirectArrow--boolean
        param kwargs: isYellowSubHeaderBackground--boolean
        param kwargs: isSpotlightTemplate--True-- while creating spotlight template
        param kwargs: isVerdictTemplate--True-- while creating verdict template
        return: object with all information about just created campaign post (id etc)
        """
        timeline_post = self.get_timeline_post(post_id)
        path = f'timeline/post/{post_id}'
        data = {
            "brand": self.brand,
            "name": timeline_post['template']['name'],
            "template": {
                "id": timeline_post['template']['id'],
                "brand": self.brand,
                "name": kwargs.get('name', timeline_post['template']['name']),
                "draft": False,
                "postIconSvgId": kwargs.get('postIconSvgId', timeline_post['template']['postIconSvgId']),
                "headerIconSvgId": kwargs.get('headerIconSvgId', timeline_post['template']['headerIconSvgId']),
                "headerText": kwargs.get('headerText', timeline_post['template']['headerText']),
                "yellowHeaderText": kwargs.get('yellowHeaderText', timeline_post['template']['yellowHeaderText']),
                "subHeader": kwargs.get('subHeader', timeline_post['template']['subHeader']),
                "eventId": kwargs.get("eventId", timeline_post['template']['eventId']),
                "selectionId": kwargs.get("selectionId", timeline_post['template']['selectionId']),
                "topRightCornerImage": {
                    "filename": "",
                    "originalname": "",
                    "path": "",
                    "size": "0",
                    "filetype": ""
                },
                "price": 'null',
                "betPromptHeader": kwargs.get('betPromptHeader', timeline_post['template']['betPromptHeader']),
                "postHref": kwargs.get('postHref', timeline_post['template']['postHref']),
                "text": "<p>" + kwargs.get('text', timeline_post['template']['text']) + "<p>",
                "showLeftSideRedLine": kwargs.get('showLeftSideRedLine', timeline_post['template']['showLeftSideRedLine']),
                "showLeftSideBlueLine": kwargs.get('showLeftSideBlueLine', timeline_post['template']['showLeftSideBlueLine']),
                "showTimestamp": kwargs.get('showTimestamp', timeline_post['template']['showTimestamp']),
                "showRedirectArrow": kwargs.get('showRedirectArrow', timeline_post['template']['showRedirectArrow']),
                "showRacingPostLogoInHeader": kwargs.get('showRacingPostLogoInHeader', timeline_post['template']['showRacingPostLogoInHeader']),
                "isYellowSubHeaderBackground": kwargs.get('isYellowSubHeaderBackground', timeline_post['template']['isYellowSubHeaderBackground']),
                "isSpotlightTemplate": kwargs.get('isSpotlightTemplate', timeline_post['template']['isSpotlightTemplate']),
                "isVerdictTemplate": kwargs.get('isVerdictTemplate', timeline_post['template']['isVerdictTemplate'])
            },
            "campaignId": kwargs.get('campaignId', timeline_post['campaignId']),
            "campaignName": "",
            "postStatus": poststatus,
            "pinned": False,
            "publishedAt": get_date_time_as_string(time_format='%Y-%m-%dT%H:%M:%SZ', url_encode=False),
            "id": post_id
        }
        data = json.dumps(data)
        return self.request.put(path, data=data)

    def spotlight_related_events(self, class_id, **kwargs):
        """
        param class_id: class id
        param kwargs: restrictToUkAndIre- boolean
        return: spolight related events
        """
        path = f'timeline/spotlight/brand/{self.brand}/related-events'
        data = {
            "refreshEventsFrom": kwargs.get('refreshEventsFrom', get_date_time_as_string(time_format='%Y-%m-%dT%H:%M:%SZ', url_encode=False)),
            "refreshEventsClassesString": class_id,
            "restrictToUkAndIre": kwargs.get('restrictToUkAndIre', True)
        }
        data = json.dumps(data)
        return self.request.post(path, data=data)

    def get_spotlight_data(self, event_id, campaign_id) -> dict:
        """
        param event_id: eventid
        param campaign_id: campaignid
        return: dict of spolight events data
        """
        path = f'timeline/spotlight/brand/{self.brand}/campaignId/{campaign_id}/spotlight-data/{event_id}'
        return self.request.get(path)

    def delete_timeline_post(self, post_id):
        """
        param post_id: postid
        return: deleting the timeline post
        """
        path = f'timeline/post/{post_id}'
        return self.request.delete(path, parse_response=False)

    def delete_timeline_template(self, template_id):
        """
        param template_id: template_id
        return: deleteing the timeline template
        """
        path = f'timeline/template/{template_id}'
        return self.request.delete(path, parse_response=False)

    def get_timeline_post(self,post_id):
        """
        param post_id: postid
        return: returning single timeline post
        """
        path = f'timeline/post/{post_id}'
        return self.request.get(path)

    def get_timeline_single_template(self,template_id):
        """
        param template_id: template_id
        return: returning single timeline template
        """
        path= f'timeline/template/{template_id}'
        return self.request.get(path)

    # Question Engine
    def get_qe_splash_page(self) -> list:
        """
        Returns list of available splash-page items.
        :return: List of splash page items
        """
        path = 'splash-page/brand/%s' % self.brand
        return self.request.get(path)

    def create_question_engine_spalsh_page(self, **kwargs):
        """
        @param kwargs:
        @return: splash page dictionary object
        """
        parameters =\
            {
             "title": "Autotest_Splash_Page",
             "strapLine": kwargs.get("starp_line", "Predict four match stats and you could win FREE BETS, "
                                                   "£50 CASH and a share of our NEW £25K Monthly Jackpot!"),
             "paragraphText1": "paragraphText1",
             "paragraphText2": "paragraphText2",
             "paragraphText3": "paragraphText3",
             "playForFreeCTAText":kwargs.get("CTA_1", "Play Now For Free!"),
             "seeYourSelectionsCTAText": kwargs.get("CTA_2", "See Your Selections"),
             "seePreviousSelectionsCTAText": kwargs.get("CTA3", "See previous games"),
             "loginToViewCTAText": kwargs.get("CTA4", "Log-in to play"),
             "footerText": "18+ Only. T&Cs apply",
             "brand": self.brand,
             "showPreviousGamesButton": kwargs.get("show_previous_games_button", True),
             "isChanged": False
             }
        data = json.dumps(parameters)
        splash_page = self.request.post('splash-page', data=data)
        self._logger.info('*** Added splash page {splash_page}'.format(splash_page=splash_page))
        return splash_page

    def delete_spalsh_page(self, _id: str):
        """
        Delete splash-page
        :param _id: str, splash-page id
        """
        path = f'splash-page/{_id}'
        self.request.delete(path, parse_response=False)

    # Question Engine Quicklinks
    def get_qe_quick_link_pages(self) -> list:
        """
        Returns list of available quick-link-page items.
        :return: List of quick-link-page items
        """
        path = 'question-engine/quick-links/brand/%s' % self.brand
        return self.request.get(path)

    def create_question_enigne_quick_links(self):
        """
        :return: Quick link page dictionary object
        """
        parameters = \
            {
            "brand": self.brand,
            "title": "Autotest_Quick_Links",
            "links": [{"title": "Prizes",
                       "relativePath": "Prizes",
                       "description": """
                                        £25k Jackpot\n
                                        Finish top of our monthly leaderboard to win a share of £25k\n
                                        £50 Cash\n
                                        Predict all four match stats correctly to win £50 Cash\n
                                        £2 Free Bet\n
                                        Predict three match stats correctly to win a £2 Free Bet\n
                                        £1 Free Bet\n
                                        Predict two match stats correctly to win a £1 Free Bet\n
                                        All prizes will be credited within 24 hours of the final whistle\n"""},

                      {"title": "Frequently Asked Questions",
                       "relativePath": "FAQs",
                       "description": """·When will my prize be credited?\n
                                        All prizes will be credited within 24 hours of the final whistle in the selected match.\n
                                        · What happens if my First Goalscorer selection becomes void?\n
                                        Your answer will be resulted as incorrect.\n 
                                        However, it will not impact your entire entry and you will still be eligible for a prize.\n
                                        · Does extra time count if the selected match is in a cup competition?\n
                                        No – your answers for the selected Correct4 match counts to 90 minutes only."""},

                       {"title": "Terms and Conditions",
                        "relativePath": "TandCs",
                        "description": "Terms and Conditions description"}]
            }
        data = json.dumps(parameters)
        question_engine_quick_link = self.request.post('question-engine/quick-links', data=data)
        return question_engine_quick_link

    def delete_question_engine_quick_links(self, _id: str):
        """
        Delete question_engine_quick_links
        :param _id: str, question_engine_quick_link id
        """
        path = f'question-engine/quick-links/{_id}'
        self.request.delete(path, parse_response=False)

    #Question Engine End Page
    def get_qe_end_pages(self) -> list:
        """
        Returns list of available end-page items.
        :return: List of end-page items
        """
        path = 'end-page/brand/%s' % self.brand
        return self.request.get(path)

    def create_question_engine_end_page(self, **kwargs):
        """
        :param kwargs:
        :return: End page object in dictionary
        """
        parameters = \
            {"title": "Autotest_End_Page",
             "brand": self.brand,
             "isChanged": False,
             "gameDescription": kwargs.get("game_description", "Game Description"),
             "noLatestRoundMessage": kwargs.get("no_latest_round_message", "No latest rounds"),
             "noPreviousRoundMessage": kwargs.get("no_previous_round_message", "No previous rounds"),
             "showPrizes": kwargs.get("show_prizes", True),
             "showAnswersSummary": kwargs.get("show_answers", True),
             "showResults": kwargs.get("show_results", True),
             "submitMessage": kwargs.get("submit_message", "Submitted your Quiz successfully"),
             "submitCta": kwargs.get("submit_cta", "Submit your answers"),
             "showUpsell": kwargs.get("show_upsell", True),
             "upsellAddToBetslipCtaText": kwargs.get("add_to_betslip_cta_upsell_text", "Add to betslip"),
             "upsellBetInPlayCtaText": kwargs.get("bet_in_play_cta_upsell_text", "Bet In-play"),
             "successMessage": kwargs.get("successMessage", "Congrats!! You earned ! {value} Coins!!"),
             "errorMessage": kwargs.get("errorMessage","Oops something's gone wrong, please check your account later, Thank you !!."),
             "redirectionButtonLabel": kwargs.get("redirectionButtonLabel", "Tap for more details for FSS Page 1"),
             "redirectionButtonUrl": kwargs.get("redirectionButtonUrl", "/sport/tennis"),
             "bannerSiteCoreId": kwargs.get("bannerSiteCoreId", None)
             }

        data = json.dumps(parameters)
        end_page = self.request.post('end-page', data=data)
        return end_page

    def delete_end_page(self, _id: str):
        """
        Delete end-page
        :param _id: str, end-page id
        """
        path = f'end-page/{_id}'
        self.request.delete(path, parse_response=False)

    # Question Engine Pop up
    def get_qe_pop_up_page(self):
        """
        Returns list of available popup items.
        :return: List of popup page items
        """
        path = 'quiz-popup-setting/brand/%s' % self.brand
        return self.request.get(path)

    def create_question_engine_pop_up(self, quiz_id, **kwargs):
        """
        @param quiz_id: created quiz id
        @param kwargs:
        @return:
        """
        popup_id = self.get_qe_pop_up_page()['id']
        parameters = {"id": popup_id,
                      "brand":self.brand,
                      "enabled":kwargs.get("enabled", True),
                      "pageUrls": kwargs.get("url", "/sport/football/*"),
                      "popupText":kwargs.get("pop_up_text", "Autotest_Quiz_Popup"),
                      "popupTitle":kwargs.get("pop_up_titile", "Autotest_Title"),
                      "quizId":quiz_id,
                      "yesText":kwargs.get("yes_text", "Yes"),
                      "remindLaterText":kwargs.get("remind_me_later", "Remind me later"),
                      "dontShowAgainText":kwargs.get("dont_show_again", "Don't show me again")}
        data = json.dumps(parameters)
        pop_up_page = self.request.put("quiz-popup-setting/"+ popup_id, data=data)
        return pop_up_page

    # Qestion engine Quiz
    def get_qe_quizzes(self) -> list:
        """
        Returns list of active quiz items
        :return: list of active quiz items
        """
        path = 'question-engine/brand/%s' % self.brand
        return self.request.get(path)

    def update_question_engine_quiz(self, quiz_id, title, **kwargs):
        """
        @param quiz_id: id of the quiz
        @param title: titile of the quiz
        @param kwargs: submit_prizetype: "FREE_BETS", "CREDIT", "NONE"
        @param kwargs: login_rule--"START", "SUBMIT", "NONE
        @param kwargs: quiz_state--True, False
        @param kwargs: actual_scores: Expample;- [1,3]
        @return: updated quiz dictionary object
        """
        payload = kwargs.get("payload", False)
        if payload:
            data = json.dumps(payload)
            quiz_page = self.request.put('question-engine/' + quiz_id, data=data)
            return quiz_page

        parameters ={"id": quiz_id, "title": title,
         "sourceId": "/footballsuperseries", "brand": self.brand,
         "firstQuestion": {"id": "111",
             "answers": [
                 {"id": "11",
                  "text": "Man City by exactly 1 goal",
                  "correctAnswer": False,
                  "nextQuestionId": "123",
                  "questionAskedId": "111",
                  "selectionId": None,
                  "endPage": None},
                 {"id": "12",
                  "text": "Man City by 2+ goals",
                  "correctAnswer": False,
                  "nextQuestionId": "123",
                  "questionAskedId": "111",
                  "selectionId": None,
                  "endPage": None
                  },
                 {"id": "13",
                  "text": "Draw",
                  "correctAnswer": False,
                  "nextQuestionId": "123",
                  "questionAskedId": "111",
                  "selectionId": None,
                  "endPage": None
                  }],
             "titleLength": {"isValid": True},
             "questionType": "SINGLE",
             "text": "Who will win the match?",
             "hint": "",
             "questionDetails":{
                 "topLeftHeader":None,
                 "topRightHeader":None,
                 "middleHeader":None,
                 "homeTeamName":None,
                 "homeTeamSvg":{"originalname":""},
                 "awayTeamName":None,
                 "awayTeamSvg":{"originalname":""},
                 "channelSvg":{"originalname":""},
                 "description":None,
                 "signposting":"Question 1 of 4"},
                 "titleLength":{"isValid":True},
             "nextQuestions": {
                 "123": {"id": "123", "answers": [
                     {"id": "21",
                      "text": "De Bruyne (MCI) or Foden (MCI)",
                      "correctAnswer": False,
                      "nextQuestionId": "234",
                      "questionAskedId": "123",
                      "selectionId": None,
                      "endPage": None
                      },
                     {"id": "22",
                      "text": "Werner (CHE) or Mount (CHE)",
                      "correctAnswer": False,
                      "nextQuestionId": "234",
                      "questionAskedId": "123",
                      "selectionId": None,
                      "endPage": None
                      },
                     {"id": "23",
                      "text": "Sterling (MCI) or Gundogan (MCI)",
                      "correctAnswer": False,
                      "nextQuestionId": "234",
                      "questionAskedId": "123",
                      "selectionId": None,
                      "endPage": None
                      },
                     {"id": "24",
                      "text": "Ziyech (CHE) or Jorginho (CHE)",
                      "correctAnswer": False,
                      "nextQuestionId": "234",
                      "questionAskedId": "123",
                      "selectionId": None,
                      "endPage": None
                      },
                     {"id": "25",
                      "text": "Anyone Else or Own Goal",
                      "correctAnswer": False,
                      "nextQuestionId": "234",
                      "questionAskedId": "123",
                      "selectionId": None,
                      "endPage": None
                      }],
                 "titleLength": {"isValid": True},
                 "questionType": "SINGLE",
                 "text": "Who will score the first goal? ", "hint": "",
                 "questionDetails":{
                     "topLeftHeader":None,
                     "topRightHeader":None,
                     "middleHeader":None,
                     "homeTeamName":None,
                     "homeTeamSvg":{"originalname":""},
                     "awayTeamName":None,
                     "awayTeamSvg":{"originalname":""},
                     "channelSvg":{"originalname":""},
                     "description":None,
                     "signposting":"Question 2 of 4"},
                     "titleLength":{"isValid":True},
                 "nextQuestions": {"234": {
                                   "id": "234", "answers": [
                                  {"id": "31",
                                   "text": "0-7",
                                   "correctAnswer": False,
                                   "nextQuestionId": "345",
                                   "questionAskedId": "234",
                                   "selectionId": None,
                                   "endPage": None
                                   },
                                  {
                                   "id": "32",
                                   "text": "8-9",
                                   "correctAnswer": False,
                                   "nextQuestionId": "345",
                                   "questionAskedId": "234",
                                   "selectionId": None,
                                   "endPage": None
                                  },
                                  {"id": "33",
                                   "text": "10-11",
                                   "correctAnswer": False,
                                   "nextQuestionId": "345",
                                   "questionAskedId": "234",
                                   "selectionId": None,
                                   "endPage": None
                                   },
                                  {"id": "34",
                                   "text": "12-13",
                                   "correctAnswer": False,
                                   "nextQuestionId": "345",
                                   "questionAskedId": "234",
                                   "selectionId": None,
                                   "endPage": None
                                   },
                                  {"id": "35",
                                   "text": "14+",
                                   "correctAnswer": False,
                                   "nextQuestionId": "345",
                                   "questionAskedId": "234",
                                   "selectionId": None,
                                   "endPage": None
                                   }],
                     "titleLength": {"isValid": True},
                     "questionType": "SINGLE",
                     "text": "How many corners will there be?", "hint": "",
                     "questionDetails":{
                         "topLeftHeader":None,
                         "topRightHeader":None,
                         "middleHeader":None,
                         "homeTeamName":None,
                         "homeTeamSvg":{"originalname":""},
                         "awayTeamName":None,
                         "awayTeamSvg":{"originalname":""},
                         "channelSvg":{"originalname":""},
                         "description":None,
                         "signposting":"Question 3 of 4"},
                         "titleLength":{"isValid":True},
                     "nextQuestions": {"345": {
                         "id": "345",
                         "answers": [
                             {"id": "41",
                              "text": "0-1",
                              "correctAnswer": False,
                              "questionAskedId": "345",
                              "selectionId": None,
                              "endPage": None
                              },
                             {"id": "42",
                              "text": "2",
                              "correctAnswer": False,
                              "questionAskedId": "345",
                              "selectionId": None,
                              "endPage": None
                              },
                             {"id": "43",
                              "text": "3",
                              "correctAnswer": False,
                              "questionAskedId": "345",
                              "selectionId": None,
                              "endPage": None
                              },
                             {"id": "44",
                              "text": "4",
                              "correctAnswer": False,
                              "questionAskedId": "345",
                              "selectionId": None,
                              "endPage": None
                              },
                             {"id": "45",
                              "text": "5+",
                              "correctAnswer": False,
                              "questionAskedId": "345",
                              "selectionId": None,
                              "endPage": None
                              }],
                         "titleLength": {"isValid": True},
                         "questionType": "SINGLE",
                         "text": "How many players will be carded?",
                         "hint": "",
                         "questionDetails":{
                             "topLeftHeader":None,
                             "topRightHeader":None,
                             "middleHeader":None,
                             "homeTeamName":None,
                             "homeTeamSvg":{"originalname":""},
                             "awayTeamName":None,
                             "awayTeamSvg":{"originalname":""},
                             "channelSvg":{"originalname":""},
                             "description":None,
                             "signposting":"Question 4 of 4"},
                             "titleLength":{"isValid":True},
                         "nextQuestions": {}}}}}}}},
                     "displayFrom": kwargs.get("display_from"),
                     "displayTo": kwargs.get("display_to"),
                     "entryDeadline":  kwargs.get("dead_line"),
                     "active": kwargs.get("quiz_state", True),
                     "quizLogoSvg": {},
                     "quizBackgroundSvg": {},
                     "splashPage": kwargs.get("splash_page"),
                     "qeQuickLinks":kwargs.get("quick_links"),
                     "quizLoginRule": kwargs.get("login_rule", "START"),
                     "defaultQuestionsDetails": {"topLeftHeader": "Top left header", "topRightHeader": "Top right header",
                                                 "middleHeader": "Middle header", "homeTeamName": "Home Team Name",
                                                 "homeTeamSvg": {}, "awayTeamName": "Away Team Name", "awayTeamSvg": {},
                                                 "channelSvg": {}, "description": "Description", "signposting": "Signposting"},
                     "upsell": {
                         "options": {
                             "11;21": kwargs.get("selection_1", None)
                         },
                         "defaultUpsellOption": 3,
                         "fallbackImage": None,
                         "imageUrl": ""
                          },
                     "endPage": kwargs.get("end_page"),
                     "submitPopup": {"icon": {}, "header": "Confirm your selections",
                                     "description": "Don't forget, once you hit submit you can't go back",
                                     "submitCTAText": "Submit", "closeCTAText": "Go back and edit"},
                     "exitPopup": {"icon": {}, "header": "Are you sure you want to leave?",
                                   "description": "Leaving the quiz now will mean your answers will not be submitted",
                                   "submitCTAText": "Keep Playing", "closeCTAText": "Yes, I want to leave"},
                     "correctAnswersPrizes": [
                         {"correctSelections": 0, "prizeType": kwargs.get("submit_prize_type", "NONE"),
                          "amount": kwargs.get("submit_amount", 0), "currency": "£",
                          "promotionId": kwargs.get("submit_promotion_id", "")},
                         {"correctSelections": 1, "prizeType": kwargs.get("1st_prize_type", "NONE"),
                          "amount": kwargs.get("1st_amount", 0), "currency": "£",
                          "promotionId": kwargs.get("1st_promotion_id", "")},
                         {"correctSelections": 2, "prizeType": kwargs.get("2nd_prize_type", "NONE"),
                          "amount": kwargs.get("2nd_amount", 0), "currency": "£",
                          "promotionId": kwargs.get("2nd_promotion_id", "")},
                         {"correctSelections": 3, "prizeType": kwargs.get("3rd_prize_type", "NONE"),
                          "amount": kwargs.get("3rd_amount", 0), "currency": "£",
                          "promotionId": kwargs.get("3rd_promotion_id", "")},
                         {"correctSelections": 4, "prizeType": kwargs.get("4th_prize_type", "NONE"),
                          "amount": kwargs.get("4th_amount", 0), "currency": "£",
                          "promotionId": kwargs.get("4th_promotion_id", "")},
                     ],
                     "eventDetails": {"eventId": kwargs.get("event_id", None),
                                      "eventName": kwargs.get("event_name", None),
                                      "startTime": kwargs.get("start_time", None),
                                      "actualScores": kwargs.get("actual_scores", []),
                                      "liveNow": kwargs.get("live_now", False)},
                     "quizConfiguration": {"showSubmitPopup": kwargs.get("show_submit_popup", True),
                                           "showExitPopup": kwargs.get("show_exit_popup", True),
                                           "showSplashPage": kwargs.get("show_splash_page" ,True),
                                           "showEventDetails": kwargs.get("show_event_details", True),
                                           "showProgressBar": kwargs.get("show_progress_bar", True),
                                           "showQuestionNumbering": kwargs.get("show_question_numbering", True),
                                           "showSwipeTutorial": kwargs.get("show_swipe_tutorial", True),
                                           "useBackButtonToExitAndHideXButton": kwargs.get(
                                           "use_back_button_to_exit_and_hide_x_button", True),
                                           "showPreviousAndLatestTabs": kwargs.get("show_previous_and_latest_tabs", True)},
                     "isChanged": True,
                     "notValid": False,
                     "coin": kwargs.get("coin_config",None)
                     }
        data = json.dumps(parameters)
        quiz_page = self.request.put('question-engine/'+quiz_id, data=data)
        return quiz_page

    def create_question_engine_quiz(self, **kwargs):
        """
        @param kwargs:
        @return: returns quiz dictionary object
        """
        now = kwargs.get("now")
        time_format = kwargs.get("time_format")
        displayFrom = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False, hours=-6,
                                              minutes=-1)[:-3] + 'Z'
        displayTo = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False, hours=-3,
                                            days=1)[:-3] + 'Z'
        deadline = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False, hours=-3,
                                           seconds=-1, days=1)[:-3] + 'Z'

        splash_pages = self.get_qe_splash_page()
        splash_page_exits = [module for module in splash_pages if module.get('title') == "Autotest_Splash_Page"]
        splash_page = splash_page_exits[0] if splash_page_exits else self.create_question_engine_spalsh_page(**kwargs)

        quick_link_pages = self.get_qe_quick_link_pages()
        quick_link_page_exits = [module for module in quick_link_pages if module.get('title') == "Autotest_Quick_Links"]
        quick_links = quick_link_page_exits[0] if quick_link_page_exits else self.create_question_enigne_quick_links()

        end_pages = self.get_qe_end_pages()
        end_pages_exits = [module for module in end_pages if module.get('title') == "Autotest_End_Page"]
        end_page = end_pages_exits[0] if end_pages_exits else self.create_question_engine_end_page(**kwargs)

        parameters = {"sourceId":"/footballsuperseries",
                      "splashPage":splash_page,
                      "qeQuickLinks":quick_links,
                      "displayFrom":displayFrom,
                      "displayTo":displayTo,
                      "entryDeadline":deadline,
                      "firstQuestion":None,
                      "id":"",
                      "active":True,
                      "quizLoginRule":"START",
                      "title":self.auto_test_quiz_name,
                      "notValid":False,
                      "brand":self.brand,
                      "isChanged":False,
                      "upsell":None,
                      "endPage":end_page,
                      "quizLogoSvg":{},"quizBackgroundSvg":{},"defaultQuestionsDetails":{},
                      "submitPopup":{},"exitPopup":{},"correctAnswersPrizes":[],
                      "eventDetails":{},"highlighted":False,"quizConfiguration":{}}
        data = json.dumps(parameters)
        quiz_page = self.request.post('question-engine', data=data)
        quiz_page_param = namedtuple('quiz_page_qe', ['title', 'id'])
        quiz_page_params = quiz_page_param(quiz_page['title'], quiz_page['id'])
        self._logger.info('*** Added end page {quiz_page_params}'.format(quiz_page_params=quiz_page_params))
        updated_quiz = self.update_question_engine_quiz(quiz_id=quiz_page_params.id, title=quiz_page_params.title,
                                                        display_from=displayFrom,
                                                        display_to=displayTo, dead_line=deadline,
                                                        splash_page=splash_page,
                                                        quick_links=quick_links, end_page=end_page, **kwargs)
        self._created_question_engine_quiz.append(updated_quiz.get('id'))
        return updated_quiz

    def check_update_and_create_question_engine_quiz(self, **kwargs):
        """
        @param kwargs:
        @return: creates the quiz and returns quiz dict
        """
        active_autotest = None
        flag = False
        now = datetime.now()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        all_quizzes = self.get_qe_quizzes()
        active_quizzes = [module for module in all_quizzes if module.get('active') == True and
                module.get('displayFrom') <= datetime.utcnow().isoformat() <= module.get('displayTo')]

        for quiz in active_quizzes:
            if quiz['title'] != 'Automation_QE_DONT_EDIT_DELETE':
                quiz['active'] = False
                self.update_question_engine_quiz(quiz_id=quiz['id'], title=quiz['title'], payload=quiz)
            else:
                flag = True
                active_autotest = quiz
        if flag:
            return active_autotest
        # else: # not able to change of date old quiz
        #     quizzes = [module for module in all_quizzes if module.get('title') == 'Autotest_Quiz']
        #     if quizzes:
        #         quiz = quizzes[0]
        #         quiz['active'] = True
        #         quiz['displayTo'] = \
        #             get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False, hours=-3,
        #                                         days=1)[:-3] + 'Z'
        #         quiz['entryDeadline'] = \
        #             get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False, hours=-1,
        #                                           minutes=-1)[:-3] + 'Z'
        #         updated_quiz = self.update_question_engine_quiz(quiz_id=quiz['id'], title=quiz['title'], payload=quiz)
        #         return updated_quiz

        created_quiz = self.create_question_engine_quiz(now=now, time_format=time_format)
        return created_quiz

    def create_five_a_side_show_down(self, contest_name, entryStake=1,**kwargs):
        """
        param contest_name: contest_name
        @return: creates the contest and returns contest data
        """
        path = f'contest'
        data = {
            "id": "",
            "brand": self.brand,
            "name": contest_name,
            "startDate": get_date_time_as_string(time_format='%Y-%m-%dT%H:%M:%SZ', url_encode=False),
            "event": kwargs.get("event_id", ""),
            "description": kwargs.get("description", ""),
            "entriesSize": kwargs.get("entriesSize", ""),
            "entryConfirmationText": kwargs.get("entryConfirmationText", ""),
            "nextContestId": kwargs.get("nextContestId", ""),
            "entryStake": kwargs.get("entryStake", entryStake),
            "maxEntries": kwargs.get("size", ""),
            "maxEntriesPerUser": kwargs.get("teams", ""),
            "description": kwargs.get("description", ""),
            "display": kwargs.get("display", True),
            "realAccount": False,
            "testAccount": True,
            "isInvitationalContest": kwargs.get("isInvitationalContest", False),
            "isPrivateContest": kwargs.get("isPrivateContest", False)
        }
        data = json.dumps(data)
        response = self.request.post(path, data=data)
        self.update_five_a_side_show_down(response['id'],  **kwargs)
        self._created_five_a_side_show_down.append(response.get('id'))
        return response

    def update_five_a_side_show_down(self, contest_id, **kwargs):
        """
        param contest_name: contest_name
        @return: update the contest and returns contest data
        """
        contest = self.get_five_a_side_show_down_contest(contest_id)
        path = f'contest/' + contest_id
        data = {
            "id": contest_id,
            "brand": self.brand,
            "name": contest['name'],
            "startDate": kwargs.get("startDate", contest['startDate']),
            "utcStartDate" : contest['startDate'],
            "event": kwargs.get("event_id", contest['event']),
            "description": kwargs.get("description", contest['description']),
            "entriesSize": kwargs.get("entriesSize", contest['entriesSize']),
            "entryConfirmationText": kwargs.get("entryConfirmationText", contest['entryConfirmationText']),
            "nextContestId": kwargs.get("nextContestId", contest['nextContestId']),
            "entryStake": kwargs.get("entryStake", contest['entryStake']),
            "maxEntries": kwargs.get("size",  contest.get('maxEntries')),
            "maxEntriesPerUser": kwargs.get("teams",  contest.get('maxEntriesPerUser')),
            "description": kwargs.get("description", contest['description']),
            "display": kwargs.get("display", contest['display']),
            "realAccount": False,
            "testAccount": kwargs.get("testAccount", contest['testAccount']),
            "isInvitationalContest": kwargs.get("isInvitationalContest", contest['isInvitationalContest']),
            "isPrivateContest": kwargs.get("isPrivateContest", contest['isPrivateContest'])
        }
        data = json.dumps(data)
        return self.request.put(path, data=data)

    def get_five_a_side_show_down_contest(self, contestId) -> list:
        """
         : return the contest
        """
        path = f'contest/{contestId}'
        return self.request.get(path)

    def delete_five_a_side_show_down(self, contestId):
        """
        param contestId: contestId
        return: deleting the contest
        """
        path = f'contest/{contestId}'
        return self.request.delete(path, parse_response=False)

    def get_show_down_overlay(self) -> list:
        """
         : return the show down overlay
        """
        path = f'overlay/brand/{self.brand}'
        return self.request.get(path)

    def enable_disable_show_down_overlay(self, enabled=True):
        """
        param enabled: enabled
        return: show down overlay data
        """
        overlay = self.get_show_down_overlay()
        path = f'overlay/' + overlay['id']
        overlay.update({'overlayEnabled': enabled})
        data = json.dumps(overlay)
        return self.request.put(path, data=data)

    #Free Ride
    def get_freeride_splash_page(self):
        """
        return: splash page data
        """
        path = 'freeride/splashpage/brand/%s' % self.brand
        return self.request.get(path)

    def get_freeride_campaigns(self) -> list:
        """
        return: list of free ride campaigns
        """
        path = 'freeride/campaign/brand/%s' % self.brand
        return self.request.get(path)

    def get_freeride_campaign_details(self,freeride_campaignid):
        """
        param freeride_campaignid: free ride campaign Id
        return: campaign id details
        """
        path = f'freeride/campaign/{freeride_campaignid}'
        return self.request.get(path)

    def check_update_and_create_freeride_campaign(self, **kwargs):
        """
        return: freeride active campaign id
        """
        now = datetime.now()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        all_campaigns = self.get_freeride_campaigns()
        non_active_freeride_campaign=[module for module in all_campaigns if (module.get('isPotsCreated') == False and
        int(module.get('displayFrom').split('-')[2].split('T')[0]) == datetime.strptime(str(datetime.utcnow().isoformat()), time_format).day) or
                                      (module.get('isPotsCreated') == True and
                                       module.get('displayFrom')> datetime.utcnow().isoformat() and
                                       int(module.get('displayTo').split('-')[2].split('T')[0]) == datetime.strptime(str(datetime.utcnow().isoformat()), time_format).day
                                       ) or (module.get('isPotsCreated') == True and
                                       module.get('displayTo')< datetime.utcnow().isoformat() and
                                       int(module.get('displayTo').split('-')[2].split('T')[0]) == datetime.strptime(str(datetime.utcnow().isoformat()), time_format).day
                                       ) ]
        if non_active_freeride_campaign:
           for freeride_campaignid in non_active_freeride_campaign:
                self.delete_freeride_campaign(freeride_campaignid['id'])

        all_campaigns = self.get_freeride_campaigns()
        active_freeride_campaign = [module for module in all_campaigns if module.get('isPotsCreated') == True and
                                    int(module.get('displayTo').split('-')[2].split('T')[0]) == datetime.strptime(str(datetime.utcnow().isoformat()), time_format).day]

        if active_freeride_campaign:
            return active_freeride_campaign[0]['id']

        created_quiz = self.create_free_ride_campaign(now=now, time_format=time_format)
        return created_quiz

    def create_free_ride_campaign(self, **kwargs):
        """
        param kwargs:
        return: returns Created Free Ride campaign
        """
        now = kwargs.get("now")
        time_format = kwargs.get("time_format")
        displayFrom = datetime.utcnow().isoformat()[:-3] + 'Z'
        displayTo = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False, hours=-2,
                                            minutes=+40)[:-3] + 'Z'

        path = f'freeride/campaign'
        data = {
            "name": "Auto_Test_Freeride_Campaign",
            "displayFrom": kwargs.get("displayFrom", displayFrom ),
            "displayTo": kwargs.get("displayTo", displayTo ),
            "openBetCampaignId": "111",
            "optimoveId": "111",
            "id": "",
            "brand": self.brand
        }
        data = json.dumps(data)
        response = self.request.post(path, data=data)
        questions_response = self.update_freeride_questions(response.get('id'), **kwargs)
        createpots_response = self.create_pots(questions_response.get('id'))
        if createpots_response['message']=='Pots created successfully':
             return questions_response.get('id')
        else:
            raise CMSException("pots not created")

    def update_freeride_questions(self,freeride_campaignid, **kwargs):
        """
        param freeride_campaign_id:
        param kwargs:
        return: returns campaign questions data and related spotlight events data
        """
        now = kwargs.get("now")
        time_format = kwargs.get("time_format")
        events_reponse=" "
        for x in range(0, 3):
              refreshEventsFrom = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False, hours=-6,
                                              minutes=-1, days=x)[:-3] + 'Z'
              events_reponse = self.spotlight_related_events(class_id='223', refreshEventsFrom=refreshEventsFrom)
              if len(events_reponse['typeEvents'])!=0:
                  break
        if events_reponse['typeEvents'] is None:
            raise CMSException("No events Found")

        events_len= len([events_reponse['typeEvents'][0]['events']][0])
        data=[]
        for i in range(len([events_reponse['typeEvents'][0]['events']][0])):
           data.append({"id": events_reponse['typeEvents'][0]['events'][i]['id'], "name": events_reponse['typeEvents'][0]['events'][i]['name']})

        marketplace=[{"typeId": events_reponse['typeEvents'][0]['typeId'], "typeName": events_reponse['typeEvents'][0]['typeName'] ,"events":data}]

        response=self.get_freeride_campaign_details(freeride_campaignid=freeride_campaignid)

        path= f'freeride/campaign/{freeride_campaignid}/false'
        data={
            "id": freeride_campaignid,
            "name": response.get('name'),
            "brand": self.brand,
            "displayFrom": response.get('displayFrom'),
            "displayTo": response.get('displayTo'),
            "openBetCampaignId": response.get('openBetCampaignId'),
            "optimoveId": response.get('optimoveId'),
            "isPotsCreated": False,
            "questionnarie": {
                "questions": [
                    {
                        "questionId": 1,
                        "quesDescription": "How highly rated do you want your horse to be?",
                        "chatBoxResp": "That's an interesting choice!",
                        "options": [
                            {
                                "optionId": 1,
                                "optionText": "Top player"

                            },
                            {
                                "optionId": 2,
                                "optionText": "Dark horse"
                            },
                            {
                                "optionId": 3,
                                "optionText": "Surprise me!"
                            }
                        ]
                    },
                    {
                        "questionId": 2,
                        "quesDescription": "In terms of size, what sort of horse do you prefer to back?",
                        "chatBoxResp": "I wasn't expecting that!",
                        "options": [
                            {
                                "optionId": 4,
                                "optionText": "Big & Strong"
                            },
                            {
                                "optionId": 5,
                                "optionText": "Small & Nimble"
                            },
                            {
                                "optionId": 6,
                                "optionText": "Surprise me!"
                            }
                        ]
                    },
                    {
                        "questionId": 3,
                        "quesDescription": "What length odds are you interested in?",
                        "chatBoxResp": "That's a great choice",
                        "options": [
                            {
                                "optionId": 7,
                                "optionText": "Good Chance"
                            },
                            {
                                "optionId": 8,
                                "optionText": "Nice Price"
                            },
                            {
                                "optionId": 9,
                                "optionText": "Surprise me!"
                            }
                        ]
                    }
                ],
                "summaryMsg": "Let's go over your selections again",
                "welcomeMessage": "Welcome to Free Ride. Answer three simple questions and we'll place a £1 bet for you on this afternoon's Cheltenham card",
                "horseSelectionMsg": "Here we go! We've PLACED a £1 FREE BET on this horse for you. Click on the link below to go to the racecard. Good luck!"
            },
            "eventClassInfo": {"categoryId": 21, "classId": 223, "marketPlace": marketplace}

        }
        data = json.dumps(data)
        response = self.request.put(path, data=data)
        return response

    def create_pots(self,freeride_campaignid):
        """
        param freeride_campaignid:
        return: get successfull message for pots creation
        """
        path=f'freeride/campaign/createpots/{freeride_campaignid}'
        return self.request.get(path)

    def delete_freeride_campaign(self, freeride_campaignid) -> None:
        """
        param freeride_campaignid: specifies id of free ride campaign which should be removed
        """
        path = f'freeride/campaign/brand/ladbrokes/{freeride_campaignid}'
        self.request.delete(path,parse_response=False)

    def get_pots(self, freeride_campaignid):
        """
        param freeride_campaignid:
        returns pots data for the given campaign id
        """
        path = f'freeride/campaign/viewpots/brand/{self.brand}/{freeride_campaignid}'
        return self.request.get(path)

    def get_lucky_dip_configuration(self):
        """
        returns lucky dip description
        """
        path = f'luckydip/brand/{self.brand}'
        return self.request.get(path)

    def update_lucky_dip_configuration(self, **kwargs):
        """
        Method used to update lucky dip fields in CMS
        :param Kwargs: ID for Featured module
        :param kwargs: data parameter if needed to be modified
        :return: Updated object with all information about just updated Featured module (id, title, etc)
        """
        luckdip_config = self.get_lucky_dip_configuration()
        path = f'luckydip/' + luckdip_config['id']
        data = {
            "id": luckdip_config['id'],
            "createdBy": luckdip_config['createdBy'],
            "createdByUserName": luckdip_config['createdByUserName'],
            "updatedBy": luckdip_config['updatedBy'],
            "updatedByUserName": luckdip_config['updatedByUserName'],
            "createdAt": luckdip_config['createdAt'],
            "updatedAt": luckdip_config['updatedAt'],
            "brand": self.brand,
            "luckyDipBannerConfig": {
                "animationImgPath": kwargs.get("animationImgPath",
                                               luckdip_config['luckyDipBannerConfig']['animationImgPath']),
                "bannerImgPath": kwargs.get("bannerImgPath", luckdip_config['luckyDipBannerConfig']['bannerImgPath']),
                "overlayBannerImgPath": kwargs.get("overlayBannerImgPath",
                                                   luckdip_config['luckyDipBannerConfig']['overlayBannerImgPath']),
            },
            "luckyDipFieldsConfig": {
                "title": kwargs.get("title", luckdip_config['luckyDipFieldsConfig']['title']),
                "desc": kwargs.get("desc", luckdip_config['luckyDipFieldsConfig']['desc']),
                "welcomeMessage": kwargs.get("welcomeMessage",
                                             luckdip_config['luckyDipFieldsConfig']['welcomeMessage']),
                "betPlacementTitle": kwargs.get("betPlacementTitle",
                                                luckdip_config['luckyDipFieldsConfig']['betPlacementTitle']),
                "betPlacementStep1": kwargs.get("betPlacementStep1",
                                                luckdip_config['luckyDipFieldsConfig']['betPlacementStep1']),
                "betPlacementStep2": kwargs.get("betPlacementStep2",
                                                luckdip_config['luckyDipFieldsConfig']['betPlacementStep2']),
                "betPlacementStep3": kwargs.get("betPlacementStep3",
                                                luckdip_config['luckyDipFieldsConfig']['betPlacementStep3']),
                "termsAndConditionsURL": kwargs.get("termsAndConditionsURL",
                                                    luckdip_config['luckyDipFieldsConfig']['termsAndConditionsURL']),
                "playerCardDesc": kwargs.get("playerCardDesc",
                                             luckdip_config['luckyDipFieldsConfig']['playerCardDesc']),
                "potentialReturnsDesc": kwargs.get("potentialReturnsDesc",
                                                   luckdip_config['luckyDipFieldsConfig']['potentialReturnsDesc']),
                "placebetCTAButton": kwargs.get("placebetCTAButton",
                                                luckdip_config['luckyDipFieldsConfig']['placebetCTAButton']),
                "backCTAButton": kwargs.get("backCTAButton", luckdip_config['luckyDipFieldsConfig']['backCTAButton']),
                "gotItCTAButton": kwargs.get("gotItCTAButton",
                                             luckdip_config['luckyDipFieldsConfig']['gotItCTAButton']),
                "depositButton": kwargs.get("depositButton", luckdip_config['luckyDipFieldsConfig']['depositButton'])
            }
        }
        data = json.dumps(data)
        response = self.request.put(path, data=data)
        return response

    #Lotto

    def get_lotto_main_page_configuration(self):
        """
        return: lotto page data
        """
        path = f'lotto-config/brand/{self.brand}'
        return self.request.get(path)

    def get_lotto_lottery_config(self, lottery_id=None):
        """
        return : Returns lottery configuration data
        """

        path = f'lotto-config/{lottery_id}'
        return self.request.get(path)

    def update_lotto_lottery_cnfig(self, lottery_id=None, **kwargs):
        """
        Method used to update lotto fields in CMS
        :param Kwargs: ID for lotto_config
        :param kwargs: data parameter if needed to be modified
        :return: Updated object with all information about just updated lotto_config (id, title, etc)
        """
        path = f'lotto-config/{lottery_id}'
        lottery_response =self.get_lotto_lottery_config(lottery_id=lottery_id)
        for key in lottery_response.keys():
            if key in kwargs:
                lottery_response[key] = kwargs[key]
        data = json.dumps(lottery_response)
        request = self.request.put(path, data=data)
        return request

    # Fanzone
    def get_fanzones(self) -> list:
        """
        returns list of fanzones
        """
        path = f'{self.brand}/fanzone'
        return self.request.get(path)

    def get_fanzone_syc(self):
        """
        return fanzone show your colours popup data
        """
        path = f'{self.brand}/fanzone-syc'
        return self.request.get(path)

    def get_fanzone_club(self) -> list:
        """
        return list of fanzone clubs
        """
        path = f'{self.brand}/fanzone-club'
        return self.request.get(path)

    def get_fanzone_preference_center(self):
        """
        return fanzone preference center data
        """
        path = f'{self.brand}/fanzone-preference-center'
        return self.request.get(path)

    def get_fanzone(self, fanzone_name):
        """
        @param: fanzone eg:Arsenal
        return respective fanzone data eg: Arsenal,Astonvilla response
        """
        fanzone_id = " "
        fanzone_list = self.get_fanzones()
        for fanzone in range(len(fanzone_list)):
            if fanzone_list[fanzone]['name'] == fanzone_name:
                fanzone_id = fanzone_list[fanzone]['id']
                break
        path = f'{self.brand}/fanzone/id/{fanzone_id}'
        return self.request.get(path)

    def update_fanzone(self, fanzone_name, active=True, **kwargs):
        """
        @param fanzone_name:eg:Everton,Brighton
        @param typeId:specifies typeId of the league
        @param active: To make fanzone active
        @return updated fanzone response
        """
        response = self.get_fanzone(fanzone_name)
        typeId = kwargs.get('typeId', response['primaryCompetitionId'])
        if typeId not in response['primaryCompetitionId']:
            if typeId not in response['secondaryCompetitionId']:
                response['secondaryCompetitionId'] = response['secondaryCompetitionId'] + ',' + typeId
        path = f'{self.brand}/fanzone/id/' + response['id']
        for key in kwargs:
            if key in response and kwargs[key] != response[key]:
                response[key] = kwargs[key]
            elif key in response['fanzoneConfiguration'].keys() and kwargs[key] != response['fanzoneConfiguration'][
                key]:
                response['fanzoneConfiguration'][key] = kwargs[key]
        data = json.dumps(response)
        response = self.request.put(path, data=data)
        return response

    def _change_fanzone_promotion_description(self, description: str, fanzone_config_status: bool, **kwargs) -> str:
        """
        Change the fanzone promotion description based on the fanzone configuration status.
        don't use change_fanzone_promotion_description directly, use update_fanzone_SYC_Url

        Args:
            description (str): The original fanzone promotion description.
            fanzone_config_status (bool): The status of the fanzone configuration.

        Returns:
            str: The modified fanzone promotion description.
        """
        modified_html_string_description = description
        if fanzone_config_status:
            tree = fromstring(description)
            # Select the anchor tag with the text "Show Your Colours"
            a_tag = tree.xpath('//a[text()="Show Your Colours"]')[0]
            # Change the href attribute
            a_tag.attrib['href'] = kwargs.get(uri, 'fanzone/sport-football/show-your-colours')
            # Verify changes
            modified_html_string_description = tostring(tree, pretty_print=True, method='html').decode()
        else:
            # if fanzone_config_status is False, Show Your Colours Should Redirect to vacation
            tree = fromstring(description)
            # Select the anchor tag with the text "Show Your Colours"
            a_tag = tree.xpath('//a[text()="Show Your Colours"]')[0]
            # Change the href attribute
            a_tag.attrib['href'] = kwargs.get(uri, 'fanzone/sport-football/vacation')
            # Verify changes
            modified_html_string_description = tostring(tree, pretty_print=True, method='html').decode()
        return modified_html_string_description

    def update_fanzone_SYC_Url(self, title: str, fanzone_status, **kwargs):
        """
            Change the fanzone promotion description based on the fanzone configuration status.

            Args:
                title (str): The original fanzone promotion description.
                fanzone_status (bool): The status of the fanzone configuration.
        """
        fanzone_config_status = fanzone_status
        promotions = self.get_promotion_by_name(title=title)
        fanzone_promotion_description = promotions['description']
        modified_description = self._change_fanzone_promotion_description(description=fanzone_promotion_description,
                                                                          fanzone_config_status=fanzone_config_status,
                                                                          **kwargs)
        self.update_promotion(promotion_id=promotions['id'], description=modified_description)

    def get_sport_categories_fanzone(self):
        """
        return fanzone response from sports category
        """
        fanzone_category = " "
        for category in self.get_sport_categories():
            if category['imageTitle'] == "Fanzone":
                fanzone_category = category
                return category
        if fanzone_category is " ":
            raise CMSException("Fanzone sport category is not configured in CMS")

    def add_fanzone_surface_bet(self, selection_id: (str, int), **kwargs) -> dict:
        """
         Creates Surface bet
        :param selection_id: selection ID for Surface bet
        :Kwargs: prices num and price den value passing if required
        :return: object with all information about just created Surface Bet (id, title, etc)
        """
        all_fanzones = self.get_fanzones()
        fanzone_teamIds = []
        if kwargs.get("fanzone_teams"):
            for team in kwargs.get("fanzone_teams"):
                teamID= next((fanzone['teamId'] for fanzone in all_fanzones if fanzone['name'].upper() == team.upper()),None)
                if teamID:
                    fanzone_teamIds.append(teamID)
                else:
                    raise CMSException(f'team name which is sent"{team}" is not available')
        else:
            for fanzone in all_fanzones:
                fanzone_teamIds.append(fanzone['teamId'])
        fanzone_categories = self.get_sport_categories_fanzone()
        now = datetime.utcnow()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        displayFrom = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False, hours=-3,
                                              minutes=-1)[:-3] + 'Z'
        displayTo = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False, hours=-3,
                                            days=1)[:-3] + 'Z'
        price_num = kwargs.get('priceNum', fake.random_int(min=1, max=50))
        price_num = int(price_num) if price_num else None
        price_den = kwargs.get('priceDen', fake.random_int(min=51, max=99))
        price_den = int(price_den) if price_den else None
        content_header = kwargs.get('contentHeader', 'Fanzone Surface Bet Header')
        svg_icon = kwargs.get('svg_icon', None)
        svg_bg_id = kwargs.get('svg_bg_id', None)
        svg_bg_image = kwargs.get('svg_bg_image', None)
        data = {
            "content": fake.paragraph(),
            "contentHeader": content_header,
            "disabled": False,
            "title": f'Auto {fake.name_female()}',
            "displayFrom": displayFrom,
            "displayTo": displayTo,
            "eventIDs": [],
            "selectionId": selection_id,
            "categoryIDs": fanzone_categories['categoryId'],
            "fanzoneInclusions": fanzone_teamIds,
            "sortOrder": None,
            'svgId': svg_icon,
            "svg": None,
            "svgFilename": None,
            "svgBgId": svg_bg_id,
            "svgBgImgPath": svg_bg_image,
            "price": {
                'priceDec': None,
                'priceDen': price_den,
                'priceNum': price_num,
                'priceType': None
            },
            "references": [],
            "highlightsTabOn": False,
            "edpOn": False,
            "displayOnDesktop": False,
            "exclusionList": [],
            "inclusionList": [],
            "universalSegment": True,
            "id": None,
            "brand": self.brand,
        }
        global_references = []
        if kwargs.get('eventIDs'):
            references = [{
                'enabled': True,
                'refId': event_id,
                'relatedTo': 'edp'
            } for event_id in kwargs.get('eventIDs')]
            references += [{
                'refId': fanzone_categories['categoryId'],
                'relatedTo': 'sport',
                'enabled': True}]
        else:
            references = [{
                'refId': fanzone_categories['categoryId'],
                'relatedTo': 'sport',
                'enabled': True}]
        global_references = references
        kwargs['references'] = global_references
        data.update(kwargs) if kwargs else data
        data = json.dumps(data)
        surface_bet = self.request.post('surface-bet', data=data)
        self._created_surface_bets.append(surface_bet.get('id'))
        return surface_bet

    def get_fanzone_highlight_carousels(self,segment='Universal') -> dict:
        """
        Gets all highlight carousels.
        return: whole highlight carousel object
        """
        fanzone_response = self.get_sport_categories_fanzone()
        path = f'highlight-carousel/brand/{self.brand}/segment/{segment}/sport/' + str(fanzone_response['categoryId'])
        return self.request.get(path)

    def update_fanzone_highlights_carousel(self, type_id):
        """
        @param: typeId specifies the typeId of the league
        return  updated fanzone highlight carousel data
        """
        hightlight_carousel = self.get_fanzone_highlight_carousels()[0]
        if type_id not in hightlight_carousel['typeIds']:
            hightlight_carousel['typeIds'].append(type_id)

        path = f'highlight-carousel/' + hightlight_carousel['id']
        data = {
            "id": hightlight_carousel['id'],
            "createdBy": hightlight_carousel['createdBy'],
            "createdByUserName": hightlight_carousel['createdByUserName'],
            "updatedBy": hightlight_carousel['updatedBy'],
            "updatedByUserName": hightlight_carousel['updatedByUserName'],
            "createdAt": hightlight_carousel['createdAt'],
            "updatedAt": hightlight_carousel['updatedAt'],
            "sortOrder": hightlight_carousel['sortOrder'],
            "brand": self.brand,
            "pageId": hightlight_carousel['pageId'],
            "pageType": hightlight_carousel['pageType'],
            "disabled": hightlight_carousel['disabled'],
            "segmentReferences": hightlight_carousel['segmentReferences'],
            "exclusionList": hightlight_carousel['exclusionList'],
            "inclusionList": hightlight_carousel['inclusionList'],
            "fanzoneInclusions": hightlight_carousel['fanzoneInclusions'],
            "archivalId": hightlight_carousel['archivalId'],
            "universalSegment": hightlight_carousel['universalSegment'],
            "message": hightlight_carousel['message'],
            "title": hightlight_carousel['title'],
            "displayFrom": hightlight_carousel['displayFrom'],
            "displayTo": hightlight_carousel['displayTo'],
            "limit": hightlight_carousel['limit'],
            "inPlay": hightlight_carousel['inPlay'],
            "typeId": hightlight_carousel['typeId'],
            "typeIds": hightlight_carousel['typeIds'],
            "events": hightlight_carousel['events'],
            "svg": hightlight_carousel['svg'],
            "svgFilename": hightlight_carousel['svgFilename'],
            "svgId": hightlight_carousel['svgId'],
            "sportId": hightlight_carousel['sportId']
        }
        data = json.dumps(data)
        response = self.request.put(path, data=data)
        return response

    def get_sport_category(self, sport_category_id):
        """
        : return the sport category data
        """
        path = f'sport-category/{sport_category_id}'
        return self.request.get(path)

    def create_sport_category(self, title, categoryId, ssCategoryCode, **kwargs):
        """
        param title: Sport title
        param categoryId: Sport categoryId
        param ssCategoryCode: ssCategoryCode
        @return: creates the sport category and returns sport category data
        """
        path = f'sport-category'
        data = {
            "id": "",
            "aggrigatedMarkets": kwargs.get("aggrigatedMarkets", []),
            "alt": kwargs.get("alt", ""),
            "brand":self.brand,
            "tier":kwargs.get("tier", "TIER_2"),
            "categoryId": categoryId,
            "collectionType": kwargs.get("collectionType", ""),
            "disabled": kwargs.get("disabled", False),
            "key": "",
            "lang":"",
            "path":"",
            "spriteClass":"",
            "imageTitle": title,
            "inApp": kwargs.get("inApp", True),
            "isTopSport": kwargs.get("isTopSport", False),
            "link": kwargs.get("link", ""),
            "showInMenu": kwargs.get("showInMenu", False),
            "sortOrder": kwargs.get("sortOrder", 0),
            "scoreBoardUri": kwargs.get("scoreBoardUri", ""),
            "ssCategoryCode": ssCategoryCode,
            "oddsCardHeaderType": kwargs.get("oddsCardHeaderType"),
            "outrightSport": kwargs.get("outrightSport", True),
            "multiTemplateSport": kwargs.get("multiTemplateSport", False),
            "typeIds": kwargs.get("typeIds", 'null'),
            "dispSortNames": kwargs.get("dispSortNames", ""),
            "primaryMarkets": kwargs.get("primaryMarkets", ""),
            "targetUri": kwargs.get("targetUri", "sport/autotest"),
            "showInAZ": kwargs.get("showInAZ", False),
            "showInHome": kwargs.get("showInHome", False),
            "showInPlay": kwargs.get("showInPlay", False),
            "topMarkets": kwargs.get("topMarkets", ""),
            "filename":
                {
                    "filename": kwargs.get("filename", ""),
                    "originalfilename": kwargs.get("originalfilename", ""),
                    "path": kwargs.get("path", ""),
                    "size": kwargs.get("size", 0),
                    "filetype": kwargs.get("filetype", ""),
                },
            "icon":
                {
                    "filename": kwargs.get("filename", ""),
                    "originalfilename": kwargs.get("originalfilename", ""),
                    "path": kwargs.get("path", ""),
                    "size": kwargs.get("size", 0),
                    "filetype": kwargs.get("filetype", ""),
                },
            "hasEvents": kwargs.get("hasEvents", True),
            "showScoreboard": kwargs.get("showScoreboard", False),
            "highlightCarouselEnabled": kwargs.get("highlightCarouselEnabled", False),
            "quickLinkEnabled": kwargs.get("quickLinkEnabled", False),
            "inplayEnabled": kwargs.get("inplayEnabled", False),
            "inplaySportModule":
                {
                    "enabled": kwargs.get("inplaySportModuleEnabled", False),
                    "inplayCount": kwargs.get("inplayCount", 10),
                }
            }
        data = json.dumps(data)
        response = self.request.post(path, data=data)
        self.update_sport_category(response['id'], **kwargs)
        self._created_sport_category.append(response.get('id'))
        return response

    def update_sport_category(self, sport_category_id, **kwargs):
        """
        param Sport Category_id:Sport Category_id
        @return: Update the sport category and returns sport category data
        """
        sport_category = self.get_sport_category(sport_category_id)
        path = f'sport-category/' + sport_category_id
        data = {
            "id": sport_category_id,
            "segmentReferences": kwargs.get("segmentReferences", sport_category.get('segmentReferences', [])),
            "exclusionList": kwargs.get("exclusionList", []),
            "inclusionList": kwargs.get("inclusionList", []),
            "universalSegment": kwargs.get("universalSegment", True),
            "alt": kwargs.get("alt", sport_category.get('alt')),
            "brand": self.brand,
            "categoryId": kwargs.get("categoryId", sport_category.get('categoryId')),
            "disabled": kwargs.get("disabled", sport_category.get('disabled')),
            "tier": kwargs.get("tier", sport_category.get('tier')),
            "filename":
                {
                    "filename": kwargs.get("filename", sport_category['filename']['filename']),
                    "path": kwargs.get("path", sport_category['filename']['path']),
                    "size": kwargs.get("size", sport_category['filename']['size']),
                    "filetype": kwargs.get("filetype", sport_category['filename']['filetype']),
                } if sport_category.get('filename') else None,
            "icon":
                {
                    "filename": kwargs.get("filename", sport_category['icon']['filename']),
                    "path": kwargs.get("path", sport_category['icon']['path']),
                    "size": kwargs.get("size", sport_category['icon']['size']),
                    "filetype": kwargs.get("filetype", sport_category['icon']['filetype']),
                } if sport_category.get('icon') else None,
            "imageTitle": kwargs.get("imageTitle", sport_category.get('imageTitle')),
            "inApp": kwargs.get("inApp", sport_category.get('inApp')),
            "isTopSport": kwargs.get("isTopSport", sport_category.get('isTopSport')),
            "key": kwargs.get("key", sport_category.get('key')),
            "lang": kwargs.get("lang", sport_category.get('lang')),
            "link": kwargs.get("link", sport_category.get('link')),
            "outrightSport": kwargs.get("outrightSport", sport_category.get('outrightSport')),
            "multiTemplateSport": kwargs.get("multiTemplateSport", sport_category.get('multiTemplateSport')),
            "oddsCardHeaderType": kwargs.get("oddsCardHeaderType", sport_category.get('oddsCardHeaderType')),
            "typeIds": kwargs.get("typeIds", sport_category.get('typeIds')),
            "dispSortNames": kwargs.get("dispSortNames", sport_category.get('dispSortNames')),
            "primaryMarkets": kwargs.get("primaryMarkets", sport_category.get('primaryMarkets')),
            "topMarkets": kwargs.get("topMarkets", sport_category.get('topMarkets')),
            "aggrigatedMarkets": kwargs.get("aggrigatedMarkets", sport_category.get('aggrigatedMarkets')),
            "showInMenu": kwargs.get("showInMenu", sport_category.get('showInMenu')),
            "spriteClass": kwargs.get("spriteClass", sport_category.get('spriteClass')),
            "ssCategoryCode": kwargs.get("ssCategoryCode", sport_category.get('ssCategoryCode')),
            "svg": kwargs.get("svg", sport_category.get('svg')),
            "svgFilename": kwargs.get("svgFilename", sport_category.get('svgFilename')),
            "svgId": kwargs.get("svgId", sport_category.get('svgId')),
            "targetUri": kwargs.get("targetUri", sport_category.get('targetUri')),
            "collectionType": kwargs.get("collectionType", sport_category.get('collectionType')),
            "showInAZ": kwargs.get("showInAZ", sport_category.get('showInAZ')),
            "showInHome": kwargs.get("showInHome", sport_category.get('showInHome')),
            "showInPlay": kwargs.get("showInPlay", sport_category.get('showInPlay')),
            "showScoreboard": kwargs.get("showScoreboard", sport_category.get('showScoreboard')),
            "scoreBoardUri": kwargs.get("scoreBoardUri", sport_category.get('scoreBoardUri')),
            "inplayEnabled": kwargs.get("inplayEnabled", sport_category.get('inplayEnabled')),
            "hasEvents": kwargs.get("hasEvents", sport_category.get('hasEvents')),
            "showFreeRideBanner": kwargs.get("showFreeRideBanner", sport_category.get('showFreeRideBanner')),
            "inplaySportModule":
                {
                    "enabled": kwargs.get("inplaySportModuleEnabled", False),
                    "inplayCount": kwargs.get("inplayCount", 10),
                },
            "messageLabel": kwargs.get("messageLabel", sport_category.get('messageLabel'))
        }
        data = json.dumps(data)
        return self.request.put(path, data=data)

    def delete_sport_category(self, sport_category_id):
        """
        param Sport Category_id: Sport Category_id
        return: deleting the Sport Category
        """
        path = f'sport-category/{sport_category_id}'
        return self.request.delete(path, parse_response=False)

    def get_segments(self) -> list:
        """
        Get all segments
        :return: list of dict with all configured segments
        """
        path = f'segments/brand/{self.brand}'
        response = self.request.get(path)
        return response

    def get_segment_id(self, segment_name) -> list:
        """
        Get segment id
        :return: segment id
        """
        all_segments = self.get_segments()
        for segment in all_segments:
            if segment['name'] == segment_name:
                return segment['id']
        raise CMSException(f'Segment "{segment_name}" is not available')

    def delete_segment(self, segment_name: str):
        """
        Delete segment
        :param segment_name: str, segment name
        """
        segment_id = self.get_segment_id(segment_name=segment_name)
        path = f'segments/{segment_id}/brand/{self.brand}'
        self.request.delete(path, parse_response=False)

    def get_inplay_module_items(self, segment_name='Universal'):
        """
        Get all the sports in inplay module
        """
        path = f'home-inplay-sport/brand/{self.brand}/segment/{segment_name}'
        response = self.request.get(path)
        return response

    def get_inplay_sport_module_id(self, sport_name):
        """
        Get segment id
        :return: segment id
        """
        sport_name = sport_name.title()
        segment_name = kwargs.get('segment_name', 'Universal')
        sports = self.get_inplay_module_items(segment_name=segment_name)
        for sport in sports:
            if sport_name == sport['sportName'].title():
                return sport['id']
        raise CMSException(f'Inplay sport module "{sport_name}" is not available')

    def update_inplay_sport_module(self, sport_name: str, **kwargs):
        """
        Update a sport in inplay module
        :param sport_name: name of the sport that should be created/updated
        :return: response of updated sport
        """
        segment_name = kwargs.get('segment_name', 'Universal')
        sports = self.get_inplay_module_items(segment_name=segment_name)
        sport_name = sport_name.title()
        for sport in sports:
            if sport_name == sport['sportName'].title():
                path = f'home-inplay-sport/{sport["id"]}'
                payload = {
                    "id": sport['id'],
                    "archivalId": sport['archivalId'],
                    "eventCount": kwargs.get("event_count",sport['eventCount']),
                    "categoryId": sport['categoryId'],
                    "sportName": sport_name,
                    "brand": self.brand,
                    "tier": sport['tier'],
                    "inclusionList": kwargs.get('inclusionList', sport['inclusionList']),
                    "exclusionList": kwargs.get('exclusionList', sport['exclusionList']),
                    "sportNumber": kwargs.get('sportNumber', sport['sportNumber']),
                    "sortOrder": kwargs.get('sortOrder', sport['sortOrder']),
                    "segmentReferences": kwargs.get('segmentReferences', sport['segmentReferences']),
                    "universalSegment": kwargs.get('universalSegment', sport['universalSegment']),
                    "message": kwargs.get('message', sport['message'])
                }
                response = self.request.put(
                    url=path,
                    data=json.dumps(payload)
                )
                return response
        else:
            raise CMSException(f'{sport_name} not found')

    def create_inplay_sport_module(self, sport_name: str, tier: str, **kwargs):
        """
        Create a sport in inplay module
        :param sport_name: name of the sport that should be created/updated
        :param tier: tier of the sport
        :return: response of created sport
        """
        # use this method only to test in QA2 or lower environments

        sport_name = sport_name.title()
        path = 'home-inplay-sport'
        payload = {
            "eventCount": kwargs.get('eventcount', 1),
            "sportName": sport_name,
            "brand": self.brand,
            "tier": tier,
            "inclusionList": kwargs.get('inclusionList', []),
            "exclusionList": kwargs.get('exclusionList', []),
            "universalSegment": kwargs.get('universalSegment', True)
        }
        response = self.request.post(
            url=path,
            data=json.dumps(payload)
        )
        self._created_inplay_module.append(response.get('sportName'))
        return response

    def delete_inplay_sport_module(self, sport_name: str):
        """
        Delete Inplay module
        :param _id: str, inplay module id
        """
        id = self.get_inplay_sport_module_id(sport_name=sport_name.title())
        path = f'home-inplay-sport/{id}'
        self.request.delete(path, parse_response=False)

    def set_quicklinks_ordering(self, new_order: list, moving_item, **kwargs):
        """
         Method allows to change quicklinks ordering in CMS
        :param new_order: list of sports e.g.["5ce4ca43c9e77c000135fc24", "5d11ae63c9e77c0001d4f884", "5ce4ca42c9e77c0001e08fca"]
        :param moving_item: Item id e.g.'5eb9ebd9c9e77c00018cdb27'
        """
        data = {
            "order": new_order,
            "id": moving_item,
            "pageId": 'null',
            "pageType": 'null',
            "segmentName": kwargs.get('segmentName', 'Universal')
        }
        data = json.dumps(data)
        path = f'sport-quick-link/ordering'
        self.request.post(path, data=data, parse_response=False)

    def get_featured_events(self, segment='Universal'):
        """
         Method used to get all Featured events info from CMS
        :param segment:passing segment to retrieve all detailes of particular segment
        :return: List of active feature events
        """
        path=f'home-module/brand/{self.brand}/segment/{segment}?active=true'
        return self.request.get(path)

    def set_featured_events_ordering(self, new_order: list, moving_item, **kwargs):
        """
         Method allows to change featured_events ordering in CMS
        :param new_order: list of sports e.g.["5ce4ca43c9e77c000135fc24", "5d11ae63c9e77c0001d4f884", "5ce4ca42c9e77c0001e08fca"]
        :param moving_item: Item id e.g.'5eb9ebd9c9e77c00018cdb27'
        """
        data = {
            "order": new_order,
            "id": moving_item,
            "pageId": 'null',
            "pageType": 'null',
            "segmentName": kwargs.get('segmentName', 'Universal')
        }
        data = json.dumps(data)
        path = f'home-module/ordering'
        self.request.post(path, data=data, parse_response=False)

    def set_surfacebet_ordering(self, new_order: list, moving_item, **kwargs):
        """
         Method allows to change surfacebet ordering in CMS
        :param new_order: list of sports e.g.["5ce4ca43c9e77c000135fc24", "5d11ae63c9e77c0001d4f884", "5ce4ca42c9e77c0001e08fca"]
        :param moving_item: Item id e.g.'5eb9ebd9c9e77c00018cdb27'
        """
        data = {
            "order": new_order,
            "id": moving_item,
            "pageId": kwargs.get('pageId', '0'),
            "pageType": kwargs.get('pageType', "sport"),
            "segmentName": kwargs.get('segmentName', 'Universal')
        }
        data = json.dumps(data)
        path = f'surface-bet/ordering'
        self.request.post(path, data=data, parse_response=False)

    def set_superbutton_ordering(self, new_order: list, moving_item, **kwargs):
        """
         Method allows to change super button ordering in CMS
        :param new_order: list of super Button id's e.g.["5ce4ca43c9e77c000135fc24", "5d11ae63c9e77c0001d4f884", "5ce4ca42c9e77c0001e08fca"]
        :param moving_item: Item id e.g.'5eb9ebd9c9e77c00018cdb27'
        """
        data = {
            "order": new_order,
            "id": moving_item,
            "pageId": kwargs.get('pageId'),
            "pageType": kwargs.get('pageType'),
            "segmentName": kwargs.get('segmentName', 'Universal')
        }
        data = json.dumps(data)
        path = f'navigation-points/ordering'
        self.request.post(path, data=data, parse_response=False)

    def set_highlight_courousel_ordering(self, new_order: list, moving_item, **kwargs):
        """
         Method allows to change highlight_courousel ordering in CMS
        :param new_order: list of sports e.g.["5ce4ca43c9e77c000135fc24", "5d11ae63c9e77c0001d4f884", "5ce4ca42c9e77c0001e08fca"]
        :param moving_item: Item id e.g.'5eb9ebd9c9e77c00018cdb27'
        """
        data = {
            "order": new_order,
            "id": moving_item,
            "pageId": 'null',
            "pageType": 'null',
            "segmentName": kwargs.get('segmentName', 'Universal')
        }
        data = json.dumps(data)
        path = f'highlight-carousel/ordering'
        self.request.post(path, data=data, parse_response=False)

    def create_footer_menu(self, **kwargs):
        """
        @param kwargs: title : Title of the footer menu
        @param kwargs: showItemFor: {'Both', 'loggedIn', 'loggedOut'}
        @param kwargs: uri - navigation uri
        """
        path = 'footer-menu'
        payload = {"id": "",
                   "sortOrder": 0,
                   "brand": self.brand,
                   "linkTitle": kwargs.get("title", "AutoTest"),
                   "linkTitleBrand": f"auto test-{self.brand}",
                   "segmentReferences": kwargs.get('segmentReferences', []),
                   "inclusionList": kwargs.get('inclusionList', []),
                   "universalSegment": kwargs.get('universalSegment', True),
                   "exclusionList": kwargs.get('exclusionList', []),
                   "archivalId": "",
                   "desktop": False,
                   "disabled": False,
                   "inApp": True,
                   "mobile": True,
                   "showItemFor": kwargs.get("showItemFor", "Both"),
                   "tablet": True,
                   "targetUri": kwargs.get("uri", "sport/football/matches"),
                   "authRequired": False}
        data = json.dumps(payload)
        response = self.request.post(path, data=data)
        self._created_footer_menu.append(response.get('id'))
        return response

    def delete_footer_menu(self, id):
        path = 'footer-menu/%s' % id
        self.request.delete(path, parse_response=False)

    def change_order_of_desktop_quick_links(self, new_order, moving_item, **kwargs):
        """
        Method allows to change desktop quick links ordering in CMS
        :param new_order: list of desktop quick links e.g.["5ce4ca43c9e77c000135fc24", "5d11ae63c9e77c0001d4f884"]
        :param moving_item: Item id e.g.'5eb9ebd9c9e77c00018cdb27'
        """
        data = {
            "order": new_order,
            "id": moving_item,
        }
        data = json.dumps(data)
        path = f'desktop-quick-link/ordering'
        self.request.post(path, data=data, parse_response=False)

    def change_order_of_footer_items(self, new_order, moving_item, **kwargs):
        """
         Method allows to change footer items ordering in CMS
        :param new_order: list of footer items e.g.["5ce4ca43c9e77c000135fc24", "5d11ae63c9e77c0001d4f884"]
        :param moving_item: Item id e.g.'5eb9ebd9c9e77c00018cdb27'
        """
        data = {
            "order": new_order,
            "id": moving_item,
            "pageId": 'null',
            "pageType": 'null',
            "segmentName": kwargs.get('segmentName', 'Universal')
        }
        data = json.dumps(data)
        path = f'footer-menu/ordering'
        self.request.post(path, data=data, parse_response=False)

    def change_order_of_home_inpaly_module_items(self, new_order, moving_item, **kwargs):
        """
         Method allows to change inplay module items ordering in CMS
        :param new_order: list of inplay module items e.g.["5ce4ca43c9e77c000135fc24", "5d11ae63c9e77c0001d4f884"]
        :param moving_item: Item id e.g.'5eb9ebd9c9e77c00018cdb27'
        """
        data = {
            "order": new_order,
            "id": moving_item,
            "pageId": 'null',
            "pageType": 'null',
            "segmentName": kwargs.get('segmentName', 'Universal')
        }
        data = json.dumps(data)
        path = f'home-inplay-sport/ordering'
        self.request.post(path, data=data, parse_response=False)

    # use methoud to change the order of the home page modules such as highlight_carousel,surface bet etc
    def change_order_of_module_items(self, new_order, moving_item, **kwargs):
        """
         Method allows to change event hub module items ordering in CMS
        :param new_order: list of event hub module items e.g.["5ce4ca43c9e77c000135fc24", "5d11ae63c9e77c0001d4f884"]
        :param moving_item: Item id e.g.'5eb9ebd9c9e77c00018cdb27'
        """
        data = {
            "order": new_order,
            "id": moving_item,
        }
        data = json.dumps(data)
        path = f'sport-module/ordering'
        self.request.post(path, data=data, parse_response=False)

    # 1-2 Free Gamification
    def get_seasons(self):
        """
        return: Get all the seasons
        """
        path = f'season/brand/{self.brand}'
        response = self.request.get(path)
        return response

    def create_season(self, **kwargs):
        """
        param kwargs: seasonName
        return: created season response
        """
        displayFrom = get_date_time_as_string(time_format='%Y-%m-%dT%H:%M:%SZ', url_encode=False)
        displayTo = get_date_time_as_string(time_format='%Y-%m-%dT%H:%M:%SZ', url_encode=False, days=1)
        path= f'season'
        payload={
         "displayFrom": displayFrom,
         "displayTo": displayTo,
         "seasonName": kwargs.get("seasonName", "Auto Test Season"+ str(fake.random_int(min=1, max=500))),
         "seasonInfo": "Auto Test season",
          "brand": self.brand
         }
        data = json.dumps(payload)
        return self.request.post(path, data=data)

    def update_season(self, current_season):
        """
        param current_season: current season response
        return: updated active season details
        """
        season_id = current_season.get('id')
        path = f'season/{season_id}/true'
        displayFrom = get_date_time_as_string(time_format='%Y-%m-%dT%H:%M:%SZ', url_encode=False)
        current_season['displayFrom'] = displayFrom
        return self.request.put(path, data=json.dumps(current_season))

    def get_gamification(self):
        """
        return: all gamifications
        """
        path=f'gamification/brand/{self.brand}'
        return self.request.get(path)

    def delete_gamification(self,gamification_id):
        """
        param gamification_id: gamification id
        deleting the gamification
        """
        path=f'gamification/{gamification_id}'
        self.request.delete(path, parse_response=False)

    def get_teams(self):
        """
        return: all the teams
        """
        path= f'asset-management/brand/{self.brand}'
        response = self.request.get(path)
        return response

    def create_gamification(self,seasonId,**kwargs):
        """
        param seasonId: seasonId for which we are creating the gamification
        Kwargs related to badges for primary and secondary params
        return: created gamification response
        """
        pl_teams={'ARSENAL','ASTON VILLA','BRENTFORD','BRIGHTON', 'BURNLEY','CHELSEA', 'CRYSTAL PALACE', 'EVERTON',
                  'LEEDS','LEICESTER','LIVERPOOL', 'MAN CITY', 'MAN UTD', 'NEWCASTLE','NORWICH', 'SOUTHAMPTON','TOTTENHAM',
                  'WATFORD', 'WEST HAM','WOLVES','BOURNEMOUTH','NOTTM FOREST','FULHAM'}

        response = self.get_teams()
        teams_data=[teams for teams in response if teams['active'] is True and teams['teamName'] in pl_teams]
        teamList=[]
        for team in teams_data:
            teamList.append({"displayName": team['teamName'],
                             "svg": team['teamsImage']['svg'],
                             "svgId": team['teamsImage']['svg'].partition('"')[2].partition('"')[0],
                             "assetManagementObjectId": team['id']})
        path=f'gamification'
        payload = {
              "teams": teamList,
              "badgeTypes": [
                {
                  "name": "Primary",
                  "numberOfBadges": kwargs.get("primary_numberOfBadges","2"),
                  "congratsMsg": kwargs.get("primary_congratsMsg","You have won the primary Badge"),
                  "prizeType": kwargs.get("primary_prizeType","freeBet"),
                  "amount": kwargs.get("primary_amount",0.1)
                },
                {
                  "name": "Secondary",
                  "numberOfBadges": kwargs.get("secondary_badges_count","2"),
                  "congratsMsg":kwargs.get("secondary_congratsMsg","You have won the secondary Badge"),
                  "prizeType": kwargs.get("secondary_prizeType","freeBet"),
                  "amount": kwargs.get("secondary_amount",0.1)
                }
              ],
              "seasonId": seasonId,
              "brand": self.brand
            }
        data = json.dumps(payload)
        return self.request.post(path, data=data)

    def delete_season(self,seasonId):
        """
        param sesonId: passing season Id to delete season
        deleting the season
        """
        path = f'season/{seasonId}'
        self.request.delete(path, parse_response=False)

    def get_games(self):
        """
        return: all the game views
        """
        path= f'game/brand/{self.brand}'
        return self.request.get(path)

    def get_game(self,gameId):
        """
        param gameId
        return: game view response of that particular game id
        """
        path=f'game/{gameId}'
        return self.request.get(path)

    def create_gameView(self,seasonId):
        """
        param seasonId: creating gameview for that particular season
        return: created game view response
        """
        displayFrom = get_date_time_as_string(time_format='%Y-%m-%dT%H:%M:%SZ', url_encode=False)
        displayTo = get_date_time_as_string(time_format='%Y-%m-%dT%H:%M:%SZ', url_encode=False, days=1)
        path=f'game'
        payload={
            "status": "",
            "displayFrom": displayFrom,
            "displayTo": displayTo,
            "id": "",
            "sortOrder": 0,
            "brand": self.brand,
            "highlighted": False,
            "events": [],
            "prizes": [],
            "title": "Auto Test Game"+ str(fake.random_int(min=1, max=500)),
            "enabled": False,
            "seasonId": seasonId
        }
        data = json.dumps(payload)
        return self.request.post(path, data=data)

    def get_team_names_by_eventid(self,eventId):
        """
        param: eventId
        return: home and away team names of that eventId
        """
        path=f'game/brand/{self.brand}/event-id/{eventId}'
        return self.request.get(path)

    def get_score_of_event(self,eventId):
        """
        param eventId
        return: score of the event
        """
        path=f'game/{eventId}/score'
        return self.request.get(path)

    def set_score_for_event(self,gameId,eventId,eventPosition,scores):
        """
        params gameId as string to set the score for that gameview
        params eventId as string
        params scores as list [[1,2],[3,4]] for home and teams
        return: success message as score is set
        """
        path=f'game/{gameId}/score'
        payload={
            "eventId": eventId,
            "eventPosition": eventPosition,
            "actualScores": scores
           }
        data = json.dumps(payload)
        return self.request.post(path, data=data)

    def update_game_view(self,game_response,eventId,**kwargs):
        """
        params: gameresponse response of the game view to update
        params:eventsId as a single eventID
        kwargs pl_teams as list [[False, True], [True, False]] when pl teams are required
        """
        displayFrom = get_date_time_as_string(time_format='%Y-%m-%dT%H:%M:%SZ', url_encode=False, seconds=10)
        displayTo = get_date_time_as_string(time_format='%Y-%m-%dT%H:%M:%SZ', url_encode=False, days=1)
        gameId = game_response.get('id')
        events = game_response.get('events') if game_response.get('events') else []
        prizes = game_response.get('prizes') if game_response.get('prizes') else []
        isNonPLTeam = kwargs.get("pl_checkbox",[[False,False],[False,False],[False,False]])

        team=self.get_team_names_by_eventid(eventId)
        events.append({
              "tvIcon":None,
              "eventId": team.get('eventId'),
              "startTime": team.get('startTime'),
              "home": {
                "name": team.get('homeTeamName'),
                "displayName": team.get('homeTeamName'),
                "teamKitIcon": None,
                "isNonPLTeam": isNonPLTeam[len(game_response["events"])][0]
              },
              "away": {
                "name": team.get('awayTeamName'),
                "displayName": team.get('awayTeamName'),
                "teamKitIcon": None,
                "isNonPLTeam": isNonPLTeam[len(game_response["events"])][1]
              }
        })

        prizes.append({
            "correctSelections": len(events),
            "prizeType": kwargs.get("prizeType", "FREE_BETS"),
            "amount": kwargs.get("amount", 1)
        })

        path=f'game/{gameId}'
        payload={
              "id": gameId,
              "brand":self.brand ,
              "title": game_response.get('title'),
              "displayFrom": displayFrom,
              "displayTo": displayTo,
              "enabled": False,
              "prizes": prizes,
              "events": events,
              "seasonId": game_response.get('seasonId')
            }
        data = json.dumps(payload)
        return self.request.put(path, data=data)

    def add_prediction_to_game_view(self, game_id, event_ids, no_of_predictions=3, **kwargs):
        """
        Add predictions to the game view for the specified game id with the given event IDs.

        Parameters:
        - game_id (str): The ID of the game.
        - event_ids (list): A list of event IDs to add predictions.
        - no_of_predictions (int, optional): The maximum number of predictions to add. Default is 3.
        - **kwargs: Additional keyword arguments. (e.g., pl_checkbox to specify checkboxes values)

        Note:
            if you are sending no_of_predictions value greater than 3 then it is mandatory to send the values of pl_checkbox.
            example: no_of_predictions=4, pl_checkbox=[[True, False], [False, True], [True, True], [True, True]]

        Raises:
        - CMSException: If there is no event data available for the provided event IDs.

        Usage:
        add_prediction_to_game_view(game_id, ["event1", "event2"], no_of_predictions=2)
        """
        pl_checkbox= kwargs.get("pl_checkbox", [[False, False], [False, False], [False, False]])
        current_count_of_predictions_added = 0
        for event_id in event_ids:
            if current_count_of_predictions_added == no_of_predictions:
                break
            try:
                game = self.get_game(game_id)
                self.update_game_view(game, event_id, pl_checkbox=pl_checkbox)
                current_count_of_predictions_added += 1
            except InvalidResponseException as ex:
                if '500' in ex.args[0]:
                    continue
        else:
            raise CMSException(f'No event data available in the given event ID list: {event_ids}')

        return self.get_game(game_id)

    def update_game_view_status(self, gameId, enabled):
        """
        param game_response
        param enabled:true
        return: updated active game view response
        """
        path=f'game/{gameId}'
        game_response = self.get_game(gameId=gameId)
        game_response['enabled']=enabled
        return self.request.put(path, data=json.dumps(game_response))

    def delete_game_view(self, game_view_id):
        """
        param: Pass game view ID of Game
        Deleting the game view
        """
        path = f'game/{game_view_id}'
        self.request.delete(path, parse_response=False)

    def get_bet_sharing_configuration(self):
        """
        return: bet sharing configuration details
        """
        path = f'bet-sharing/brand/{self.brand}'
        return self.request.get(path)

    def update_luckyDip_BetSharing_configuration(self, openBetControl_list = None, **kwargs):
        """
        param: Pass list of data which is required to chage in openbetcontrol for luckyDipBetSharingConfigs
        return: updated luckyDipBetSharingConfigs response in betsharing
        """
        response = self.get_bet_sharing_configuration()
        bet_sharing_id = response.get('id')
        path = f'bet-sharing/{bet_sharing_id}'
        luckyDip_BetSharing_response = response.get('luckyDipBetSharingConfigs')
        fields_to_update = [
            'enable','header','luckyDipLabel','backgroundImageUrl','luckyDipAffiliateLink','wonLabel',
            'potentialReturnsLabel','openBetControl'
        ]
        for field in fields_to_update:
            if field == 'openBetControl' and openBetControl_list:
                for obj in luckyDip_BetSharing_response[field]:
                    if obj['name'].upper() in openBetControl_list.keys():
                        obj['isSelected'] = openBetControl_list.get(obj['name'].upper()).get("isSelected")
            else:
                luckyDip_BetSharing_response[field] = kwargs.pop(field,luckyDip_BetSharing_response[field])
        data = json.dumps(response)
        self.request.put(path,data=data)

    def update_ftp_bet_sharing_configuration(self, **kwargs):
        """
        Update the configuration for Free To Play(FTP) bet sharing.
        In Ladbrokes, the feature applicable is One two Free.
        And for Coral it is Football Super Series.

        :param kwargs: Dictionary of data to be updated in openbetcontrol for ftpBetSharingConfigs.
                       Possible keys include 'affiliateLink', 'backgroundImageUrl', 'enable', 'header',
                       'playLabel', 'subHeader', and 'teamDetails'.
        The casing of both keys and values as it is from the CMS response is crucial.
        :return: Updated ftpBetSharingConfigs response for betsharing.
        """
        response = self.get_bet_sharing_configuration()
        bet_sharing_id = response.get('id')
        path = f'bet-sharing/{bet_sharing_id}'
        one_two_free_bet_sharing_response = response.get('ftpBetSharingConfigs')
        fields_to_update = ['affiliateLink', 'backgroundImageUrl', 'enable', 'header', 'playLabel', 'subHeader', 'teamDetails']
        # Loop through each field to update
        for field in fields_to_update:
            if field not in kwargs:
                continue
            if field == 'teamDetails':
                # Extract the team names from the existing configuration
                response_team_names = [team['teamName'] for team in one_two_free_bet_sharing_response.get('teamDetails')]
                teamDetails = kwargs.get('teamDetails')
                # Loop through each team detail object provided in kwargs
                for team_detail_obj in teamDetails:
                    # Check if the team name already exists in the configuration
                    if team_detail_obj['teamName'] in response_team_names:
                        # If the team exists, update its details
                        for item in one_two_free_bet_sharing_response['teamDetails']:
                            if item['teamName'] == team_detail_obj['teamName']:
                                item['teamLogoUrl'] = team_detail_obj.get('teamLogoUrl') or item.get('teamLogoUrl')
                                item['activated'] = team_detail_obj.get('activated') or item.get('activated')
                                break
                    else:
                        # If the team does not exist, add it to the configuration
                        one_two_free_bet_sharing_response['teamDetails'].append(team_detail_obj)
            else:
                # Update other fields in the configuration
                one_two_free_bet_sharing_response[field] = kwargs.get(field)

        # Check if there are teams to delete
        delete_team_detail_module_names = kwargs.get('delete_team_detail_module_names')
        if delete_team_detail_module_names:
            # Remove teams that are specified to be deleted
            one_two_free_bet_sharing_response['teamDetails'] = [x for x in one_two_free_bet_sharing_response['teamDetails']
                                                                if x.get('teamName') not in delete_team_detail_module_names]

        data = json.dumps(response)
        return self.request.put(path, data=data)

    def get_most_popular_or_trending_bets_bet_slip_config(self):
        """
        getting the config of in cms "Most popular bet/trending bet" >> "best slip"
        """
        path = f'trending-bet/brand/{self.brand}?type=bet-slip'
        return self.request.get(path)

    def update_most_popular_or_trending_bets_bet_slip_config(self,**kwargs):
        """
        updating the config of in cms "Most popular bet/trending bet" >> "best slip"
        """
        config = self.get_most_popular_or_trending_bets_bet_slip_config()
        path = f'trending-bet/{config.get("id")}?type=bet-slip'
        for key in kwargs:
            if key in config and kwargs[key] != config[key]:
                config[key] = kwargs[key]

        data = json.dumps(config)
        return self.request.put(path, data=data)

    def get_most_popular_or_trending_bets_bet_receipt_config(self):
        """
        getting the config of in cms "Most popular bet/trending bet" >> "best receipt"
        """
        path = f'trending-bet/brand/{self.brand}?type=bet-receipt'
        return self.request.get(path)

    def update_most_popular_or_trending_bets_bet_receipt_config(self,**kwargs):
        """
        updating the config of in cms "Most popular bet/trending bet" >> "best receipt"
        """
        config = self.get_most_popular_or_trending_bets_bet_receipt_config()
        path = f'trending-bet/{config.get("id")}?type=bet-receipt'
        for key in kwargs:
            if key in config and kwargs[key] != config[key]:
                config[key] = kwargs[key]

        data = json.dumps(config)
        return self.request.put(path, data=data)

    def delete_quiz(self, quiz_id):
        path = f'question-engine/{quiz_id}'
        return self.request.delete(path, parse_response=False)

    def delete_quizes_created_by_automation_scripts(self):
        """
        this method is to delete the all quizes created through Automation
        """
        all_quizzes = self.get_qe_quizzes()
        ids = [quiz['id'] for quiz in all_quizzes if quiz['title'] == self.auto_test_quiz_name]
        for id in ids:
            self.delete_quiz(quiz_id=id)

    def get_seo_pages(self):
        """
        Retrieve the data of "SEO pages" associated with the current brand.
        :return: A response containing the SEO pages data.
        """
        path = f'seo-page/brand/{self.brand}'
        return self.request.get(path)

    def create_seo_page(self, title, url, **kwargs):
        """
        Retrieve the data of "SEO pages" associated with the current brand.
        :return: A response containing the SEO pages data.
        This method makes a request to the API endpoint to fetch SEO pages data for the
        specified brand. It returns a response object containing the retrieved data.
        """

        seo_pages = self.get_seo_pages()
        response = next((seo_page for seo_page in seo_pages if seo_page.get('url') == url), None)
        if response:
            return response
        path = 'seo-page'
        payload = {
            "brand": self.brand,
            "changefreq": kwargs.get('changefreq', "daily"),
            "description": kwargs.get('description', ""),
            "disabled": kwargs.get('disabled', True),
            "staticBlock": kwargs.get('staticBlock', ""),
            "staticBlockTitle": kwargs.get('staticBlockTitle', ""),
            "title": title,
            "id": "",
            "url": url,
            "lang": "",
            "priority": kwargs.get('priority', '0'),
            "urlBrand": ""
        }
        data = json.dumps(payload)
        seo_page_response = self.request.post(path, data=data)
        self._created_seo_page.append(seo_page_response.get('id'))
        return seo_page_response

    def update_seo_page(self, url, **kwargs):
        """
        Retrieve the data of SEO pages associated with the current brand.
        :return: A response object containing the SEO pages data.
        This method sends a request to the API endpoint to obtain data for SEO pages
        associated with the specified brand. The response object includes the retrieved data.
        """
        seo_pages = self.get_seo_pages()
        response = next((seo_page for seo_page in seo_pages if seo_page.get('url') == url), None)
        if not response:
            response = self.create_seo_page(title="Auto_Seo_Page", url=url)
        id = response.get('id')
        path = f'seo-page/{id}'
        fields_to_update = [
            'changefreq', 'description', 'disabled', 'pageTitleBlock', 'priority', 'staticBlock', 'staticBlockTitle',
            'title', 'url', 'urlBrand'
        ]
        for field in fields_to_update:
            response[field] = kwargs.pop(field, response[field])
        data = json.dumps(response)
        return self.request.put(path, data=data)

    def delete_seo_page(self, seo_page_id):
        """
        Delete an SEO page with the specified ID.
        param seo_page_id: The ID of the SEO page to be deleted.
        :type seo_page_id: str
        This method sends a request to the API endpoint to delete the SEO page with the
        provided ID. It does not return any response data.
        """
        path = f'seo-page/{seo_page_id}'
        self.request.delete(path, parse_response=False)

    def get_my_stable_config(self):
        """
        this method return configuration of my stable
        """
        path = f'my-stable/configuration/brand/{self.brand}'
        return self.request.get(path)

    def update_my_stable_config(self, **kwargs):
        """
        this method is allows to update the my stable config
        """
        my_stable_config = self.get_my_stable_config()
        path = f'my-stable/configuration/{my_stable_config.get("id")}'
        for attribute, value in kwargs.items():
            if attribute not in my_stable_config:
                raise CMSException(f'attribute "{attribute}" is not valid')
            my_stable_config[attribute] = value

        data = json.dumps(my_stable_config)
        return self.request.put(path, data=data)

    def get_acca_insurance_config(self):
        """
        this method return configuration of acca insurance
        """
        path = f'acca-insurance-messages/brand/{self.brand}'
        return self.request.get(path)

    def update_acca_insurance_config(self, **kwargs):
        """
        this method is allows to update the acca insurance config
        """
        acca_insurance_config = self.get_acca_insurance_config()
        path = f'acca-insurance-messages/{acca_insurance_config.get("id")}'
        for field in kwargs:
            if field in acca_insurance_config:
                acca_insurance_config[field] = kwargs.get(field, acca_insurance_config[field])
            else:
                raise CMSException(f'Sent field "{field}" is not available in Acca Insurance response from CMS,'
                                   )

        data = json.dumps(acca_insurance_config)
        return self.request.put(path, data=data)

    def get_my_bets_message_configuration(self):
        """ Retrieve the configuration for the "My Bets" message.

        This method constructs the path to the "My Bets" open bets endpoint
        for the specified brand and performs a GET request to fetch the
        configuration details.

        Returns:
            Response: The response object resulting from the GET request
                      to the "My Bets" open bets endpoint.
                       """
        path = f'{self.brand}/my-bets/open-bets'
        return self.request.get(path)

    def update_my_bets_message_configuration(self, **kwargs):
        """
        Update the configuration for the "My Bets" message.

        This method retrieves the current configuration for the "My Bets"
        open bets, updates it with the provided keyword arguments, and
        then sends a PUT request to save the updated configuration.

        Args:
            **kwargs: Arbitrary keyword arguments representing the configuration
                      fields to be updated. Only existing fields in the response
                      will be updated.

        Returns:
            Response: The response object resulting from the PUT request to
                      update the "My Bets" open bets configuration.
        """
        response = self.get_my_bets_message_configuration
        tab_id = response.get('id')
        path = f'{self.brand}/my-bets/open-bets/{tab_id}'
        for key in kwargs:
            if key in response:
                response['key'] = kwargs['key']
        return self.request.put(path, data=json.dumps(response))

    def update_system_configuration_structure_by_filed(self, device_type, field_names: {},
                                                       config_item='NextRacesFiltersHorseRacing', ):
        """
        General method for updating CMS System Structure
        :param config_item: Config item. e.g. CompetitionsFootball, NextRaces...
        :param field_name: Available config item's field
        :param field_value: Field value
        :return: Updated System Structure
        """
        system_configuration = self.get_initial_data(device_type).get('systemConfiguration')
        self._logger.info(f"responce for request in validate in cms{system_configuration}")
        try:
            for field_name in field_names.keys():
                system_configuration[config_item][field_name] = field_names[field_name]
        except KeyError:
            raise CMSException(f'Config item/name {config_item}/{field_name} not found in System Structure')
        path = f'structure/brand/{self.brand}'
        payload = {
            'lang': 'en',
            'brand': self.brand,
            'structure': system_configuration
        }
        request = self.request.put(path, data=json.dumps(payload))
        self._cached_initial_data = {'mobile': None,
                                     'desktop': None}  # so new data will be returned for the next request
        return request


if __name__ == '__main__':
    c = CMSClient()
