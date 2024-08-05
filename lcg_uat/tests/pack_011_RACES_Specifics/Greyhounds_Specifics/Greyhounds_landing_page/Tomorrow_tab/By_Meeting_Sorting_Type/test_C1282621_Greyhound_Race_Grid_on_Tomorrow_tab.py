import pytest
import collections
import tests
import re
import datetime
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
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@vtest
class Test_C1282621_Greyhound_Race_Grid_on_Tomorrow_tab(BaseRacing):
    """
    TR_ID: C1282621
    NAME: Greyhound Race Grid on Tomorrow tab
    DESCRIPTION: This test case verifies the Race Grid on Tomorrow tab of Greyhounds
    DESCRIPTION: New Design (LADBROKES Desktop) - https://app.zeplin.io/project/5c6d3e910cb0f599dfd2145b/screen/5d01033ae1287915e4816435
    PRECONDITIONS: Greyhound landing page is opened
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
    PRECONDITIONS: Parameter **startTime** defines event start time (note, this is not a race local time)
    PRECONDITIONS: Load the app
    PRECONDITIONS: Navigate to Greyhounds landing page -> 'TODAY'tab is selected by default
    """
    keep_browser_open = True

    @property
    def basic_query_params(self):
        return self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_FLAG_CODES, OPERATORS.INTERSECTS, 'UK,IE')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_FLAG_CODES, OPERATORS.NOT_INTERSECTS, 'SP')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.NAME, OPERATORS.NOT_EQUALS, '%7Cnull%7C')) \
            .add_filter(
            simple_filter(LEVELS.EVENT, ATTRIBUTES.DRILLDOWN_TAG_NAMES, OPERATORS.NOT_CONTAINS, 'EVFLAG_AP')) \
            .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.DRILLDOWN_TAG_NAMES,
                                                                  OPERATORS.NOT_INTERSECTS, 'MKTFLAG_SP')))

    def compare_ui_events_with_ss_response(self, resp):
        meetings_events_ss, meetings_events_ui = collections.defaultdict(list), collections.defaultdict(list)

        meetings_list_ss = self.get_meetings_list_from_response(response=resp)
        self._logger.debug(f'*** SiteServe Response: Meetings list: "{meetings_list_ss}"')

        for meeting in meetings_list_ss:
            for event_resp in resp:
                if event_resp['event']['typeName'].strip() == meeting:
                    search = re.search(r'([\d:]+)', event_resp['event']['name'])
                    event_time = search.group(1) if search else ''
                    meetings_events_ss[meeting].append(event_time)

        meetings_events_ss = [{key.upper(): sorted(value)} for key, value in meetings_events_ss.items()]
        meetings_events_ss = sorted(meetings_events_ss, key=lambda d: sorted(d.items()))

        self._logger.debug(f'*** SiteServe Response: List of events in each meeting: "{meetings_events_ss}"')
        section_name = vec.racing.UK_AND_IRE_TYPE_NAME.upper() if self.brand == 'bma' and self.device_type == 'mobile' else vec.racing.UK_AND_IRE_TYPE_NAME
        if self.brand == 'ladbrokes':
            sections = self.get_sections('greyhound-racing')
        else:
            sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
        section = sections[section_name]
        section.expand()
        self.assertTrue(section.is_expanded(),
                        msg=f'Section sections {vec.racing.UK_AND_IRE_TYPE_NAME.upper()} is not expanded')

        meetings_list_ui = section.items_as_ordered_dict
        self.assertTrue(meetings_list_ui, msg=f'No meetings found in {vec.racing.UK_AND_IRE_TYPE_NAME.upper()}')

        self._logger.debug(f'*** greyhound race page: Meetings list: "{list(meetings_list_ui.keys())}"')

        meetings_list_ss_sorted = sorted([meeting.upper() for meeting in meetings_list_ss])
        for date_tab_name in meetings_list_ss_sorted:
            self.assertIn(date_tab_name, meetings_list_ss_sorted,
                          msg=f'\nMeetings list on UI: \n:"{date_tab_name}", '
                              f'\nMeetings list from SiteServe: \n"{meetings_list_ss_sorted}"')

        for meeting_name, meeting in meetings_list_ui.items():
            events = meeting.items_as_ordered_dict
            meeting_name = meeting_name.upper()
            self.assertTrue(events, msg=f'No events found for meeting "{meeting_name}"')
            meetings_events_ui[meeting_name] = events.keys()

        meetings_events_ui = [{key: sorted(value)} for key, value in meetings_events_ui.items()]
        meetings_events_ui = sorted(meetings_events_ui, key=lambda d: sorted(d.items()))

        self._logger.debug(f'*** greyhound Racing page: List of events in each meeting: "{meetings_events_ui}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create greyhound events
        EXPECTED: Events are created
        """
        self.__class__.ss_req_hr = SiteServeRequests(env=tests.settings.backend_env,
                                                     class_id=self.ob_config.virtuals_config.virtual_greyhounds.class_id,
                                                     category_id=self.ob_config.backend.ti.greyhound_racing.category_id,
                                                     brand=self.brand)
        self.__class__.tomorrow = vec.sb.SPORT_DAY_TABS.tomorrow
        if tests.settings.backend_env != 'prod':
            start_time_tomorrow = self.get_date_time_formatted_string(days=1, hours=2)
            self.ob_config.add_virtual_greyhound_racing_event(number_of_runners=1,
                                                              start_time=start_time_tomorrow)
            self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1,
                                                         start_time=start_time_tomorrow)

            uk_event1 = self.ob_config.add_UK_greyhound_racing_event(days=1, hours=1)
            self.__class__.event_off_time1 = uk_event1.event_off_time

    def test_001_navigate_to_tomorrow_tab(self):
        """
        DESCRIPTION: Navigate to Tomorrow tab
        EXPECTED: **FOR CORAL:**
        EXPECTED: - 'TOMORROW' tab is opened and race grid is shown with 'BY MEETING' sorting switched on by default
        EXPECTED: - 'TOMORROW' tab contains 2 sub-tabs - 'BY MEETING' and 'BY TIME'
        EXPECTED: **FOR LADBROKES:**
        EXPECTED: - 'TOMORROW' tab is opened and race grid is shown with 'BY MEETING' sorting switched on by default
        EXPECTED: - NO sub-tabs available
        """
        self.navigate_to_page(name='greyhound-racing')
        self.site.wait_content_state('Greyhoundracing')
        if self.brand == 'ladbrokes':
            tomorrow = vec.sb.TABS_NAME_TOMORROW
        else:
            tomorrow = vec.sb.SPORT_DAY_TABS.tomorrow
        self.site.greyhound.tabs_menu.click_button(tomorrow)
        self.assertTrue(self.site.greyhound.tabs_menu.items_as_ordered_dict.get(tomorrow).is_selected(),
                        msg='"Tomorrow tab" is not present')

    def test_002_verify_race_grid_sections(self):
        """
        DESCRIPTION: Verify race grid sections
        EXPECTED: The following sections are displayed and expanded by default:
        EXPECTED: **FOR CORAL (Mobile/Desktop):**
        EXPECTED: - UK&IRE
        EXPECTED: - VIRTUAL
        EXPECTED: **FOR LADBROKES (Mobile/Desktop):**
        EXPECTED: - UK/IRELAND RACES
        EXPECTED: - VIRTUAL RACES
        """
        if self.brand == 'ladbrokes':
            sections = self.get_sections('greyhound-racing')
        else:
            sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
        sections = list(sections.values())
        self.assertTrue(sections, msg='No sections found in today tab')
        for i in range(len(sections)):
            self.assertTrue(sections[i].is_expanded(), msg=f'Event "{sections[i]}" is not expanded')
            sections[i].collapse()
            self.assertFalse(sections[i].is_expanded(expected_result=False),
                             msg=f'Event "{sections[i]}" is not collapsed')
            if not self.brand == 'ladbrokes' and self.device_type == 'mobile':
                self.assertTrue(sections[i].is_chevron_down(),
                                msg=f'Event "{sections[i]}" Chevron arrow to point to the top')
            sections[i].expand()
            self.assertTrue(sections[i].is_expanded(), msg=f'Event "{sections[i]}" is not expanded')
            if self.brand == 'bma' and self.device_type == 'desktop':
                self.assertTrue(sections[i].is_chevron_up(),
                                msg=f'Event "{sections[i]}" Chevron arrow to point to the bottom')

    def test_003_collapse_and_expand_the_grid_by_tapping_on_the_headers(self):
        """
        DESCRIPTION: Collapse and expand the grid by tapping on the headers
        EXPECTED: It is possible to collapse/expand accordions by tapping on the headers
        EXPECTED: **FOR MOBILE (Coral/Ladbrokes) and DESKTOP (Ladbrokes):**
        EXPECTED: - After collapsing: the downward arrow is displayed on the right side
        EXPECTED: - After expanding: No arrows displayed
        EXPECTED: **FOR DESKTOP (Coral):**
        EXPECTED: - After collapsing: the downward arrow is displayed on the right side
        EXPECTED: - After expanding: the upward arrow is displayed on the right side
        """
        # covered in step 2

    def test_004_veriy_race_grid_content(self):
        """
        DESCRIPTION: Veriy Race Grid content
        EXPECTED: All events from SS response with start time ( **startTime** attribute) corresponding to the day tomorrow are displayed within corresponding type (race meeting) section
        """
        start_date = f'{get_date_time_as_string(date_time_obj=datetime.date.today(), days=1, time_format="%Y-%m-%dT%H:%M:%S.000Z")}'
        end_date = f'{get_date_time_as_string(date_time_obj=datetime.date.today(), days=2, time_format="%Y-%m-%dT%H:%M:%S.000Z")}'
        query_params_tomorrow = self.basic_query_params \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL, start_date)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.LESS_THAN, end_date)) \
            .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.TEMPLATE_MARKET_NAME,
                                                                  OPERATORS.EQUALS, '|Win or Each Way|')))
        resp = self.ss_req_hr.ss_event_to_outcome_for_class(class_id=[286],
                                                            query_builder=query_params_tomorrow)
        self.compare_ui_events_with_ss_response(resp=resp)

    def test_005_verify_filtered_out_events(self):
        """
        DESCRIPTION: Verify filtered out events
        EXPECTED: - Antepost events are not received and are not shown (drilldownTagNames:"EVFLAG_AP)
        EXPECTED: - Events that passed "Suspension Time" are not received and shown (**suspendAtTime** attribute)
        """
        section_name = vec.racing.UK_AND_IRE_TYPE_NAME.upper() if self.brand == 'bma' and self.device_type == 'mobile' else vec.racing.UK_AND_IRE_TYPE_NAME
        if self.brand == 'ladbrokes':
            sections = self.get_sections('greyhound-racing')
        else:
            sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found in tomorrow tab')
        section = sections.get(section_name)
        section.expand()
        rows = section.items_as_ordered_dict
        self.assertTrue(rows, msg=f'No one row was found in section: "{section_name}"')
        events = rows.items()
        self.assertTrue(events, msg=f'No one event was found in row: "{rows}"')
        # can not automate "Suspension Time" in tomorrows tab
