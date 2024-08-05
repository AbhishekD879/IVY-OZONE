import pytest

import tests
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from selenium.common.exceptions import WebDriverException

from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result, wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.mobile_only
@pytest.mark.football
@pytest.mark.competitions
@vtest
class Test_C492062_Verify_Football_Competition_Details_page(BaseSportTest):
    """
    TR_ID: C492062
    VOL_ID: C33082825
    NAME: Verify Football Competition Details page
    DESCRIPTION: This test case verifies Football competitions details page
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Football landing page > Competitions tab
    PRECONDITIONS: 3. Expand any class accordion and click on any type
    PRECONDITIONS: Note! To have classes/types displayed on frontend, put class ID's in **'InitialClassIDs' and/or 'A-ZClassIDs' fields** in **CMS>SystemConfiguration>Competitions Football**. Events for those classes should be present as well.
    """
    keep_browser_open = True

    def is_element_displayed(self, element):
        """
        Method to click on the element if visible on the page
        :param element: First tab in the list of tabs
        :return: True or False
        """
        try:
            element.check_click()  # if element is displayed, the element is clicked
        except WebDriverException:
            return False
        return True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add football event for specific league
        EXPECTED: Navigate to Football Competition page
        """
        if tests.settings.backend_env != 'prod':

            competitions_countries = self.get_initial_data_system_configuration().get('CompetitionsFootball')
            if not competitions_countries:
                competitions_countries = self.cms_config.get_system_configuration_item('CompetitionsFootball')
            if str(self.ob_config.football_config.autotest_class.class_id) not in competitions_countries.get('A-ZClassIDs').split(','):
                raise CmsClientException(f'{tests.settings.football_autotest_competition} class '
                                         f'is not configured on Competitions tab')

            self.ob_config.add_autotest_premier_league_football_event(selections_number=1)
            self.ob_config.add_autotest_premier_league_football_outright_event(ew_terms=self.ew_terms)
            self.__class__.section_name_list = tests.settings.football_autotest_competition
            self.__class__.league = tests.settings.football_autotest_competition_league.title()
        else:
            event = self.get_competition_with_results_and_standings_tabs(
                category_id=self.ob_config.football_config.category_id, raise_exceptions=True)
            sport_name = event.class_name.upper().split(" ")
            if sport_name[0] == vec.siteserve.FOOTBALL_TAB.upper():
                self.__class__.section_name_list = sport_name[1]
            else:
                self.__class__.section_name_list = sport_name[0]
            self.__class__.league = event.league_name

        self.site.open_sport(name='FOOTBALL')
        self.site.football.tabs_menu.click_button(button_name=self.get_sport_tab_name(name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                                                      category_id=self.ob_config.football_config.category_id))

    def test_001_select_any_competition_type_within_expanded_class(self):
        """
        DESCRIPTION: Select any competition (type) within expanded class
        EXPECTED: Competition details page is opened
        """
        sections = self.site.football.tab_content.all_competitions_categories.get_items(name=self.section_name_list)
        self.assertTrue(sections, msg=f'Competitions page does not have any "{self.section_name_list}" section')
        section = sections.get(self.section_name_list)
        self.assertTrue(section, msg=f'Cannot find "{self.section_name_list}" section on Competitions page')
        section.expand()
        leagues = wait_for_result(lambda: section.get_items(name=self.league),
                                  name=f'"{self.section_name_list}" to expand for "{self.league}"', timeout=3)
        self.assertTrue(leagues, msg=f'No events are present for the league "{self.league}"')
        league = leagues.get(self.league)
        self.assertTrue(league, msg=f'Cannot find "{self.league}" on Competitions page')
        league.click()
        self.site.wait_content_state('CompetitionLeaguePage')

    def test_002_verify_competition_details_page(self):
        """
        DESCRIPTION: Verify Competition details page
        EXPECTED: The following elements are present on the page:
        EXPECTED: * 'COMPETITIONS' label next to the 'back' ('<') button (Coral only)
        EXPECTED: * 'Favorites' (star) icon (top right corner) (Coral only)
        EXPECTED: * Competition header with competition name and 'Change Competition' selector
        EXPECTED: * 3 tabs: 'Matches', 'Outrights', 'Results' (displayed only if at least two of them have content)
        EXPECTED: * Market selector drop-down
        EXPECTED: * 'Matches' tab is selected by default and events from the league are shown
        """
        if self.brand != 'ladbrokes':
            coral_title = self.site.competition_league.header_line.page_title.title
            self.assertEqual(coral_title, self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper(),
                             msg=f'Actual title "{coral_title}" is not equal to expected title'
                                 f'"{self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper()}"')
            self.assertTrue(self.site.competition_league.header_line.go_to_favourites_page.is_displayed(),
                            msg='Favorites (star) icon is not displayed')

        competition_name = self.site.competition_league.title_section.type_name.text
        self.assertEqual(competition_name, self.league,
                         msg=f'Competition header with competition name is not same '
                             f'Actual: "{competition_name}" '
                             f'Expected: "{self.league}"')
        change_competition_selector = self.site.competition_league.title_section.competition_selector_link.name
        self.assertEqual(change_competition_selector, vec.sb.CHANGE_COMPETITION,
                         msg=f'Competition header with Change Competition selector is not same'
                             f'Actual: "{change_competition_selector}" '
                             f'Expected: "{vec.sb.CHANGE_COMPETITION}"')

        self.__class__.tabs_menu = self.site.competition_league.tabs_menu.items_as_ordered_dict
        self.assertTrue(self.tabs_menu, msg='Tabs menu items are not present')

        current_tab = self.site.competition_league.tabs_menu.current
        self.assertEqual(current_tab, self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches.upper(),
                         msg=f'"Matches" tab is not selected by default'
                             f'Actual: "{current_tab}" '
                             f'Expected: "{self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches.upper()}"')

        events_in_tab = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(events_in_tab, msg='Matches tab has no content')

        market_selector = self.site.competition_league.tab_content.has_dropdown_market_selector()
        self.assertTrue(market_selector, msg='Market selector drop-down is not present')

    def test_003_navigate_between_the_tabs(self):
        """
        DESCRIPTION: Navigate between the tabs
        EXPECTED: * User is able to navigate between the tabs
        EXPECTED: * Relevant information is shown in each case
        """
        for tab_name, tab in self.tabs_menu.items():
            tab.click()
            result = wait_for_result(lambda: self.site.competition_league.tabs_menu.current == tab_name,
                                     timeout=2,
                                     name='Navigation to next tab')
            self.assertTrue(result,
                            msg=f'Relevant tab is not opened. Actual: "{self.site.competition_league.tabs_menu.current}".'
                            f' Expected: "{tab_name}"')

    def test_004_tap_the_back__button(self):
        """
        DESCRIPTION: Tap the back ('<') button
        EXPECTED: User is taken to the 'Competitions' tab on the Football Landing page
        """
        self.site.back_button_click()
        self.site.wait_content_state('Football')
        self.assertEqual(self.site.football.tabs_menu.current, self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper(),
                         msg=f'User is not taken to "Competitions" tab.'
                             f'Actual: "{self.site.football.tabs_menu.current}" '
                             f'Expected: "{self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper()}"')

    def test_005_repeat_step_1(self):
        """
        DESCRIPTION: Repeat step 1
        EXPECTED: User is taken to the selected competition details page
        """
        self.test_001_select_any_competition_type_within_expanded_class()

    def test_006_scroll_the_page_down(self):
        """
        DESCRIPTION: Scroll the page down
        EXPECTED: * Competition header, 'Change Competition' selector and Market selector are sticky (remain at the top of the scrolling page)
        EXPECTED: * 'Matches', 'Results' and 'Outrights' switcher are hidden (if available)
        """
        competition_league = self.site.competition_league
        self.__class__.competition_name = competition_league.title_section.type_name
        self.__class__.change_competition_selector = competition_league.title_section.competition_selector_link
        self.__class__.market_selector = competition_league.tab_content.dropdown_market_selector
        self.__class__.tabs_menu = competition_league.tabs_menu.items_as_ordered_dict

        sections = competition_league.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        last_section_name, last_section = list(sections.items())[-1]

        last_section.scroll_to()
        self.assertTrue(self.is_element_displayed(self.competition_name), msg='"Competition header" is not displayed')
        self.assertTrue(self.is_element_displayed(self.change_competition_selector),
                        msg='"Change Competition selector is not displayed')
        self.change_competition_selector.perform_click()  # reverting the click action done in is_element_displayed()
        self.assertTrue(self.site.football.tab_content.has_dropdown_market_selector(),
                        msg='"Market selector" is not displayed')
        self.site.footer.scroll_to()  # same as line 181
        wait_for_haul(1)
        self.assertFalse(self.is_element_displayed(list(self.tabs_menu.values())[0]),
                         msg='Switcher tab is not hidden and is visible')

    def test_007_scroll_the_page_up(self):
        """
        DESCRIPTION: Scroll the page up
        EXPECTED: * Competition header, 'Change Competition' selector and Market selector are sticky (remain at the top of the scrolling page)
        EXPECTED: * 'Matches', 'Results' and 'Outrights' switchers are hidden (if available)
        EXPECTED: * After the page is scrolled all the way up, user sees switchers
        """
        events_tab1 = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
        self.assertFalse(self.is_element_displayed(list(self.tabs_menu.values())[0]),
                         msg='Switcher tab is not hidden and is visible')
        self.site.header.scroll_to()
        self.assertTrue(self.is_element_displayed(self.competition_name), msg='"Competition header" is not displayed')
        self.assertTrue(self.is_element_displayed(self.change_competition_selector), msg='"Change Competition" selector is not displayed')
        self.change_competition_selector.perform_click()  # reverting the click action done in is_element_displayed()
        self.assertTrue(self.is_element_displayed(self.market_selector), msg='"Market selector" is not displayed')
        self.assertTrue(self.is_element_displayed(list(self.tabs_menu.values())[0]),
                        msg='Switcher tab is not hidden and is visible')

    def test_008_scroll_the_page_down_and_click_on_market_selector(self):
        """
        DESCRIPTION: Scroll the page down and click on Market selector
        EXPECTED: Market selector is clickable and displays available markets
        """
        self.site.competition_league.tab_content.dropdown_market_selector.click()
        markets = self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict
        self.assertTrue(markets, msg='Market does not displays available markets')

    def test_009_scroll_the_page_down_and_click_on_change_competition_selector(self):
        """
        DESCRIPTION: Scroll the page down and click on 'Change Competition' selector
        EXPECTED: 'Change Competition' selector is clickable and displays available competitions
        """
        self.site.footer.scroll_to()
        self.site.competition_league.title_section.competition_selector_link.click()
        competitions = self.site.competition_league.competition_list.items_as_ordered_dict
        self.assertTrue(competitions, msg='Available competitions are not displayed on page')
