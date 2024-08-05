import pytest
import tests
import voltron.environments.constants as vec
from time import sleep
from selenium.webdriver import ActionChains
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.pages.shared import get_driver
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C1203369_Verify_Outright_events_and_markets_on_Competitions_Details_page_on_Desktop(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C1203369
    NAME: Verify Outright events and markets on Competitions Details page on Desktop
    DESCRIPTION: This test case verifies Outright events and markets on Competitions Details page on Desktop.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS:
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get events
        """
        self.__class__.is_mobile = self.device_type == 'mobile'
        if tests.settings.backend_env != 'prod':
            competitions_countries = self.get_initial_data_system_configuration().get('CompetitionsFootball')
            if not competitions_countries:
                competitions_countries = self.cms_config.get_system_configuration_item('CompetitionsFootball')
            if str(self.ob_config.football_config.autotest_class.class_id) not in competitions_countries.get(
                    'A-ZClassIDs').split(','):
                raise CmsClientException('Football competition class is not configured on Competitions tab')
            self.ob_config.add_autotest_premier_league_football_event()
            self.ob_config.add_autotest_premier_league_football_outright_event(ew_terms=self.ew_terms)
            self.__class__.section_name_list = 'Auto Test' if self.brand == 'ladbrokes' else tests.settings.football_autotest_competition

        else:
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            self._logger.info(f'*** Found event: {event}')
            self.__class__.section_name_list = event['event']['className']

        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='football')
        self.__class__.competitions_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
            self.ob_config.football_config.category_id)
        self.assertTrue(self.competitions_tab_name, msg='competition tab is not available')

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        # covered in above step

    def test_002_navigate_to_football_competitions_details_page(self):
        """
        DESCRIPTION: Navigate to Football Competitions Details page
        EXPECTED: * Competition Details page is opened
        EXPECTED: * 'Matches' and 'Outrights' switchers are displayed below Competitions header and Breadcrumbs trail in the same row as 'Market Selector'
        EXPECTED: * 'Matches' switcher is selected by default and highlighted
        EXPECTED: * List of events is loaded on the page
        """
        self.site.football.tabs_menu.click_button(
            button_name=self.get_sport_tab_name(name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                category_id=self.ob_config.football_config.category_id))
        self.__class__.competitions = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.competitions, msg='No competitions are present on page')

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
        competition = self.competitions[league]
        competition.expand()
        leagues = wait_for_result(lambda: competition.items_as_ordered_dict,
                                  name='Leagues list is loaded',
                                  timeout=2)
        self.assertTrue(leagues, msg='No leagues are present on page')
        self.assertIn(competition_league, leagues.keys(),
                      msg=f'League "{competition_league}" is not found in "{list(leagues.keys())}"')
        self.__class__.league = leagues[competition_league]
        self.league.click()
        self.site.wait_content_state('CompetitionLeaguePage')

        tabs_menu = self.site.competition_league.tabs_menu
        self.assertTrue(tabs_menu, msg='Tabs menu was not found')

        desktop_tabs = list(vec.sb.COMPETITION_DETAILS_PAGE_TABS._asdict().values()) \
            if self.brand == 'bma' else [tab.title() for tab in
                                         vec.sb.COMPETITION_DETAILS_PAGE_TABS._asdict().values()]
        for tab_name, tab in tabs_menu.items_as_ordered_dict.items():
            self.assertIn(tab_name, desktop_tabs,
                          msg=f'Market switcher tab {tab_name} is not present in the list')
        current_tab = tabs_menu.current
        if self.brand == "bma":
            self.assertEqual(current_tab, vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches,
                             msg=f'Relevant tab is not opened, Actual "{current_tab}" '
                                 f'expected "{desktop_tabs[0]}"')
        else:
            self.assertEqual(current_tab, vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches.title(),
                             msg=f'Relevant tab is not opened, Actual "{current_tab}" '
                                 f'expected "{desktop_tabs[0]}"')

    def test_003_choose_outrights_switcher_and_verify_outrights_layout_displaying_for_the_league_with_one_event_available_ie_premier_league_championship_etc(self):
        """
        DESCRIPTION: Choose 'Outrights' switcher and verify Outrights Layout displaying for the league with one event available (i.e. 'Premier League', 'Championship', etc.)
        EXPECTED: The following elements are displayed on the page:
        EXPECTED: * Event Name Panel (i.e. 'Premier League 2017/2018')
        EXPECTED: * 'Outrights market' accordions (i.e. 'Top Goalscorer', 'Top 4 Finish', etc.)
        EXPECTED: * Markets card
        """
        competitions_countries = self.get_initial_data_system_configuration().get('CompetitionsFootball')
        if not competitions_countries:
            competitions_countries = self.get_system_configuration_item('CompetitionsFootball')
        self.__class__.cms_initial_class_ids = competitions_countries.get('InitialClassIDs', '')
        tabs = self.site.competition_league.tabs_menu.items_as_ordered_dict
        tabs.get(vec.SB.TABS_NAME_OUTRIGHTS.upper()).click() if self.brand == 'bma' else tabs.get(
            vec.SB.TABS_NAME_OUTRIGHTS).click()

        if self.cms_initial_class_ids:
            initial_sections = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
            self.__class__.first_accordian = list(initial_sections.values())[0]
            selections = self.first_accordian.outright_selections
            self.assertTrue(selections, msg='selections are not displayed')
            self.assertTrue(initial_sections,
                            msg=f'No Initial sections found on "{self.competitions_tab_name}" tab')

    def test_004_verify_outrights_market_accordion_displaying(self):
        """
        DESCRIPTION: Verify 'Outrights Market' accordion displaying
        EXPECTED: The following elements are displayed on 'Outrights Market' accordion:
        EXPECTED: * 'Outrights market name' on accordion (i.e. 'Top Goalscorer', 'Top 4 Finish', etc.) on the left side
        EXPECTED: * 'Chevron' (Up and Down depends on expanding/collapsing of accordion) on the right side
        EXPECTED: * 'Cashout' icon before the Chevron (if applicable)
        EXPECTED: * The first 'Outrights Market' accordion is expanded by default, the rest are collapsed
        """
        if self.cms_initial_class_ids:
            self.assertTrue(self.first_accordian.group_sport_header, msg='Market name is not present')
            self.assertTrue(self.first_accordian.chevron_arrow, msg='"Chevron" is not present')
            self.assertTrue(self.first_accordian.section_header.has_cash_out_mark, msg='"Cashout" icon is not present')
            self.assertTrue(self.first_accordian.is_expanded(), msg='First accordian is not expanded by default')

    def test_005_hover_the_mouse_over_the_outrights_market_accordion(self):
        """
        DESCRIPTION: Hover the mouse over the 'Outrights Market' accordion
        EXPECTED: * The background color of accordion is changed
        EXPECTED: * Pointer is changed view from 'Normal select' to 'Link select' for realizing the possibility to click on particular area
        """
        if self.cms_initial_class_ids:
            if self.brand == 'bma':
                before = self.first_accordian.group_sport_header.background_color_value
                self.first_accordian.group_sport_header.mouse_over()
                after = self.first_accordian.group_sport_header.background_color_value
                self.assertNotEqual(before, after, msg='Button color did not change')

            self.first_accordian.group_sport_header.click()
            sleep(2)
            self.assertFalse(self.first_accordian.is_expanded(), msg='Accordian is not collapsed after click')
            self.first_accordian.group_sport_header.click()
            sleep(2)
            self.assertTrue(self.first_accordian.is_expanded(), msg='Accordian is not expanded after click')

    def test_006_click_on_outrights_market_accordion(self):
        """
        DESCRIPTION: Click on 'Outrights Market' accordion
        EXPECTED: * 'Outrights Market' accordion is expandable/collapsible
        EXPECTED: * 'Outrights Market' card is displayed within the expanded 'Outrights Market' accordion
        """
        # Covered in step 5

    def test_007_verify_outrights_market_card(self):
        """
        DESCRIPTION: Verify 'Outrights Market' card
        EXPECTED: The following elements are displayed on 'Outrights Market' card:
        EXPECTED: * 'Each Way' terms on the left side of market header (if applicable)
        EXPECTED: * Event start date is shown in **'<name of the day>, DD-MMM-YY 24 hours HH:MM'** (e.g. 14:00 or 05:00) format on the right side of header for every 'Outright market' card
        EXPECTED: * Selection names and 'Price/Odds' buttons in tile view (from left to right order)
        """
        if self.cms_initial_class_ids:
            self.assertTrue(self.first_accordian.outright_ew_terms, msg='"Each Way" terms are not present')
            self.assertTrue(self.first_accordian.outright_date_time, msg='"Each Way" terms are not present')

    def test_008_hover_the_mouse_over_the_priceodds_button(self):
        """
        DESCRIPTION: Hover the mouse over the 'Price/Odds' button
        EXPECTED: * The background color of 'Price/Odds' button is changed
        EXPECTED: * Pointer is changed view from 'Normal select' to 'Link select' for realizing the possibility to click on particular area
        """
        if self.cms_initial_class_ids:
            bet_button = self.site.competition_league.bet_buttons[0]
            before = bet_button.value_of_css_property('background-color')
            ActionChains(get_driver()).move_to_element(bet_button).perform()
            after = bet_button.value_of_css_property('background-color')
            self.assertEqual(before, after, msg='Button color did not change')

    def test_009_click_on_priceodds_button(self):
        """
        DESCRIPTION: Click on 'Price/Odds' button
        EXPECTED: * 'Price/Odds' button is clickable
        EXPECTED: * 'Price/Odds' button looks as selected (it changes color to green)
        EXPECTED: * Selection is added to the Betslip
        """
        if self.cms_initial_class_ids:
            bet_button = self.site.competition_league.bet_buttons[0]
            bet_button.click()
            sleep(2)
            singles_section = self.get_betslip_sections().Singles
            self.assertTrue(singles_section, msg='Selection not added to betslip')
            bet_button.click()

    def test_010_navigate_to_competitions_details_page_outrights_switcher_that_has_several_outright_events_ie_world_cup_2018_europa_cup_copa_america_etc(self):
        """
        DESCRIPTION: Navigate to Competitions Details page ('Outrights' switcher) that has several Outright events (i.e. 'World Cup 2018', 'Europa Cup', 'Copa America' etc.)
        EXPECTED: The following elements are displayed on the page:
        EXPECTED: * 'Outrights event' accordions (i.e. 'Group A', 'Group B', etc.)
        EXPECTED: * Separate markets cards
        """
        # Covered in step 3

    def test_011_verify_outrights_event_accordion(self):
        """
        DESCRIPTION: Verify 'Outrights Event' accordion
        EXPECTED: The following elements are displayed on 'Outrights Event' accordion:
        EXPECTED: * 'Outrights event name' on accordion (i.e. 'Group A', 'Group B', etc.) on the left side
        EXPECTED: * 'Chevron' (Up and Down depends on expanding/collapsing of accordion) on the right side
        EXPECTED: * 'Cashout' icon before the Chevron (if applicable)
        """
        self.test_004_verify_outrights_market_accordion_displaying()

    def test_012_repeat_steps_5_6_for_outrights_event_accordion(self):
        """
        DESCRIPTION: Repeat steps 5-6 for 'Outrights Event' accordion
        EXPECTED:
        """
        self.test_005_hover_the_mouse_over_the_outrights_market_accordion()
        self.test_006_click_on_outrights_market_accordion()

    def test_013_verify_outrights_market_cards(self):
        """
        DESCRIPTION: Verify 'Outrights Market' cards
        EXPECTED: * Every market is displayed in the separate 'Outrights Market' card
        EXPECTED: * The following elements are displayed on 'Outrights Market' card:
        EXPECTED: * Name of market (i.e. 'Group Winner', 'To Qualify', etc.) on the left side of market header
        EXPECTED: * 'Each Way' terms next to 'Market name' (if applicable)
        EXPECTED: * Event start date is shown in **'<name of the day>, DD-MMM-YY 12 hours AM/PM'** format on the right side of header for every 'Outright market' card
        EXPECTED: * Selection names and 'Price/Odds' buttons in tile view (from left to right order)
        """
        self.test_007_verify_outrights_market_card()

    def test_014_repeat_steps_8_9(self):
        """
        DESCRIPTION: Repeat steps 8-9
        EXPECTED:
        """
        self.test_008_hover_the_mouse_over_the_priceodds_button()
        self.test_009_click_on_priceodds_button()

    def test_015_verify_content_of_outrights_page_if_there_are_no_available_events(self):
        """
        DESCRIPTION: Verify content of Outrights page if there are no available events
        EXPECTED: "No events found" is displayed in case there are no available events on Outrights page
        """
        if not self.cms_initial_class_ids:
            self.assertTrue(self.site.competition_league.tab_content.has_no_events_label(),
                            msg='No events label is not shown')
