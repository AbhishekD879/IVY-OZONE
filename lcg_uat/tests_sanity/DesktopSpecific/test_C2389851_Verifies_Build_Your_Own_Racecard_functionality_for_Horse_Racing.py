import re
import tests
import pytest
import pytz
import voltron.environments.constants as vec
from collections import namedtuple
from datetime import datetime, timedelta
from crlat_siteserve_client.siteserve_client import SiteServeRequests
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.datafabric.datafabric import Datafabric
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2  # Very often absence of bog, promotions, raceForm, etc.
# @pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.navigation
@pytest.mark.build_own_racecard
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.slow
@pytest.mark.sanity
@vtest
class Test_C2389851_Verifies_Build_Your_Own_Racecard_functionality_for_Horse_Racing(BaseRacing):
    """
    TR_ID: C2389851
    VOL_ID: C58068811
    NAME: Verifies 'Build Your Own Racecard' functionality for 'Horse Racing'
    DESCRIPTION: This test case verifies 'Build Your Own Racecard' functionality for 'Horse Racing'.
    DESCRIPTION: Need to check on Windows (Chrome) and Mac OS (Safari).
    PRECONDITIONS: 1. Open Oxygen app
    PRECONDITIONS: 2. Navigate to 'Horse Racing' Landing page
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    counter = 0
    device_name = tests.desktop_default
    vec.racing.OFFERS_AND_FEATURED_RACES = 'OFFERS & FEATURED RACES'
    sections_to_skip = [vec.tote.TOTE_TITLE,
                        vec.racing.EXTRA_PLACE_TITLE,
                        vec.racing.NEXT_RACES,
                        vec.virtuals.VIRTUAL_SPORTS,
                        vec.racing.EXTRA_PLACE_TITLE,
                        vec.racing.NEXT_RACES.upper(),
                        vec.racing.ENHANCED_RACES,
                        vec.racing.OFFERS_AND_FEATURED_RACES
                        ]

    def test_000_preconditions(self):
        """
        DESCRIPTION: Navigate to Horse Racing Landing page
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')

        self.__class__.sections_to_skip.append(self.virtual_type_name)
        self.__class__.sections_to_skip.append(self.international_tote_type_name)

    def test_001_click_on_build_a_racecard_button(self):
        """
        DESCRIPTION: Click on 'Build a Racecard' button
        EXPECTED: * 'Build a Racecard' button is clickable
        EXPECTED: * 'Build a Racecard' button is replaced by 'Exit Builder' with 'Close' icon
        EXPECTED: * 'Clear All Selections' and 'Build Your Own Racecard' buttons appear below the 'Build Your Own Racecard' section and it's disabled and NOT clickable
        EXPECTED: * Section with 'Clear All Selections' and 'Build Your Own Racecard' buttons is sticky
        EXPECTED: * Checkboxes appear before each of 'Event off time' tab only for 'UK&IRE' and 'INTERNATIONAL' sections
        """
        selected_tab = self.site.horse_racing.tabs_menu.current
        self.assertEqual(selected_tab, vec.racing.RACING_DEFAULT_TAB_NAME,
                         msg=f'"{selected_tab}" tab is selected by default instead of "{vec.racing.RACING_DEFAULT_TAB_NAME}"')

        build_card = self.site.horse_racing.tab_content.build_card
        self.assertTrue(build_card, msg='Build card section is not found')
        self.assertTrue(build_card.build_race_card_button.is_displayed(), msg=f'"{vec.racing.BUILD_YOUR_RACECARD_BUTTON}" is not shown')

        build_race_card_button_location = build_card.build_race_card_button.location.get('y')
        build_card.build_race_card_button.click()

        self.assertTrue(build_card.exit_builder_button.is_displayed(), msg='"Exit Builder" button is not shown')
        self.assertTrue(build_card.close_icon.is_displayed(), msg='Close Button is not shown')
        self.assertTrue(build_card.clear_all_selections_button.is_displayed(), msg='"Clear all selections" button is not shown')
        self.assertFalse(build_card.clear_all_selections_button.is_enabled(expected_result=False),
                         msg='"Clear all selections" button is enabled')
        self.assertTrue(build_card.build_your_race_card_button.is_displayed(), msg='"Build your Racecard" button is not shown')
        self.assertFalse(build_card.build_your_race_card_button.is_enabled(expected_result=False),
                         msg='"Build your Racecard" button is enabled')

        self.assertLessEqual(build_race_card_button_location, build_card.clear_all_selections_button.location.get('y'),
                             msg=f'"Clear all selections" button is not below "{vec.racing.BUILD_YOUR_RACECARD_BUTTON}"')

        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Horse Racing sections are not present')
        for name, section in sections.items():
            if name not in self.sections_to_skip:
                section.scroll_to()

        self.assertTrue(build_card.clear_all_selections_button.is_displayed(),
                        msg='"Clear all selections" button is not sticky')
        self.assertTrue(build_card.build_your_race_card_button.is_displayed(),
                        msg='"Build your Racecard" button is not sticky')

    def test_002_tick_at_least_one_checkbox_before_event_off_time_tab_and_verify_clear_all_selectionsbuild_your_own_racecard_buttons(self):
        """
        DESCRIPTION: Tick at least one checkbox before 'Event off time' tab and verify 'Clear All Selections'/'Build Your Own Racecard' buttons
        EXPECTED: * Checkbox before 'Event off time' tabs is ticked
        EXPECTED: * 'Clear All Selections' and 'Build Your Own Racecard' buttons became active and clickable
        """
        self.site.wait_content_state('Horseracing')
        self.__class__.sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='No section found on Horse Racing Landing page')

        checked = False
        for section_name, section in self.sections.items():
            if section_name not in self.sections_to_skip:
                self._logger.info(f'*** Working with section "{section_name}"')
                racing_events = section.items_as_ordered_dict
                self.assertTrue(racing_events, msg=f'No racing events found in "{section_name}" section')
                for event_name, event in racing_events.items():
                    racing_meetings = event.items_as_ordered_dict
                    self.assertTrue(racing_meetings, msg=f'No racing events found in "{event_name}" section')
                    for meeting_name, meeting in racing_meetings.items():
                        if meeting.has_checkbox():
                            meeting.scroll_to()
                            meeting.check_box.value = True
                            self.assertTrue(meeting.check_box.value, msg=f'Checkbox of "{meeting_name}" meeting is not ticked')
                            self.__class__.meeting = meeting
                            self.__class__.meeting_name = meeting_name
                            self.__class__.event_name = event_name
                            checked = True
                            break
                    if checked:
                        break
            if checked:
                break
        build_card = self.site.horse_racing.tab_content.build_card
        self.assertTrue(build_card, msg='Build card section is not found')
        self.assertTrue(build_card.clear_all_selections_button.is_enabled(),
                        msg='"Clear all selections" button is enabled')
        self.assertTrue(build_card.build_your_race_card_button.is_enabled(),
                        msg='"Build your Racecard" button is enabled')

    def test_003_click_at_clear_all_selections_button(self):
        """
        DESCRIPTION: Click at 'Clear All Selections' button
        EXPECTED: * All ticked checkboxes before each 'Event off time' tab become unchecked
        EXPECTED: * 'Clear All Selections' and 'Build Your Own Racecard' buttons became disabled and NOT clickable
        """
        self.site.horse_racing.tab_content.build_card.clear_all_selections_button.click()

        result = wait_for_result(lambda: self.meeting.check_box.value is True,
                                 name=f'"{self.event_name} {self.meeting_name}" checkbox is become unticked',
                                 expected_result=False,
                                 timeout=2)
        self.assertFalse(result, msg=f'"{self.event_name} {self.meeting_name}" checkbox is still ticked')

        build_card = self.site.horse_racing.tab_content.build_card
        self.assertFalse(build_card.clear_all_selections_button.is_enabled(expected_result=False),
                         msg='"Clear all selections" button is enabled')
        self.assertFalse(build_card.build_your_race_card_button.is_enabled(expected_result=False),
                         msg='"Build your Racecard" button is enabled')

    def test_004_tick_10_checkboxes_before_event_off_time_tabs(self):
        """
        DESCRIPTION: Tick 10 checkboxes before 'Event off time' tabs
        EXPECTED: * All unselected checkboxes before 'Event off time' tabs are disabled and NOT clickable
        EXPECTED: * 'You cannot select anymore races for build your racecard' message appears below 'Clear All Selections' and 'Build Your Own Racecard' buttons
        """
        self.__class__.ui_event_ids = []
        self.__class__.counter = 0
        disabled_checkboxes_verified = 0
        for section_name, section in self.sections.items():
            if section_name not in self.sections_to_skip:
                racing_events = section.items_as_ordered_dict
                self.assertTrue(racing_events, msg=f'No racing events found in "{section_name}" section')
                for event_name, event in racing_events.items():
                    racing_meetings = event.items_as_ordered_dict
                    self.assertTrue(racing_meetings, msg=f'No racing events found in "{event_name}" section')
                    for meeting_name, meeting in racing_meetings.items():
                        if meeting.has_checkbox():
                            meeting.scroll_to()
                            if self.counter < 10:
                                meeting.check_box.value = True
                                self.counter = self.counter + 1
                                self.__class__.meeting_to_uncheck = meeting
                                self.__class__.event_to_uncheck = event
                                self.__class__.meeting_name_to_uncheck = meeting_name
                                self.__class__.event_name = event_name
                                self.ui_event_ids.append(meeting.event_id)
                            else:
                                if disabled_checkboxes_verified < 2:
                                    self.assertFalse(meeting.check_box.is_enabled(expected_result=False, timeout=2),
                                                     msg=f'10 checkboxes already checked, '
                                                         f'but checkbox of "{event_name} {meeting_name}" meeting is not disabled')
                                    self.assertFalse(meeting.check_box.value,
                                                     msg=f'10 checkboxes already checked, '
                                                         f'but checkbox of "{event_name} {meeting_name}" meeting is still clickable')
                                    disabled_checkboxes_verified = disabled_checkboxes_verified + 1
                                else:
                                    break
                        if disabled_checkboxes_verified == 2:
                            break
                    if disabled_checkboxes_verified == 2:
                        break
            if disabled_checkboxes_verified == 2:
                break

        self.softAssert(self.assertTrue, self.counter == 10, msg='There are less than 10 active events')
        self.__class__.counter = 10

        actual_limit_message = self.site.horse_racing.tab_content.build_card.build_card_limit_message
        self.assertEqual(actual_limit_message, vec.racing.BUILD_YOUR_RACE_CARD_LIMIT_MESSAGE,
                         msg=f'"{vec.racing.BUILD_YOUR_RACE_CARD_LIMIT_MESSAGE}" is not shown. '
                             f'Actual message is:"{actual_limit_message}')

    def test_005_untick_one_of_the_checkboxes_before_event_off_time_tabs(self):
        """
        DESCRIPTION: Untick one of the checkboxes before 'Event off time' tabs
        EXPECTED: * Checkbox before 'Event off time' tab is unticked
        EXPECTED: * 'You cannot select anymore races for build your racecard' message disappears
        """
        self.softAssert(self.assertTrue, self.counter == 10, msg='There are less than 10 active events')

        self.event_to_uncheck.scroll_to()
        self.meeting_to_uncheck.scroll_to()
        self.meeting_to_uncheck.check_box.value = False
        self.assertFalse(self.meeting_to_uncheck.check_box.value,
                         msg=f'Checkbox of "{self.event_name} {self.meeting_name_to_uncheck}" meeting was not unchecked')

        self.assertTrue(self.site.horse_racing.tab_content.build_card.build_card_limit_message == '',
                        msg=f'"{vec.racing.BUILD_YOUR_RACE_CARD_LIMIT_MESSAGE}" is still shown')

    def test_006_click_at_build_your_own_racecard_button(self):
        """
        DESCRIPTION: Click at 'Build Your Own Racecard' button
        EXPECTED: * User is navigated to 'Build Your Own Racecard' page
        EXPECTED: * Selected multiple race cards are displayed one after another, separated by 'Event details' sections
        EXPECTED: * Selected multiple race cards are ordered by start date and time in ascending i.e. starting from earliest one
        EXPECTED: * In case start time is identical, alphabetically
        """
        self.site.horse_racing.tab_content.build_card.build_your_race_card_button.click()

        result = wait_for_result(lambda: len(self.site.build_your_card.tab_content.accordions_list.items_as_ordered_dict) > 0,
                                 name='Race Cards to load',
                                 timeout=5)
        self.assertTrue(result, msg='Race Cards were not loaded')

        self.__class__.sections = self.site.build_your_card.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='No sections found on Build Your Own Racecard page')

        self.__class__.event_ids = ",".join(self.ui_event_ids)

        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.ob_config.horseracing_config.category_id)

        self.__class__.response = ss_req.ss_event_to_outcome_for_event(event_id=self.event_ids, query_builder=self.ss_query_builder)
        self.__class__.events = []

        event_properties_named_tuple = namedtuple('event_properties_named_tuple', ['event_name', 'event_time',
                                                                                   'cashout_avail', 'ew_terms_present',
                                                                                   'bog_present', 'promotions',
                                                                                   'countdown_present',
                                                                                   'each_way_class'])
        data_fabric = Datafabric()

        for event in self.response:
            cashout = False
            ew_terms = False
            bog_present = False
            promotions = False
            for market in event['event']['children']:
                if market['market']['name'] == 'Win or Each Way':
                    ew_terms = True if market['market'].get('isEachWayAvailable') is not None else False
                    bog_present = 'GP' in market['market'].get('priceTypeCodes', '')
                    promotions = 'MKTFLAG_EPR' in market['market'].get('drilldownTagNames', '')
                    cashout = market['market'].get('cashoutAvail') == 'Y'
            time_diff = datetime.strptime(event['event']['startTime'], self.ob_format_pattern) - datetime.now(tz=pytz.timezone('GMT')).replace(tzinfo=None)
            countdown = True if 0 < time_diff.total_seconds() < 2700 else False

            event_id = event['event']['id']
            event_data = data_fabric.get_datafabric_data(event_id=event_id,
                                                         category_id=self.ob_config.backend.ti.horse_racing.category_id)
            each_way_class = bool(event_data.get('document', {}).get(event_id, {}).get('raceClass'))

            event = event_properties_named_tuple(event_name=event['event']['name'],
                                                 event_time=datetime.strptime(event['event']['startTime'], self.ob_format_pattern),
                                                 cashout_avail=cashout,
                                                 ew_terms_present=ew_terms,
                                                 bog_present=bog_present,
                                                 promotions=promotions,
                                                 countdown_present=countdown,
                                                 each_way_class=each_way_class)
            self.events.append(event)

        self.events.sort(key=lambda x: (x[1], x[0]))
        sorted_events = [event[0] for event in self.events]

        names_order_ui = []
        for event in list(self.sections.keys()):
            self._logger.info(f'*** Parsing event name "{event}"')
            if self.brand == 'ladbrokes':
                names_order_ui.append(f'{event.splitlines()[0]} {event.splitlines()[1]}')
            else:
                names_order_ui.append(f'{event.splitlines()[1]} {event.splitlines()[0]}')

        sorted_events = sorted_events[:-1]
        self.assertListEqual(names_order_ui, sorted_events,
                             msg=f'Race cards are not ordered alphabetically. Actual \n"{names_order_ui}. '
                                 f'Expected \n"{sorted_events}')

        for section_name, section in self.sections.items():
            self.assertTrue(section.race_event_detail, msg=f'"{section_name}" section has no details container')

    def test_007_verify_event_details_section(self):
        """
        DESCRIPTION: Verify 'Event details' section
        EXPECTED: Event details section contains:
        EXPECTED: * Event name (corresponds to attribute 'name' in SS response)
        EXPECTED: * Event off time (taken from attribute 'name' and corresponds to the race local time)
        EXPECTED: * Date (for tomorrow and future events only) in the format: 'Tuesday 22nd May' (attribute 'startTime')
        EXPECTED: * Race Event Status e.g. 'Going GOOD' (attribute 'going' within 'racingFormEvent' section)
        EXPECTED: * Distance in the format: 'Distance: Xm Yf Zy' (attribute 'distance')
        EXPECTED: * Countdown timer (shown only for events with Race start time less then or equal to 45 minutes)
        """
        names = [event['event']['name'] for event in self.response]
        start_times = [datetime.strptime(event['event']['startTime'], self.ob_format_pattern) + timedelta(hours=1) for
                       event in self.response]
        start_times_hour_minute = [datetime.strftime(event_time, '%H:%M') for event_time in start_times]

        datafabric = Datafabric()
        self.__class__.event_ids = self.event_ids.split(',')

        event_index = 0
        for section_name, section in self.sections.items():
            if len(section_name.splitlines()) == 3:
                future_time = section_name.splitlines()[2]
                day = int(re.search('\d+', future_time).group(0))
                expected_format = self.get_time_format_pattern_for_desktop(day=day)
                try:
                    datetime.strptime(future_time, expected_format)
                except Exception:
                    raise VoltronException(f'Future time format "{future_time}" '
                                           f'is not the same expected "{expected_format}"')

            section_name = f'{section_name.splitlines()[0]} {section_name.splitlines()[1]}' \
                if self.brand == 'ladbrokes' else f'{section_name.splitlines()[1]} {section_name.splitlines()[0]}'
            self.assertIn(section_name, names, msg=f'"{section_name}" not found '
                                                   f'in the list of expected_names "{names}"')
            self.assertIn(section_name[:5], start_times_hour_minute,
                          msg=f'"{section_name[:5]}" time not found in the list of times "{start_times_hour_minute}"')

            if self.events[event_index].countdown_present:
                self.assertTrue(section.has_countdown_timer(),
                                msg=f'Countdown timer is not shown for {section_name}')
            event_index = event_index + 1

            for event_id in self.event_ids:

                data = datafabric.get_datafabric_data(event_id=event_id)
                if not data['Error']:
                    going_code = data['document'][str(event_id)].get('goingCode')
                    race_going = vec.racing.RACING_FORM_EVENT_GOING._asdict().get(going_code) if going_code else None

                    race_distance = data['document'][str(event_id)].get('distance')
                    race_dist = race_distance.strip()
                    course_name = data['document'][str(event_id)].get('courseName').title()
                    df_time = datetime.strptime(data['document'][str(event_id)].get('time'), '%Y-%m-%dT%H:%M:%S')
                    df_time = datetime.strftime(df_time, '%H:%M')

                    if f'{df_time} {course_name}' == section_name:
                        if race_going:
                            self.assertEqual(section.race_event_detail.race_going.value, race_going.upper(),
                                             msg=f'Race going status "{section.race_event_detail.race_going.value}" '
                                                 f'is not the same as in Datafabric response "{race_going}"')
                        if race_dist:
                            self.assertEqual(section.race_event_detail.race_distance.value, race_dist,
                                             msg=f'Race distance "{section.race_event_detail.race_distance.value}" '
                                                 f'is not the same as in Datafabric response "{race_dist}" '
                                                 f'for event with id "{event_id}"')
                        names.remove(section_name)
                        break

    def test_008_verify_displaying_of_markets_tabs(self):
        """
        DESCRIPTION: Verify displaying of Markets tabs
        EXPECTED: * Market tabs are displayed below 'Event details' section
        EXPECTED: * The next tabs are displayed in the following order:
        EXPECTED: * 'Win Or E/W' tab
        EXPECTED: * 'Tricast' Tab
        EXPECTED: * 'Forecast' tab
        EXPECTED: * 'Win Only' tab
        EXPECTED: * 'Betting WO' tab
        EXPECTED: * 'To Finish' tab
        EXPECTED: * 'Top Finish' tab
        EXPECTED: * 'Place Insurance' tab
        EXPECTED: * 'More Markets' tab
        EXPECTED: * 'Totepool' Tab
        EXPECTED: * 'Win or E/W' market is selected by default
        """
        all_tabs = {vec.racing.RACING_EDP_MARKET_TABS.win_or_ew: 1,
                    vec.racing.RACING_EDP_MARKET_TABS.forecast: 2,
                    vec.racing.RACING_EDP_MARKET_TABS.tricast: 3,
                    vec.racing.RACING_EDP_MARKET_TABS.win_only: 4,
                    vec.racing.RACING_EDP_MARKET_TABS.betting_wo: 5,
                    vec.racing.RACING_EDP_MARKET_TABS.to_finish: 6,
                    vec.racing.RACING_EDP_MARKET_TABS.top_finish: 7,
                    vec.racing.RACING_EDP_MARKET_TABS.place_insurance: 8,
                    vec.racing.RACING_EDP_MARKET_TABS.more_markets: 9,
                    vec.racing.RACING_EDP_MARKET_TABS.totepool: 10}
        for section_name, section in self.sections.items():
            ui_tabs = section.tabs_menu.items_as_ordered_dict
            self.assertTrue(ui_tabs, msg=f'No tabs found for "{section_name}" event')
            if vec.racing.RACING_EDP_DEFAULT_MARKET_TAB in ui_tabs.keys():
                self.assertEqual(section.tabs_menu.selected_tab, vec.racing.RACING_EDP_DEFAULT_MARKET_TAB,
                                 msg=f'Default tab "{section.tabs_menu.selected_tab}" '
                                     f'is not the same as expected "{vec.racing.RACING_EDP_DEFAULT_MARKET_TAB}"')
            tabs_indexes = []
            for ui_tab in ui_tabs:
                if 'BETTING W' in ui_tab:
                    ui_tab = 'BETTING W/O'
                ui_tab_index = all_tabs.get(ui_tab)
                if ui_tab_index:
                    tabs_indexes.append(ui_tab_index)

            self.assertEqual(tabs_indexes, sorted(tabs_indexes),
                             msg='Market tabs are not displayed in the proper order')

    def test_009_verify_event_cards(self):
        """
        DESCRIPTION: Verify Event cards
        EXPECTED: Event cards consist of the next items:
        EXPECTED: * 'Each way' terms are displayed above the list of selection
        EXPECTED: * 'Class' of Race parameter is displayed next to 'Each way' terms/places
        EXPECTED: * BPG icon is displayed in the same line as the Each-way terms (but on the right-hand side)
        EXPECTED: * 'CASH OUT' icon is displayed in the same line as 'Each way' terms from the right side (next to BPG icon if available)
        EXPECTED: * Promotion icon is shown on the same line as 'Each way' terms, on the right side, next to BPG/CashOut icons
        EXPECTED: * List of selections/outcomes are displayed for every Event card
        """
        event_index = 0

        for section_name, section in self.sections.items():
            market_list = section.event_markets_list.items_as_ordered_dict
            self.assertTrue(market_list, msg='Market list not found')
            market_section = list(market_list.values())[0]
            self.assertTrue(market_section, msg=f'"Market section not found')

            if market_section.has_header():
                header = market_section.section_header

                status = header.has_cashout_label(timeout=2, expected_result=self.events[event_index].cashout_avail)
                self.assertEqual(status, self.events[event_index].cashout_avail,
                                 msg=f'Cash out label status "{status}" for "{section_name}" section is not as '
                                     f'expected "{self.events[event_index].cashout_avail}"')

                status = header.has_each_way_terms(expected_result=self.events[event_index].ew_terms_present)
                self.assertEqual(status, self.events[event_index].ew_terms_present,
                                 msg=f'EW terms status "{status}" for "{section_name}" section is not as '
                                     f'expected "{self.events[event_index].ew_terms_present}"')

                status = header.is_bpg_icon_present(timeout=2, expected_result=self.events[event_index].bog_present)
                self.assertEqual(status, self.events[event_index].bog_present,
                                 msg=f'BOG icon status "{status}" for "{section_name}" section is not as '
                                     f'expected "{self.events[event_index].bog_present}"')

                # under promotion verification test actually asks to verify only extra place icon
                # as BPG/CashOut icons already have separate verifications
                status = header.has_extra_place_icon(timeout=2, expected_result=self.events[event_index].promotions)
                self.assertEqual(status, self.events[event_index].promotions,
                                 msg=f'Promotion icons status "{status}" for "{section_name}" section is not as '
                                     f'expected "{self.events[event_index].promotions}"')

                status = header.has_each_way_class(timeout=2, expected_result=self.events[event_index].each_way_class)
                self.assertEqual(status, self.events[event_index].each_way_class,
                                 msg=f'Each way class status "{status}" for "{section_name}" section is not as '
                                     f'expected "{self.events[event_index].each_way_class}"')

            event_index += 1
