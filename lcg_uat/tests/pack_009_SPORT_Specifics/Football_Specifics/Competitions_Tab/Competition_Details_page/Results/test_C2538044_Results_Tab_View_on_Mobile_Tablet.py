import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2 # result/standing tabs will be displayed for real events
# @pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.mobile_only
@vtest
class Test_C2538044_Results_Tab_View_on_Mobile_Tablet(BaseSportTest):
    """
    TR_ID: C2538044
    NAME: Results Tab View on Mobile/Tablet
    DESCRIPTION:
    PRECONDITIONS:
    """
    keep_browser_open = True

    def check_empty_strings(self, league):
        """
        DESCRIPTION:  This condition ensures that the league itself is not empty
                      and also checks if all keys in the league,
                      after stripping any whitespace, are non-empty strings.
        """
        league_name = league.keys()
        return league if league and all(item.strip() for item in league_name) else False

    def test_001_choose_competitions_tab(self):
        """
        DESCRIPTION: Choose 'Competitions' tab
        EXPECTED: 'Competitions' tab is selected
        """
        self.site.open_sport(name='FOOTBALL')
        self.site.wait_content_state('football')
        expected_sport_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                     self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(expected_sport_tab)
        self.site.wait_content_state_changed()
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, expected_sport_tab,
                         msg=f'Competition tab is not active, active is "{active_tab}"')

    def test_002_choose_some_competition_from_expanded_class_accordion_and_tap_on_it(self):
        """
        DESCRIPTION: Choose some competition from expanded 'Class' accordion and tap on it
        EXPECTED: Competitions Details page is opened
        EXPECTED: 'Matches' tab is selected by default
        """
        competitions = wait_for_result(lambda: self.check_empty_strings(self.site.football.tab_content.all_competitions_categories.items_as_ordered_dict),
                                       name='Leagues list is loaded',
                                       timeout=5)
        competition_league_name = vec.siteserve.PREMIER_LEAGUE_NAME
        league_name = vec.siteserve.ENGLAND
        competition = competitions[league_name]
        competition.expand()
        leagues = wait_for_result(lambda: self.check_empty_strings(competition.items_as_ordered_dict),
                                  name='Leagues list is loaded',
                                  timeout=5)
        competition.expand()
        league_object = leagues[competition_league_name]
        league_object.click()
        self.site.wait_content_state('CompetitionLeaguePage')
        current_tab = self.site.competition_league.tabs_menu.current
        self.assertEqual(current_tab, vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches,
                         msg=f'Relevant tab is not opened, Actual "{current_tab}" '
                         f'expected "{vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches}"')

    def test_003_verify_results_tab_displaying(self):
        """
        DESCRIPTION: Verify 'Results' tab displaying
        EXPECTED: 'Results' tab is located at the top of the page after 'Outrights' tab
        """
        self.site.competition_league.tabs_menu.click_button(vec.sb.COMPETITION_DETAILS_PAGE_TABS.results)
        current_tab = self.site.competition_league.tabs_menu.current
        self.assertEqual(current_tab, vec.sb.COMPETITION_DETAILS_PAGE_TABS.results,
                         msg=f'Relevant tab is not opened, Actual "{current_tab}" '
                         f'expected "{vec.sb.COMPETITION_DETAILS_PAGE_TABS.results}"')

    def test_004_verify_content(self):
        """
        DESCRIPTION: Verify content
        EXPECTED: Every date section is expandable/collapsible
        """
        try:
            results_tab_content = wait_for_result(lambda: self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict,
                                       name='event list is loaded', timeout=10)
            self.assertTrue(results_tab_content, msg='Results is not displayed')
        except Exception:
            no_events = wait_for_result(lambda: self.site.contents.tab_content.has_no_events_label(),
                                        timeout=3,
                                        name='"No Events Found" msg not displayed')
            self.assertTrue(no_events, msg='"No Events Found" msg not displayed')
            self._logger.error(msg='"No events found" message is displayed')