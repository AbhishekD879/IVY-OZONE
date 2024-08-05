import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Events with specific markets cannot be created in Prod/Beta
@pytest.mark.market_switcher
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C60089516_Verify_MS_behavior_on_Inplay_Tab_for_Basketball(BaseSportTest):
    """
    TR_ID: C60089516
    NAME: Verify MS behavior on Inplay Tab for Basketball
    DESCRIPTION: This test case verifies the behavior of 'Market Selector' dropdown
    PRECONDITIONS: Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Basketball ->Inplay Tab and Inplay from (Desktop - Inplay tab(Sub header menu) -> Basketball) and in Mobile (Inplay (Sports ribbon menu) ->Basketball)
    PRECONDITIONS: 4. Be aware that below markets are available in the 'Market Selector' dropdown list
    PRECONDITIONS: * |Money Line (WW)| - "Money Line"
    PRECONDITIONS: * |Total Points (Over/Under)| - "Total Points"
    PRECONDITIONS: * |Handicap 2-way (Handicap)| - "Handicap"
    PRECONDITIONS: * |Half Total Points  (Over/Under)| - "Current Half Total Points"
    PRECONDITIONS: * |Quarter Total Points (Over/Under)| - "Current Quarter Total Points"
    """
    keep_browser_open = True
    expected_market_selector_options = [vec.siteserve.EXPECTED_MARKETS_NAMES.money_line,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.total_points,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.handicap,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.half_total_points,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.quarter_total_points]
    event_markets = [
        ('total_points',),
        ('handicap_2_way',),
        ('half_total_points',),
        ('quarter_total_points',)]

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Basketball events
        EXPECTED: Event is successfully created
        """
        all_sport_MS_Status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports', status=True)
        self.assertTrue(all_sport_MS_Status, msg='Market switcher is disabled for all sport')

        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='basketball',
                                                                                          status=True)
        self.assertTrue(market_switcher_status, msg='Market switcher is disabled for basketball sport')
        start_time = self.get_date_time_formatted_string(seconds=20)
        self.cms_config.verify_and_update_sport_config(
            sport_category_id=self.ob_config.backend.ti.basketball.category_id,
            disp_sort_names='HL,WH,HH',
            primary_markets='|Money Line|,|Total Points|,|Handicap 2-way|,|Home team total points|,'
                            '|Away team total points|')
        self.ob_config.add_basketball_event_to_us_league(is_live=True, markets=self.event_markets,
                                                         start_time=start_time)
        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state(state_name='basketball')
        expected_tab = self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play
        self.site.basketball.tabs_menu.click_button(self.expected_sport_tabs.in_play)
        expected_tab_name = self.get_sport_tab_name(expected_tab, self.ob_config.basketball_config.category_id)
        current_tab_name = self.site.contents.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as'
                             f'Expected tab: "{expected_tab_name}".')

    def test_001_verify_displaying_of_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Verify displaying of the 'Market selector' drop down
        EXPECTED: Mobile:
        EXPECTED: • The 'Market Selector' is displayed below the 'Live Now (n)' header
        EXPECTED: • 'Main Markets' option is selected by default
        EXPECTED: • 'Change' button is placed next to 'Main Markets' name with the chevron pointing downwards
        EXPECTED: Desktop:
        EXPECTED: • The 'Market Selector' is displayed below the 'Live Now' (n) switcher
        EXPECTED: • 'Main Markets' option is selected by default
        EXPECTED: • 'Change Market' button is placed next to 'Main Markets' name with the chevron pointing downwards (for Ladbrokes)
        EXPECTED: • 'Market' title is placed before 'Main Markets' name and the chevron pointing downwards is placed at the right side of dropdown (for Coral)
        """
        inplay_tab_content = self.site.inplay.tab_content
        self.assertTrue(inplay_tab_content.has_dropdown_market_selector(),
                        msg='"Market Selector" drop-down is not displayed on basketball inplay tab page')
        if self.device_type == 'desktop':
            if self.brand == "bma":
                self.assertTrue(inplay_tab_content.has_down_arrow,
                                msg='chevron (pointing down) arrow not displayed')
            else:
                dropdown = self.site.inplay.tab_content.dropdown_market_selector
                self.assertTrue(dropdown.change_button, msg=f'"Change Market" button is not displayed')
                dropdown.click()
        else:
            dropdown = self.site.inplay.tab_content.dropdown_market_selector
            self.assertTrue(dropdown.is_expanded(),
                            msg='chevron (pointing down) arrow not displayed')
            self.assertTrue(dropdown.change_button, msg=f'"Change button" is not displayed')
            dropdown.click()

    def test_002_tap_on_market_selector(self):
        """
        DESCRIPTION: Tap on Market Selector
        EXPECTED: 'Market Selector' dropdown is displayed
        """
        if self.brand == 'bma':
            dropdown = self.site.basketball.tab_content.dropdown_market_selector
        else:
            dropdown = self.site.inplay.tab_content.dropdown_market_selector
        self.assertTrue(dropdown, msg=f'"Market Selector" dropdown list not opened')
        dropdown.click()
        sleep(1)
        self.assertFalse(dropdown.is_expanded(),
                         msg='chevron (pointing up) arrow not displayed')

    def test_003_verify_the_behavior_of_the_market_drop_down_list(self):
        """
        DESCRIPTION: Verify the behavior of the market drop down list
        EXPECTED: User should be able to mouse over the markets in the list,The market which is in focus will get highlighted.
        """
        if self.device_type == 'desktop':
            if not self.brand == "bma":
                list_of_drop_down = self.site.inplay.tab_content.dropdown_market_selector.items_as_ordered_dict
                dropdown = self.site.inplay.tab_content.dropdown_market_selector
                for option, element in list_of_drop_down.items():
                    dropdown = self.site.inplay.tab_content.dropdown_market_selector
                    sleep(2)
                    element.mouse_over()
                    # when mouse over, color is not reflecting immediately
                    actual_bg_color = element.background_color_value
                    self.assertEqual(actual_bg_color, vec.colors.MARKET_SWITCHER_HIGHLIGHTED_COLOR,
                                     msg=f'Actual background color: "{actual_bg_color}" is not same as'
                                         f'Expected background color: "{vec.colors.MARKET_SWITCHER_HIGHLIGHTED_COLOR}"')
                    dropdown.select_value(value=option)
                    selected_value = self.site.basketball.tab_content.selected_market
                    self.assertEqual(selected_value.upper(), option.upper(),
                                     msg=f'Actual selected value: "{selected_value}" is not same as '
                                         f'Expected selected value: "{option}"')
            else:
                # TODO The market which is in focus will get highlighted as On UI
                #  we are not having any style attribute for coral
                list_of_drop_down = self.site.basketball.tab_content.dropdown_market_selector.options
                for element in range(len(list_of_drop_down)):
                    list_of_drop_down[element].click()
                    selected_value = self.site.basketball.tab_content.dropdown_market_selector.first_selected_option.text
                    self.assertEqual(selected_value, list_of_drop_down[element].text,
                                     msg=f'Actual selected value: "{selected_value}" is not same as '
                                         f'Expected selected value: "{list_of_drop_down[element].text}"')

    def test_004_click_on_the_market_which_is_higlighted(self):
        """
        DESCRIPTION: Click on the market which is higlighted
        EXPECTED: Selected market should be displayed in the dropdown
        """
        # Covered in above step

    def test_005_tap_on_the_change_button_again_and_mouse_over_content(self):
        """
        DESCRIPTION: Tap on the 'Change' button again and mouse over content
        EXPECTED: • 'Market Selector' dropdown list opens
        EXPECTED: • List the Markets will be displayed
        EXPECTED: • The chevron near 'Change' button is pointed upwards(Ladbrokes)
        """
        # Covered in step 2
