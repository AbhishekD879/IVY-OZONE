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
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C10530957_Verify_events_grouping_and_ordering_on_Competitions_tab_for_Tier_2_Sports(BaseSportTest):
    """
    TR_ID: C10530957
    NAME: Verify events grouping and ordering on 'Competitions' tab for Tier 2 Sports
    DESCRIPTION: This test case verifies how events are grouped and ordered on 'Competitions' tab for Tier 2 Sports
    DESCRIPTION: **From 102.0 for Coral and Ladbrokes**
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - To verify queries from Front-end to SiteServe for data availability checking use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+get+data+from+Openbet+Site+Server
    PRECONDITIONS: - To verify queries from CMS to SiteServe for data availability checking use the following instruction: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-QueriestoSiteServe(SS)
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. 'Competitions' tab is enabled in CMS for 'Tier 2' Sport and data are available ( **MATCHES** including live and pre-match and **OUTRIGHTS** )
    PRECONDITIONS: 2. Load the app
    PRECONDITIONS: 3. Navigate to the selected 'Tier 2' Sports Landing Page
    PRECONDITIONS: 4. Choose the 'Competitions' tab
    """
    keep_browser_open = True
    expected_events_order = []
    expected_outrights_events_order = []

    def verify_events_are_present(self, resp):
        event = next((event for event in resp if
                      event.get('event') and event['event'] and event['event'].get('children')), None)
        if not event:
            raise SiteServeException(
                f'No active events found for category id "1"')

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
        DESCRIPTION: Create american football events
        """
        am_football_category_id = 1
        if tests.settings.backend_env == 'prod':
            event1 = self.get_active_events_for_category(category_id=am_football_category_id)[0]
            self._logger.info(f'*** Found event: {event1}')
        else:
            tab_id = self.cms_config.get_sport_tab_id(sport_id=am_football_category_id,
                                                      tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights)
            self.cms_config.update_sports_tab_status(sport_tab_id=tab_id, enabled="true",
                                                     sport_id=am_football_category_id)
            tab_id = self.cms_config.get_sport_tab_id(sport_id=am_football_category_id,
                                                      tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches)
            self.cms_config.update_sports_tab_status(sport_tab_id=tab_id, enabled="true",
                                                     sport_id=am_football_category_id)
            tab_id = self.cms_config.get_sport_tab_id(sport_id=am_football_category_id,
                                                      tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions)
            self.cms_config.update_sports_tab_status(sport_tab_id=tab_id, enabled="true",
                                                     sport_id=am_football_category_id)

            self.check_sport_configured(am_football_category_id)
            self.ob_config.add_american_football_event_to_autotest_league()
            self.ob_config.add_american_football_event_to_nfl()
            self.ob_config.add_american_football_event_to_ncaa_bowls()
            self.ob_config.add_american_football_event_to_cfl()

            event_params = self.ob_config.add_american_football_event_to_autotest_league(
                start_time=self.get_date_time_formatted_string(hours=1))
            self.__class__.expected_events_order.append(f'{event_params.team1} v {event_params.team2}')

            event_params2 = self.ob_config.add_american_football_event_to_autotest_league(
                start_time=self.get_date_time_formatted_string(hours=2))
            self.__class__.expected_events_order.append(f'{event_params2.team1} v {event_params2.team2}')

            event_params3 = self.ob_config.add_american_football_event_to_autotest_league(
                start_time=self.get_date_time_formatted_string(hours=3))
            self.__class__.expected_events_order.append(f'{event_params3.team1} v {event_params3.team2}')

            event_params4 = self.ob_config.add_american_football_event_to_autotest_league(
                start_time=self.get_date_time_formatted_string(hours=4))
            self.__class__.expected_events_order.append(f'{event_params4.team1} v {event_params4.team2}')

            for outright in range(0, 4):
                start_time = self.get_date_time_formatted_string(hours=outright + 3)
                outright_name = f'Outright {int(time.time())}'
                self.ob_config.add_american_football_outright_event_to_autotest_league(
                    event_name=outright_name, start_time=start_time)
                self.expected_outrights_events_order.append(outright_name)

        self.__class__.start_date = f'{get_date_time_as_string(days=-1)}T21:00:00.000Z'
        days_for_match = 0
        if self.device_type != 'desktop':
            days_for_match = 2

        query = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.INTERSECTS, str(am_football_category_id))) \
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
        class_ids = self.get_class_ids_for_category(category_id=am_football_category_id)

        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=am_football_category_id)
        events_list = ss_req.ss_event_to_outcome_for_class(query_builder=query, class_id=class_ids)
        self.verify_events_are_present(resp=events_list)

        sorted_leagues = self.sort_by_disp_order(events_list)
        self.__class__.league_name = sorted_leagues[0]
        self.__class__.expected_leagues_order = [item.upper() for item in sorted_leagues]

        self.__class__.expected_events_order = self.get_order_of_events(league=self.league_name,
                                                                        sports_list=events_list)
        self.site.wait_content_state(state_name='Homepage')
        self.navigate_to_page(name='sport/american-football')
        self.site.wait_content_state('american-football', timeout=30)

        tabs_menu = self.site.american_football.tabs_menu
        if vec.sb.TABS_NAME_COMPETITIONS.upper() in tabs_menu.items_names:
            tabs_menu.click_item(vec.sb.TABS_NAME_COMPETITIONS.upper())
        current_tab = tabs_menu.current
        self.assertEqual(current_tab, self.expected_sport_tabs.competitions,
                         msg=f'\nDefault tab: "{current_tab}" opened'
                             f'\nExpected tab: "{self.expected_sport_tabs.competitions}" opened')

    def test_001_verify_events_grouping(self):
        """
        DESCRIPTION: Verify event's grouping
        EXPECTED: * Events are grouped by **classId** and **typeId**
        EXPECTED: * Events are displayed in accordions
        EXPECTED: * First 3 accordions are expanded by default, the rest - collapsed
        """
        self.__class__.sections = self.site.american_football.tab_content.competitions_categories_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='No Specials sections found')

        if len(self.sections) > 1:
            for comp_name, competition in list(self.sections.items())[:3]:
                self.assertTrue(competition.is_expanded(expected_result=True),
                                msg=f'Special section "{comp_name}" is not expanded by default')

        # If event is displayed in this league it is automatically verifies that events are grouped by TypeID
        self.__class__.league = self.sections.get(self.league_name.upper())
        self.assertEqual(self.league.fixture_header.header1, '1',
                         msg=f'Actual fixture header "{self.league.fixture_header.header1}" does not '
                             f'equal expected is 1')
        self.assertEqual(self.league.fixture_header.header3, '2',
                         msg=f'Actual fixture header "{self.league.fixture_header.header3}" does not '
                             f'equal expected is 2')

    def test_002_verify_accordion_titles(self):
        """
        DESCRIPTION: Verify accordion titles
        EXPECTED: Accordion titles correspond to **className-typeName**
        """
        # covered in step 1

    def test_003_verify_order_of_accordions(self):
        """
        DESCRIPTION: Verify order of accordions
        EXPECTED: Accordions are ordered by:
        EXPECTED: 1) Class **displayOrder ** in ascending
        EXPECTED: 2) Type **displayOrder ** in ascending
        """
        actual_order = list(self.sections.keys())
        self.softAssert(self.assertListEqual, actual_order, self.expected_leagues_order,
                        msg=f'\nActual leagues order: "{actual_order}" '
                            f'\nExpected leagues order: "{self.expected_leagues_order}"')

    def test_004_verify_matches_and_outrights_events_order_in_each_accordion(self):
        """
        DESCRIPTION: Verify 'Matches' and 'Outrights' events order in each accordion
        EXPECTED: - 'Matches' events are displayed above the 'Outrights' within each 'Type' accordion
        EXPECTED: - 'Matches' events are ordered in the following way:
        EXPECTED: 1) startTime - chronological order in the first instance
        EXPECTED: 2) Event displayOrder in ascending
        EXPECTED: 3) Alphabetical order
        EXPECTED: - 'Outrights' events are ordered in the following way:
        EXPECTED: 1) Event displayOrder in ascending
        EXPECTED: 2) startTime - chronological order in the first instance
        EXPECTED: 3) Alphabetical order
        """
        tabs_menu = self.site.american_football.tabs_menu
        if vec.sb.TABS_NAME_MATCHES.upper() in tabs_menu.items_names:
            tabs_menu.click_item(vec.sb.TABS_NAME_MATCHES.upper())

        # matches tab
        sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No leagues sections found')
        league = sections.get(self.league_name.upper())
        if not league.is_expanded():
            league.expand()
        self.assertTrue(league.is_expanded(), msg=f'Section "{self.league_name}" is not expanded')

        actual_events_order = list(league.items_as_ordered_dict)
        self.assertTrue(actual_events_order, msg=f'No events found')
        if self.device_type == 'desktop':
            if self.brand == 'bma':
                expected_events_order = self.expected_events_order[:len(actual_events_order)]
            else:
                expected_events_order = self.expected_events_order
                actual_events_order = actual_events_order[:len(expected_events_order)]
        else:
            expected_events_order = self.expected_events_order
        try:
            self.assertListEqual(actual_events_order, expected_events_order,
                                 msg=f'\nActual events order: "{actual_events_order}" '
                                     f'\nExpected events order: "{expected_events_order}"')
        except Exception:
            new_actual_events_order = []
            for i in range(len(actual_events_order)):
                team1, team2 = actual_events_order[i].split(' v ')
                new_actual_events_order.append(f'{team2.strip()} v {team1.strip()}')
            self.assertListEqual(new_actual_events_order, expected_events_order,
                                 msg=f'\nActual events order: "{new_actual_events_order}" '
                                     f'\nExpected events order: "{expected_events_order}"')

        # outrights tab
        tabs_menu = self.site.american_football.tabs_menu
        if vec.sb.TABS_NAME_OUTRIGHTS.upper() in tabs_menu.items_names:
            tabs_menu.click_item(vec.sb.TABS_NAME_OUTRIGHTS.upper())

        sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No leagues sections found')
        league = list(sections.values())[0]
        if not league.is_expanded():
            league.expand()
        self.assertTrue(league.is_expanded(), msg=f'Section "{self.league_name}" is not expanded')

        actual_outrights_events_order = list(league.items_as_ordered_dict)
        self.assertTrue(actual_events_order, msg=f'No events found')
        self.assertTrue(set(self.expected_outrights_events_order).issubset(set(actual_outrights_events_order)),
                        msg=f'\nActual events order: "{actual_events_order}" '
                            f'\nExpected events order: "{self.expected_outrights_events_order}"')
