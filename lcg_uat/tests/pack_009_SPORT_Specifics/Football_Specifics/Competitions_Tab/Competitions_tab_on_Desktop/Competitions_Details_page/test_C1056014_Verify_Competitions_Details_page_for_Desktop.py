import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@vtest
class Test_C1056014_Verify_Competitions_Details_page_for_Desktop(BaseBetSlipTest):
    """
    TR_ID: C1056014
    NAME: Verify Competitions Details page for Desktop
    DESCRIPTION: This test case verifies Competitions Details page for Desktop.
    DESCRIPTION: Need to run test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS:
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    markets = [('to_qualify', ),
               ('over_under_total_goals', {'over_under': 2.5}),
               ('both_teams_to_score', ),
               ('draw_no_bet', ),
               ('first_half_result', ),
               ('match_result_and_both_teams_to_score', ),
               ('next_team_to_score', ),
               ('extra_time_result', ),
               ('to_win_not_to_nil', )]

    def test_000_pre_conditions(self):
        """
        DESCRIPTION: User should be logged in
        """
        if tests.settings.backend_env != 'prod':
            competitions_countries = self.get_initial_data_system_configuration().get('CompetitionsFootball')
            if not competitions_countries:
                competitions_countries = self.cms_config.get_system_configuration_item('CompetitionsFootball')
            if str(self.ob_config.football_config.autotest_class.class_id) not in competitions_countries.get(
                    'A-ZClassIDs').split(','):
                raise CmsClientException(f'{tests.settings.football_autotest_competition} class '
                                         f'is not configured on Competitions tab')

            all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports', status=True)
            self.assertTrue(all_sports_status, msg='"All Sports" market switcher status is disabled')
            market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='football', status=True)
            self.assertTrue(market_switcher_status, msg='Market switcher is disabled for football sport')

            self.ob_config.add_autotest_premier_league_football_event(markets=self.markets)

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        self.site.wait_content_state("Homepage")
        self.site.open_sport(name='FOOTBALL')

    def test_002_navigate_to_football_landing_page___competitions_tab(self):
        """
        DESCRIPTION: Navigate to Football Landing page -> 'Competitions' tab
        EXPECTED: Competitions Landing page is opened
        """
        self.site.wait_content_state('football')
        expected_sport_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                     self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(expected_sport_tab)
        self.site.wait_content_state_changed()
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, expected_sport_tab,
                         msg=f'Competition tab is not active, active is "{active_tab}"')

        if self.device_type == 'desktop':
            self.site.football.tab_content.grouping_buttons.items_as_ordered_dict[vec.sb_desktop.COMPETITIONS_SPORTS].click()
            competitions = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        else:
            competitions = self.site.football.tab_content.all_competitions_categories.items_as_ordered_dict
        self.assertTrue(competitions, msg='No competitions are present on page')

        if tests.settings.backend_env == 'prod':
            competition_league = vec.siteserve.PREMIER_LEAGUE_NAME
            if tests.settings.brand == 'ladbrokes' and self.device_type == 'desktop':
                league = vec.siteserve.ENGLAND.title()
            else:
                league = vec.siteserve.ENGLAND
        else:
            if tests.settings.brand == 'ladbrokes' and self.device_type == 'desktop':
                league = 'Auto Test'
            else:
                league = 'AUTO TEST'
            competition_league = vec.siteserve.AUTO_TEST_PREMIER_LEAGUE_NAME

        competition = competitions[league]
        competition.expand()
        leagues = wait_for_result(lambda: competition.items_as_ordered_dict,
                                  name='Leagues list is loaded',
                                  timeout=2)
        self.assertTrue(leagues, msg='No leagues are present on page')
        self.assertIn(competition_league, leagues.keys(),
                      msg=f'League "{competition_league}" is not found in "{list(leagues.keys())}"')
        self.__class__.league = leagues[competition_league]
        self.__class__.league_name = self.league.name
        self.league.click()
        self.site.wait_content_state('CompetitionLeaguePage')

    def test_003_expand_any_classes_accordion_and_select_any_type_competition(self):
        """
        DESCRIPTION: Expand any Classes accordion and select any Type (Competition)
        EXPECTED: * Competition Details page is opened
        EXPECTED: * List of events is loaded on the page
        """
        sections = list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(sections, msg='"Sections" are not available')
        for section in sections:
            events = list(section.items_as_ordered_dict.values())
            self.assertTrue(events, msg=' "Events" are not available')

    def test_004_verify_the_competitions_page_on_desktop(self):
        """
        DESCRIPTION: Verify the 'Competitions' page on Desktop:
        EXPECTED: The following elements are present on the page:
        EXPECTED: * 'COMPETITION NAME' inscription next to the 'Back' ('<') button
        EXPECTED: * 'Change Competition' selector at the right side of the Competition header
        EXPECTED: * Breadcrumbs trail below the Competitions header in the next format: 'Home' > 'Football' > 'Competitions' > 'Type (Competition) name'
        EXPECTED: * 'Matches' and 'Outrights' switchers
        EXPECTED: * 'Matches' switcher is selected by default and events are shown
        EXPECTED: * 'Market selector' drop-down at the same row as switchers (at the right side of row)
        """
        competition_name = self.site.competition_league.title_section.type_name.text
        self.assertEqual(competition_name.upper(), self.league_name.upper(),
                         msg=f'Competition header with competition name is not same '
                             f'Actual: "{competition_name}" '
                             f'Expected: "{self.league_name.upper()}"')

        change_competition_selector = self.site.competition_league.title_section.competition_selector_link.name
        self.assertEqual(change_competition_selector, vec.sb.CHANGE_COMPETITION,
                         msg=f'Competition header with Change Competition selector is not same'
                             f'Actual: "{change_competition_selector}" '
                             f'Expected: "{vec.sb.CHANGE_COMPETITION}"')

        tabs_menu = self.site.competition_league.tabs_menu.items_as_ordered_dict
        self.assertTrue(tabs_menu, msg="'Matches' and 'Outrights' switchers are not displayed")

        current_tab = self.site.competition_league.tabs_menu.current
        self.assertEqual(current_tab.upper(), self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches.upper(),
                         msg=f'"Matches" tab is not selected by default'
                             f'Actual: "{current_tab}" '
                             f'Expected: "{self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches.upper()}"')

    def test_005_click_on_the_back__button(self):
        """
        DESCRIPTION: Click on the 'Back' ('<') button
        EXPECTED: User is taken to the 'Competitions' tab on the Football Landing page
        """
        self.site.back_button_click()
        self.test_002_navigate_to_football_landing_page___competitions_tab()

    def test_006_click_on_change_competition_selector(self):
        """
        DESCRIPTION: Click on 'Change Competition selector'
        EXPECTED: * 'Change Competition selector' drop-down list of countries e.g. England, Scotland, Spain is opened
        EXPECTED: * Countries items inside 'Change Competition selector' drop-down list are expandable/collapsible
        """
        self.site.competition_league.title_section.competition_selector_link.click()
        countries = self.site.competition_league.competitions_selector.items_as_ordered_dict
        self.assertTrue(countries, msg="list of countries are not displayed")
        for section_name, section in countries.items():
            section.click()
            leagues = section.league_selector.items_as_ordered_dict
            self.assertTrue(leagues, msg='No leagues found in Leagues selector')
            break
        self.site.competition_league.title_section.competition_selector_link.click()

    def test_007_click_on_any_country_in_change_competition_selector(self):
        """
        DESCRIPTION: Click on any country in 'Change Competition selector'
        EXPECTED: * List of Competitions is contained within expanded Country item in 'Change Competition selector' drop-down list
        """
        # covered in above step

    def test_008_click_on_market_selector(self):
        """
        DESCRIPTION: Click on 'Market Selector'
        EXPECTED: * 'Market Selector' drop-down list of markets is opened
        EXPECTED: * The following items are displayed in 'Market Selector' drop-down list:
        EXPECTED: * Match Result
        EXPECTED: * To Qualify
        EXPECTED: * Next Team to Score
        EXPECTED: * Extra Time Result
        EXPECTED: * Total Goals Over/Under 2.5
        EXPECTED: * Both Teams to Score
        EXPECTED: * To Win & Both Team to Score
        EXPECTED: * Draw No Bet
        EXPECTED: * 1st Half Result
        """
        markets = self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict
        self.assertTrue(markets, msg='Market does not displays available markets')

        expected_market_list = vec.siteserve.EXPECTED_MARKETS_NAMES
        actual_market_list = list(self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())

        for market in actual_market_list:
            self.assertIn(market, expected_market_list,
                          msg=f'Market "{market}" is not in expected market list')

    def test_009_navigate_between_the_matches_and_outrights_switchers(self):
        """
        DESCRIPTION: Navigate between the 'Matches' and 'Outrights' switchers
        EXPECTED: * User is able to navigate between the switchers
        EXPECTED: * Relevant information is shown in each case
        EXPECTED: * 'Market Selector' is displayed only if 'Matches' switcher is selected
        """
        tabs_menu = self.site.competition_league.tabs_menu.items_as_ordered_dict
        for tab_name, tab in tabs_menu.items():
            tab.click()
            result = wait_for_result(lambda: self.site.competition_league.tabs_menu.current == tab_name,
                                     timeout=2,
                                     name='Navigation to next tab')
            self.assertTrue(result,
                            msg=f'Relevant tab is not opened. Actual: "{self.site.competition_league.tabs_menu.current}".'
                            f' Expected: "{tab_name}"')
            if tab_name.upper() == self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches.upper():
                self.assertTrue(self.site.competition_league.tab_content.has_dropdown_market_selector(),
                                msg="market selector is not displayed in matches switcher ")
            else:
                self.assertFalse(self.site.competition_league.tab_content.has_dropdown_market_selector(),
                                 msg="market selector is displayed in outrights switcher ")
        for tab_name, tab in tabs_menu.items():
            if tab_name.upper() == self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches.upper():
                tab.click()

    def test_010_scroll_the_page_down(self):
        """
        DESCRIPTION: Scroll the page down
        EXPECTED: * 'Market selector' is NOT sticky. It becomes hidden when scrolling the page down
        EXPECTED: * 'Change Competition selector' is NOT sticky. It becomes hidden when scrolling the page down
        """
        self.site.contents.scroll_to_bottom()
        self.assertFalse(self.site.contents.tab_content.is_market_selector_sticky, msg="Market selector is sticky")

    def test_011_scroll_the_page_up(self):
        """
        DESCRIPTION: Scroll the page up
        EXPECTED: * 'Market selector' is NOT sticky. It becomes visible when scrolling the page up
        EXPECTED: * 'Change Competition selector' is NOT sticky. It becomes visible when scrolling the page up
        """
        self.site.contents.scroll_to_top()
        self.assertFalse(self.site.contents.tab_content.is_market_selector_sticky, msg="Market selector is sticky")
