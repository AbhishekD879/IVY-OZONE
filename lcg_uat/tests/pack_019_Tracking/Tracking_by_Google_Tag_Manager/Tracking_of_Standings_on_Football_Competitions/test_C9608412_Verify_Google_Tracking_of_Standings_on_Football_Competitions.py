import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.waiters import wait_for_result
from time import sleep


# @pytest.mark.tst2 # removed ts2, stg2 markers due to result/standing tabs will be displayed for real events
# @pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.sports
@vtest
class Test_C9608412_Verify_Google_Tracking_of_Standings_on_Football_Competitions(BaseSportTest, BaseDataLayerTest):
    """
    TR_ID: C9608412
    NAME: Verify Google Tracking of Standings on Football Competitions
    DESCRIPTION: This test case verifies Google Analytics tracking of Standings on Football Competitions
    PRECONDITIONS: 1)Navigate to Football landing page > Competitions tab
    PRECONDITIONS: 2)Expand any class accordion and click on any type (e.g. Premier League)
    PRECONDITIONS: NOTE:
    PRECONDITIONS: 'Standings' tab is displayed if a league table is available for that league on the competition page(received from Bet Radar)
    """
    keep_browser_open = True
    expected_response_standings_tab = {'event': "trackEvent",
                                       'eventAction': "league table",
                                       'eventCategory': "football",
                                       'eventLabel': "view league table"
                                       }
    expected_response_standings_previous_session = {'event': "trackEvent",
                                                    'eventAction': "league table",
                                                    'eventCategory': "football",
                                                    'eventLabel': "change season"
                                                    }

    def verify_dataLayer_actual_and_expected_values(self, actual_response, expected_response):
        self.assertEqual(expected_response.get("eventAction"), actual_response.get("eventAction"),
                         msg=f'Expected eventAction value "{expected_response.get("eventAction")}" is not '
                             f'same as actual eventAction value "{actual_response.get("eventAction")}"')
        self.assertEqual(expected_response.get("event"), actual_response.get("event"),
                         msg=f'Expected event value "{expected_response.get("event")}" is not '
                             f'same as actual event value "{actual_response.get("event")}"')
        self.assertEqual(expected_response.get("eventCategory"), actual_response.get("eventCategory"),
                         msg=f'Expected eventCategory value "{expected_response.get("eventCategory")}" is not '
                             f'same as actual eventCategory value "{actual_response.get("eventCategory")}"')
        self.assertEqual(expected_response.get("eventLabel"), actual_response.get("eventLabel"),
                         msg=f'Expected eventLabel value "{expected_response.get("eventLabel")}" is not '
                             f'same as actual eventLabel value "{actual_response.get("eventLabel")}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get event and league
        """
        event = self.get_competition_with_results_and_standings_tabs(
            category_id=self.ob_config.football_config.category_id, raise_exceptions=True)
        sport_name = event.class_name.upper().split(" ")
        if sport_name[0] == vec.sb.FOOTBALL.upper():
            self.__class__.section_name_list = sport_name[1]
        else:
            self.__class__.section_name_list = sport_name[0]
        self.__class__.league = event.league_name

        self.__class__.league_table_label = vec.sb.LEAGUE_TABLE_LABEL.title() if self.brand == 'bma' else vec.sb.LEAGUE_TABLE_LABEL
        self.navigate_to_page("sport/football")
        self.site.wait_content_state(state_name=vec.sb.FOOTBALL)
        self.site.football.tabs_menu.click_button(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper())
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper(),
                         msg=f'"{self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper()}" tab is not active, '
                             f'active is "{active_tab}"')

        country_sections = self.site.football.tab_content.competitions_categories.items_as_ordered_dict
        self.assertTrue(country_sections, msg='Competitions page does not have any section')

        sections = self.site.football.tab_content.all_competitions_categories.get_items(name=self.section_name_list)
        self.assertTrue(sections, msg=f'Competitions page does not have any "{self.section_name_list}" section')
        section = sections.get(self.section_name_list)
        self.assertTrue(section, msg=f'"{self.section_name_list}" section not found in "{sections.keys()}"')
        if not section.is_expanded():
            section.expand()
        leagues = wait_for_result(lambda: section.get_items(name=self.league),
                                  name=f'"{self.section_name_list}" to expand for "{self.league}"', timeout=3)
        self.assertTrue(leagues, msg=f'No events are present for the league "{self.league}"')
        league = leagues.get(self.league)
        self.assertTrue(league, msg=f'Cannot find "{self.league}" on Competitions page')
        league.click()
        self.site.wait_content_state('CompetitionLeaguePage')

        self.__class__.tabs_menu = self.site.competition_league.tabs_menu
        self.assertTrue(self.tabs_menu, msg='Tabs menu was not found')

    def test_001_tap_on_standings_tab(self):
        """
        DESCRIPTION: Tap on "Standings" tab
        EXPECTED: - User is navigated to the appropriate (e.g. Premier League) competition page
        EXPECTED: - The league table for that competition for current season is displayed
        """
        self.tabs_menu.click_button(vec.sb.COMPETITION_DETAILS_PAGE_TABS.standings)
        current_tab = self.tabs_menu.current
        self.assertEqual(current_tab, vec.sb.COMPETITION_DETAILS_PAGE_TABS.standings,
                         msg=f'Relevant tab is not opened, Actual "{current_tab}" '
                             f'expected "{vec.sb.COMPETITION_DETAILS_PAGE_TABS.standings}"')

    def test_002_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: dataLayer.push(
        EXPECTED: {     'event' : 'trackEvent',     'eventCategory' : 'football',     'eventAction' : 'league table',     'eventLabel' : 'view league table'                 }
        EXPECTED: );
        """
        sleep(5)
        actual_response = self.get_data_layer_specific_object(object_key='eventAction', object_value='league table')
        self.verify_dataLayer_actual_and_expected_values(actual_response, expected_response=self.expected_response_standings_tab)

    def test_003_tap_on_previous_season_link_if_it_is_available(self):
        """
        DESCRIPTION: Tap on previous season link (if it is available)
        EXPECTED: - User is navigated to page with the previous league table for that competition
        """
        tab_content = self.site.competition_league.tab_content
        if tab_content.previous_arrow.is_displayed():
            self.assertTrue(tab_content.previous_arrow.is_displayed(),
                            msg='Arrow to switch to previos season is not shown')
            self.site.competition_league.tab_content.previous_arrow.click()
            self.assertTrue(self.site.competition_league.tab_content.results_table.is_displayed(),
                            msg='Table with result was not found')
            sleep(5)
            actual_response = self.get_data_layer_specific_object(object_key='eventLabel',
                                                                  object_value='change season')
            self.verify_dataLayer_actual_and_expected_values(actual_response,
                                                             expected_response=self.expected_response_standings_previous_session)
        else:
            self._logger.info(msg='there is no previous league table available')

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: dataLayer.push(
        EXPECTED: {     'event' : 'trackEvent',     'eventCategory' : 'football',     'eventAction' : 'league table',     'eventLabel' : 'change season' }
        EXPECTED: );
        """
        # Covered in test_003_tap_on_previous_season_link_if_it_is_available
