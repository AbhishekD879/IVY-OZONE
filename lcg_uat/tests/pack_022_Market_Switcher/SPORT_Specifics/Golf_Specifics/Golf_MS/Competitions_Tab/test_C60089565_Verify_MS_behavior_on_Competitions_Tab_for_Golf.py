import pytest
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Events with specific markets cannot be created in Prod/Beta
@pytest.mark.desktop
@pytest.mark.market_switcher
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C60089565_Verify_MS_behavior_on_Competitions_Tab_for_Golf(Common):
    """
    TR_ID: C60089565
    NAME: Verify MS behavior on Competitions Tab for Golf
    DESCRIPTION: This test case verifies the behavior of 'Market Selector' dropdown list
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) Is Outright sport should be ‘enabled’ and Odds card Header type should be ‘None’
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Golf Competitions page -> 'Matches' tab
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |3 Ball Betting| - "3 Ball Betting"
    PRECONDITIONS: * |2 Ball Betting| - "2 Ball Betting"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    event_markets = [('2_ball_betting',)]

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events with required markets
        DESCRIPTION: Navigate to Golf page
        EXPECTED: Event is successfully created
        """
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='golf',
                                                                                          status=True)
        self.assertTrue(market_switcher_status, msg='Market switcher is disabled for Golf sport')
        all_sport_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                             status=True)
        self.assertTrue(all_sport_switcher_status, msg='"All Sports" is disabled')
        self.ob_config.add_golf_event_to_golf_all_golf(markets=self.event_markets)
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                    self.ob_config.golf_config.category_id)
        self.navigate_to_page(name='sport/golf')
        self.site.wait_content_state('golf')
        self.site.contents.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
        self.site.wait_content_state_changed(timeout=10)
        current_tab = self.site.contents.tabs_menu.current
        self.assertEqual(expected_tab_name, current_tab, msg=f'Actual tab: "{current_tab}" is not same as '
                                                             f'Expected tab: "{expected_tab_name}"')

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: Desktop:
        EXPECTED: • 'Market Selector' is displayed next to Day Selectors (Today/Tomorrow/Future) on the right side
        EXPECTED: • '3 Ball Betting' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to '3 Ball Betting' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to '3 Ball Betting' in 'Market selector' Coral
        """
        has_market_selector = self.site.competition_league.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Golf Leauge')
        dropdown = self.site.competition_league.tab_content.dropdown_market_selector
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(dropdown.change_button, msg=f'"Change button" is not displayed')
            dropdown.click()
            self.assertFalse(dropdown.is_expanded(), msg=f'"Dropdown arrow" is not pointing downwards')
        else:
            if self.brand == 'bma':
                self.assertTrue(dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                dropdown.click()
                self.assertFalse(dropdown.is_expanded(), msg=f' "Dropdown Arrow" is not pointing downwards')
        selected_value = self.site.competition_league.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.two_ball_betting.upper(),
                         msg=f'Actual selected value: "{selected_value}" is not same as'
                             f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.two_ball_betting}"')

    def test_002_tap_on_the_change_button_in_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Tap on the 'Change' button in 'Market Selector' dropdown list
        EXPECTED: • 'Market Selector' dropdown list opens
        EXPECTED: • List of markets are displayed
        EXPECTED: • The chevron near 'Change' button is pointed upwards
        """
        self.__class__.list_of_drop_down = self.site.contents.tab_content.dropdown_market_selector.items_as_ordered_dict
        self.assertTrue(self.list_of_drop_down, msg=f'"Market Selector" dropdown list not opened')
        self.__class__.expected_list = [vec.siteserve.EXPECTED_MARKETS_NAMES.three_ball_betting,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.two_ball_betting]
        actual_list = list(self.list_of_drop_down.keys())
        self.assertListEqual(actual_list, self.expected_list,
                             msg=f'Actual list : "{actual_list}" is not same as '
                                 f'Expected list : "{self.expected_list}"')

    def test_003_verify_the_behavior_of_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify the behavior of 'Market Selector' dropdown list
        EXPECTED: User should be able to mouse overthe markets in the list,The market which is in focus will get highlighted.
        """
        if self.device_type == 'desktop':
            dropdown = self.site.contents.tab_content.dropdown_market_selector
            for option, element in self.list_of_drop_down.items():
                element.mouse_over()
                # when mouse over, color is not reflecting immediately
                sleep(2)
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

    def test_004_click_on_the_market_which_is_higlighted(self):
        """
        DESCRIPTION: Click on the market which is higlighted
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
        if self.device_type == 'desktop':
            dropdown_expanded = self.site.contents.tab_content.dropdown_market_selector.is_expanded()
            self.assertTrue(dropdown_expanded, msg=f'"Market Selector" dropdown list is not opened')
            actual_list = list(self.list_of_drop_down.keys())
            self.assertListEqual(actual_list, self.expected_list, msg=f'Actual list : "{actual_list}" is not same as'
                                                                      f'Expected list : "{self.expected_list}"')
