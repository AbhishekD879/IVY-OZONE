import random
from datetime import datetime, timedelta
from time import sleep

import pytest
import pytz
from dateutil.parser import parse
from tzlocal import get_localzone
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter, exists_filter, prune
from crlat_siteserve_client.siteserve_client import SiteServeRequests

import tests
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.datafabric.datafabric import Datafabric
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.waiters import wait_for_result
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.critical
@pytest.mark.races
@pytest.mark.horseracing
@pytest.mark.navigation
@pytest.mark.desktop
@pytest.mark.screen_resolution
@pytest.mark.hotfix
@pytest.mark.sanity
@vtest
class Test_C874353_Navigation_Horse_Racing(BaseRacing):
    """
    TR_ID: C874353
    NAME: Navigation Horse Racing
    PRECONDITIONS: Open Oxygen app
    """
    keep_browser_open = True
    maximized_browser = False
    enable_bs_performance_log = True

    def get_events(self):
        horse_category_id = self.ob_config.backend.ti.horse_racing.category_id

        base_query_params = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_FLAG_CODES, OPERATORS.NOT_INTERSECTS, 'SP')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL, self.start_date)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN_OR_EQUAL, self.start_date_minus)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CLASS_ID, OPERATORS.NOT_INTERSECTS, '227')) \
            .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.DRILLDOWN_TAG_NAMES, OPERATORS.NOT_INTERSECTS, 'MKTFLAG_SP'))) \
            .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.DRILLDOWN_TAG_NAMES, OPERATORS.NOT_CONTAINS, 'EVFLAG_AP')))

        horse_query_params = base_query_params \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.INTERSECTS, horse_category_id)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_FLAG_CODES, OPERATORS.INTERSECTS, 'UK,IE'))
        horse_events = self.ss_req_horses.ss_event_to_outcome_for_class(query_builder=horse_query_params)

        virtual_horses_events = []
        if tests.settings.backend_env == 'prod':
            virtuals_category_id = self.ob_config.backend.ti.virtuals.category_id
            virtual_horse_query_params = base_query_params \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.INTERSECTS, virtuals_category_id)) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_FLAG_CODES, OPERATORS.INTERSECTS, 'VR'))
            virtual_horses_events = self.ss_req_virtual_horses.ss_event_to_outcome_for_class(query_builder=virtual_horse_query_params)

        return horse_events + virtual_horses_events

    @staticmethod
    def sort_events_by_type(response):
        events_from_response = {'UK': [], 'IE': [], 'VR': []}
        events_with_outcomes = []
        for event in response:
            if event['event'].get('children'):
                markets = event['event'].get('children')
                for market in markets:
                    if market.get('market').get('children'):
                        events_with_outcomes.append(event)
                        break

        all_events = []
        for event in events_with_outcomes:
            if event['event'].get('typeFlagCodes'):
                flag_codes = event['event'].get('typeFlagCodes').split(',')[:-1]
                for flag in flag_codes:
                    if flag in events_from_response.keys():
                        if event['event']['typeName'] not in all_events:
                            events_from_response[flag].append(event['event']['typeName'])
                            all_events.append(event['event']['typeName'])
                        break

        events_from_response['UK,IE'] = events_from_response['UK']
        events_from_response['UK,IE'].extend(events_from_response['IE'])

        del events_from_response['UK']
        del events_from_response['IE']

        return events_from_response

    def get_expected_race_grid_accordions(self):
        expected_race_grid_accordions = []
        meetings = self.sort_events_by_type(self.get_events())
        for meeting_code in meetings:
            if meetings[meeting_code]:
                accordion = self.type_flag_codes[meeting_code] \
                    if self.device_type == 'desktop' and self.brand != 'ladbrokes' else self.type_flag_codes[
                    meeting_code].upper()
                expected_race_grid_accordions.append(accordion)
        return expected_race_grid_accordions

    def verify_accordions_placed_under_each_other(self, accordions: list):
        """
        Method verifies that accordions are placed under each other according to the placed order in the list

        :param accordions: List that contains accordions to verify
        """
        accordions = [module for module in accordions if module]
        first_module = accordions[0]
        for module in accordions[1:]:
            self.assertTrue(first_module.location['y'] < module.location['y'],
                            msg=f'Module "{first_module.name}" with "y" coordinate "{first_module.location["y"]}" is '
                            f'not placed above module "{module.name}" with "y" coordinate "{module.location["y"]}"')
            first_module = module

    def verify_accordions_placed_in_the_second_column(self, first_column_module, accordions: list):
        """
        Method verifies that accordions are placed in the second column

        :param first_column_module: Any module that placed in first column to get it's 'x' coordinate
        :param accordions: List that contains accordions from second column to verify
        """
        accordions = [module for module in accordions if module]
        first_column_x_coordinate = first_column_module.location['x']
        for module in accordions:
            self.assertTrue(first_column_x_coordinate + 50 < module.location['x'],
                            msg=f'Module "{module.name}" is not placed in the second column')

    def get_ss_event_name(self, event) -> str:
        event_name = event.get('event').get('name')
        return ' '.join(event_name.split()[1:])

    def is_post_info_present_for_ss_event(self, event, event_id) -> bool:
        if event.get('document'):
            return all(key in event.get('document').get(event_id) and event.get('document').get(event_id).get(key)
                       for key in ['verdict', 'newspapers', 'courseGraphicsLadbrokes', 'horses'])
        else:
            return False

    def is_race_distance_present_for_ss_event(self, event, event_id) -> bool:
        if event.get('document'):
            return bool(event.get('document').get(event_id).get('distance'))
        else:
            return False

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add or find events
        DESCRIPTION: Load Oxygen application
        """
        self.__class__.type_flag_codes = {'UK,IE': vec.racing.UK_AND_IRE_TYPE_NAME,
                                          'VR': vec.virtuals.VIRTUAL_SPORTS}
        self.__class__.ss_req_horses = SiteServeRequests(env=tests.settings.backend_env,
                                                         class_id=self.ob_config.backend.ti.horse_racing.class_ids,
                                                         category_id=self.ob_config.backend.ti.horse_racing.category_id,
                                                         brand=self.brand)

        next_races_status = self.get_initial_data_system_configuration().get('NextRacesToggle', {}).get('nextRacesTabEnabled')
        if not next_races_status:
            next_races_status = self.cms_config.get_system_configuration_item('NextRacesToggle').get('nextRacesTabEnabled')

        self._logger.debug(f'*** Next Races CMS enable status is "{next_races_status}"')
        self.__class__.next_races_available = False if self.brand == 'ladbrokes' else next_races_status  # coral only, ladbrokes has separate tab and it's present always

        data_fabric = Datafabric()

        if tests.settings.backend_env != 'prod':
            event = self.ob_config.add_UK_racing_event(time_to_start=20,
                                                       market_extra_place_race=True,
                                                       perform_stream=True,
                                                       at_races_stream=True,
                                                       forecast_available=True,
                                                       tricast_available=True,
                                                       ew_terms=self.ew_terms)

            self.__class__.event_name = f'{event.event_off_time} {self.horseracing_autotest_uk_name_pattern}'
            event_id = event.event_id
            self.__class__.enhanced_races_available = True
            self.__class__.event_off_time = event.event_off_time
            self.__class__.meeting_name = self.horseracing_autotest_uk_name_pattern
            self.__class__.has_countdown_timer = True
            if self.brand == 'ladbrokes':
                if self.device_type == 'desktop':
                    self.__class__.enhanced_event_name = f"{vec.racing.EXTRA_PLACE_TITLE} - {event.event_off_time} {self.horseracing_autotest_uk_name_pattern[:4]}"
                else:
                    self.__class__.enhanced_event_name = f"{vec.racing.EXTRA_PLACE_TITLE.title()} - {event.event_off_time} {self.horseracing_autotest_uk_name_pattern[:4]}"
            else:
                self.__class__.enhanced_event_name = f"{vec.racing.EXTRA_PLACE_TITLE} - {event.event_off_time} {self.horseracing_autotest_uk_name_pattern}"
            self.__class__.has_stream_expected = True

            event2 = self.ob_config.add_UK_racing_event(time_to_start=30,
                                                        market_extra_place_race=True,
                                                        perform_stream=True,
                                                        at_races_stream=True,
                                                        forecast_available=True,
                                                        tricast_available=True,
                                                        ew_terms=self.ew_terms)
            event_id_2 = event2.event_id
            self.__class__.event_name2 = f'{event2.event_off_time} {self.horseracing_autotest_uk_name_pattern}'
            self.__class__.has_stream_expected2 = True
            self.__class__.meeting_name2 = self.horseracing_autotest_uk_name_pattern
        else:
            watch_live_flags = ['EVFLAG_AVA', 'EVFLAG_IVM', 'EVFLAG_PVM', 'EVFLAG_RVA', 'EVFLAG_RPM', 'EVFLAG_GVM']

            self.__class__.ss_req_virtual_horses = SiteServeRequests(env=tests.settings.backend_env,
                                                                     class_id=self.ob_config.backend.ti.virtuals.virtual_horseracing.class_id,
                                                                     category_id=self.ob_config.backend.ti.virtuals.category_id,
                                                                     brand=self.brand)

            query_builder = self.basic_active_events_filter()
            query = query_builder. \
                add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')). \
                add_filter(exists_filter(LEVELS.EVENT,
                                         simple_filter(LEVELS.MARKET, ATTRIBUTES.DRILLDOWN_TAG_NAMES,
                                                       OPERATORS.INTERSECTS, 'MKTFLAG_EPR'))). \
                add_filter(simple_filter(LEVELS.MARKET, ATTRIBUTES.TEMPLATE_MARKET_NAME, OPERATORS.EQUALS,
                                         self.ob_config.horseracing_config.default_market_name)). \
                add_filter(prune(LEVELS.EVENT)). \
                add_filter(prune(LEVELS.MARKET))
            events = self.ss_req_horses.ss_event_to_outcome_for_class(query_builder=query)
            event = next((event for event in events if
                          event.get('event') and event['event'] and event['event'].get('children')), None)
            if event:
                start_time = event.get('event').get('startTime')
                timezone = str(get_localzone())
                self._logger.debug(f'*** Current timezone is: "{timezone}"')
                if datetime.now(tz=pytz.timezone(timezone)) + timedelta(minutes=30) > parse(start_time):
                    self.__class__.has_countdown_timer = True
                else:
                    self.__class__.has_countdown_timer = False

                enhanced_event_name = event.get('event').get('name')
                event_off_time, meeting_name = enhanced_event_name.split()[0], ' '.join(enhanced_event_name.split()[1:])

                if self.brand == 'ladbrokes':
                    if self.device_type == 'desktop':
                        self.__class__.enhanced_event_name = f"{vec.racing.EXTRA_PLACE_TITLE} - {event_off_time} {meeting_name[:4]}"
                    else:
                        self.__class__.enhanced_event_name = f"{vec.racing.EXTRA_PLACE_TITLE.title()} - {event_off_time} {meeting_name[:4]}"
                else:
                    self.__class__.enhanced_event_name = f"{vec.racing.EXTRA_PLACE_TITLE} - {event_off_time} {meeting_name}"

                self.__class__.enhanced_races_available = True
            else:
                self.__class__.enhanced_races_available = False

            query_params = self.basic_active_events_filter() \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.INTERSECTS,
                                          self.ob_config.backend.ti.horse_racing.category_id)) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_FLAG_CODES, OPERATORS.INTERSECTS, 'UK,IE')) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_FALSE)) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_RESULTED, OPERATORS.IS_FALSE)) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CLASS_ID, OPERATORS.NOT_INTERSECTS, '227')) \
                .add_filter(simple_filter(LEVELS.MARKET, ATTRIBUTES.TEMPLATE_MARKET_NAME, OPERATORS.EQUALS,
                                          self.ob_config.horseracing_config.default_market_name)) \
                .add_filter(exists_filter(LEVELS.EVENT,
                                          simple_filter(LEVELS.MARKET, ATTRIBUTES.DRILLDOWN_TAG_NAMES,
                                                        OPERATORS.NOT_INTERSECTS, 'MKTFLAG_SP')))
            events = self.ss_req_horses.ss_event_to_outcome_for_class(query_builder=query_params)

            test_events = []
            for event in events:
                if next((event for event in events if
                         event.get('event') and event['event'] and event['event'].get('children')), None):
                    event_id = event.get('event').get('id')
                    event_info = data_fabric.get_datafabric_data(event_id=event_id,
                                                                 category_id=self.ob_config.backend.ti.horse_racing.category_id)
                    self.__class__.has_race_distance_info = self.is_race_distance_present_for_ss_event(
                        event=event_info,
                        event_id=event_id)
                    self.__class__.has_racing_post_verdict = self.is_post_info_present_for_ss_event(event=event_info,
                                                                                                    event_id=event_id)

                    if test_events and test_events[0].get('event').get('typeId') == event.get('event').get('typeId'):
                        continue
                    else:
                        if self.has_race_distance_info and self.has_racing_post_verdict:
                            test_events.append(event)
                    if len(test_events) >= 2:
                        break

            if len(test_events) < 2:
                raise SiteServeException(f'Less than 2 events with Post Info and Race Distance found to perform the test. '
                                         f'Number of events available: "{len(test_events)}"')

            event, event2 = test_events

            # First event
            event_id = event.get('event').get('id')

            self.__class__.event_name = event.get('event').get('name')
            event_off_time = self.event_name.split()[0]
            self.__class__.event_off_time = event_off_time
            self.__class__.meeting_name = event.get('event').get('typeName')

            if not any(flag in event['event'].get('drilldownTagNames', '') for flag in watch_live_flags):
                self.__class__.has_stream_expected = False
            else:
                self.__class__.has_stream_expected = True

            # Second event
            event_id_2 = event2.get('event').get('id')
            self.__class__.event_name2 = event2.get('event').get('name')
            self.__class__.meeting_name2 = event2.get('event').get('typeName')

            if not any(flag in event2['event']['drilldownTagNames'] for flag in watch_live_flags):
                self.__class__.has_stream_expected2 = False
            else:
                self.__class__.has_stream_expected2 = True

        self.__class__.event_off_time2 = self.event_name2.split()[0]

        self._logger.info(f'*** Found first event with id "{event_id}", name "{self.event_name}" and meeting name "{self.meeting_name}')
        self._logger.info(f'*** Found second event with id "{event_id_2}", name "{self.event_name2}" and meeting name "{self.meeting_name2}')

        event_info_1 = data_fabric.get_datafabric_data(event_id=event_id,
                                                       category_id=self.ob_config.backend.ti.horse_racing.category_id)
        self.__class__.has_race_distance_info = self.is_race_distance_present_for_ss_event(event=event_info_1,
                                                                                           event_id=event_id)
        self.__class__.has_racing_post_verdict = self.is_post_info_present_for_ss_event(event=event_info_1,
                                                                                        event_id=event_id)
        event_info_2 = data_fabric.get_datafabric_data(event_id=event_id_2,
                                                       category_id=self.ob_config.backend.ti.horse_racing.category_id)
        self.__class__.has_race_distance_info_2 = self.is_race_distance_present_for_ss_event(event=event_info_2,
                                                                                             event_id=event_id_2)
        self.__class__.has_racing_post_verdict_2 = self.is_post_info_present_for_ss_event(event=event_info_2,
                                                                                          event_id=event_id_2)

        self.navigate_to_page(name='/')
        self.site.wait_content_state('Homepage')
        if self.device_type == 'desktop':
            self.device.set_viewport_size(width=1600, height=1280)

    def test_001_click_on_horse_racing_button_from_the_main_menu(self):
        """
        DESCRIPTION: Click on Horse Racing button from the Main Menu
        EXPECTED: 1. Horse Racing Page is loaded
        EXPECTED: 2. The Featured tab is selected by default
        EXPECTED: 3. "Enhanced Races" (if available) is displayed on the top of the page
        EXPECTED: 4. Under the "Enhanced Races" > "Next Races" module
        EXPECTED: 5. 'Starts in' label with countdown clock “MM:SS” is available for events that start less than 45 minutes in 'Next Races’ > REMOVED FOR NOW: Once next race status is received, it is displayed on corresponding badges
        EXPECTED: 6. "UK & IRE" section is displayed followed by "International" ( divided by coutries) and then "Virtual"
        EXPECTED: 7. "Enhanced Multiples" module (if available) is displayed below  "International"
        EXPECTED: 8. The Horse Racing meetings with video stream available should be marked with "Play" icon
        EXPECTED: On Desktop:
        EXPECTED: - Enhanced Multiples carousel (if available)
        EXPECTED: - "UK & IRE" section is displayed followed by "International" and then "Virtual"
        EXPECTED: **For screen width > 970 px, 1025px next accordions are displayed below in main display area
        EXPECTED: **For screen width 1280px, 1600px next accordions are displayed on the second column of the display area
        EXPECTED: - "Next Races" module
        EXPECTED: - "Enhanced Races" module
        EXPECTED: - "Virtuals" carousel
        EXPECTED: - "YourCall Specials" module
        """
        self.site.open_sport(self.get_sport_title(category_id=self.ob_config.horseracing_config.category_id))

        expected_accordions_names = self.get_expected_race_grid_accordions()
        self._logger.debug(f'*** Expected accordion list is "{expected_accordions_names}"')

        current_tab_name = self.site.horse_racing.tabs_menu.current
        self.assertEqual(current_tab_name, vec.racing.RACING_DEFAULT_TAB_NAME,
                         msg=f'Default tab is "{current_tab_name}" not "{vec.racing.RACING_DEFAULT_TAB_NAME}" tab')

        bypass_exceptions = (NoSuchElementException, StaleElementReferenceException, VoltronException)
        accordions = wait_for_result(lambda: self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict,
                        timeout=5,
                        bypass_exceptions=bypass_exceptions)
        self.assertTrue(accordions, msg='Accordion list is empty on Horse Racing page')

        enhanced_races_module = None
        if self.enhanced_races_available:
            module_name = self.enhanced_races_name
            enhanced_races_module = accordions.get(module_name)
            self.assertTrue(enhanced_races_module, msg=f'"{module_name}" is not found in {accordions.keys()}')
            if not enhanced_races_module.is_expanded():
                enhanced_races_module.expand()
            if self.device_type == 'mobile':
                # adapt this block of code for 101 branch for Desktop version
                # for 100.2.x this verification is skipped on Desktop execution due to attr issue
                events = enhanced_races_module.items_as_ordered_dict
                self.assertTrue(events, msg=f'No events found in "{module_name}" section')
                self.assertIn(self.enhanced_event_name, list(events.keys()),
                              msg=f'Event "{self.enhanced_event_name}" does not located in "{list(events.keys())}"')
                if self.brand != 'ladbrokes':
                    event = events[self.enhanced_event_name]
                    self.assertEqual(event.has_countdown_timer, self.has_countdown_timer,
                                     msg=f'Event countdown timer presence status is not "{self.has_countdown_timer}"')
        else:
            self._logger.warning(f'*** Verification for module "Enhanced races" is skipped as this module is disabled')

        next_races_module = None
        if self.next_races_available:
            next_races_name = vec.racing.NEXT_RACES.upper() if self.device_type == 'mobile' else vec.racing.NEXT_RACES
            next_races_module = accordions.get(next_races_name)
            self.assertTrue(next_races_module, msg=f'"{next_races_name}" is not found in {accordions.keys()}')
        else:
            self._logger.warning(f'*** Verification for module "Next Races" is skipped as this module is disabled')

        uk_and_ire_module = None
        if vec.racing.UK_AND_IRE_TYPE_NAME in expected_accordions_names:
            uk_and_ire_module = accordions.get(vec.racing.UK_AND_IRE_TYPE_NAME)
            self.assertTrue(uk_and_ire_module, msg=f'"{vec.racing.UK_AND_IRE_TYPE_NAME}" is not found in {accordions.keys()}')
        else:
            self._logger.warning(f'*** Verification for module "Enhanced races" is skipped as this module is disabled')

        international_module = None
        if self.brand != 'ladbrokes':
            international_module = self.site.horse_racing.tab_content.international_label
            expected_international_name = vec.racing.INTERNATIONAL_TYPE_NAME.upper() if self.device_type == 'mobile' \
                else vec.racing.INTERNATIONAL_TYPE_NAME.title()

            self.assertEqual(international_module.name, expected_international_name,
                             msg=f'Actual module name "{international_module.name}" != Expected "{expected_international_name}"')
        else:
            self._logger.warning(f'*** Verification for "International" module is skipped as this module is disabled')

        virtuals_module = None
        if vec.virtuals.VIRTUAL_SPORTS in expected_accordions_names:
            virtuals_module = accordions.get(vec.virtuals.VIRTUAL_SPORTS)
            self.assertTrue(virtuals_module, msg=f'"{vec.virtuals.VIRTUAL_SPORTS}" is not found in {accordions.keys()}')
        else:
            self._logger.warning(f'*** Verification for "Virtuals" module is skipped as this module is disabled')

        if self.device_type == 'desktop':
            yourcall_specials = accordions.get(vec.racing.YOURCALL_SPECIALS.upper())
            accordions = [next_races_module, enhanced_races_module, virtuals_module, yourcall_specials]
            self.verify_accordions_placed_in_the_second_column(first_column_module=uk_and_ire_module,
                                                               accordions=accordions)
            accordions_order = [uk_and_ire_module,
                                international_module]
            self.verify_accordions_placed_under_each_other(accordions_order)
        else:
            accordions_order = [enhanced_races_module,
                                next_races_module,
                                uk_and_ire_module,
                                international_module,
                                virtuals_module]
            self.verify_accordions_placed_under_each_other(accordions_order)

    def test_002_click_on_specials_if_available_yourcall_results_tabs(self):
        """
        DESCRIPTION: Click on Specials (if available)/Yourcall/Results tabs
        EXPECTED: Check that each tab loads proper information
        """
        expected_tabs = [vec.racing.RACING_SPECIALS_TAB_NAME,
                         vec.racing.RACING_RESULTS_TAB_NAME]
        self.__class__.horse_racing_ui_tabs = self.site.horse_racing.tabs_menu.items_as_ordered_dict
        self.assertTrue(self.horse_racing_ui_tabs, msg='There is no tabs on horse racing page')
        for tab in expected_tabs:
            if tab in self.horse_racing_ui_tabs.keys():
                self.horse_racing_ui_tabs[tab].click()
                if tab != vec.racing.RACING_YOURCALL_TAB_NAME:
                    self.assertTrue(self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict,
                                    msg=f'Accordion accordions are not found on Horse Racing page for tab "{tab}"')

    def test_003_navigate_to_featured_tab_and_select_any_horse_racing_event_eg_kempton_640(self):
        """
        DESCRIPTION: Navigate to Featured tab and select any Horse Racing event (e.g. Kempton 6:40)
        EXPECTED: 1. The Horse Racing event race card is loaded
        EXPECTED: 2. The meeting selector is available on the top of the page in format Horse Racing/*Type name* (opens an overlay)
        EXPECTED: 3. The event selector (time ribbon) is displayed right under the the meeting selector
        EXPECTED: 4. There is an are with the race details (name, distance, Racing Post info and Video stream button)
        EXPECTED: 5. The Win or Each Way market is selected by default
        EXPECTED: 6. Check that the Each Way terms is displayed right under the market name
        EXPECTED: 7. Check that the selections are correctly displayed (with silks - if available) and SP or LP
        """
        featured_tab = self.horse_racing_ui_tabs.get(vec.racing.RACING_DEFAULT_TAB_NAME)
        self.assertTrue(featured_tab,
                        msg=f'"{vec.racing.RACING_DEFAULT_TAB_NAME}" was not found in "{self.horse_racing_ui_tabs.keys()}"')
        featured_tab.click()
        sleep(5)
        edp_meeting_name = self.meeting_name.upper() if self.brand != 'ladbrokes' else self.meeting_name
        self.open_racing_event_details(section_name=self.uk_and_ire_type_name,
                                       meeting_name=edp_meeting_name,
                                       event_off_time=self.event_off_time)
        if self.site.wait_for_stream_and_bet_overlay():
            self.site.stream_and_bet_overlay.close_button.click()
        edp = self.site.racing_event_details
        breadcrumbs = edp.breadcrumbs.items_as_ordered_dict
        self.assertTrue(breadcrumbs, msg='No breadcrumbs found')

        breadcrumbs = list(breadcrumbs.keys())

        if self.device_type in ['mobile', 'tablet']:
            if self.meeting_name.find(breadcrumbs[1]) == -1:
                breadcrumbs[1] = self.meeting_name
            expected_breadcrumbs = [vec.sb.HORSERACING, self.meeting_name]
            self.assertEqual(breadcrumbs, expected_breadcrumbs,
                             msg=f'Breadcrumbs "{breadcrumbs}" are not the same as expected "{expected_breadcrumbs}"')
            self.assertTrue(self.site.racing_event_details.breadcrumbs.toggle_icon.is_displayed(),
                            msg='Toggle icon is not displayed')
        else:
            expected_breadcrumbs = ['Home', vec.sb.HORSERACING, self.meeting_name.title()]
            self.assertEqual(expected_breadcrumbs, breadcrumbs,
                             msg=f'Breadcrumbs {breadcrumbs} are not the same as expected {expected_breadcrumbs}')

        if self.brand != 'ladbrokes':
            self.assertTrue(edp.is_back_button_displayed(), msg='Back button was not found')
        else:
            self.assertTrue(self.site.has_back_button, msg='Back button was not found')
        self.assertTrue(self.site.racing_event_details.has_meeting_selector(), msg='Meeting selector was not found')

        tab_content = edp.tab_content
        self.assertTrue(tab_content.has_event_off_times_list(expected_result=True),
                        msg='"Event selector" ribbon is not found')
        self.assertEqual(tab_content.race_details.has_race_distance(expected_result=self.has_race_distance_info), self.has_race_distance_info,
                         msg=f'Distance presence status is not "{self.has_race_distance_info}"')
        self.assertEqual(tab_content.has_post_info(expected_result=self.has_racing_post_verdict), self.has_racing_post_verdict,
                         msg=f'"Racing Post" presence status is not "{self.has_racing_post_verdict}"')
        self.assertEqual(tab_content.has_video_stream_button(expected_result=self.has_stream_expected), self.has_stream_expected,
                         msg=f'"Video Stream" button status expected to be "{self.has_stream_expected}" but it '
                         f'is "{not self.has_stream_expected}"')
        actual_event_name = tab_content.race_details.event_title
        self.assertEqual(actual_event_name, self.event_name,
                         msg=f'Event name "{actual_event_name}" is not the same as expected "{self.event_name}"')

        current_tab = tab_content.event_markets_list.current_market_tab_name
        try:
            self.assertEqual(current_tab, vec.racing.RACING_EDP_DEFAULT_MARKET_TAB,
                             msg=f'{vec.racing.RACING_EDP_DEFAULT_MARKET_TAB} is not opened by default, '
                             f'instead "{current_tab}" is opened')
        except Exception:
            self._logger.info(f'{vec.racing.RACING_EDP_DEFAULT_MARKET_TAB} is not opened by default, '
                              f'instead "{current_tab}" is opened')
            market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
            for market_name, market_value in market_tabs.items():
                if market_name == vec.racing.RACING_EDP_DEFAULT_MARKET_TAB:
                    market_value.click()
                    self.site.wait_splash_to_hide(5)
                    current_tab = tab_content.event_markets_list.current_market_tab_name
                    self.assertEqual(current_tab, vec.racing.RACING_EDP_DEFAULT_MARKET_TAB,
                                     msg=f'Expected tab: {vec.racing.RACING_EDP_DEFAULT_MARKET_TAB} is not '
                                         f'same as Actual tab: "{current_tab}" is opened')
                    break

        market_list_tabs = tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(market_list_tabs, msg='Event market list is empty')
        ew_tab = market_list_tabs.get(vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)
        self.assertTrue(ew_tab, msg=f'"{vec.racing.RACING_EDP_DEFAULT_MARKET_TAB}" tab was not found')

        self.assertTrue(ew_tab.has_header(), msg='Each Way terms is not displayed')

        event_selections = ew_tab.items_as_ordered_dict
        self.assertTrue(event_selections, msg='Horse racing selection list is empty')

        for horse_name, selection in event_selections.items():
            self.assertTrue(horse_name, msg='Selection Horse name is not displayed')
            self.assertTrue(selection.bet_button.outcome_price, msg='Price for selection is not displayed')
            if tests.settings.backend_env == 'prod':
                if horse_name not in [vec.racing.UNNAMED_FAVORITE, vec.racing.UNNAMED_FAVORITE_2ND] and not selection.is_non_runner:
                    self.assertTrue(selection.has_silks, msg=f'Selection {selection.name} silk is not displayed')
            else:
                self._logger.warning(f'*** Automation created events does not contain silks, verification is skipped')

    def test_004_check_all_other_markets_of_the_event(self):
        """
        DESCRIPTION: Check all other markets of the event
        EXPECTED: Each market is correctly loaded showing the selections (Each Way terms - if available, silks - if available)
        """
        other_markets = list(self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict.items())[1:]
        self.assertTrue(other_markets, msg=f'There is no other markets except "{vec.racing.RACING_EDP_DEFAULT_MARKET_TAB}"')

        for name, market in other_markets:
            market.click()
            market_list_tabs = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
            self.assertTrue(market_list_tabs, msg='Event market list is empty')
            content = market_list_tabs.get(name)
            self.assertTrue(content, msg=f'"{name}" tab was not found')

            event_selections = content.items_as_ordered_dict if name != vec.racing.RACING_EDP_MARKET_TABS.totepool else content.pool.items_as_ordered_dict
            self.assertTrue(event_selections, msg='Horse racing selection list is empty')

            for horse_name, selection in event_selections.items():
                self.assertTrue(horse_name, msg='Selection Horse name is not displayed')
                selection_button_status = selection.bet_button.is_displayed() if name != vec.racing.RACING_EDP_MARKET_TABS.totepool else selection.items
                self.assertTrue(selection_button_status, msg='Selection button is not displayed')

    def test_005_select_a_different_meeting_from_the_meeting_selector(self):
        """
        DESCRIPTION: Select a different meeting from the meeting selector
        EXPECTED: The first event from the selected meeting should be loaded by default
        """
        self.site.racing_event_details.meeting_selector.click()
        result = wait_for_result(lambda: self.site.racing_event_details.meetings_list.is_displayed(), timeout=10)
        self.assertTrue(result, msg='Meetings list is not shown')

        sections = self.site.racing_event_details.meetings_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Meeting list is empty')

        if tests.settings.backend_env != 'prod':
            if self.device_type == 'mobile':
                other_international = sections.get(vec.racing.UK_AND_IRE_TYPE_NAME)
                self.assertTrue(other_international, msg=f'"{vec.racing.UK_AND_IRE_TYPE_NAME}" is not found in meeting list')
                events_names = other_international.items_as_ordered_dict
                self.assertTrue(events_names, msg=f'Events list is empty for "{vec.racing.UK_AND_IRE_TYPE_NAME}"')
            else:
                events_names = sections

            names = list(events_names.keys())
            names.remove(self.meeting_name2)

            name_to_click = random.choice(names)
            events_names[name_to_click].click()

            self.site.racing_event_details.meeting_selector.click()
            self.assertTrue(self.site.racing_event_details.meetings_list.is_displayed(),
                            msg='Meetings list is not shown')

            sections = self.site.racing_event_details.meetings_list.items_as_ordered_dict
            self.assertTrue(sections, msg='Meeting list is empty')

        # if self.device_type == 'mobile':
        # the functionality as changed same as mobile for desktop to so there is no need of the below code
        uk_and_ire_type_name = next((name for name in sections.keys() if name.upper() == self.uk_and_ire_type_name.upper()),None)
        uk_and_ire = sections.get(uk_and_ire_type_name)
        self.assertTrue(uk_and_ire, msg=f'"{uk_and_ire_type_name}" is not found in "{sections.keys()}"')
        events_names = uk_and_ire.items_as_ordered_dict
        event_items = list(uk_and_ire.items_as_ordered_dict.values())
        self.assertTrue(events_names, msg=f'Events list is empty for "{self.uk_and_ire_type_name}"')
        count = 0
        if self.brand == "bma" and self.device_type == 'mobile':
            self.meeting_name2 = self.meeting_name2.upper()
        for meeting in range(len(event_items)):
            if event_items[meeting].name in self.meeting_name2:
                for event in range(len(event_items[meeting].items)):
                    if event_items[meeting].items[event].is_resulted() is not True:
                        event_items[meeting].items[event].click()
                        count = 1
                        break
            if count == 1:
                break
        # else:
        #     events_names = sections
        #
        #     self.assertIn(self.meeting_name2, events_names,
        #                   msg=f'Meeting "{self.meeting_name2}" not found in "{events_names.keys()}"')
        #     events_names[self.meeting_name2].click()

        events_ribbon = self.site.racing_event_details.tab_content.event_off_times_list
        selected_event = events_ribbon.selected_item
        events = events_ribbon.items_as_ordered_dict
        self.assertTrue(events, msg='Events are not found in the events ribbon')
        expected_first_event = events_ribbon.get_first_available_event()
        self.assertEqual(selected_event, expected_first_event,
                         msg=f'Selected event is "{selected_event}" when expected event is "{expected_first_event}"')

    def test_006_select_a_different_event_from_the_event_selector(self):
        """
        DESCRIPTION: Select a different event from the event selector
        EXPECTED: The selected event is loaded
        """
        events_ribbon = self.site.racing_event_details.tab_content.event_off_times_list

        all_events = events_ribbon.items_as_ordered_dict
        self.assertTrue(all_events, msg='Events ribbon does not contain any event')

        event_to_open = all_events.get(self.event_off_time2)
        self.assertTrue(event_to_open, msg=f'Event with time "{self.event_off_time2}" does not found in Events ribbon')

        if not event_to_open.is_selected():
            event_to_open.click()
        if self.site.wait_for_stream_and_bet_overlay():
            self.site.stream_and_bet_overlay.close_button.click()

        edp = self.site.racing_event_details

        tab_content = edp.tab_content
        self.assertTrue(tab_content.has_event_off_times_list(expected_result=True),
                        msg='"Event selector" ribbon is not found')
        self.assertEqual(tab_content.race_details.has_race_distance(expected_result=self.has_race_distance_info_2),
                         self.has_race_distance_info_2,
                         msg=f'Distance presence status is not "{self.has_race_distance_info_2}"')
        self.assertEqual(tab_content.has_post_info(expected_result=self.has_racing_post_verdict_2),
                         self.has_racing_post_verdict_2,
                         msg=f'"Racing Post" presence status is not "{self.has_racing_post_verdict_2}"')
        self.assertEqual(tab_content.has_video_stream_button(expected_result=self.has_stream_expected2), self.has_stream_expected2,
                         msg=f'"Video Stream" button status expected to be "{self.has_stream_expected2}" but it '
                         f'is "{not self.has_stream_expected2}"')
        actual_event_name = tab_content.race_details.event_title
        self.assertIn(self.event_off_time2, actual_event_name,
                      msg=f'Event name "{self.event_off_time2}" is not the subpart as expected "{actual_event_name}"')

        current_tab = tab_content.event_markets_list.current_market_tab_name
        try:
            self.assertEqual(current_tab, vec.racing.RACING_EDP_DEFAULT_MARKET_TAB,
                             msg=f'{vec.racing.RACING_EDP_DEFAULT_MARKET_TAB} is not opened by default, '
                                 f'instead "{current_tab}" is opened')
        except Exception:
            self._logger.info(f'{vec.racing.RACING_EDP_DEFAULT_MARKET_TAB} is not opened by default, '
                              f'instead "{current_tab}" is opened')
            market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
            for market_name, market_value in market_tabs.items():
                if market_name == vec.racing.RACING_EDP_DEFAULT_MARKET_TAB:
                    market_value.click()
                    self.site.wait_splash_to_hide(5)
                    current_tab = tab_content.event_markets_list.current_market_tab_name
                    self.assertEqual(current_tab, vec.racing.RACING_EDP_DEFAULT_MARKET_TAB,
                                     msg=f'Expected tab: {vec.racing.RACING_EDP_DEFAULT_MARKET_TAB} is not '
                                         f'same as Actual tab: "{current_tab}" is opened')
                    break

        market_list_tabs = tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(market_list_tabs, msg='Event market list is empty')
        ew_tab = market_list_tabs.get(vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)
        self.assertTrue(ew_tab, msg=f'"{vec.racing.RACING_EDP_DEFAULT_MARKET_TAB}" tab was not found')

        self.assertTrue(ew_tab.has_header(), msg='Each Way terms is not displayed')

        event_selections = ew_tab.items_as_ordered_dict
        self.assertTrue(event_selections, msg=f'Selection list is empty')

        for horse_name, selection in event_selections.items():
            self.assertTrue(selection.bet_button.outcome_price,
                            msg=f'Price for selection "{horse_name}" is not displayed')
            if tests.settings.backend_env == 'prod':
                if horse_name not in [vec.racing.UNNAMED_FAVORITE, vec.racing.UNNAMED_FAVORITE_2ND] and not selection.is_non_runner:
                    self.assertTrue(selection.has_silks, msg=f'Selection {selection.name} silk is not displayed')
            else:
                self._logger.warning(f'*** Automation created events does not contain silks, verification is skipped')
