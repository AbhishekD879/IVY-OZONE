import pytest
from tests.base_test import vtest
from time import sleep
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  #cannot create event with all markets in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.market_switcher
@vtest
class Test_C60089513_Verify_MS_behavior_on_Specific_Competitions_page_for_Basketball(BaseSportTest):
    """
    TR_ID: C60089513
    NAME: Verify MS behavior on Specific Competitions page for Basketball
    DESCRIPTION: This test case verifies the behaviour of 'Market Selector' dropdownon competitions page
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Basketball Competition Tab -> 'Click on Specific Competition'
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Money Line (WW)| - "Money Line"
    PRECONDITIONS: * |Total Points (Over/Under)| - "Total Points"
    PRECONDITIONS: * |Handicap 2-way (Handicap)| - "Handicap"
    PRECONDITIONS: * |Home Team Total Points (Over/Under)| - "Home Team Total Points"
    PRECONDITIONS: * |Away Team Total Points (Over/Under)| - "Away Team Total Points"
    PRECONDITIONS: * |Half Total Points  (Over/Under)| - "Current Half Total Points"
    PRECONDITIONS: * |Quarter Total Points (Over/Under)| - "Current Quarter Total Points"
    """
    keep_browser_open = True
    market_selector_options = [
        ('total_points',),
        ('handicap_2_way',),
        ('home_team_total_points',),
        ('away_team_total_points',),
        ('half_total_points',),
        ('quarter_total_points',)
    ]

    expected_market_selector_options = [vec.siteserve.EXPECTED_MARKETS_NAMES.money_line,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.total_points,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.handicap_2_way,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.home_team_total_points,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.away_team_total_points,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.half_total_points,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.quarter_total_points,
                                        ]

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create basketball event
        EXPECTED: Event is successfully created
        """
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='basketball',
                                                                                          status=True)
        self.assertTrue(market_switcher_status, msg='Market switcher is disabled for basketball sport')
        self.cms_config.verify_and_update_sport_config(
            sport_category_id=self.ob_config.backend.ti.basketball.category_id,
            disp_sort_names='HL,WH,HH',
            primary_markets='|Money Line|,|Total Points|,'
                            '|Home team total points|,|Away team total points|,'
                            '|Half Total Points|,|Quarter Total Points|,'
                            '|Handicap 2-way|')
        self.ob_config.add_basketball_event_to_us_league(markets=self.market_selector_options)
        self.__class__.market_selector_default_value = vec.siteserve.EXPECTED_MARKETS_NAMES.money_line
        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state(state_name='basketball')
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                    self.ob_config.basketball_config.category_id)
        self.site.basketball.tabs_menu.click_button(vec.SB.TABS_NAME_COMPETITIONS.upper())
        current_tab = self.site.contents.tabs_menu.current
        self.assertEqual(expected_tab_name, current_tab, msg=f'Actual tab: "{current_tab}" is not same as '
                                                             f'Expected tab: "{expected_tab_name}"')
        self.navigate_to_page(name='competitions/basketball/basketball-usa/nba')
        self.device.refresh_page()

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: Desktop:
        EXPECTED: • 'Market Selector' is displayed next to Day Selectors (Today/Tomorrow/Future) on the right side
        EXPECTED: • 'Match Result' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Match result' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to 'Match result' in 'Market selector' Coral
        """
        has_market_selector = self.site.sports_page.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for basketball')
        dropdown = self.site.sports_page.tab_content.dropdown_market_selector
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(dropdown.change_button, msg=f'"Change button" is not displayed')
            dropdown.click()
            self.assertFalse(dropdown.is_expanded(), msg=f' "Dropdown arrow" is not pointing downwards')
        else:
            if self.brand == 'bma':
                self.assertTrue(dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                dropdown.click()
                sleep(1)
                self.assertFalse(dropdown.is_expanded(), msg=f'"Dropdown Arrow" is not pointing downwards')
        market_selector_default_value = self.market_selector_default_value.upper() \
            if self.brand == 'ladbrokes' and self.device_type == 'desktop' else self.market_selector_default_value
        self.assertEqual(
            self.site.sports_page.tab_content.dropdown_market_selector.selected_market_selector_item,
            market_selector_default_value,
            msg=f'Incorrect market name is selected by default:\n'
                f'Actual: "{self.site.sports_page.tab_content.dropdown_market_selector.selected_market_selector_item}"\n'
                f'Expected: "{market_selector_default_value}"')

    def test_002_tap_on_the_change_button_in_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Tap on the 'Change' button in 'Market Selector' dropdown list
        EXPECTED: • 'Market Selector' dropdown list opens
        EXPECTED: • List of markets are displayed
        EXPECTED: • The chevron near 'Change' button is pointed upwards
        """
        if self.brand == 'bma':
            self.expected_market_selector_options[2] = 'Spread'
        self.__class__.list_of_drop_down = self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict
        available_markets = list(self.list_of_drop_down.keys())
        self.assertEqual(available_markets, self.expected_market_selector_options,
                         msg=f'Incorrect list/order of markets in Market Selector drop-down.\n'
                             f'Actual: {available_markets}\nExpected: {self.expected_market_selector_options}')
        dropdown = self.site.sports_page.tab_content.dropdown_market_selector
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(dropdown.change_button, msg=f'"Change button" is not displayed')
            dropdown.click()
            self.assertFalse(dropdown.is_expanded(), msg=f'dropdown arrow is not pointing downwards')

    def test_003_verify_the_behavior_of_the_market_drop_down_list(self):
        """
        DESCRIPTION: Verify the behavior of the market drop down list
        EXPECTED: • User should be able to mouse over the markets in the list,The market which is in focus will get highlighted.
        """
        # cannot automate for mobile
        if self.device_type == 'desktop':
            drop_down = self.site.sports_page.tab_content.dropdown_market_selector
            for option, element in self.list_of_drop_down.items():
                element.mouse_over()
                # when mouse over, color is not reflecting immediately
                sleep(2)
                actual_bg_color = element.background_color_value
                self.assertEqual(actual_bg_color, vec.colors.MARKET_SWITCHER_HIGHLIGHTED_COLOR,
                                 msg=f'Actual background color: "{actual_bg_color}" is not same as'
                                     f'Expected background color: "{vec.colors.MARKET_SWITCHER_HIGHLIGHTED_COLOR}"')
                drop_down.select_value(value=option)
                dropdown = self.site.sports_page.tab_content.dropdown_market_selector
                selected_value = dropdown.selected_market_selector_item
                self.assertEqual(selected_value.upper(), option.upper(),
                                 msg=f'Actual selected value: "{selected_value}" is not same as '
                                     f'Expected selected value: "{option}"')

    def test_004_click_on_the_market_which_is_higlighted(self):
        """
        DESCRIPTION: Click on the market which is higlighted
        EXPECTED: • Selected market should be displayed in the dropdown
        """
        # covered in step test_003

    def test_005_tap_on_the_change_button_again_and_mouse_over_the_content(self):
        """
        DESCRIPTION: Tap on the 'Change' button again and mouse over the content
        EXPECTED: • 'Market Selector' dropdown list opens
        EXPECTED: • List the Markets will be displayed
        EXPECTED: • The chevron near 'Change' button is pointed upwards(Ladbrokes)
        """
        drop_down = self.site.sports_page.tab_content.dropdown_market_selector
        self.assertTrue(drop_down, msg='"Market Selector" dropdown is available')
        self.test_002_tap_on_the_change_button_in_market_selector_dropdown_list()
