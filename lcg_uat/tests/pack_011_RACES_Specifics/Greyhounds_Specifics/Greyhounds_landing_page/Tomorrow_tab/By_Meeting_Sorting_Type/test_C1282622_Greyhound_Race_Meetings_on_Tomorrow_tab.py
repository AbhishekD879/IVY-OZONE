import pytest
import tests
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.environments import constants as vec
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import SiteServeRequests
from crlat_siteserve_client.siteserve_client import exists_filter
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.utils.date_time import get_date_time_as_string


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Can not create events in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@vtest
class Test_C1282622_Greyhound_Race_Meetings_on_Tomorrow_tab(BaseRacing):
    """
    TR_ID: C1282622
    NAME: Greyhound Race Meetings on Tomorrow tab
    DESCRIPTION: This test case verifies Race Meetings displaying within Greyhound Race Grid on Tomorrow tab
    DESCRIPTION: New design (Ladbrokes Desktop): https://app.zeplin.io/project/5c6d3e910cb0f599dfd2145b/screen/5d01033ae1287915e4816435
    PRECONDITIONS: To retrieve data from the Site Server use the following:
    PRECONDITIONS: 1) To get Classe IDs use a link
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Where:
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: XX - category id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Greyhound category id = 19
    PRECONDITIONS: 2) To get all 'Events' for the class ID's use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?translationLang=LL
    PRECONDITIONS: Where:
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY is a comma separated list of class ID's (e.g. 97 or 97, 98).
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Parameter  **'typeName'**  defines 'Race Meetings' name
    PRECONDITIONS: Parameter **'startTime'** defines event start time (note, this is not a race local time)
    PRECONDITIONS: NOTE: Cashout icons removed for LADBROKES within BMA-39817
    PRECONDITIONS: Load the app
    PRECONDITIONS: Go to the Greyhound landing page -> 'TODAY'tab is selected by default
    PRECONDITIONS: Navigate to the 'TOMORROW' tab
    """
    keep_browser_open = True

    @property
    def basic_query_params(self):
        return self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_FLAG_CODES, OPERATORS.INTERSECTS, 'UK,IE')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.NAME, OPERATORS.NOT_EQUALS, '%7Cnull%7C')) \
            .add_filter(
            simple_filter(LEVELS.EVENT, ATTRIBUTES.DRILLDOWN_TAG_NAMES, OPERATORS.NOT_CONTAINS, 'EVFLAG_AP')) \
            .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.DRILLDOWN_TAG_NAMES,
                                                                  OPERATORS.NOT_INTERSECTS, 'MKTFLAG_SP')))

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create UK & IRE events
        EXPECTED: Events are created
        """
        start_time_tomorrow = self.get_date_time_formatted_string(days=1, hours=1)
        param2 = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1,
                                                              start_time=start_time_tomorrow, cashout=True,
                                                              at_races_stream=True)

        start_time_tomorrow = self.get_date_time_formatted_string(days=1, hours=2)
        self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1, start_time=start_time_tomorrow, cashout=True,
                                                     at_races_stream=True)

        start_time_tomorrow = self.get_date_time_formatted_string(days=1, hours=3)
        self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1,
                                                     start_time=start_time_tomorrow, cashout=True,
                                                     at_races_stream=True)

        start_time_tomorrow = self.get_date_time_formatted_string(days=1, hours=4)
        self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1,
                                                     start_time=start_time_tomorrow, cashout=True,
                                                     at_races_stream=True)

        start_time_tomorrow = self.get_date_time_formatted_string(days=1, hours=5)
        self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1, start_time=start_time_tomorrow, cashout=True,
                                                     at_races_stream=True)

        self.ob_config.add_virtual_greyhound_racing_event(number_of_runners=1, days=1, hours=2, cashout=True,
                                                          at_races_stream=True)

        self.__class__.event2_name = param2.event_off_time
        self.__class__.autotest_racing_meeting = self.ob_config.backend.ti.greyhound_racing.greyhounds_live.autotest.name_pattern if self.brand == 'ladbrokes' \
            else self.ob_config.backend.ti.greyhound_racing.greyhounds_live.autotest.name_pattern.upper()

    def test_001_check_order_of_race_meetings_inside_the_race_grid_section_eg_tomorrows_races(self):
        """
        DESCRIPTION: Check order of race meetings inside the race grid section (e.g. 'TOMORROWS RACES')
        EXPECTED: Race meetings are ordered in ascending alphabetical order (A-Z)
        """
        self.navigate_to_page(name='greyhound-racing')
        self.site.wait_content_state('Greyhoundracing', timeout=30)

        if self.brand == 'ladbrokes':
            tomorrow = vec.sb.TABS_NAME_TOMORROW
        else:
            tomorrow = vec.sb.SPORT_DAY_TABS.tomorrow
        try:
            selection_buttons = self.site.greyhound.tabs_menu.items_as_ordered_dict
            selection_buttons[tomorrow].click()
            self.assertTrue(self.site.greyhound.tabs_menu.items_as_ordered_dict.get(tomorrow).is_selected(),
                            msg='"Tomorrow tab" is not present')
        except Exception:
            selection_buttons = self.site.greyhound.tabs_menu.items_as_ordered_dict
            selection_buttons[tomorrow].click()
            self.assertTrue(self.site.greyhound.tabs_menu.items_as_ordered_dict.get(tomorrow).is_selected(),
                            msg='"Tomorrow tab" is not present')
        if self.brand == 'bma':
            actual_sub_tabs = self.site.greyhound.tab_content.items_names
            self.assertEqual(actual_sub_tabs, vec.racing.EXPECTED_TIME_GROUPING_BUTTONS_RACING,
                             msg=f'Actual tabs: "{actual_sub_tabs}" is not equal with the'
                                 f'Expected tabs: "{vec.racing.EXPECTED_TIME_GROUPING_BUTTONS_RACING}"')
            actual_sub_tab = self.site.greyhound.tab_content.current
            self.assertEqual(actual_sub_tab, vec.racing.DEFAULT_TIME_GROUPING_BUTTON_RACING,
                             msg=f'Actual tabs: "{actual_sub_tab}" is not equal with the'
                                 f'Expected tab: "{vec.racing.DEFAULT_TIME_GROUPING_BUTTON_RACING}"')

    def test_002_verify_race_meeting_sections_content(self):
        """
        DESCRIPTION: Verify Race meeting sections content
        EXPECTED: * Race meeting header
        EXPECTED: * Row of events start time
        """
        if self.brand == 'ladbrokes':
            sections = self.get_sections('greyhound-racing')
        else:
            self.device.refresh_page()
            sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found in tomorrow tab')
        section_name = vec.racing.UK_AND_IRE_TYPE_NAME.upper() if self.brand == 'bma' and self.device_type == 'mobile' else vec.racing.UK_AND_IRE_TYPE_NAME
        section = sections[section_name]
        section.expand()
        self.__class__.meetings_on_ui = section.items_as_ordered_dict
        self.assertTrue(self.meetings_on_ui, msg=f'No meetings found in "{section_name}"')

        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   class_id=self.ob_config.virtuals_config.virtual_greyhounds.class_id,
                                   category_id=self.ob_config.backend.ti.greyhound_racing.category_id)

        start_date = f'{get_date_time_as_string(days=0)}T00:00:00.000Z'
        query_params = self.basic_query_params \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL, start_date)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.LESS_THAN, self.end_date)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN_OR_EQUAL,
                                      self.start_date_minus)) \
            .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.DRILLDOWN_TAG_NAMES,
                                                                  OPERATORS.NOT_CONTAINS, 'EVFLAG_AP')))

        resp = ss_req.ss_event_to_outcome_for_class(query_builder=query_params)

        if self.brand == 'ladbrokes':
            meetings = {event['event']['typeName'].strip(): int(event['event']['typeDisplayOrder'])
                        for event in resp}
        else:
            meetings = {event['event']['typeName'].strip().upper(): int(event['event']['typeDisplayOrder'])
                        for event in resp}

        for event in list(meetings.keys()):
            self.assertIn(event, list(meetings.keys()),
                          msg=f'Meetings displayed on ui: {list(self.meetings_on_ui.keys())} '
                              f'are not the same as on the siteserver: {meetings}')

        for meeting_name, meeting in self.meetings_on_ui.items():
            self.assertTrue(meeting.items_as_ordered_dict, msg='No events found for meeting "%s"' % meeting_name)

        self.assertIn(self.autotest_racing_meeting, self.meetings_on_ui.keys(),
                      msg=f'{self.autotest_racing_meeting} is not in {self.meetings_on_ui.keys()}')

    def test_003_verify_race_meeting_header_line_content(self):
        """
        DESCRIPTION: Verify Race meeting header line content
        EXPECTED: * Race race meeting name on the left
        EXPECTED: * Each race meeting name corresponds to the '**typeName'** parameter from the Site Server response
        EXPECTED: * Race meeting name is NOT clickable
        EXPECTED: * Live Stream icon (if available) on the right
        """
        # covered in step 3

    def test_004_only_coral_verify_cash_out_icon_displaying(self):
        """
        DESCRIPTION: Only Coral: Verify 'Cash Out' icon displaying
        EXPECTED: **FOR CORAL Only**
        EXPECTED: 'CASH OUT' icon is shown if at least one of it's events has cashoutAvail="Y" and on all higher levels cashoutAvail="Y"
        """
        if self.brand != 'ladbrokes':
            has_cashout = self.meetings_on_ui[self.autotest_racing_meeting].cash_out_label.is_displayed()
            self.assertTrue(has_cashout, msg=f'"{self.autotest_racing_meeting}" meeting cash out label not displayed')

    def test_005_verify_live_stream_icon(self):
        """
        DESCRIPTION: Verify 'Live Stream' icon
        EXPECTED: * Stream icon is displayed (if available) on the right
        EXPECTED: * **FOR CORAL** Play icon for races with live stream (if available) on the right
        EXPECTED: ![](index.php?/attachments/get/36628)
        EXPECTED: * **FOR LADBROKES** WATCH icon for races with live stream (if available) on the right
        EXPECTED: ![](index.php?/attachments/get/36629)
        EXPECTED: * Stream icon is shown for event type where stream is applicable
        EXPECTED: * Stream icon is for informational purpose only
        """
        has_live_stream = self.meetings_on_ui[self.autotest_racing_meeting].has_live_stream
        self.assertTrue(has_live_stream,
                        msg=f'"{self.autotest_racing_meeting}" meeting live stream icon is not displayed')

    def test_006_verify_row_of_events_displaying(self):
        """
        DESCRIPTION: Verify row of events displaying
        EXPECTED: * Event off times are displayed horizontally across the page
        EXPECTED: * **FOR CORAL** Events off times are displayed in bold if 'priceTypeCodes="LP"' attribute is available for 'Win or Each way' market only
        EXPECTED: * **FOR LADBROKES** ALL events off times are displayed in bold no matter if it is 'LP' or 'SP' prices
        EXPECTED: * Ladbrokes: Race Statuses displayed for started or resulted events:
        EXPECTED: Race Off - event has 'isOff=Yes'
        EXPECTED: Live - event has 'isOff=Yes'and at least one of markets has 'betInRunning=true'
        EXPECTED: Resulted - event has 'isResulted=true' + 'isFinished=true'
        EXPECTED: * Coral: Signposting icons are displayed next to event off time (if available)
        EXPECTED: * Ladbrokes: Signposting icons are NOT displayed next to event off time
        """
        self.__class__.autotest_uk_events = self.meetings_on_ui[self.autotest_racing_meeting].items_as_ordered_dict
        self.assertTrue(self.autotest_uk_events, msg=f'Event not found for "{self.autotest_racing_meeting}"')
        self.assertIn(self.event2_name, self.autotest_uk_events.keys(),
                      msg=f'{self.event2_name} is not in {self.autotest_uk_events.keys()}')
        if self.brand != 'ladbrokes':
            event1_is_priced = self.autotest_uk_events[self.event2_name].is_priced
            self.assertFalse(event1_is_priced, msg=f'Event "{self.event2_name}" is priced')

    def test_007_verify_event_off_times(self):
        """
        DESCRIPTION: Verify event off times
        EXPECTED: Event off times corresponds to the race local time from the **'name'** attribute from the Site Server
        """
        # Covered in step 2

    def test_008_verify_scrolling_between_event_off_times(self):
        """
        DESCRIPTION: Verify scrolling between event off times
        EXPECTED: On **Mobile/Tablet** ability to scroll left and right is available via swiping
        EXPECTED: On **Desktop** Race meeting with too many event off times to be shown in one line has arrows which appear on hover to scroll horizontally.
        EXPECTED: Events off times are scrolled one by one after click arrows
        """
        if self.device_type == 'mobile':
            if self.brand == 'ladbrokes':
                sections = self.get_sections('greyhound-racing')
            else:
                try:
                    sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
                    self.assertTrue(sections, msg='No race found in tomorrow tab section')
                except Exception:
                    self.device.refresh_page()
                    sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No race found in tomorrow tab section')
            sections = list(sections.values())
            self.assertTrue(sections, msg='No sections found in tomorrow tab')
            next_races_section = sections[len(sections) - 2]
            next_races = next_races_section.items_as_ordered_dict
            self.assertTrue(next_races, msg='No race found in tomorrow section')
            list(next_races.values())[0].scroll_to()
            for i, (race_name, race) in enumerate(next_races.items()):
                race.scroll_to()
                self.assertTrue(race.is_displayed(),
                                msg=f'Next race: "{race_name}" not displayed after scrolling to')
                if i > 1:
                    prev_race_name, prev_race = list(next_races.items())[i - 2]
                    self.assertFalse(prev_race.is_displayed(expected_result=False, scroll_to=False),
                                     msg=f'Previous race: "{prev_race_name}" still displayed after scrolling to next')

            for i, (race_name, race) in enumerate(list(next_races.items())[::-1]):
                race.scroll_to()
                self.assertTrue(race.is_displayed(),
                                msg=f'Previous race: "{race_name}" not displayed after scrolling to')
                if 1 < i < (len(next_races.items()) - 2):
                    next_race_name, next_race = list(next_races.items())[::-1][i - 3]
                    self.assertFalse(next_race.is_displayed(expected_result=False, scroll_to=False),
                                     msg=f'Next race: "{next_race_name}" still displayed after scrolling to previous')
            self.device.driver.implicitly_wait(0)

    def test_009_tap_on_event_off_time(self):
        """
        DESCRIPTION: Tap on event off time
        EXPECTED: Corresponding Event details page is opened
        """
        self.autotest_uk_events[self.event2_name].click()
        self.site.wait_content_state(state_name='GreyHoundEventDetails')

    def test_010_tap_back_button(self):
        """
        DESCRIPTION: Tap 'Back' button
        EXPECTED: Greyhound Landing page is opened
        """
        self.site.back_button_click()
        self.site.wait_content_state(state_name='Greyhoundracing')
