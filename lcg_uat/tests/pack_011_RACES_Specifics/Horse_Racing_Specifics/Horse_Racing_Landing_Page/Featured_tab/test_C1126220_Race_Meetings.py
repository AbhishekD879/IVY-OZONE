from random import randint
import pytest
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.siteserve_client import SiteServeRequests
from crlat_siteserve_client.utils.date_time import get_date_time_as_string

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.racing
@pytest.mark.high
@pytest.mark.back_button
@pytest.mark.horseracing
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.safari
@vtest
class Test_C1126220_Race_Meetings(BaseRacing):
    """
    TR_ID: C1126220
    NAME: Race Meetings
    DESCRIPTION: This test verifies Race Meetings displaying within Race Grids sections
    PRECONDITIONS: In order to get a list with Classe IDs use a link
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?simpleFilter=class.categoryId:equals:YY&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Where:
    PRECONDITIONS: * X.XX - current supported version of OpenBet release
    PRECONDITIONS: * YY - category id (Horse Racing category id =21)
    PRECONDITIONS: * LL - language (e.g. en, ukr)
    PRECONDITIONS: To retrieve all events for class id indentified in step 1 use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?simpleFilter=market.dispSortName:equals:MR&simpleFilter=class.categoryId:equals:YY&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Where:
    PRECONDITIONS: * X.XX - current supported version of OpenBet release
    PRECONDITIONS: * YYYY is a comma separated list of Class id's(e.g. 97 or 97, 98);
    PRECONDITIONS: * YY - sport category id (Horse Racing category id = 21)
    PRECONDITIONS: * LL - language (e.g. en, ukr)
    PRECONDITIONS: Parameter **typeName** defines 'Race Meetings' name
    PRECONDITIONS: Parameter 'startTime' defines event start time (note, this is not a race local time)
    PRECONDITIONS: REMOVED FUNCTIONALITY: List of HR Statuses:
    PRECONDITIONS: 'race_stage'='**D**' correspond to 'Delayed' badge
    PRECONDITIONS: 'race_stage'='**B**' correspond to 'Going Down' badge
    PRECONDITIONS: 'race_stage'='**C**' correspond to 'At the Post' badge
    PRECONDITIONS: 'race_stage'='**E**' correspond to 'Going Behind' badge
    PRECONDITIONS: 'race_stage'='**O**' correspond to 'Off' badge
    PRECONDITIONS: 'race_stage'='**W**' correspond to 'Awaiting Result' badge
    """
    keep_browser_open = True

    @property
    def basic_query_params(self):
        return self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_FLAG_CODES, OPERATORS.INTERSECTS, 'UK,IE')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.NAME, OPERATORS.NOT_EQUALS, '%7Cnull%7C')) \
            .add_filter(
                simple_filter(LEVELS.EVENT, ATTRIBUTES.DRILLDOWN_TAG_NAMES, OPERATORS.NOT_CONTAINS, 'EVFLAG_AP')) \
            .add_filter(exists_filter(LEVELS.EVENT,
                                      simple_filter(LEVELS.MARKET, ATTRIBUTES.DRILLDOWN_TAG_NAMES,
                                                    OPERATORS.NOT_INTERSECTS, 'MKTFLAG_SP')))

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create UK & IRE events
        EXPECTED: Events are created
        """
        off_time1 = randint(1, 1000)
        off_time2 = randint(1, 20)
        param1 = self.ob_config.add_UK_racing_event(off_time=off_time1, cashout=True, at_races_stream=True)
        param2 = self.ob_config.add_UK_racing_event(number_of_runners=2, lp_prices={0: '1/5', 1: '1/17'},
                                                    off_time=off_time2)
        self.__class__.event1_name = param1.event_off_time
        self.__class__.event2_name = param2.event_off_time
        self.__class__.autotest_racing_meeting = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.name_pattern if self.brand == 'ladbrokes' \
            else self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.name_pattern.upper()

    def test_001_navigate_to_hr_featured_tab_uk_ire_race_grid(self):
        """
        DESCRIPTION: Navigate to HR -> Featured tab -> UK & IRE race grid
        EXPECTED: * Tab for first available day is opened by default
        EXPECTED: * List of Race meeting sections for first day tab is displayed
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')
        current_tab = self.site.horse_racing.tabs_menu.current
        self.assertEqual(current_tab, vec.racing.RACING_DEFAULT_TAB_NAME,
                         msg=f'Current tab "{current_tab}" is not the same as expected "{vec.racing.RACING_DEFAULT_TAB_NAME}"')

        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertIn(self.uk_and_ire_type_name, sections, msg=f'{self.uk_and_ire_type_name} is not in {list(sections.keys())}')
        section = sections[self.uk_and_ire_type_name]
        section.expand()
        self.__class__.meetings_on_ui = section.items_as_ordered_dict
        self.assertTrue(self.meetings_on_ui, msg=f'No meetings found in "{self.uk_and_ire_type_name}"')

    def test_002_verify_race_meeting_sections_content(self):
        """
        DESCRIPTION: Check order of race meetings
        DESCRIPTION: Verify Race meeting sections content
        EXPECTED: Race meetings are ordered according to Disporder parameter from TI tool for appropriate racing type
        EXPECTED: Race meeting header line
        EXPECTED: Each race meeting name corresponds to the '**typeName'** parameter from the Site Server response
        EXPECTED: Cash Out icon on the right
        EXPECTED: Row of events start time
        """
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   class_id=self.horse_racing_live_class_ids,
                                   category_id=self.ob_config.backend.ti.horse_racing.category_id)

        start_date = f'{get_date_time_as_string(days=0)}T00:00:00.000Z'

        query_params = self.basic_query_params \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL, start_date)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.LESS_THAN, self.end_date)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN_OR_EQUAL, self.start_date_minus)) \
            .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.DRILLDOWN_TAG_NAMES, OPERATORS.NOT_CONTAINS, 'EVFLAG_AP')))

        resp = ss_req.ss_event_to_outcome_for_class(query_builder=query_params)
        if self.brand == 'ladbrokes':
            meetings = {event['event']['typeName'].strip(): int(event['event']['typeDisplayOrder'])
                        for event in resp}
        else:
            meetings = {event['event']['typeName'].strip().upper(): int(event['event']['typeDisplayOrder'])
                        for event in resp}

        self._logger.debug(f'*** Meetings list from SS response: "{meetings}"')
        self._logger.debug(f'*** Meetings list from UI: "{self.meetings_on_ui.keys()}"')
        for event in list(meetings.keys()):
            self.assertIn(event, list(meetings.keys()),
                          msg=f'Meetings displayed on ui: {list(self.meetings_on_ui.keys())} '
                              f'are not the same as on the siteserver: {meetings}')

        for meeting_name, meeting in self.meetings_on_ui.items():
            self.assertTrue(meeting.items_as_ordered_dict, msg='No events found for meeting "%s"' % meeting_name)

        self.assertIn(self.autotest_racing_meeting, self.meetings_on_ui.keys(),
                      msg=f'{self.autotest_racing_meeting} is not in {self.meetings_on_ui.keys()}')
        if self.brand != 'ladbrokes':
            has_cashout = self.meetings_on_ui[self.autotest_racing_meeting].cash_out_label.is_displayed()
            self.assertTrue(has_cashout, msg=f'"{self.autotest_racing_meeting}" meeting cash out label not displayed')

    def test_003_verify_next_race_statuses_displaying(self):
        """
        DESCRIPTION: Verify Next Race statuses displaying
        EXPECTED: * Race status badges are not displayed
        EXPECTED: REMOVED FUNCTIONALITY: Next Race status is displayed (if available) for the most recent available event from corresponding meeting grid (if received from push update or SiteServe response) in next format:
        EXPECTED: * 'Next Race' label
        EXPECTED: * Status badge ('Going Down', 'At the Post', 'Going Behind', 'Off', 'Awaiting Result')
        EXPECTED: Next Race status is NOT displayed for resulted event
        """
        # TODO next races is not in scope of this task, will be covered in VOL-909

    def test_004_verify_live_stream_icon(self):
        """
        DESCRIPTION: Verify 'Live Stream' icon
        EXPECTED: * Stream icon is displayed (if available)
        """
        has_live_stream = self.meetings_on_ui[self.autotest_racing_meeting].has_live_stream
        self.assertTrue(has_live_stream, msg=f'"{self.autotest_racing_meeting}" meeting live stream icon is not displayed')

    def test_005_verify_row_of_events_displaying(self):
        """
        DESCRIPTION: Verify row of events displaying
        EXPECTED: * Events off times are displayed in bold if 'priceTypeCodes="LP"' attribute is available for 'Win or Each way' market only
        """
        self.__class__.autotest_uk_events = self.meetings_on_ui[self.autotest_racing_meeting].items_as_ordered_dict
        self.assertTrue(self.autotest_uk_events, msg=f'Event not found for "{self.autotest_racing_meeting}"')
        self.assertIn(self.event1_name, self.autotest_uk_events.keys(),
                      msg=f'{self.event1_name} is not in {self.autotest_uk_events.keys()}')
        self.assertIn(self.event2_name, self.autotest_uk_events.keys(),
                      msg=f'{self.event2_name} is not in {self.autotest_uk_events.keys()}')
        if self.brand != 'ladbrokes':
            event1_is_priced = self.autotest_uk_events[self.event1_name].is_priced
            self.assertFalse(event1_is_priced, msg=f'Event "{self.event1_name}" is priced')
            event2_is_priced = self.autotest_uk_events[self.event2_name].is_priced
            self.assertTrue(event2_is_priced, msg=f'Event "{self.event2_name}" is not priced')

    def test_006_tap_on_event_off_time(self):
        """
        DESCRIPTION: Tap on event off time
        EXPECTED: Corresponding Event details page is opened
        """
        self.autotest_uk_events[self.event2_name].click()
        self.site.wait_content_state(state_name='RacingEventDetails')

    def test_007_tap_back_button(self):
        """
        DESCRIPTION: Tap 'Back' button
        EXPECTED: Horse Races Landing page is opened
        """
        self.site.back_button_click()
        self.site.wait_content_state(state_name='Horseracing')
