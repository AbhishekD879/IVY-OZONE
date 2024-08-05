import json
from time import sleep

import tests
from tests.Common import Common
from voltron.utils.helpers import normalize_name


class BaseDataLayerTest(Common):
    keep_browser_open = True
    deposit_amount = 5.5

    expected_yc_show_all_button_response = {
        'event': 'trackEvent',
        'eventCategory': 'your call',
        'eventAction': 'market',
        'eventLabel': 'show all',
        'market': 'market'
    }

    expected_yc_expand_response = {
        'event': 'trackEvent',
        'eventCategory': 'your call',
        'eventAction': 'league',
        'eventLabel': 'expand',
        'league': 'league'
    }

    expected_yc_collapse_response = {
        'event': 'trackEvent',
        'eventCategory': 'your call',
        'eventAction': 'league',
        'eventLabel': 'collapse',
        'league': 'league'
    }

    expected_market_selector_response = {
        'categoryID': 'categoryID',
        'event': 'trackEvent',
        'eventAction': 'change market',
        'eventCategory': 'market selector',
        'eventLabel': 'market_name'
    }

    expected_add_favourites_response = {
        'event': 'trackEvent',
        'eventCategory': 'favourites',
        'eventAction': 'add',
        'eventLabel': 'favourite icon',
        'location': 'football matches'
    }

    expected_tote_response = {
        'event': 'trackEvent',
        'eventCategory': 'international tote',
        'eventAction': ''
    }

    expected_betslip_response = {
        'event': 'trackEvent',
        'eventCategory': 'betslip',
        'eventAction': ''
    }

    def get_data_layer_specific_object(self, object_key, object_value=None, timeout=0.1, eventAction=None):
        result = None
        sleep(timeout)
        data_layer_objects = self.site.get_data_layer
        for object_item in reversed(data_layer_objects):
            if isinstance(object_item, list):
                continue
            if object_value!="" and not object_value:
                if object_key in object_item.keys():
                    object_item.pop('gtm.uniqueEventId', None)
                    result = object_item
                    return result
            try:
                if object_item[object_key].upper() == object_value.upper():
                    if eventAction and object_item['eventAction'] != eventAction:
                        continue
                    object_item.pop('gtm.uniqueEventId', None)
                    result = object_item
                    return result
                else:
                    continue

            except KeyError:
                self._logger.warning(f'There is no key "{object_key}" for object "{object_item}"')
        self.assertTrue(result, msg=f'Required object with key: "{object_key}" value "{object_value}" was not found')

    def get_data_layer_objects_count(self, object_key, object_value=None):
        result = []
        data_layer_objects = self.site.get_data_layer
        for object_item in reversed(data_layer_objects):
            if isinstance(object_item, list):
                continue
            if not object_value:
                if object_key in object_item.keys():
                    result.append(object_item)
            try:
                if object_item[object_key] == object_value:
                    result.append(object_item)
                else:
                    continue
            except KeyError:
                self._logger.warning(f'There is no key "{object_key}" for object "{object_item}"')
        return len(result) if result else 0

    def compare_json_response(self, check_actual_response, check_expected_response):
        if 'errorMessage' in check_actual_response:
            check_actual_response['errorMessage'] = check_actual_response['errorMessage'].replace('\n', ' ')
        actual = json.dumps(check_actual_response, indent=2)
        expected = json.dumps(check_expected_response, indent=2)
        self.assertDictEqual(
            check_actual_response,
            check_expected_response,
            msg='Dict mismatch. Actual:\n%s\nExpected:\n%s' % (
                actual,
                expected
            )
        )

        self._logger.debug('*** Actual data layer response \n %s' % actual)
        self._logger.debug('*** Expected data layer response \n %s' % expected)

    def check_data_layer_favourites_response(self, object_key, action, location):
        actual_response = self.get_data_layer_specific_object(object_key=object_key, object_value=action)
        self.expected_add_favourites_response['eventAction'] = action
        self.expected_add_favourites_response['location'] = location
        self.compare_json_response(actual_response, self.expected_add_favourites_response)
        self._logger.debug('*** Actual data layer response \n %s' % json.dumps(actual_response, indent=2))
        self._logger.debug('*** Expected data layer response \n %s' % json.dumps(self.expected_add_favourites_response, indent=2))

    def verify_coupon_selection_tracking(self, coupon_name):
        expected_response = {
            'event': 'trackEvent',
            'eventAction': 'Select Coupon',
            'eventCategory': 'Coupon Selector',
            'eventLabel': coupon_name,
        }
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value=coupon_name)
        self.compare_json_response(actual_response, expected_response)

    def verify_coupon_market_selector_tracking(self, market_name):
        expected_response = {
            'event': 'trackEvent',
            'eventAction': 'change market',
            'eventCategory': 'market selector',
            'eventLabel': market_name,
            'categoryID': str(self.ob_config.football_config.category_id)
        }
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value=market_name)
        self.compare_json_response(actual_response, expected_response)

    def verify_ga_tracking_record(self, brand, category, event_id, selection_id, inplay_status, customer_built,
                                  location, module, name, variant, event, event_action, event_category, event_label,
                                  stream_active, stream_ID, **kwargs):
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value='success')
        normalize = kwargs.get('normalize_name')
        if normalize:
            actual_response['ecommerce']['add']['products'][0]['name'] = normalize_name(actual_response['ecommerce']['add']['products'][0]['name'])
        actual_response['ecommerce']['add']['products'][0]['brand'] = actual_response['ecommerce']['add']['products'][0]['brand'].lower()
        expected_response = {
            'event': event,
            'eventCategory': event_category,
            'eventAction': event_action,
            'eventLabel': event_label,
            'ecommerce': {
                'add': {
                    'products': [
                        {
                            'name': name,
                            'category': str(category),
                            'variant': str(variant),
                            'brand': brand.lower(),
                            'dimension60': str(event_id),
                            'dimension61': str(selection_id),
                            'dimension62': inplay_status,
                            'dimension63': customer_built,
                            'dimension64': str(location),
                            'dimension65': module
                        }
                    ]
                }
            }
        }
        if kwargs.get('dimension86', False) is not False:
            expected_response['ecommerce']['add']['products'][0].update({'dimension86': kwargs['dimension86']})
        if kwargs.get('dimension87', False) is not False:
            expected_response['ecommerce']['add']['products'][0].update({'dimension87': kwargs['dimension87']})
        if kwargs.get('dimension88', False) is not False:
            expected_response['ecommerce']['add']['products'][0].update({'dimension88': kwargs['dimension88']})
        if kwargs.get('dimension166', False) is not False:
            expected_response['ecommerce']['add']['products'][0].update({'dimension166': kwargs['dimension166']})
        if kwargs.get('dimension177', False) is not False:
            expected_response['ecommerce']['add']['products'][0].update({'dimension177': kwargs['dimension177']})
        if kwargs.get('dimension180', False) is not False:
            expected_response['ecommerce']['add']['products'][0].update({'dimension180': kwargs['dimension180']})
        if kwargs.get('quantity', False) is not False:
            expected_response['ecommerce']['add']['products'][0].update({'quantity': kwargs['quantity']})
        if kwargs.get('metric1', False) is not False:
            expected_response['ecommerce']['add']['products'][0].update({'metric1': kwargs['metric1']})
        self.compare_json_response(actual_response, expected_response)


class BaseYourCallTrackingTest(BaseDataLayerTest):
    proxy = tests.settings.banach_socks_proxy_hostname

    def verify_tracking_of_expanding_collapsing_market_accordion(self, accordion_action):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'your call',
        EXPECTED: 'eventAction' : 'build bet',
        EXPECTED: 'eventLabel' : 'expand market accordion' })
        """
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel',
                                                              object_value=accordion_action)
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'your call',
                             'eventAction': 'build bet',
                             'eventLabel': accordion_action,
                             }
        self.compare_json_response(actual_response, expected_response)

    def verify_tracking_of_added_selections(self, market_name):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'your call',
        EXPECTED: 'eventAction' : 'match bet',
        EXPECTED: 'sportName' : '<< SPORT NAME >>',
        EXPECTED: 'eventName' : '<< EVENT NAME >>',
        EXPECTED: 'eventID' : '<< EVENT ID >>'})
        """
        actual_response = self.get_data_layer_specific_object(object_key='eventCategory', object_value='your call')
        expected_response = {'event': 'trackEvent',
                             'eventAction': market_name,
                             'eventCategory': 'your call',
                             'eventID': int(self.eventID),
                             'eventName': f'{self.team1} v {self.team2}',
                             'sportName': 'Football'
                             }
        self.compare_json_response(actual_response, expected_response)

    def verify_tracking_of_deselecting_selection(self, place_of_action):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'your call',
        EXPECTED: 'eventAction' : 'dashboard',
        EXPECTED: 'eventLabel' : 'remove selection'})
        """
        actual_response = self.get_data_layer_specific_object(object_key='eventAction',
                                                              object_value=place_of_action)
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'your call',
                             'eventAction': place_of_action,
                             'eventLabel': 'remove selection'
                             }
        self.compare_json_response(actual_response, expected_response)

    def verify_tracking_of_removing_selection(self, market_name, place_of_action):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'your call',
        EXPECTED: 'eventAction' : 'dashboard',
        EXPECTED: 'eventLabel' : 'remove selection'
        EXPECTED: 'market' : '<< MARKET >>' })
        """
        actual_response = self.get_data_layer_specific_object(object_key='eventAction',
                                                              object_value=place_of_action)
        actual_response['market'] = actual_response['market'].title()
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'your call',
                             'eventAction': place_of_action,
                             'eventLabel': 'remove selection',
                             'market': market_name.title()
                             }
        self.compare_json_response(actual_response, expected_response)
