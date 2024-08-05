import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.low
@pytest.mark.desktop
@pytest.mark.football
@pytest.mark.market_selector
@pytest.mark.sports
@vtest
class Test_C157470_Verify_previously_selected_market_state_is_saved_after_switching_between_Today_Tomorrow_Future_tabs_on_Football_landing_page(BaseSportTest):
    """
    TR_ID: C157470
    NAME: Verify previously selected market state is saved after switching between Today/Tomorrow/Future tabs on Football landing page
    DESCRIPTION: This test case verifies that previously selected market state is saved after switching between Today/Tomorrow/Future tabs on Football landing page
    """
    keep_browser_open = True
    both_teams_to_score_market = vec.siteserve.EXPECTED_MARKETS_NAMES.both_teams_to_score
    default_date_tab = vec.sb.SPORT_DAY_TABS.today
    market = [('both_teams_to_score', {'cashout': True})]

    def verify_displaying_of_the_selected_market(self, event_name):
        sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found on page')
        self.assertIn(tests.settings.football_autotest_league, sections,
                      msg=f'Can not find "{tests.settings.football_autotest_league}" in "{sections}"')
        section = sections.get(tests.settings.football_autotest_league, None)
        self.assertTrue(section, msg=f'"{tests.settings.football_autotest_league}" section not found on page')
        events = section.items_as_ordered_dict
        self.assertTrue(events, msg='No event groups found on page')
        self.assertIn(event_name, events.keys(),
                      msg=f'Can not find "{event_name}" in "{events.keys()}"')
        event = events.get(event_name, None)
        self.assertTrue(event, msg=f'Incorrect filtering by "{self.both_teams_to_score_market}" market. Event '
                                   f'with "{event_name}" is not present')
        actual_buttons = event.template.items_as_ordered_dict
        self.assertTrue(actual_buttons, msg=f'No Price/Odds buttons found')
        for price_button_name, price_button in actual_buttons.items():
            self.softAssert(self.assertTrue, price_button.is_displayed(),
                            msg=f'Price/Odds button "{price_button_name}" is not displayed')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Adds football events
        """
        self.__class__.both_teams_to_score_market_name = self.both_teams_to_score_market.upper() \
            if (self.device_type == 'desktop' and self.brand == 'ladbrokes') else self.both_teams_to_score_market

        today_event = self.ob_config.add_autotest_premier_league_football_event(markets=self.market)
        self.__class__.today_event_name = f'{today_event.team1} v {today_event.team2}'

        tomorrow_start_time = self.get_date_time_formatted_string(days=1)
        tomorrow_event = self.ob_config.add_autotest_premier_league_football_event(start_time=tomorrow_start_time,
                                                                                   markets=self.market)
        self.__class__.tomorrow_event_name = f'{tomorrow_event.team1} v {tomorrow_event.team2}'

        future_start_time = self.get_date_time_formatted_string(days=14)
        future_event = self.ob_config.add_autotest_premier_league_football_event(start_time=future_start_time,
                                                                                 markets=self.market)
        self.__class__.future_event_name = f'{future_event.team1} v {future_event.team2}'

    def test_001_go_to_the_football_landing_page(self):
        """
        DESCRIPTION: Go to the 'Football' Landing page
        EXPECTED: **Desktop:**
        EXPECTED: * <Sport> Landing Page is opened
        EXPECTED: * 'Matches'->'Today' sub tab is opened by default
        EXPECTED: **Mobile:**
        EXPECTED: * <Sport> Landing Page is opened
        EXPECTED: * 'Matches' tab is opened by default
        """
        self.site.open_sport(name='FOOTBALL')
        self.site.wait_content_state(vec.siteserve.FOOTBALL_TAB)
        expected_sport_tab = self.site.football.tabs_menu.current
        sport_tab_from_cms = \
            self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches, self.ob_config.football_config.category_id)
        self.assertEqual(expected_sport_tab, sport_tab_from_cms,
                         msg=f'Default tab is not "{sport_tab_from_cms}", it is "{expected_sport_tab}"')
        if self.device_type == 'desktop':
            current_date_tab = self.site.football.date_tab.current_date_tab
            self.assertEqual(current_date_tab, self.default_date_tab, msg=f'"{self.default_date_tab}" is not active '
                                                                          f'date tab, active is "{current_date_tab}"')

    def test_002_verify_displaying_of_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Verify displaying of the 'Market selector' drop down
        DESCRIPTION: (in case Enhanced Multiples are NOT available)
        EXPECTED: For tablet/mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing up) on the module header opens the MS dropdown
        EXPECTED: For desktop:
        EXPECTED: • 'Market selector' is displayed next to Date Selector on the right side
        EXPECTED: • 'Match Result' is selected by default in 'Market selector' drop down
        EXPECTED: • Up and down arrows are shown next to 'Match result' in 'Market selector'
        """
        if self.brand == 'ladbrokes':
            market_selector_default_value = 'Match Result' if self.device_type == 'mobile' else 'MATCH RESULT'
        else:
            market_selector_default_value = vec.siteserve.EXPECTED_MARKETS_NAMES.match_result
        self.__class__.football_tab_content = self.site.football.tab_content
        self.assertTrue(self.football_tab_content.has_dropdown_market_selector(),
                        msg='"Market Selector" drop-down is not displayed on Football landing page')
        self.assertEqual(self.football_tab_content.dropdown_market_selector.selected_market_selector_item,
                         market_selector_default_value,
                         msg=f'Incorrect market name is selected by default:\n'
                             f'Actual: {self.football_tab_content.dropdown_market_selector.selected_market_selector_item}\n'
                             f'Expected: {market_selector_default_value}')

    def test_003_select_any_other_market_in_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Select any other market in the Market selector drop down
        EXPECTED: * The events for selected market are shown
        EXPECTED: * Values on Fixture header are changed for each event according to selected market
        EXPECTED: * Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        market_dropdown = self.football_tab_content.dropdown_market_selector
        market_dropdown.value = self.both_teams_to_score_market
        self.verify_displaying_of_the_selected_market(self.today_event_name)

    def test_004_switch_to_tomorrow_tab_desktop(self):
        """
        DESCRIPTION: Switch to 'Tomorrow' tab (Desktop)
        EXPECTED: * Previously selected market is displayed in the 'Market selector' drop down
        EXPECTED: * The events for selected market are shown
        EXPECTED: * Values on Fixture header are displayed for each event according to selected market
        EXPECTED: * Number and order of 'Price/Odds' buttons are displayed for each event according to selected market
        """
        if self.device_type == 'desktop':
            self.site.sports_page.date_tab.tomorrow.click()
            self.assertEqual(self.site.sports_page.date_tab.current_date_tab, vec.sb.SPORT_DAY_TABS.tomorrow,
                             msg=f'Current active tab: "{self.site.sports_page.date_tab.current_date_tab}", '
                                 f'expected: "{vec.sb.SPORT_DAY_TABS.tomorrow}"')
            self.__class__.football_tab_content = self.site.football.tab_content

            self.assertEqual(self.football_tab_content.dropdown_market_selector.selected_market_selector_item,
                             self.both_teams_to_score_market_name,
                             msg=f'Incorrect market name is selected:\n'
                                 f'Actual: {self.football_tab_content.dropdown_market_selector.selected_market_selector_item}\n'
                                 f'Expected: {self.both_teams_to_score_market_name}')
            self.verify_displaying_of_the_selected_market(self.tomorrow_event_name)

    def test_005_repeat_step_4_for_future_tab_desktop(self):
        """
        DESCRIPTION: Repeat step 4 for 'Future' tab (Desktop)
        EXPECTED:
        """
        if self.device_type == 'desktop':
            self.site.sports_page.date_tab.future.click()
            self.assertEqual(self.site.sports_page.date_tab.current_date_tab, vec.sb.SPORT_DAY_TABS.future,
                             msg=f'Current active tab: "{self.site.sports_page.date_tab.current_date_tab}", '
                                 f'expected: "{vec.sb.SPORT_DAY_TABS.future}"')
            self.__class__.football_tab_content = self.site.football.tab_content
            self.assertEqual(self.football_tab_content.dropdown_market_selector.selected_market_selector_item,
                             self.both_teams_to_score_market_name,
                             msg=f'Incorrect market name is selected:\n'
                                 f'Actual: {self.football_tab_content.dropdown_market_selector.selected_market_selector_item}\n'
                                 f'Expected: {self.both_teams_to_score_market_name}')
            self.verify_displaying_of_the_selected_market(self.future_event_name)
