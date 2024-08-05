import re
import pytest
import tests
import voltron.environments.constants as vec
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import SiteServeRequests, simple_filter, exists_filter, prune
from crlat_siteserve_client.utils.date_time import get_date_time_as_string
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.waiters import wait_for_haul
from voltron.utils.datafabric.datafabric import Datafabric


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.adhoc_suite
@pytest.mark.adhoc24thJan24
@pytest.mark.lad_beta2
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.event_details
@pytest.mark.reg167_fix
@pytest.mark.races
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C1049083_Verify_Horse_Race_Meeting_Selector(BaseRacing):
    """
    TR_ID: C1049083
    NAME: Verify Horse Race Meeting Selector
    PRECONDITIONS: - '**typeName' **to check race meetings name;
    PRECONDITIONS: - **'typeFlagCodes'** to verify a race group
    PRECONDITIONS: *   'UK' or 'IE' parameter, this event should be included in the group 'UK & IRE'
    PRECONDITIONS: *   **'**INT' parameter, this event should be included to the 'INT' group
    PRECONDITIONS: *   'VR' parameter, this event should be included in the 'VR' group
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    end_date = f'{get_date_time_as_string(days=0)}T23:59:59.999Z'
    start_date = f'{get_date_time_as_string(days=-1)}T23:59:59.999Z'
    start_date_minus = f'{get_date_time_as_string(days=-1)}T23:59:59.999Z'

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

    @staticmethod
    def sort_events_by_type(response):
        events_from_response = {'UK': [], 'IE': [], 'FR': [], 'IN': [], 'AE': [], 'CL': [], 'AU': [], 'US': [],
                                'ZA': [], 'INT': [], 'VR': []}
        events_with_outcomes = []
        for event in response:
            if event['event'].get('children'):
                markets = event['event'].get('children')
                for market in markets:
                    if market.get('market').get('children'):
                        events_with_outcomes.append(event)

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

        return events_from_response

    def base_filter(self):
        return self.basic_active_events_filter() \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.INTERSECTS, self.ob_config.backend.ti.horse_racing.category_id))\
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M'))\
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CLASS_ID, OPERATORS.NOT_INTERSECTS, '227')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.NAME, OPERATORS.NOT_EQUALS, '%7Cnull%7C')) \
            .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.DRILLDOWN_TAG_NAMES,
                                                                  OPERATORS.NOT_INTERSECTS, 'MKTFLAG_SP'))) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.DRILLDOWN_TAG_NAMES, OPERATORS.NOT_CONTAINS, 'EVFLAG_AP'))

    def get_events(self):
        query_params = self.base_filter() \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_FLAG_CODES, OPERATORS.NOT_INTERSECTS, 'SP'))
        events = self.ss_req_hr.ss_event_to_outcome_for_class(query_builder=query_params)

        # meeting selector will show same as mobile as per new update story OZONE-5872--GRAY HOUNDS and OZONE-3480 horse racing
        # if self.device_type == 'desktop':
        #     query_params = self.base_filter() \
        #         .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_FLAG_CODES, OPERATORS.CONTAINS, 'SP')) \
        #         .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_FLAG_CODES, OPERATORS.INTERSECTS, 'UK'))
        #     events += self.ss_req_hr.ss_event_to_outcome_for_class(query_builder=query_params)
        #     query_params = self.base_filter() \
        #         .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_FLAG_CODES, OPERATORS.CONTAINS, 'SP')) \
        #         .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_FLAG_CODES, OPERATORS.INTERSECTS, 'INT'))
        #     events += self.ss_req_hr.ss_event_to_outcome_for_class(query_builder=query_params)

        return events

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create racing event in TI
        """
        self.__class__.ss_req_hr = SiteServeRequests(env=tests.settings.backend_env,
                                                     class_id=self.horse_racing_live_class_ids,
                                                     category_id=self.ob_config.backend.ti.horse_racing.category_id,
                                                     brand=self.brand)
        if tests.settings.backend_env != 'prod':
            self.ob_config.add_international_racing_event(number_of_runners=1, market_extra_place_race=True)
            event_params = self.ob_config.add_UK_racing_event(number_of_runners=1, market_extra_place_race=True)
            self.__class__.eventID = event_params.event_id
            self.__class__.event_ss_name = 'Autotest - UK'
        else:
            query_params = self.basic_active_events_filter() \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.INTERSECTS,
                                          self.ob_config.backend.ti.horse_racing.category_id)) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_RESULTED, OPERATORS.IS_FALSE)) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CLASS_ID, OPERATORS.NOT_INTERSECTS, '227')) \
                .add_filter(simple_filter(LEVELS.MARKET, ATTRIBUTES.TEMPLATE_MARKET_NAME, OPERATORS.EQUALS,
                                          self.ob_config.horseracing_config.default_market_name)) \
                .add_filter(exists_filter(LEVELS.EVENT,
                                          simple_filter(LEVELS.MARKET, ATTRIBUTES.DRILLDOWN_TAG_NAMES,
                                                        OPERATORS.NOT_INTERSECTS, 'MKTFLAG_SP')))
            events = self.ss_req_hr.ss_event_to_outcome_for_class(query_builder=query_params)
            event = next((event for event in events if
                          event.get('event') and event['event'] and event['event'].get('children')), None)
            self.__class__.eventID = event.get('event').get('id')
            self.__class__.event_ss_name = event['event']['typeName']
            self._logger.info(f'*** Found Horse racing event with id "{self.eventID}"')

            test_events = []
            data_fabric = Datafabric()
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
                raise SiteServeException(
                    f'Less than 2 events with Post Info and Race Distance found to perform the test. '
                    f'Number of events available: "{len(test_events)}"')

            event, event2 = test_events
            self.__class__.meeting_name2 = event2.get('event').get('typeName')

        query2 = self.ss_query_builder. \
            add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')). \
            add_filter(exists_filter(LEVELS.EVENT,
                                     simple_filter(LEVELS.MARKET, ATTRIBUTES.DRILLDOWN_TAG_NAMES,
                                                   OPERATORS.INTERSECTS, 'MKTFLAG_EPR'))). \
            add_filter(simple_filter(LEVELS.MARKET, ATTRIBUTES.TEMPLATE_MARKET_NAME, OPERATORS.EQUALS,
                                     self.ob_config.horseracing_config.default_market_name)). \
            add_filter(prune(LEVELS.EVENT)). \
            add_filter(prune(LEVELS.MARKET))
        self.__class__.extra_place = self.ss_req_hr.ss_event_to_outcome_for_class(query_builder=query2)

    def test_001_check_meeting_selector(self):
        """
        DESCRIPTION: Check 'Meeting' selector
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='HorseRacing')
        self.__class__.type_flag_codes_flipped = dict((y, x) for x, y in self.type_flag_codes.items())
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.assertTrue(self.site.racing_event_details.meeting_selector.is_displayed(),
                        msg='Meeting Selector is not displayed')

    def test_002_mobile_tablet_tap_on_the_part_of_breadcrumb_event_name_next_races_plus_down_arrow_in_the_page_subheader_desktop_click_on_the_meeting_link_and_up__down_arrows(
            self):
        """
        DESCRIPTION: **Mobile&Tablet:** Tap on the part of breadcrumb: '[Event Name]'/'Next Races' +'Down' arrow in the page subheader
        DESCRIPTION: **Desktop:** Click on the 'Meeting' link and 'up & down' arrows
        EXPECTED: **For Mobile&Tablet:**
        EXPECTED: * 'Down' arrow is switched to 'Up' arrow
        EXPECTED: *  An overlay is slides from the bottom with list of available meetings
        EXPECTED: **For Desktop:**
        EXPECTED: * 'up & down' arrows are changed their location
        EXPECTED: * Widget with list of available meetings is opened right-aligned on the event name level
        """
        self.site.racing_event_details.meeting_selector.click()
        wait_for_haul(2)
        self.assertTrue(self.site.racing_event_details.meetings_list.is_displayed(), msg='Meetings list is not shown')

    def test_003_check_the_list_of_meetings(self):
        """
        DESCRIPTION: Check the list of meetings
        EXPECTED: The following data are present:
        EXPECTED: * 'OFFERS AND FEATURED RACES' section with only 1 option available
        EXPECTED: - Extra Place Races
        EXPECTED: * All race meetings that belong to the 'UK&URE', '%Countries sections%'  'Other International', 'Virtual', 'Next Races', and Enhanced Multiples;
        EXPECTED: * Sub Regions as per below order:
        EXPECTED: UK + Ireland
        EXPECTED: France
        EXPECTED: UAE
        EXPECTED: South Africa
        EXPECTED: India
        EXPECTED: USA
        EXPECTED: Australia
        EXPECTED: Other International
        EXPECTED: Virtual
        EXPECTED: * Groups correspond to the **'typeFlagCodes' **attribute from the Site Server response
        EXPECTED: * The list of available meetings displays data only on the same day as the selected event. (e.g. If user selects today race event that the list of meetings available for today only is displayed)
        """
        self.__class__.sections = self.site.racing_event_details.meetings_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='No sections found')
        meetings = self.sort_events_by_type(self.get_events())  # Grouped by subregions (key_flag)
        extra_place_name, _ = list(self.sections.items())[0]
        if extra_place_name.upper() != 'UK AND IRISH RACES' or "UK & IRE":
            self.assertTrue(extra_place_name, msg=f'section is displayed as {extra_place_name}, '
                                                  f'expected is "UK AND IRISH RACES" or "UK & IRE"')
        for section_name, section in list(self.sections.items()):
            if section_name == 'VIRTUAL RACING':
                if self.brand == 'bma':
                    section_name = vec.racing.LEGENDS_TYPE_NAME.upper()
                else:
                    section_name = vec.racing.LEGENDS_TYPE_NAME.upper()
            section_name = next((section_nam for section_nam in list(self.type_flag_codes_flipped) if section_nam.upper() == section_name.upper()),None)
            section.expand()
            key_flag = self.type_flag_codes_flipped[section_name]
            striped_meeting = []
            ss_meetings = []
            for event in meetings.get(key_flag):
                striped_meeting.append(re.sub(r'\(.*?\)', '',event).strip().upper())
            ss_meetings += striped_meeting
            ui_meetings = section.items_as_ordered_dict.keys()
            if not ui_meetings:
                section.expand()
                ui_meetings = section.items_as_ordered_dict.keys()
            ui_meetings = [re.sub(r'\(.*?\)', '', meeting).strip().upper()for meeting in ui_meetings]
            self.assertListEqual(sorted(ss_meetings), sorted(ui_meetings),
                                 msg=f'Event list got from SS {sorted(ss_meetings)} '
                                 f'is not the same as on UI {sorted(ui_meetings)} for "{section_name}" section')

            # events will show same as mobile as per new update story OZONE-5872--GRAY HOUNDS and OZONE-3480 horse racing
            # else:
            #     del meetings['UK']
            #     del meetings['IE']  # To avoid duplication
            #     ss_meetings = []
            #     for meeting in meetings.values():
            #         striped_meeting = []
            #         for event in meeting:
            #             striped_meeting.append(event.strip())
            #         ss_meetings += striped_meeting
            #     ui_meetings = list(self.sections.keys())
            #     for meeting in ui_meetings:
            #         self.assertIn(meeting, ss_meetings,
            #                       msg=f'UI meeting "{meeting}" is not present in the Expected meetings: "{sorted(ss_meetings)}"')

    def test_004_mobile_tablet_tap_on_x_button_in_the_overlay_header_desktop_click_on_the_meeting_link_and_up_down_arrows(
            self):
        """
        DESCRIPTION: **Mobile&Tablet:** Tap on 'X' button in the overlay header.
        DESCRIPTION: **Desktop:** Click on the 'Meeting' link and 'up & down' arrows
        EXPECTED: **For mobile&tablet:**
        EXPECTED: * Overlay with list of meetings is closed
        EXPECTED: **For desktop:**
        EXPECTED: * Widget with list of meetings is closed
        """
        section_name, section = next((section for section in self.sections.items()
                                      if section[0] != vec.racing.FEATURED_OFFERS_SECTION_TITLE), (None, None))
        self.assertTrue(section, msg=f'Only "{vec.racing.FEATURED_OFFERS_SECTION_TITLE}" section present '
                                     f'in "{self.sections.keys()}"')
        events = section.items_as_ordered_dict
        if not events:
            section.expand()
            events = section.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found in "{section_name}" section')
        event_name, event = next((event for event in events.items() if event[0] != self.event_ss_name), (None, None))
        self.assertTrue(event, msg=f'Only "{self.event_ss_name}" event is present in section "{section_name}"')
        event.click()

    def test_005_mobile_tablet_click_on_the_meeting_link_in_the_menu_desktop_click_on_the_meeting_link_and_up__down_arrows_navigate_between_event_types_using_the_selector(
            self):
        """
        DESCRIPTION: **Mobile&Tablet:** Click on the 'Meeting' link in the Menu
        DESCRIPTION: **Desktop:** Click on the 'Meeting' link and 'up & down' arrows
        DESCRIPTION: > Navigate between event types using the selector
        EXPECTED: User is redirected to the first available event from the selected event type.
        """
        expected_section = vec.racing.FEATURED_OFFERS_SECTION_TITLE if self.device_type == "mobile" else vec.racing.UK_AND_IRE_TYPE_NAME.upper()
        if self.brand == 'bma':
            self.site.racing_event_details.meeting_selector.click()
        self.assertTrue(self.site.racing_event_details.meetings_list.is_displayed(timeout=10),
                        msg='Meetings list is not shown')
        sections = self.site.racing_event_details.meetings_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        if tests.settings.backend_env != 'prod':
            section_name = self.international_type_name
            section = sections.get(section_name)
            self.assertTrue(section, msg=f'"{section_name}" is not found in "{sections.keys()}"')
        else:
            section_name, section = next((section for section in sections.items()
                                          if section[0] != expected_section), (None, None))
            self.assertTrue(section, msg=f'Only "{expected_section}" section present '
                                         f'in "{sections.keys()}"')
            uk_and_ire_type_name = next(
                section for section in sections if section.upper() == 'UK AND IRISH RACES')
            uk_and_ire = sections.get(uk_and_ire_type_name)
            self.assertTrue(uk_and_ire,
                            msg=f'"{uk_and_ire_type_name}" is not found in "{self.sections.keys()}"')
            events_names = uk_and_ire.items_as_ordered_dict
            if not events_names:
                uk_and_ire.expand()
                events_names = uk_and_ire.items_as_ordered_dict
            event_items = list(uk_and_ire.items_as_ordered_dict.values())
            self.assertTrue(events_names, msg=f'Events list is empty for "{uk_and_ire_type_name}"')
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
        self.site.wait_splash_to_hide()
        self.site.wait_content_state(state_name='RacingEventDetails')
        selected = self.site.racing_event_details.tab_content.event_off_times_list.selected_item
        if self.site.wait_for_stream_and_bet_overlay():
            self.site.stream_and_bet_overlay.close_button.click()
        first_event_name = self.site.racing_event_details.tab_content.event_off_times_list.get_first_available_event()
        self.assertEqual(selected, first_event_name,
                         msg=f'Selected event "{selected}" is not the first one available {first_event_name}')

    def test_006_scroll_up_down_event_details_page(self):
        """
        DESCRIPTION: Scroll up/down event details page
        EXPECTED: Meeting header is anchored to the top of the screen
        """
        self.site.racing_event_details.scroll_to_bottom()
        self.assertTrue(self.site.racing_event_details.breadcrumbs.is_displayed())
        self.assertTrue(self.site.racing_event_details.meeting_selector.is_displayed())
