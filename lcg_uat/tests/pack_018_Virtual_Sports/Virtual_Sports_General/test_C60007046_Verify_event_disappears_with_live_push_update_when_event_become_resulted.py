import tests
import pytest
from time import sleep
from tenacity import retry, wait_fixed, stop_after_attempt
from crlat_siteserve_client.constants import ATTRIBUTES, LEVELS, OPERATORS
from crlat_siteserve_client.siteserve_client import SiteServeRequests, simple_filter, exists_filter
from tests.base_test import vtest
from json import JSONDecodeError
from random import choice
from tests.pack_018_Virtual_Sports.BaseVirtualsTest import BaseVirtualsTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import do_request
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - Can not suspend events on Prod/Beta
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.virtual_sports
@vtest
class Test_C60007046_Verify_event_disappears_with_live_push_update_when_event_become_resulted(BaseVirtualsTest):
    """
    TR_ID: C60007046
    NAME: Verify event disappears with live push update when event become resulted
    DESCRIPTION: This test case verifies that Virtual Sport event disappears with live push update when event become resulted
    PRECONDITIONS: Get SiteServer response to verify data:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/16231,289,288,285,286,287,290,291?simpleFilter=class.categoryId:equals:39&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&simpleFilter=event.typeId:notEquals:3048&simpleFilter=event.typeId:notEquals:3049&simpleFilter=event.typeId:notEquals:3123&simpleFilter=event.startTime:lessThanOrEqual:2016-04-18T16:28:45Z&simpleFilter=event.startTime:greaterThan:2016-04-18T09:28:45Z&translationLang=en
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: List of relevant class id's:
    PRECONDITIONS: Horse Racing class id 285
    PRECONDITIONS: Greyhounds class id 286
    PRECONDITIONS: Football class id 287
    PRECONDITIONS: Motorsports class id 288
    PRECONDITIONS: Speedway class id 289
    PRECONDITIONS: Cycling class id 290
    PRECONDITIONS: Tennis class id 291
    PRECONDITIONS: Grand National class id 26604
    """
    keep_browser_open = True

    @retry(stop=stop_after_attempt(10),
           wait=wait_fixed(wait=8),
           reraise=True)
    def wait_for_event_to_suspend(self, event_name):
        for i in range(len(self.return_response()['SSResponse']['children'])):
            if event_name == self.return_response()['SSResponse']['children'][i]['event']['name']:
                result = wait_for_result(
                    lambda: self.return_response()['SSResponse']['children'][i]['event']['eventStatusCode'] == 'S',
                    timeout=10, name='event to be suspended')
                return result

    def return_response(self):
        url = 'EventToOutcomeForEvent'
        perflog = self.device.get_performance_log()
        for log in list(reversed(perflog)):
            try:
                data_dict = log[1]['message']['message']['params']['request']
                request_url = data_dict['url']
                if url in request_url:
                    response_url = request_url
            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue
        self.assertTrue(response_url, msg='EventToOutcomeForEvent data is not received after unblocking request')
        response = do_request(method='GET', url=response_url)
        self.assertTrue(response, msg='No response received for the "EventToOutcomeForEvent" call')
        return response

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get list of active virtual sport categories
        """
        start_time = self.get_date_time_formatted_string(hours=1)
        self.ob_config.add_virtual_greyhound_racing_event(number_of_runners=1, start_time=start_time)
        self.ob_config.add_virtual_racing_event(number_of_runners=1, start_time=start_time)

        virtuals_cms_class_ids = self.cms_virtual_sports_class_ids()
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.ob_config.virtuals_config.category_id)
        sports_list = ss_req.ss_class(query_builder=self.ss_query_builder.
                                      add_filter(simple_filter(LEVELS.CLASS,
                                                               ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS,
                                                               str(self.ob_config.virtuals_config.category_id))))
        if not sports_list:
            raise SiteServeException('There are no active virtual sports')

        event = None
        ss_class_id = None
        for sport_class in sports_list:
            class_id = sport_class['class']['id']
            if not event:
                additional_filter = exists_filter(LEVELS.EVENT,
                                                  simple_filter(LEVELS.MARKET, ATTRIBUTES.NCAST_TYPE_CODES,
                                                                OPERATORS.INTERSECTS, 'CF,TC')), exists_filter(
                    LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.IS_EACH_WAY_AVAILABLE,
                                                OPERATORS.IS_TRUE))
                events = self.get_active_event_for_class(class_id=class_id,
                                                         additional_filters=additional_filter,
                                                         raise_exceptions=False)
                if events:
                    temp_event = choice(events)
                    temp_ss_class_id = temp_event['event']['classId']
                    if temp_ss_class_id in virtuals_cms_class_ids:
                        event = temp_event
                        ss_class_id = temp_ss_class_id

        if not event or not ss_class_id:
            raise SiteServeException('There are no available race virtual events')

        tab_name = self.cms_virtual_sport_tab_name_by_class_ids(class_ids=[ss_class_id])
        self.__class__.expected_tab = tab_name[0]

    def test_001_open_virtual_sports_page__horse_racing_virtual_sport_tab(self, expected_tab=None):
        """
        DESCRIPTION: Open Virtual Sports page > Horse Racing virtual sport tab
        EXPECTED: * The first track from CMS is displayed as default. The display order of the tracks should be as per the CMS.
        EXPECTED: * The 'Virtual Sports' page displayed with header contains all icons for the virtual, sorted as configured on CMS.
        """
        self.navigate_to_page('virtual-sports')
        self.site.virtual_sports.sport_carousel.open_tab(self.expected_tab if expected_tab is None else expected_tab)

    def test_002__wait_when_one_of_the_events_for_selected_virtual_sport_became_resultedor_make_one_of_the_events_for_selected_virtual_sport_resulted_in_ti(self):
        """
        DESCRIPTION: * Wait when one of the events for selected Virtual Sport became resulted
        DESCRIPTION: or
        DESCRIPTION: * Make one of the events for selected Virtual Sport resulted in TI
        EXPECTED: * Push update is received with result_conf = “y” parameter for this event
        EXPECTED: * Event disappears from UI
        """
        response = self.return_response()
        event_id = None
        for i in range(len(response['SSResponse']['children'])):
            if response['SSResponse']['children'][i]['event']['eventStatusCode'] == 'A':
                event_name = response['SSResponse']['children'][1]['event']['name']
                event_id = response['SSResponse']['children'][1]['event']['id']
                break
        if event_id is None:
            raise SiteServeException('No active events found')

        self.ob_config.change_event_state(event_id=event_id, displayed=True, active=False)
        sleep(9)
        result = self.wait_for_event_to_suspend(event_name=event_name)
        self.assertTrue(result, msg=f'Event with id: "{event_name}" is not suspended')
        try:
            virtual_sports_tabs = self.site.virtual_sports.tab_content.event_off_times_list
            if event_name.split(' ')[0] in virtual_sports_tabs.items_names:
                event = virtual_sports_tabs.items_as_ordered_dict.get(event_name.split(' ')[0])
                event.click()
                selections = self.site.virtual_sports.tab_content.event_markets_list.items_as_ordered_dict
                self.assertTrue(selections, msg='No selections found')
                for selection in selections.values():
                    self.assertFalse(selection.is_enabled(), msg='selection is suspended')
        except VoltronException as e:
            self._logger.info("No events found")
        self.ob_config.change_event_state(event_id=event_id, displayed=False, active=False)
        sleep(5)
        virtual_sports_tabs = self.site.virtual_sports.tab_content.event_off_times_list.items_names
        self.assertNotIn(event_name.split(' ')[0], virtual_sports_tabs,
                         msg=f'Event "{event_name}" is not disappeared from UI')

    def test_003_repeat_this_test_case_for_the_following_virtual_sportsgreyhoundsfootballmotorsportscyclingspeedwaytennisgrand_national(self):
        """
        DESCRIPTION: Repeat this test case for the following virtual sports:
        DESCRIPTION: Greyhounds
        DESCRIPTION: Football,
        DESCRIPTION: Motorsports,
        DESCRIPTION: Cycling,
        DESCRIPTION: Speedway,
        DESCRIPTION: Tennis
        DESCRIPTION: Grand National
        """
        sports = self.site.virtual_sports.sport_carousel.items_names.remove(self.expected_tab)
        if sports:
            for sport in sports:
                self.test_001_open_virtual_sports_page__horse_racing_virtual_sport_tab(expected_tab=sport)
                self.test_002__wait_when_one_of_the_events_for_selected_virtual_sport_became_resultedor_make_one_of_the_events_for_selected_virtual_sport_resulted_in_ti()
