import pytest
import time
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from datetime import datetime
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter, SiteServeRequests, exists_filter
from crlat_siteserve_client.utils.date_time import get_date_time_as_string
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.other
@vtest
class Test_C59095268_Verify_Events_grouping_and_ordering_on_Matches_tab(BaseSportTest):
    """
    TR_ID: C59095268
    NAME: Verify Events grouping and ordering on 'Matches' tab
    DESCRIPTION: This test case verifies how events are grouped and ordered on 'Matches' tab
    PRECONDITIONS: Configurations:
    PRECONDITIONS: Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: Note:
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - To verify queries from Front-end to SiteServe for data availability checking use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+get+data+from+Openbet+Site+Server
    PRECONDITIONS: - To verify queries from CMS to SiteServe for data availability checking use the following instruction: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-QueriestoSiteServe(SS)
    PRECONDITIONS: Steps:
    PRECONDITIONS: 1. 'Matches' tab is enabled in CMS for 'Tier 1/2' Sport and data are available
    PRECONDITIONS: 3. Navigate to the selected 'Tier 1/2' Sports Landing Page
    PRECONDITIONS: 4. 'Matches'tab is opened by default
    """
    keep_browser_open = True
    expected_events_order = []

    def verify_events_are_present(self, resp):
        event = next((event for event in resp if
                      event.get('event') and event['event'] and event['event'].get('children')), None)
        if not event:
            raise SiteServeException(
                f'No active events found for category id "{self.ob_config.backend.ti.tennis.category_id}"')

    def get_event_start_time(self, league: str, sports_list: list) -> dict:
        """
        Gets events start times
        :param sports_list: list of all sports
        :param league: str league name
        :return: return dictionary where key is name and value is event startTime
        """
        events = [event['event'] for event in sports_list if event['event']['typeName'].upper() in league.upper()]
        return {x['name']: x['startTime'] for x in events}

    def sort_by_disp_order(self, sports_list: list):
        """
        :param sports_list: list of dict
        :return: sorted list by type typeDisplayOrder in ascending order otherwise sort by name
        """
        sports_list = [item for item in sports_list]
        sport_categories = {f"{sport['event']['categoryName']} - {sport['event']['typeName']}":
                                int(sport['event']['typeDisplayOrder']) for sport in sports_list}
        return sorted(sport_categories, key=lambda k: (sport_categories[k], k))

    def get_order_of_events(self, league: str, sports_list: list) -> list:
        """
        Having response gets the expected order of events in coupon
        :param league: str league name
        :param sports_list: list of all sports
        :return: expected order of events in league
        """
        if league:
            event_start_times = self.get_event_start_time(league=league, sports_list=sports_list)
        else:
            event_start_times = {x['event']['name']: x['event']['startTime'] for x in sports_list}

        event_start_times_converted = []
        for name, start_time in event_start_times.items():
            date_time_obj = datetime.strptime(start_time.split(',')[0], self.ob_format_pattern)
            event_start_times_converted.append((name, date_time_obj.timetuple()))

        expected_order_tuple = sorted(event_start_times_converted, key=lambda x: (x[1], x[0]))
        return [x for x, _ in expected_order_tuple]

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create tennis events
        """
        tennis_category_id = self.ob_config.backend.ti.tennis.category_id
        if tests.settings.backend_env == 'prod':
            event1 = self.get_active_events_for_category(category_id=tennis_category_id)[0]
            self._logger.info(f'*** Found event: {event1}')
        else:
            self.check_sport_configured(tennis_category_id)
            self.ob_config.add_tennis_event_to_autotest_trophy()
            self.ob_config.add_tennis_event_to_davis_cup()
            self.ob_config.add_tennis_event_to_european_open()
            self.ob_config.add_tennis_event_to_nice_open()

            start_time = self.get_date_time_formatted_string(hours=6)

            event_params = self.ob_config.add_tennis_event_to_autotest_trophy(
                start_time=self.get_date_time_formatted_string(hours=1))
            self.__class__.expected_events_order.append(f'{event_params.team1} v {event_params.team2}')

            event_params2 = self.ob_config.add_tennis_event_to_autotest_trophy(
                start_time=self.get_date_time_formatted_string(hours=2))
            self.__class__.expected_events_order.append(f'{event_params2.team1} v {event_params2.team2}')

            event_params3 = self.ob_config.add_tennis_event_to_autotest_trophy(
                start_time=self.get_date_time_formatted_string(hours=3))
            self.__class__.expected_events_order.append(f'{event_params3.team1} v {event_params3.team2}')

            event_params4 = self.ob_config.add_tennis_event_to_autotest_trophy(
                start_time=self.get_date_time_formatted_string(hours=4))
            self.__class__.expected_events_order.append(f'{event_params4.team1} v {event_params4.team2}')

            for outright in range(0, 4):
                outright_name = f'Outright {int(time.time())}'
                self.ob_config.add_tennis_outright_event_to_autotest_league(
                    event_name=outright_name, start_time=start_time)

        self.__class__.start_date = f'{get_date_time_as_string(days=-1)}T21:00:00.000Z'
        days_for_match = 0
        if self.device_type != 'desktop':
            days_for_match = 2

        query = self.ss_query_builder \
            .add_filter(
            simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.INTERSECTS, str(tennis_category_id))) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL,
                                      self.start_date)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.LESS_THAN,
                                      f'{get_date_time_as_string(days=days_for_match)}T21:00:00.000Z')) \
            .add_filter(simple_filter(LEVELS.MARKET, ATTRIBUTES.DISP_SORT_NAME, OPERATORS.INTERSECTS, 'HH, MH, WH')) \
            .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.DISP_SORT_NAME,
                                                                  OPERATORS.INTERSECTS, 'HH, MH, WH'))) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_FALSE)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN,
                                      self.start_date_minus))
        class_ids = self.get_class_ids_for_category(category_id=tennis_category_id)

        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=tennis_category_id)
        events_list = ss_req.ss_event_to_outcome_for_class(query_builder=query, class_id=class_ids)
        self.verify_events_are_present(resp=events_list)

        sorted_leagues = self.sort_by_disp_order(events_list)
        self.__class__.league_name = sorted_leagues[0]
        self.__class__.expected_leagues_order = [item.upper() for item in sorted_leagues]

        self.__class__.expected_events_order = self.get_order_of_events(league=self.league_name,
                                                                        sports_list=events_list)
        self.site.wait_content_state(state_name='Homepage')
        self.navigate_to_page(name='sport/tennis')
        self.site.wait_content_state(state_name=vec.bma.TENNIS, timeout=30)

        current_tab = self.site.tennis.tabs_menu.current
        self.assertEqual(current_tab, self.expected_sport_tabs.matches,
                         msg=f'\nDefault tab: "{current_tab}" opened'
                             f'\nExpected tab: "{self.expected_sport_tabs.matches}" opened')

        if self.device_type == 'desktop':
            current_date_tab = self.site.tennis.date_tab.current
            self.assertEqual(current_date_tab, vec.sb.SPORT_DAY_TABS.today,
                             msg=f'\nDefault tab: "{current_tab}" opened'
                                 f'\nExpected tab: "{self.expected_sport_tabs.matches}" opened')

    def test_001_verify_events_grouping(self):
        """
        DESCRIPTION: Verify event's grouping
        EXPECTED: * Events are grouped by **classId** and **typeId**
        EXPECTED: * Events are displayed in accordions
        EXPECTED: * First 3 accordions are expanded by default, the rest - collapsed
        """
        self.__class__.sections = self.site.tennis.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='No Specials sections found')

        if len(self.sections) > 1:
            for matches_name, matches in list(self.sections.items())[:3]:
                self.assertTrue(matches.is_expanded(expected_result=True),
                                msg=f'Special section "{matches_name}" is not expanded by default')
        # This will remove all See All Links form the League Accordian
        self.section_dict = {}
        for league_name, leauge in dict(self.__class__.sections).items():
            league_name = league_name.replace("\nSEE ALL", "")
            self.section_dict[league_name] = leauge
        # If event is displayed in this league it is automatically verifies that events are grouped by TypeID
        # self.__class__.league = self.sections_dict.get(self.league_name.upper())
        self.__class__.league = self.section_dict.get(self.__class__.league_name.upper())
        self.assertEqual(self.league.fixture_header.header1, '1',
                         msg=f'Actual fixture header "{self.league.fixture_header.header1}" does not '
                             f'equal expected is 1')
        self.assertEqual(self.league.fixture_header.header3, '2',
                         msg=f'Actual fixture header "{self.league.fixture_header.header3}" does not '
                             f'equal expected is 2')

    def test_002_verify_accordion_titles(self):
        """
        DESCRIPTION: Verify accordion titles
        EXPECTED: Accordion titles correspond to:
        EXPECTED: **for Football** Sports: **className** - **typeName**
        EXPECTED: **for other** Sports: **categoryName** - **typeName**
        """
        # covered in step 1

    def test_003_verify_order_of_accordions(self):
        """
        DESCRIPTION: Verify order of accordions
        EXPECTED: Accordions are ordered by:
        EXPECTED: 1) Type **displayOrder ** in ascending
        EXPECTED: 2) Class **displayOrder ** in ascending
        EXPECTED: 3) Alphabetically (Accordion Title name)
        """
        # This will remove all See All Links form the League Accordian
        actual_order = list(map(lambda leauge_name: leauge_name.replace('\nSEE ALL', ""), list(self.sections.keys())))
        self.softAssert(self.assertListEqual, actual_order, self.expected_leagues_order,
                        msg=f'\nActual leagues order: "{actual_order}" '
                            f'\nExpected leagues order: "{self.expected_leagues_order}"')

    def test_004_verify_matches_events_order_in_each_accordion(self):
        """
        DESCRIPTION: Verify 'Matches' events order in each accordion
        EXPECTED: 'Matches' events are ordered in the following way:
        EXPECTED: 1) startTime - chronological order in the first instance
        EXPECTED: 2) Event displayOrder in ascending
        EXPECTED: 3) Alphabetical order
        """
        if not self.league.is_expanded():
            self.league.expand()
        self.assertTrue(self.league.is_expanded(), msg=f'Section "{self.league_name}" is not expanded')

        actual_events_order = list(self.league.items_as_ordered_dict)
        self.assertTrue(actual_events_order, msg=f'No events found')
        if self.device_type == 'desktop':
            # This will not check live events in Tomorrow tab for desktop devices
            expected_events_order = self.expected_events_order[:len(actual_events_order)]
        else:
            expected_events_order = self.expected_events_order
        self.assertListEqual(actual_events_order, expected_events_order,
                             msg=f'\nActual events order: "{actual_events_order}" '
                                 f'\nExpected events order: "{expected_events_order}"')
