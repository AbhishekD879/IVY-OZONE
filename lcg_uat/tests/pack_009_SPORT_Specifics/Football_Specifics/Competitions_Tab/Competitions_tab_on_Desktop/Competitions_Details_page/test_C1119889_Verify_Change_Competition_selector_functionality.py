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
class Test_C1119889_Verify_Change_Competition_selector_functionality_on_Football_Competitions_Details_page_for_Desktop(BaseBetSlipTest):
    """
    TR_ID: C1119889
    NAME: Verify 'Change Competition' selector functionality on Football Competitions Details page for Desktop
    DESCRIPTION: This test case verifies 'Change Competition' selector functionality on Football Competitions Details page for Desktop
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
        DESCRIPTION: Create a event
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
        self.site.wait_content_state('football')

    def test_002_navigate_to_football_landing_page___competitions_tab(self):
        """
        DESCRIPTION: Navigate to Football Landing page -> 'Competitions' tab
        EXPECTED: Competitions Landing page is opened
        """
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
        competitions_countries = self.get_initial_data_system_configuration().get('CompetitionsFootball')
        if not competitions_countries:
            competitions_countries = self.get_system_configuration_item('CompetitionsFootball')
        cms_az_class_ids = competitions_countries['A-ZClassIDs'].split(',')
        self.__class__.cms_initial_class_ids = competitions_countries.get('InitialClassIDs', '')

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
        EXPECTED: * 'Matches' switcher is selected by default
        EXPECTED: * List of events is loaded on the page
        """
        sections = list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(sections, msg='"Sections" are not available')
        for section in sections:
            events = list(section.items_as_ordered_dict.values())
            self.assertTrue(events, msg=' "Events" are not available')

    def test_004_verify_the_displaying_of_change_competition_selector_on_competition_details_page(self):
        """
        DESCRIPTION: Verify the displaying of 'Change Competition' selector on Competition Details page
        EXPECTED: * 'Change Competition' selector is displayed on the right side of Competitions header
        EXPECTED: * 'Change Competition' inscription is displayed in selector by default
        EXPECTED: * Up and down arrows (chevrons) are shown next to 'Change Competition' inscription in selector
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

    def test_005_hover_the_mouse_over_the_change_competition_selector(self):
        """
        DESCRIPTION: Hover the mouse over the 'Change Competition' selector
        EXPECTED: * Background color is changed
        EXPECTED: * Pointer is changed view from 'Normal select' to 'Link select' for realizing the possibility to click on particular area
        """
        # can't automate this step

    def test_006_click_on_change_competition_selector(self):
        """
        DESCRIPTION: Click on 'Change Competition' selector
        EXPECTED: * Distance between Up and Down arrows (chevrons) on 'Change Competition' selector is increased
        EXPECTED: * '1st Level' drop-down list with 'Country' accordions and Down arrow (chevron) on each of them is opened
        EXPECTED: * 'Country' accordions inside 'Change Competition selector' drop-down list are expandable/collapsible
        EXPECTED: * All 'Country' accordions are collapsed by default
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

    def test_007_hover_the_mouse_over_the_countries_accordions_in_expanded_change_competition_selector(self):
        """
        DESCRIPTION: Hover the mouse over the 'Countries' accordions in expanded 'Change Competition' selector
        EXPECTED: * Background and text color is changed
        EXPECTED: * Pointer is changed view from 'Normal select' to 'Link select' for realizing the possibility to click on particular area
        """
        # can't automate this step

    def test_008_click_on_one_of_country_accordion_in_expanded_1st_level_drop_down(self):
        """
        DESCRIPTION: Click on one of 'Country' accordion in expanded '1st Level' drop-down
        EXPECTED: * Up arrow (chevron) is displayed on expanded 'Country' accordion
        EXPECTED: * Red vertical line appears on the left side of expanded 'Country' accordion
        EXPECTED: * '2nd Level' drop-down list of available Competitions is opened
        """
        # covered in step 6

    def test_009_hover_the_mouse_over_the_competitions_item_from_2nd_level_drop_down_in_expanded_countries_accordion(self):
        """
        DESCRIPTION: Hover the mouse over the Competitions item from '2nd Level' drop-down in expanded 'Countries' accordion
        EXPECTED: * Background and text color is changed
        EXPECTED: * Pointer is changed view from 'Normal select' to 'Link select' for realizing the possibility to click on particular area
        """
        # can't automate this step

    def test_010_click_on_another_country_accordion_in_expanded_1st_level_drop_down_than_in_step_8(self):
        """
        DESCRIPTION: Click on another 'Country' accordion in expanded '1st Level' drop-down than in step 8
        EXPECTED: * Previously selected 'Country' accordion is collapsed and '2nd Level' drop-down list of available Competitions is not displayed anymore (from step 8)
        EXPECTED: * Up arrow (chevron) is displayed on expanded 'Country' accordion
        EXPECTED: * Red vertical line appears on the left side of expanded 'Country' accordion
        EXPECTED: * '2nd Level' drop-down list of available Competitions is opened
        EXPECTED: * Scrollbar appears when list contails more than 6 items inside
        """
        # covered in step 6

    def test_011_click_on_one_of_the_competitions_in_expanded_2nd_level_drop_down_list(self):
        """
        DESCRIPTION: Click on one of the Competitions in expanded '2nd Level' drop-down list
        EXPECTED: * User navigates to the Сompetition Details page
        EXPECTED: * 'Matches' switcher is selected by default
        EXPECTED: * List of events is loaded on the page
        """
        # covered in step 6

    def test_012_click_on_the_back_button_at_the_competitions_header(self):
        """
        DESCRIPTION: Click on the 'Back' button at the Competitions header
        EXPECTED: * User navigates to the previously selected Сompetition Details page
        EXPECTED: * 'Matches' switcher is selected by default
        EXPECTED: * List of events is loaded on the page
        """
        self.site.back_button_click()
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
        self.test_003_expand_any_classes_accordion_and_select_any_type_competition()

    def test_013_repeat_steps_6_8(self):
        """
        DESCRIPTION: Repeat steps 6-8
        EXPECTED: * Up arrow (chevron) is displayed on expanded 'Country' accordion
        EXPECTED: * Red vertical line appears on the left side of expanded 'Country' accordion
        EXPECTED: * '2nd Level' drop-down list of available Competitions is opened
        """
        self.test_006_click_on_change_competition_selector()
        self.test_008_click_on_one_of_country_accordion_in_expanded_1st_level_drop_down()

    def test_014_click_on_change_competition_selector_again(self):
        """
        DESCRIPTION: Click on 'Change Competition' selector again
        EXPECTED: * Distance between Up and Down arrows (chevrons) on 'Change Competition' selector is decreased
        EXPECTED: * 'Change Competition' selector drop-down list is collapsed
        """
        # covered in step 6

    def test_015_chose_outright_switcher_on_competitions_details_page(self):
        """
        DESCRIPTION: Chose 'Outright' switcher on Competitions Details page
        EXPECTED: * 'Outrights' switcher is displayed as selected
        EXPECTED: * List of events is loaded on the page
        """
        tabs = self.site.competition_league.tabs_menu.items_as_ordered_dict
        tabs.get(vec.SB.TABS_NAME_OUTRIGHTS.upper()).click() if self.brand == 'bma' else tabs.get(
            vec.SB.TABS_NAME_OUTRIGHTS).click()
        if self.cms_initial_class_ids:
            initial_sections = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
            first_accordian = list(initial_sections.values())[0]
            selections = first_accordian.outright_selections
            self.assertTrue(selections, msg='selections are not displayed')
            self.assertTrue(first_accordian.is_expanded(),
                            msg='First accordian is not expanded by default')

    def test_016_repeat_steps_4_14(self):
        """
        DESCRIPTION: Repeat steps 4-14
        EXPECTED:
        """
        # covered in above steps
