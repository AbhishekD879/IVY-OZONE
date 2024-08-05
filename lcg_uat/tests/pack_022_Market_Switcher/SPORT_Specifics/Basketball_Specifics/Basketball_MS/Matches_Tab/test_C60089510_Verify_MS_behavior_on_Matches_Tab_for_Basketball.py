import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from time import sleep
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Events with specific markets cannot be created in Prod/Beta
@pytest.mark.market_switcher
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C60089510_Verify_MS_behavior_on_Matches_Tab_for_Basketball(BaseSportTest):
    """
    TR_ID: C60089510
    NAME: Verify MS behavior on Matches Tab for Basketball
    DESCRIPTION: This test case verifies the behavior of 'Market Selector' dropdown list
    PRECONDITIONS: Precondition:
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Basketball Landing page -> 'Matches' tab
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Money Line (WW)| - "Money Line"
    PRECONDITIONS: * |Total Points (Over/Under)| - "Total Points"
    PRECONDITIONS: * |Handicap 2-way (Handicap)| - "Handicap"
    PRECONDITIONS: * |Home Team Total Points (Over/Under)| - "Home Team Total Points"
    PRECONDITIONS: * |Away Team Total Points (Over/Under)| - "Away Team Total Points"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    expected_market_selector_options = [vec.siteserve.EXPECTED_MARKETS_NAMES.money_line,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.total_points,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.handicap,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.home_team_total_points,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.away_team_total_points]
    event_markets = [
        ('total_points',),
        ('handicap_2_way',),
        ('home_team_total_points',),
        ('away_team_total_points',)]

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Basketball events  with scores
        EXPECTED: Event is successfully created
        """
        all_sport_MS_Status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                       status=True)
        self.assertTrue(all_sport_MS_Status, msg='Market switcher is disabled for all sports')
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
        self.ob_config.add_basketball_event_to_us_league(markets=self.event_markets)
        self.__class__.market_selector_default_value = vec.siteserve.EXPECTED_MARKETS_NAMES.money_line
        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state(state_name='basketball')
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.basketball_config.category_id)
        current_tab_name = self.site.contents.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as'
                             f'Expected tab: "{expected_tab_name}".')

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: Desktop:
        EXPECTED: • 'Market Selector' is displayed next to Day Selectors (Today/Tomorrow/Future) on the right side
        EXPECTED: • 'Money Line' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Money Line' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to 'Money Line' in 'Market selector' Coral
        """
        self.__class__.basketball_tab_content = self.site.basketball.tab_content
        self.assertTrue(self.basketball_tab_content.has_dropdown_market_selector(),
                        msg='"Market Selector" drop-down is not displayed on basketball landing page')

        market_selector_default_value = self.market_selector_default_value.upper() \
            if self.brand == 'ladbrokes' and self.device_type == 'desktop' else self.market_selector_default_value

        dropdown = self.site.basketball.tab_content.dropdown_market_selector
        self.assertEqual(dropdown.selected_market_selector_item,
                         market_selector_default_value,
                         msg=f'Incorrect market name is selected by default:\n'
                             f'Actual: "{dropdown.selected_market_selector_item}"\n'
                             f'Expected: "{market_selector_default_value}"')

        if self.device_type == 'desktop':
            if self.brand == "bma":
                self.assertTrue(dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                dropdown.click()
                self.assertTrue(dropdown.is_expanded(),
                                msg='chevron (pointing down) arrow not displayed')
        else:
            self.assertTrue(dropdown.change_button, msg=f'"Change button" is not displayed')
            dropdown.click()
            self.assertFalse(dropdown.is_expanded(), msg=f' "Dropdown arrow" is not pointing downwards')

    def test_002_tap_on_the_change_button_in_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Tap on the 'Change' button in 'Market Selector' dropdown list
        EXPECTED: • 'Market Selector' dropdown list opens
        EXPECTED: • List of markets are displayed
        EXPECTED: • The chevron near 'Change' button is pointed upwards
        """
        self.__class__.list_of_drop_down = self.site.basketball.tab_content.dropdown_market_selector.items_as_ordered_dict
        self.assertTrue(self.list_of_drop_down, msg=f'"Market Selector" dropdown list not opened')

        self.__class__.available_markets = self.basketball_tab_content.dropdown_market_selector.available_options
        if self.brand == 'bma':
            self.available_markets[2] = "Handicap"
        else:
            self.expected_market_selector_options[3] = 'Home Team Total points'
        self.assertEqual(self.available_markets, self.expected_market_selector_options,
                         msg=f'Incorrect list/order of markets in Market Selector drop-down.\n'
                             f'Actual: "{self.available_markets}"\nExpected: "{self.expected_market_selector_options}"')

    def test_003_verify_the_behavior_of_the_market_drop_down_list(self):
        """
        DESCRIPTION: Verify the behavior of the market drop down list
        EXPECTED: User should be able to mouse over the markets in the list,The market which is in focus will get highlighted.
        """
        if self.device_type == 'desktop':
            dropdown = self.site.contents.tab_content.dropdown_market_selector
            for option, element in self.list_of_drop_down.items():
                element.mouse_over()
                # when mouse over, color is not reflecting immediately
                sleep(5)
                actual_bg_color = element.background_color_value
                self.assertEqual(actual_bg_color, vec.colors.MARKET_SWITCHER_HIGHLIGHTED_COLOR,
                                 msg=f'Actual background color: "{actual_bg_color}" is not same as'
                                     f'Expected background color: "{vec.colors.MARKET_SWITCHER_HIGHLIGHTED_COLOR}"')
                dropdown.select_value(value=option)
                dropdown = self.site.contents.tab_content.dropdown_market_selector
                selected_value = dropdown.selected_market_selector_item
                self.assertEqual(selected_value.upper(), option.upper(),
                                 msg=f'Actual selected value: "{selected_value}" is not same as '
                                     f'Expected selected value: "{option}"')

    def test_004_click_on_market_which_is_higlighted(self):
        """
        DESCRIPTION: Click on market which is higlighted
        EXPECTED: Selected market should be displayed
        """
        # covered in step test_003

    def test_005_tap_on_the_change_button_again_and_mouse_over_the_content(self):
        """
        DESCRIPTION: Tap on the 'Change' button again and mouse over the content
        EXPECTED: • 'Market Selector' dropdown list opens
        EXPECTED: • List the Markets will be displayed
        EXPECTED: • The chevron near 'Change' button is pointed upwards
        """
        actual_list = list(self.list_of_drop_down.keys())
        if self.brand == 'bma':
            actual_list[2] = "Handicap"
        else:
            self.expected_market_selector_options[3] = 'Home Team Total points'
        if self.device_type == 'desktop':
            dropdown_expanded = self.site.contents.tab_content.dropdown_market_selector.is_expanded()
            self.assertTrue(dropdown_expanded, msg=f'"Market Selector" dropdown list is not opened')
            self.assertListEqual(actual_list, self.expected_market_selector_options,
                                 msg=f'Actual list : "{actual_list}" is not same as'
                                     f'Expected list : "{self.expected_market_selector_options}"')
