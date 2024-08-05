import pytest
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Events with specific markets cannot created in Prod/Beta
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.market_switcher
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C60089556_Verify_MS_behavior_on_Matches_Tab_for_Boxing(Common):
    """
    TR_ID: C60089556
    NAME: Verify MS behavior on Matches Tab for Boxing
    DESCRIPTION: This test case verifies the behavior of 'Market Selector' dropdown list
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Boxing  landing page -> 'Matches' tab
    PRECONDITIONS: Note:
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Fight Betting(WDW)| - "Fight Betting"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    expected_market = [vec.siteserve.EXPECTED_MARKETS_NAMES.fight_betting.title()]

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Go to the Boxing landing page -> 'Matches' tab
        """
        all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                     status=True)
        self.assertTrue(all_sports_status, msg='"All Sports" is disabled')
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='boxing',
                                                                                          status=True)
        self.assertTrue(market_switcher_status, msg='Market switcher is disabled for Boxing sport')
        self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.boxing_config.category_id,
                                                       disp_sort_names='MR',
                                                       primary_markets='|Fight Betting|')
        self.ob_config.add_autotest_boxing_event()
        self.navigate_to_page(name='sport/boxing')
        self.site.wait_content_state_changed()
        current_tab_name = self.site.boxing.tabs_menu.current
        self.assertEqual(current_tab_name, vec.sb.TABS_NAME_FIGHTS.upper(),
                         msg=f'Default tab is "{current_tab_name}",instead of "{vec.sb.TABS_NAME_FIGHTS}"')
        self.__class__.boxing = self.site.boxing.tab_content

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: Desktop:
        EXPECTED: • 'Market Selector' is displayed next to Day Selectors (Today/Tomorrow/Future) on the right side
        EXPECTED: • 'Fight Betting' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Fight Betting' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to 'Fight Betting' in 'Market selector' Coral
        """
        has_market_selector = self.site.boxing.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Boxing')
        dropdown = self.site.boxing.tab_content.dropdown_market_selector
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(dropdown.change_button, msg=f'"Change button" is not displayed')
            dropdown.click()
            self.assertFalse(dropdown.is_expanded(), msg=f'dropdown arrow is not pointing downwards')
        else:
            if self.brand == 'bma':
                self.assertTrue(dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                dropdown.click()
                wait_for_result(lambda: dropdown.is_expanded() is not True,
                                name=f'Market switcher expanded/collapsed',
                                timeout=5)
                self.assertFalse(dropdown.is_expanded(), msg=f'dropdown arrow is not pointing downwards')
        selected_value = self.site.boxing.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.fight_betting.upper(),
                         msg=f'Actual selected value: "{selected_value.upper()}" is not same as'
                             f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.fight_betting.upper()}"')

    def test_002_tap_on_the_change_button_in_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Tap on the 'Change' button in 'Market Selector' dropdown list
        EXPECTED: • 'Market Selector' dropdown list opens
        EXPECTED: • List of markets are displayed
        EXPECTED: • The chevron near 'Change' button is pointed upwards
        """
        self.__class__.list_of_drop_down = self.site.boxing.tab_content.dropdown_market_selector.items_as_ordered_dict
        self.assertTrue(self.list_of_drop_down, msg=f'"Market Selector" dropdown list not opened')
        actual_market = list(self.list_of_drop_down.keys())
        self.assertEqual(actual_market, self.expected_market,
                         msg=f'Actual list : "{actual_market}" is not same as '
                             f'Expected list : "{self.expected_market}"')

    def test_003_verify_the_behavior_of_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify the behavior of 'Market Selector' dropdown list
        EXPECTED: User should be able to mouse overthe markets in the list,The market which is in focus will get highlighted.
        """
        if self.device_type == 'desktop':
            dropdown = self.site.boxing.tab_content.dropdown_market_selector
            for option, element in self.list_of_drop_down.items():
                element.mouse_over()
                # when mouse over, color is not reflecting immediately
                sleep(2)
                actual_bg_color = element.background_color_value
                self.assertEqual(actual_bg_color, vec.colors.MARKET_SWITCHER_HIGHLIGHTED_COLOR,
                                 msg=f'Actual background color: "{actual_bg_color}" is not same as'
                                     f'Expected background color: "{vec.colors.MARKET_SWITCHER_HIGHLIGHTED_COLOR}"')
                dropdown.select_value(value=option)
                dropdown = self.site.boxing.tab_content.dropdown_market_selector
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
        if self.device_type == 'desktop':
            dropdown_expanded = self.site.boxing.tab_content.dropdown_market_selector.is_expanded()
            self.assertTrue(dropdown_expanded, msg=f'"Market Selector" dropdown list is not opened')
            actual_market = list(self.list_of_drop_down.keys())
            self.assertEqual(actual_market, self.expected_market,
                             msg=f'Actual list : "{actual_market}" is not same as'
                                 f'Expected list : "{self.expected_market}"')
