import json
import logging
from time import sleep
from faker import Faker
from datetime import datetime
from crlat_cms_client.utils.date_time import get_date_time_as_string
from crlat_cms_client import LOGGER_NAME
from crlat_cms_client.request import CMSAPIRequest
from crlat_cms_client.utils.exceptions import CMSException

fake = Faker()


class ModuleRibbonTabs:
    base_path = 'module-ribbon-tab'
    accounts_sharing_url = 'https://accounts-sharing-dev0.coralsports.dev.cloud.ladbrokescoral.com/'

    _known_directive_names = [
        'Featured',
        'Multiples',
        'LiveStream',
        'TopBets',
        'Coupons',
        'NextRaces',
        'InPlay',
        'BuildYourBet',
        'EventHub'
    ]

    def __init__(
            self,
            brand: str = 'bma',
            env: str = 'dev0',
    ):
        self._brand = brand
        self.env = env
        self._logger = logging.getLogger(name=LOGGER_NAME).getChild('[module_ribbon]')
        self._all_tabs_data = []
        self._expired = True  # True after get request and False after any change
        self.request = CMSAPIRequest()
        self._created_tabs = []

    def expire_cache(self):
        """
        public method to expire cache. Should be used in waiters
        """
        self._expired = True

    @property
    def endpoint(self):
        return '%s/brand/%s' % (self.base_path, self._brand)

    @property
    def all_tabs_data(self):
        if self._expired:
            self._all_tabs_data = self.request.get(self.endpoint)
            self._expired = False
        return self._all_tabs_data

    @property
    def visible_tabs_data(self):
        return [tab for tab in self.all_tabs_data if tab.get('visible')]

    def get_tab_name(self, internal_id: str, raise_exceptions=False) -> str:
        tab_name = next((tab.get('title').upper() for tab in self.all_tabs_data if tab.get('internalId') == internal_id), '')
        if not tab_name and raise_exceptions:
            available_tabs = [tab.get('internalId') for tab in self.all_tabs_data]
            raise CMSException(f'Please, provide valid internalId value. \n'
                               f'"{internal_id}" is not present in "{available_tabs}"')
        return tab_name

    def update_mrt_tab(self, tab_name: str, **kwargs):
        """
          Update the specified MRT (Module ribbon tab) with the given parameters.
            Args:
                tab_name (str): The name of the MRT tab to be updated.
                **kwargs: Additional keyword arguments representing fields to be updated.
                    Valid fields for update: 'exclusionList', 'inclusionList', 'universalSegment',
                    'brand', 'directiveName', 'title', 'title_brand', 'visible', 'showTabOn',
                    'internalId', 'url', 'hubIndex', 'displayFrom', 'displayTo'.
        Returns:
            dict: A dictionary containing the updated MRT tab information.
        Raises:
            CMSException: If the specified tab name is not found in the available tabs.
                """
        tabs = self.all_tabs_data
        for tab in tabs:
            if tab['title'] == tab_name:
                path = f'{self.base_path}/{tab["id"]}'
                response = self.request.get(path)

                fields_to_update = [
                    'exclusionList', 'inclusionList', 'universalSegment', 'brand',
                    'directiveName', 'title', 'title_brand', 'visible', 'showTabOn',
                    'internalId', 'url', 'hubIndex', 'displayFrom', 'displayTo'
                ]

                for field in fields_to_update:
                    response[field] = kwargs.pop(field, response[field])

                data = json.dumps(response)
                resp = self.request.put(path, data=data)
                return resp

        raise CMSException(f'tab name {tab_name} is not available')

    def update_tab(self, tab_name: str, universal=True, inclusion_list=[], exclusion_list=[]):
        tabs = self.visible_tabs_data
        for tab in tabs:
            if tab['title'] == tab_name:
                request_data = {"id": tab['id'],
                 "exclusionList": exclusion_list,
                 "inclusionList": inclusion_list,
                 "archivalId": tab['archivalId'],
                 "universalSegment": universal,
                 "brand": self._brand,
                 "directiveName": tab['directiveName'],
                 "title": tab['title'],
                 "title_brand": tab['title_brand'],
                 "visible": tab['visible'],
                 "showTabOn": tab['showTabOn'],
                 "internalId": tab['internalId'],
                 "url": tab['url'], "hubIndex": tab['hubIndex'],
                 "displayFrom": tab['displayFrom'],
                 "displayTo": tab['displayTo']}
                resp = self.request.put(
                    '%s/%s' % (self.base_path, tab['id']),
                    data=json.dumps(request_data)
                )
                return resp
        else:
            raise CMSException(f'tab name {tab_name} is not available')

    def create_tab(
            self,
            sort_order: int = None,
            brand: str = None,
            directive_name: str = None,
            title: str = None,
            title_brand: str = None,
            visible: bool = None,
            show_tabs_on: str = None,
            internal_id: str = None,
            devices_android: bool = None,
            devices_ios: bool = None,
            devices_wp: bool = None,
            url: str = None,
            hub_index: int = None,
            display_date: bool = None,
            **kwargs
    ):
        if directive_name not in self._known_directive_names:
            raise CMSException(
                'Directive name "%s" not found in supported list ["%s"]' % (
                    directive_name,
                    '", "'.join(self._known_directive_names)
                )
            )
        brand = brand if brand else self._brand
        title_brand = title_brand if title_brand else '%s-%s' % (directive_name.lower(), brand)
        devices = {
            'android': devices_android if devices_android else True,
            'ios': devices_ios if devices_ios else True,
            'wb': devices_wp if devices_wp else True
        }
        request_data = {
            'sortOrder': sort_order if sort_order is not None else len(self.all_tabs_data),
            'brand': brand,
            'directiveName': directive_name,
            'title': title if title else f'AT {fake.city()} {directive_name}',
            'title_brand': title_brand,
            'visible': visible if visible else True,
            'showTabOn': show_tabs_on if show_tabs_on else 'both',
            'internalId': internal_id if internal_id else 'tab-%s' % directive_name.lower(),
            'devices': devices,
            'url': url if url else f'home/{"betbuilder" if (directive_name.upper() == "BUILDYOURBET" and brand!="bma") else directive_name.lower()}',
            'inclusionList': kwargs.get('inclusionList', []),
            'universalSegment': kwargs.get('universalSegment', True),
            'exclusionList': kwargs.get('exclusionList', [])
        }
        if hub_index:
            request_data.update({
                'hubIndex': hub_index,
                'url': url if url else f'/home/{directive_name.lower()}/{hub_index}',
                'internalId': internal_id if internal_id else f'tab-{directive_name.lower()}-{hub_index}'
            })
        if display_date:
            now = datetime.now()
            time_format = '%Y-%m-%dT%H:%M:%S'
            display_from = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                                   days=-1, minutes=-1)[:-3] + 'Z'
            display_to = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                                 days=1)[:-3] + 'Z'
            request_data.update({
                'displayFrom': display_from,
                'displayTo': display_to
            })
        resp = self.request.post(
            self.base_path,
            data=json.dumps(request_data)
        )
        self.expire_cache()
        self._logger.info(
            '*** Added module ribbon tab "%s(%s)"' % (
                directive_name,
                ', '.join(['%s=%s' % (k, request_data.get(k)) for k in ['title', 'id', 'url', 'internal_id']])
            )
        )
        for i in range(30):
            self.expire_cache()
            if resp.get('id') in [tab.get('id') for tab in self.all_tabs_data]:
                break
            sleep(0.5)
        self._created_tabs.append(resp.get('id'))
        return resp

    def delete_tab_by_id(self, tab_id: str = None):
        if not tab_id:
            raise CMSException('Delete failed. No Tab Id provided')
        self.expire_cache()
        if tab_id not in [tab.get('id') for tab in self.all_tabs_data]:
            self._logger.warning('ByPass Tab delete. Not found tab with id "%s"' % tab_id)
            return
        self.request.delete(f'{self.base_path}/{tab_id}', parse_response=False)
        self.expire_cache()
