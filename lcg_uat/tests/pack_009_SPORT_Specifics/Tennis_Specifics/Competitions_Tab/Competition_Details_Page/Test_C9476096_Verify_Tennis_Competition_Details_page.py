import pytest
import tests
import time
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter, SiteServeRequests, exists_filter
from selenium.common.exceptions import WebDriverException
from crlat_siteserve_client.utils.date_time import get_date_time_as_string
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.mobile_only
@vtest
class Test_C9476096_Verify_Tennis_Competition_Details_page(BaseSportTest):
    """
    TR_ID: C9476096
    NAME: Verify Tennis Competition Details page
    DESCRIPTION: This test case verifies Tennis competitions details page
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Tennis landing page > Competitions tab
    """
    keep_browser_open = True

    def is_element_displayed(self, element):
        """
        Method to click on the element if visible on the page
        :param element: First tab in the list of tabs
        :return: True or False
        """
        try:
            element.perform_click()  # if element is displayed, the element is clicked
        except WebDriverException:
            return False
        return True

    def verify_events_are_present(self, resp):
        event = next((event for event in resp if
                      event.get('event') and event['event'] and event['event'].get('children')), None)
        if not event:
            raise SiteServeException(
                f'No active events found for category id "{self.ob_config.backend.ti.tennis.category_id}"')

    def sort_by_disp_order(self, sports_list: list):
        """
        :param sports_list: list of dict
        :return: sorted list by type typeDisplayOrder in ascending order otherwise sort by name
        """
        sports_list = [item for item in sports_list]
        sport_categories = {f"{sport['event']['categoryName']} - {sport['event']['typeName']}": int(sport['event']['typeDisplayOrder']) for sport in sports_list}
        return sorted(sport_categories, key=lambda k: (sport_categories[k], k))

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add football event for specific league
        EXPECTED: Navigate to Football Competition page
        """
        tennis_category_id = self.ob_config.backend.ti.tennis.category_id
        if tests.settings.backend_env == 'prod':
            event1 = self.get_active_events_for_category(category_id=tennis_category_id)[0]
            self._logger.info(f'*** Found event: {event1}')
        else:
            self.check_sport_configured(tennis_category_id)
            self.ob_config.add_tennis_event_to_davis_cup()
            self.ob_config.add_tennis_event_to_european_open()
            self.ob_config.add_tennis_event_to_nice_open()

            start_time = self.get_date_time_formatted_string(hours=6)
            self.ob_config.add_tennis_event_to_autotest_trophy(start_time=self.get_date_time_formatted_string(hours=1))
            self.ob_config.add_tennis_event_to_autotest_trophy(start_time=self.get_date_time_formatted_string(hours=2))

            self.ob_config.add_tennis_event_to_autotest_trophy(start_time=self.get_date_time_formatted_string(hours=3))
            self.ob_config.add_tennis_event_to_autotest_trophy(start_time=self.get_date_time_formatted_string(hours=4))

            for outright in range(0, 4):
                outright_name = f'Outright {int(time.time())}'
                self.ob_config.add_tennis_outright_event_to_autotest_league(
                    event_name=outright_name, start_time=start_time)
        start_date = f'{get_date_time_as_string(days=-10)}T21:00:00.000Z'
        query = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.INTERSECTS, str(tennis_category_id))) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL,
                                      start_date)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.LESS_THAN,
                                      f'{get_date_time_as_string(days=10)}T21:00:00.000Z')) \
            .add_filter(simple_filter(LEVELS.MARKET, ATTRIBUTES.DISP_SORT_NAME, OPERATORS.INTERSECTS, 'HH, MH, WH')) \
            .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.DISP_SORT_NAME,
                                                                  OPERATORS.INTERSECTS, 'HH, MH, WH'))) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_FALSE))
        class_ids = self.get_class_ids_for_category(category_id=tennis_category_id)

        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=tennis_category_id)
        events_list = ss_req.ss_event_to_outcome_for_class(query_builder=query, class_id=class_ids)
        self.verify_events_are_present(resp=events_list)

        sorted_leagues = self.sort_by_disp_order(events_list)
        self.__class__.expected_leagues_order = [item.replace('Tennis - ', '') for item in sorted_leagues]
        if tests.settings.backend_env == 'prod':
            self.__class__.section_name_list = self.expected_leagues_order[0]
        elif self.device_type == 'mobile':
            self.__class__.section_name_list = 'Auto Test Trophy'
        else:
            self.__class__.section_name_list = tests.settings.tennis_autotest_competition_trophy

        self.site.open_sport(name='TENNIS', timeout=30)
        self.site.tennis.tabs_menu.click_button(
            button_name=self.get_sport_tab_name(name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                category_id=self.ob_config.tennis_config.category_id))

    def test_001_select_any_type_eg_wimbledon___mens_single(self):
        """
        DESCRIPTION: Select any type e.g. Wimbledon - Men's Single
        EXPECTED: Competition details page is opened
        """
        leagues = self.site.tennis.tab_content.competitions_categories.get_items(name=self.section_name_list)
        self.assertTrue(leagues, msg=f'Competitions page does not have any "{self.section_name_list}" section')
        league = leagues.get(self.section_name_list)
        self.assertTrue(league, msg=f'Cannot find "{self.section_name_list}" section on Competitions page')
        league.click()
        self.site.wait_content_state('CompetitionLeaguePage')

    def test_002_verify_competition_details_page(self):
        """
        DESCRIPTION: Verify Competition details page
        EXPECTED: The following elements are present on the page:
        EXPECTED: * 'COMPETITIONS' label next to the 'back' ('<') button
        EXPECTED: * Competition header with competition name and 'Change Competition' selector
        EXPECTED: * 2 tabs: 'Matches', 'Outrights'
        EXPECTED: * 'Matches' tab is selected by default and events from the league are shown
        """
        competition_name = self.site.competition_league.title_section.type_name.text
        self.assertEqual(competition_name, self.section_name_list,
                         msg=f'Competition header with competition name is not same '
                             f'Actual: "{competition_name}" '
                             f'Expected: "{self.section_name_list}"')

        change_competition_selector = self.site.competition_league.title_section.competition_selector_link.name
        self.assertEqual(change_competition_selector, vec.sb.CHANGE_COMPETITION,
                         msg=f'Competition header with Change Competition selector is not same'
                             f'Actual: "{change_competition_selector}" '
                             f'Expected: "{vec.sb.CHANGE_COMPETITION}"')

        if tests.settings.backend_env == 'prod':
            market_tab = self.site.tennis.tab_content.accordions_list.items
            if len(market_tab) == 0:
                market_tab = self.site.tennis.tab_content.grouping_buttons.items_as_ordered_dict
        else:
            expected_tabs = [vec.sb.SPORT_TABS_INTERNAL_NAMES.matches.upper(),
                             vec.sb.SPORT_TABS_INTERNAL_NAMES.outrights.upper()]
            market_tab = self.site.tennis.tab_content.grouping_buttons.items_as_ordered_dict

            for tab_name in list(market_tab):
                self.assertIn(tab_name.upper(), expected_tabs, msg=f'Competition tab is not loaded with sections.'
                                                                   f'Actual: "{list(market_tab)}",'
                                                                   f'Expected: "{expected_tabs}"')
        self.assertTrue(market_tab, msg='Matches/ Outright tab is not present for event type in Competition')

        self.__class__.tabs_menu = self.site.competition_league.tabs_menu.items_as_ordered_dict
        self.assertTrue(self.tabs_menu, msg='Tabs menu items are not present')

        current_tab = self.site.competition_league.tabs_menu.current
        self.assertEqual(current_tab, self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches.upper(),
                         msg=f'"Matches" tab is not selected by default'
                             f'Actual: "{current_tab}" '
                             f'Expected: "{self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches.upper()}"')

        events_in_tab = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(events_in_tab, msg='Matches tab has no content')

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
        EXPECTED: User is taken to the 'Competitions' tab on the Tennis Landing page
        """
        self.site.back_button_click()
        leagues = self.site.tennis.tab_content.competitions_categories.get_items(name=self.section_name_list)
        self.assertTrue(leagues, msg=f'Competitions page does not have any "{self.section_name_list}" section')

    def test_005_repeat_step_1(self):
        """
        DESCRIPTION: Repeat step 1
        EXPECTED: User is taken to the selected competition details page
        """
        self.test_001_select_any_type_eg_wimbledon___mens_single()

    def test_006_scroll_the_page_down(self):
        """
        DESCRIPTION: Scroll the page down
        EXPECTED: * Competition header and 'Change Competition' selector are sticky (remain at the top of the scrolling page)
        EXPECTED: * 'Matches' and 'Outrights' switcher are hidden
        """
        competition_league = self.site.competition_league
        self.__class__.competition_name = competition_league.title_section.type_name
        self.__class__.change_competition_selector = competition_league.title_section.competition_selector_link
        self.__class__.market_selector = self.site.competition_league.title_section.competition_selector_link
        self.__class__.tabs_menu = competition_league.tabs_menu.items_as_ordered_dict

        sections = competition_league.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        last_section_name, self.__class__.last_section = list(sections.items())[-1]

        self.last_section.scroll_to()
        self.assertTrue(self.competition_name.is_displayed(), msg='"Competition header" is not displayed')
        self.assertTrue(self.is_element_displayed(self.change_competition_selector),
                        msg='"Change Competition" selector is not displayed')
        self.change_competition_selector.perform_click()  # reverting the click action done in is_element_displayed()
        self.site.footer.scroll_to()  # as the element is clicked, page is scrolled to top
        self.assertFalse(self.is_element_displayed(list(self.tabs_menu.values())[0]),
                         msg='Switcher tab is not hidden and is visible')

    def test_007_scroll_the_page_up(self):
        """
        DESCRIPTION: Scroll the page up
        EXPECTED: * Competition header and 'Change Competition' selector  are sticky (remain at the top of the scrolling page)
        EXPECTED: * 'Matches' and 'Outrights' switchers are hidden
        EXPECTED: * After the page is scrolled all the way up, user sees switchers
        """
        self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
        self.assertFalse(self.is_element_displayed(list(self.tabs_menu.values())[0]),
                         msg='Switcher tab is not hidden and is visible')
        self.site.header.scroll_to()
        self.assertTrue(self.is_element_displayed(self.competition_name), msg='"Competition header" is not displayed')
        self.assertTrue(self.is_element_displayed(self.change_competition_selector),
                        msg='"Change Competition" selector is not displayed')
        self.change_competition_selector.perform_click()  # reverting the click action done in is_element_displayed()
        self.assertTrue(self.is_element_displayed(self.market_selector), msg='"Market selector" is not displayed')
        self.assertTrue(self.is_element_displayed(list(self.tabs_menu.values())[0]),
                        msg='Switcher tab is not hidden and is visible')

    def test_008_scroll_the_page_down_and_click_on_change_competition_selector(self):
        """
        DESCRIPTION: Scroll the page down and click on 'Change Competition' selector
        EXPECTED: 'Change Competition' selector is clickable and displays available competitions
        """
        self.last_section.scroll_to()
        self.site.competition_league.title_section.competition_selector_link.click()

        competitions = self.site.competition_league.competition_list.items_as_ordered_dict
        self.assertTrue(competitions, msg='Available competitions are not displayed on page')
