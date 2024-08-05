import pytest
import re
import voltron.environments.constants as vec
from voltron.environments.constants.base.racing import Racing
import random
import requests
import json
from voltron.utils.waiters import wait_for_result, wait_for_haul
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from datetime import datetime, timezone
from collections import OrderedDict
from voltron.utils.js_functions import scroll_to_center_of_element
from tenacity import retry, retry_if_exception_type, stop_after_attempt
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from crlat_cms_client.utils.exceptions import CMSException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.sports_specific
@pytest.mark.greyhounds_specific
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@vtest
class Test_C65969122_Verify_Greyhounds_data_is_loading_in_the_Todays_tab(BaseRacing):
    """
    TR_ID: C65969122
    NAME: Verify Greyhounds data is loading in the Today's tab
    DESCRIPTION: This test case verifies Race Meetings displaying within the Greyhounds Race Grid(Today's tab)
    PRECONDITIONS: Load the application.
    PRECONDITIONS: Access the Greyhounds landing page.
    PRECONDITIONS: Configure in CMS - Virtual Greyhounds Banner
    PRECONDITIONS: Sportspage-&gt; Matches tab-&gt;Virtual sports entrypoints
    PRECONDITIONS: Enable Virtual sports entrypoints in CMS
    PRECONDITIONS: Banner has to  be uploaded
    PRECONDITIONS: URL  should be configured
    PRECONDITIONS: Virtual Greyhounds Banner need to be configured in Sitecore.
    """
    keep_browser_open = True

    def check_empty_strings(self, sections):
        """
        DESCRIPTION:  This condition ensures that the sections itself is not empty
                      and also checks if all keys in the section,
                      after stripping any whitespace, are non-empty strings.
        """
        section_name = sections.keys()
        return sections if sections and all(item.strip() != '' for item in section_name) else False

    def get_greyhound_uk_irish_races(self):
        """
        Retrieve webelements inside UK and Irish greyhound races section.
        Returns:
        OrderedDict: A dictionary containing webelements of UK and Irish greyhound races section.

        Raises:
            AssertionError: If the 'UK AND IRISH RACES' section is not available or if no rows are found.

        """
        # Getting a specific Meeting
        uk_irish_races = list(self.site.greyhound.tab_content.accordions_list.get_items(
            name=self.uk_and_ire_type_name).values())[0]
        self.assertTrue(uk_irish_races, msg='UK AND IRISH RACES section is not available in Greyhound SLP')

        uk_irish_races.expand()
        rows = wait_for_result(lambda: self.check_empty_strings(uk_irish_races.items_as_ordered_dict), timeout=7)
        self.assertTrue(rows, msg='No one row was found in section: UK AND IRISH RACES')
        return OrderedDict((key.title(), value) for key, value in rows.items())

    def test_000_preconditions(self):
        """
        Extract required data from the FSC API.

        This method fetches data from the Ladbrokes or Coral API based on the brand,
        processes the response, and organizes the data based on event types and times.
        note that the manipulated date only contains Greyhounds Todays tab UK/IRISH RACES data

        Raises:
            Exception: If the API response status code is not 200.
        """
        url = 'https://cms-hl.coral.co.uk/cms/api/bma/fsc/19' if self.brand == 'bma' else \
            'https://cms-hl.ladbrokes.com/cms/api/ladbrokes/fsc/19'
        # Note that these URLs are for BETA environment for both the brands. For PROD, they are different.

        greyhounds_data = requests.get(url=url)
        # Check the response status code and print the response content
        if greyhounds_data.status_code == 200:
            # Convert the response content (which is a JSON string) to a dictionary
            greyhounds_data_response_dict = json.loads(greyhounds_data.content)
            data_objects = None
            for module in greyhounds_data_response_dict['modules']:
                section_title = module['title'].title()
                if section_title in [vec.racing.UK_TYPE_NAME.title(), vec.racing.UK_AND_IRE_TYPE_NAME.title()]:
                    data_objects = module['data']
                    self.__class__.uk_and_ire_type_name = section_title

            self.assertTrue(data_objects, msg='Data object is not expected to be empty.')

            self.__class__.expected_ss_data = {}

            for event in data_objects:
                # Convert input time string to datetime object
                input_datetime = datetime.strptime(event['startTime'], "%Y-%m-%dT%H:%M:%SZ")

                current_utc_time = datetime.now(timezone.utc)

                # Check if the date part of input time matches today's date
                if input_datetime.date() == current_utc_time.date():
                    type_name = event['typeName']

                    # Extract the time in HH:MM format if found, otherwise None.
                    match = re.search(r'\b(\d{2}:\d{2})\b', event['name'])
                    event_time = match.group(1) if match else None

                    # Create or get the inner dictionary for the 'typeName'
                    inner_dict = self.__class__.expected_ss_data.setdefault(type_name, {})

                    # Append the object to the inner dictionary based on the event time
                    if event_time in inner_dict:
                        inner_dict[event_time].append(event)
                    else:
                        inner_dict[event_time] = [event]
        else:
            raise CMSException(f'current url: {url} is sending status code: {greyhounds_data.status_code}, '
                            f'enabled the FSC call in CMS and re-run the script')

    def test_001_navigate_to_greyhounds_landing_page(self):
        """
        DESCRIPTION: Navigate to Greyhounds landing page.
        EXPECTED: '"TODAY" tab is opened and the race grid is shown with 'By Meeting' sorting switched on by default.
        Due to this story point OZONE-3455 by meeting and by time will not available in today tab
        """
        if self.brand == 'ladbrokes':
            today = vec.sb.TABS_NAME_TODAY
        else:
            today = vec.sb.SPORT_DAY_TABS.today
        sport = 'Greyhounds' if self.brand != 'bma' and self.device_type == 'mobile' else 'GREYHOUNDS'

        if self.device_type == 'desktop':
            self.site.sport_menu.click_item(sport)
        else:
            self.site.home.menu_carousel.click_item(sport)
        self.site.wait_content_state('greyhound-racing')

        self.site.greyhound.tabs_menu.click_button(today)
        self.assertEqual(self.site.greyhound.tabs_menu.current, today,
                         msg=f'Opened grouping button "{self.site.greyhound.tabs_menu.current}" '
                             f'is not the same as expected "{today}"')

        # Due to this story point OZONE-3455 by meeting and by time will not available in today tab

    def test_002_verify_race_grid_sections(self):
        """
        DESCRIPTION: Verify race grid sections.
        EXPECTED: The following sections are displayed and expanded by default:
        EXPECTED: FOR CORAL (Mobile/Desktop):
        EXPECTED: UK &amp; IRISH RACES
        EXPECTED: NEXT RACES
        EXPECTED: AUSTRALIA
        EXPECTED: FOR LADBROKES (Mobile/Desktop):
        EXPECTED: UK/IRISH RACES
        EXPECTED: NEXT RACES
        EXPECTED: AUSTRALIA RACES
        """
        if self.brand == 'ladbrokes':
            sections = wait_for_result(
                lambda: self.check_empty_strings(self.get_sections('greyhound-racing')),
                name='sections list is not loaded', timeout=5)
        else:
            sections = wait_for_result(
                lambda: self.check_empty_strings(self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict),
                name='sections list is not loaded', timeout=5)
        self.assertTrue(sections, msg='No sections found in future tab')
        sections = OrderedDict((key.title(), value) for key, value in sections.items())
        section_names = [self.uk_and_ire_type_name, vec.racing.AUSTRALIA_TYPE_NAME.title(), Racing.NEXT_RACES.title()]

        for section_name in section_names:
            if section_name in sections:
                self.assertTrue(sections[section_name].is_expanded(expected_result=True, timeout=5),
                                msg=f'Event "{section_name}" is expanded by default')

    def test_003_collapse_and_expand_the_grid_sections_by_tapping_on_the_headers(self):
        """
        DESCRIPTION: Collapse and expand the grid sections by tapping on the headers.
        EXPECTED: It is possible to collapse/expand accordions by tapping on the headers
        EXPECTED: FOR MOBILE (Coral/Ladbrokes) and DESKTOP (Ladbrokes):
        EXPECTED: After collapsing: the downward arrow is displayed on the right side
        EXPECTED: After expanding: No arrows displayed
        EXPECTED: FOR DESKTOP (Coral):
        EXPECTED: After collapsing: the downward arrow is displayed on the right side
        EXPECTED: After expanding: the upward arrow is displayed on the right side
        """
        if self.device_type == 'desktop':
            self.device.set_viewport_size(width=800, height=550)
        if self.brand == 'ladbrokes':
            sections = self.get_sections('greyhound-racing')
        else:
            sections = self.site.greyhound.tab_content.accordions_list.racing_items_as_ordered_dict
        sections = OrderedDict((key.title(), value) for key, value in sections.items())
        sections = sections.items()
        self.assertTrue(sections, msg='No sections found in today tab')
        for section, section_value in sections:
            if section == vec.sb.TABS_NAME_NEXT.title():
                continue
            self.assertTrue(section_value.is_expanded(), msg=f'Event "{section}" is not expanded')
            section_value.collapse()
            self.assertFalse(section_value.is_expanded(expected_result=False),
                             msg=f'Event "{section}" is not collapsed')
            if self.brand != 'ladbrokes' and self.device_type == 'mobile':
                self.assertTrue(section_value.is_chevron_down(),
                                msg=f'Event "{section}" Chevron arrow to point to the top')
            section_value.expand()
            self.assertTrue(section_value.is_expanded(), msg=f'Event "{section}" is not expanded')
            if self.brand == 'bma' and self.device_type == 'desktop':
                self.assertTrue(section_value.is_chevron_up(),
                                msg=f'Event "{section}" Chevron arrow to point to the bottom')

            # Verify scrolling between event off times.
            # In Mobile/Tablet scroll for left and right by swiping is covered in step 4
            # As the page would be in its default state initially, we are verifying the scroll functionality first.
            if self.device_type == 'desktop' and section == self.uk_and_ire_type_name:
                rows = wait_for_result(lambda: section_value.items_as_ordered_dict, timeout=7)
                title_case_rows = OrderedDict((key.title(), value) for key, value in rows.items())
                self.assertTrue(title_case_rows, msg=f'No row was found in section: "{title_case_rows.keys()}"')
                expected_type_names_list = sorted([item.title() for item in list(self.expected_ss_data.keys())])

                for type_name in expected_type_names_list:
                    row = title_case_rows[type_name]
                    events = row.items_as_ordered_dict
                    if len(events) > 8:
                        scroll_to_center_of_element(row._we)
                        row.mouse_over()
                        wait_for_haul()
                        self.assertTrue(row.has_right_arrow(), msg='next button visibility status is to be true')
                        self.assertFalse(row.has_left_arrow(), msg='previous button visibility status is to be False')
                        row.right_arrow.click()
                        section_value.mouse_over()
                        wait_for_haul()
                        scroll_to_center_of_element(row._we)
                        row.mouse_over()
                        wait_for_haul()
                        self.assertTrue(row.has_left_arrow(), msg='previous button visibility status is to be true')
                        row.left_arrow.click()
                        break

    @retry(stop=stop_after_attempt(4), retry=retry_if_exception_type(
        (StaleElementReferenceException, AttributeError, NoSuchElementException, ValueError)), reraise=True)
    def test_004_verify_race_grid_content(self):
        """
        DESCRIPTION: Verify Race Grid content
        EXPECTED: All events from SS response with start time (startTime attribute) corresponding to today's day  are displayed within the corresponding type (race meeting) section.
        """
        self.__class__.title_case_rows = self.get_greyhound_uk_irish_races()
        self.assertTrue(self.title_case_rows, msg='No one row was found in section: "UK AND IRISH RACES"')

        expected_type_names_list = sorted([item.title() for item in list(self.expected_ss_data.keys())])
        actual_type_names_list = sorted(list(self.title_case_rows.keys()))
        self.assertListEqual(actual_type_names_list, expected_type_names_list,
                             msg=f'In greyhounds, for UK AND IRISH RACES the type names are not equal,'
                                 f'actual = "{actual_type_names_list}" and expected = "{expected_type_names_list}"')

        self.__class__.cashout_applicable_type_names = set()
        self.__class__.live_stream_applicable_type_names = set()
        self.__class__.random_expected_type_names_list = random.sample(expected_type_names_list, 2)
        for type_name in self.random_expected_type_names_list:
            # latest results would be getting updated in the variable 'self.expected_ss_data'
            self.test_000_preconditions()

            events = wait_for_result(
                lambda: self.check_empty_strings(self.get_greyhound_uk_irish_races()[type_name].items_as_ordered_dict),
                name='sections list is not loaded', timeout=3)

            actual_events_list = list(events.keys())
            expected_events_list = sorted(list(self.expected_ss_data[type_name].keys()))
            self.assertListEqual(actual_events_list, expected_events_list,
                                 msg=f'In greyhounds "UK AND IRISH RACES" of type {type_name} are event off times are not as expected,'
                                     f' actual = "{actual_events_list}" and expected = "{expected_events_list}"')

            for event, event_value in events.items():

                expected_resulted_status = bool(self.expected_ss_data[type_name][event][0].get('isResulted'))
                actual_resulted_status = event_value.has_resulted(timeout=0, expected_result=expected_resulted_status)
                self.assertTrue(actual_resulted_status == expected_resulted_status,
                                msg=f'Race status of "RESULT" for event "{type_name} {event}" is expected as "{expected_resulted_status}" in response, but actual is "{actual_resulted_status}" ')

                if expected_resulted_status is False:
                    expected_race_off_status = self.expected_ss_data[type_name][event][0].get('rawIsOffCode') == "Y"
                    actual_race_off_status = event_value.has_race_off(timeout=0,
                                                                      expected_result=expected_race_off_status)
                    self.assertTrue(actual_race_off_status == expected_race_off_status,
                                    msg=f'Race status of "RACE OFF" for event "{type_name} {event}" is expected as '
                                        f'"{expected_race_off_status}" in response,'
                                        f' but actual is {actual_race_off_status} ')

                if self.expected_ss_data[type_name][event][0].get('cashoutAvail') == "Y":
                    self.__class__.cashout_applicable_type_names.add(type_name)

                if self.expected_ss_data[type_name][event][0].get('isStarted'):
                    self.__class__.live_stream_applicable_type_names.add(type_name)

    def test_005_verify_race_meeting_sections_content(self):
        """
        DESCRIPTION: Verify Race meeting sections content.
        EXPECTED: Race meeting header
        EXPECTED: Row of events start time
        EXPECTED: Race status (RESULT, RACE OFF)
        """
        # covered in step 4

    def test_006_in_coral_verify_cash_out_icon_displaying(self):
        """
        DESCRIPTION: In Coral: Verify 'Cash Out' icon displaying.
        EXPECTED: FOR CORAL Only
        EXPECTED: 'CASH OUT' icon is shown if at least one of it's events has cashoutAvail="Y" and on all higher levels cashoutAvail="Y"
        """
        if self.brand == 'bma':
            self.assertTrue(self.title_case_rows, msg='No one row was found in section: UK AND IRISH RACES')
            for type_name in self.cashout_applicable_type_names:
                row = self.title_case_rows[type_name]
                self.assertTrue(row.has_cash_out_label(),
                                msg=f'"CashOut" label is not displayed for type name: {type_name}')

    def test_007_verify_live_stream_icon(self):
        """
        DESCRIPTION: Verify 'Live Stream' icon.
        EXPECTED: Stream icon is displayed (if available)
        EXPECTED: FOR CORAL Play icon for races with live stream (if available) on the right
        EXPECTED: FOR LADBROKES WATCH icon for races with live stream (if available) on the right
        EXPECTED: Stream icon is shown for event type where at least 1 event has a stream available on event level ("mediaTypeCodes" parameter is available in SS response)
        EXPECTED: Stream icon is for informational purpose only (not clickable)
        """
        self.assertTrue(self.title_case_rows, msg='No one row was found in section: "UK AND IRISH RACES"')
        for type_name in self.live_stream_applicable_type_names:
            row = self.title_case_rows[type_name]
            self.assertTrue(row.has_live_stream, msg='live stream icon should not be displayed')

    @retry(stop=stop_after_attempt(4), retry=retry_if_exception_type(
        (StaleElementReferenceException, AttributeError, NoSuchElementException, ValueError)), reraise=True)
    def test_008_verify_row_of_events_displaying(self):
        """
        DESCRIPTION: Verify row of events displaying.
        EXPECTED: Event off times are displayed horizontally across the page
        EXPECTED: Events off times are displayed in bold if 'priceTypeCodes="LP"' attribute is available for 'Win or Each way' market only
        EXPECTED: Ladbrokes: Race Statuses displayed for started or resulted events:
        EXPECTED: Race Off - event has 'isOff=Yes'
        EXPECTED: Live - event has 'isOff=Yes'and at least one of markets has 'betInRunning=true'
        EXPECTED: Resulted - event has 'isResulted=true' + 'isFinished=true'
        EXPECTED: Coral:  Signposting icons are displayed next to event off time (if available)
        EXPECTED: Ladbrokes: Signposting icons are NOT displayed next to event off time
        """
        # few validations covered in step 4
        for type_name in self.random_expected_type_names_list:
            events = wait_for_result(
                lambda: self.check_empty_strings(self.get_greyhound_uk_irish_races()[type_name].items_as_ordered_dict),
                name='sections list is not loaded', timeout=3)
            locations_of_event_off_time = []
            for event, event_value in events.items():
                scroll_to_center_of_element(event_value._we)
                # verifying if Event off times are displayed horizontally across the page
                locations_of_event_off_time.append(event_value.location.get('y'))
            self.assertTrue(all(element == locations_of_event_off_time[0] for element in locations_of_event_off_time),
                            msg=' Event off times are not displayed horizontally across the page')

        # Events off times are displayed in bold if 'priceTypeCodes="LP"' attribute is available for 'Win or Each way' market only
        for type_name in self.random_expected_type_names_list:
            events = wait_for_result(
                lambda: self.check_empty_strings(self.get_greyhound_uk_irish_races()[type_name].items_as_ordered_dict),
                name='sections list is not loaded', timeout=3)
            for event, event_value in events.items():
                current_event_markets = self.expected_ss_data[type_name][event][0].get('markets')
                self._logger.info(f'*+*+*+*+*+*+** {type_name} {event}" +*+*+*+*+*+*+')
                scroll_to_center_of_element(event_value._we)
                event_attribute_class = event_value.event_off_time.css_property_value('font-weight')
                is_priced = '700' == event_attribute_class
                for current_event_market in current_event_markets:
                    if current_event_market.get('name') == 'Win or Each Way' and current_event_market.get(
                            'isLpAvailable') == True:
                        self.assertTrue(is_priced, msg=f'Event "{event}" is not priced')
                        break
                else:
                    self.assertFalse(is_priced, msg=f'Event "{event}" is priced, not as expected')

    def test_009_verify_event_off_times(self):
        """
        DESCRIPTION: Verify event off times.
        EXPECTED: Event off times corresponds to the race local time from the 'name' attribute from the Site Server.
        """
        # Covered in step 7

    def test_010_verify_scrolling_between_event_off_times(self):
        """
        DESCRIPTION: Verify scrolling between event off times.
        EXPECTED: In Mobile/Tablet user should be able to scroll left and right by swiping.
        EXPECTED: In Desktop Race meeting with too many event off times to be shown in one line has arrows which appear on hover to scroll horizontally.
        EXPECTED: Events off times are scrolled one by one after clicking the arrows.
        """
        # verified in step 3 and step 4

    def test_011_tap_on_event_off_time(self):
        """
        DESCRIPTION: Tap on event off time.
        EXPECTED: Corresponding Event details page is opened.
        """
        if self.brand == 'ladbrokes':
            sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
        else:
            sections = self.site.greyhound.tab_content.accordions_list.racing_items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found in future tab')
        sections = OrderedDict((key.title(), value) for key, value in sections.items())
        section_name = self.uk_and_ire_type_name
        if not sections[section_name].is_expanded(expected_result=True):
            sections[section_name].click()

        break_flag = False
        expected_type_names_list = sorted([item.title() for item in list(self.expected_ss_data.keys())])
        for type_name in expected_type_names_list:
            if break_flag:
                break
            events = wait_for_result(
                lambda: self.check_empty_strings(self.get_greyhound_uk_irish_races()[type_name].items_as_ordered_dict),
                name='sections list is not loaded', timeout=3)
            for event, event_value in events.items():
                scroll_to_center_of_element(event_value._we)
                if not event_value.has_resulted() or not event_value.has_race_off():
                    event_id = event_value.event_id
                    event_value.click()
                    break_flag = True
                    break
        self.site.wait_content_state(state_name='GreyHoundEventDetails')
        current_url = self.device.get_current_url()
        self.assertIn(event_id, current_url,
                      msg=f'Corresponding Event details page of event id:"{event_id}" is not opened')

    def test_012_tap_back_button(self):
        """
        DESCRIPTION: Tap 'Back' button.
        EXPECTED: User is redirected to the Greyhounds Landing page.
        """
        self.site.back_button_click()
        self.site.wait_content_state(state_name='Greyhoundracing')

    def test_013_verify_the_virtual_greyhounds_entry_point_banner_by_clicking_on_it(self):
        """
        DESCRIPTION: Verify the Virtual Greyhounds Entry point banner by clicking on it.
        EXPECTED: On clicking Virtual Banner it will redirect the user to the Virtual Greyhounds page.
        """
        self.assertTrue(self.site.greyhound.tab_content.has_virtual_entry_point_banner(expected_result=True),
                        msg='the Virtual Greyhounds Entry point banner is not displayed in Greyhound SLP')
        self.site.greyhound.tab_content.virtual_entry_point_banner.play_now_button.click()
        self.assertTrue(self.site.wait_content_state('VirtualSports', timeout=5))
