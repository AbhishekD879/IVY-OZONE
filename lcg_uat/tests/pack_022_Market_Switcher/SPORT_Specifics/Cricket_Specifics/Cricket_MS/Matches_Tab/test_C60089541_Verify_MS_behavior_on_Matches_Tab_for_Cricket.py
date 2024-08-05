import pytest
from time import sleep
from voltron.environments import constants as vec
from tests.base_test import vtest
from tests.Common import Common
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
class Test_C60089541_Verify_MS_behavior_on_Matches_Tab_for_Cricket(Common):
    """
    TR_ID: C60089541
    NAME: Verify MS behavior on Matches Tab for Cricket
    DESCRIPTION: This test case verifies behavior of 'Market Selector' dropdown list
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Cricket landing page -> 'Matches' tab
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: |Match Betting (WDW & WW)| - "Match Result"
    PRECONDITIONS: |Total Sixes (Over/Under)| - "Total Sixes"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    event_markets = [
        ('total_sixes',)]

    def test_000_preconditions(self):
        """
            PRECONDITIONS: 1. Load the app
            PRECONDITIONS: 2. Go to the Cricket landing page -> 'Matches' tab
            PRECONDITIONS: 3. Make sure that 'Market Selector' is present on the page
            """
        all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                     status=True)
        self.assertTrue(all_sports_status, msg='"All Sports" is disabled')
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='cricket',
                                                                                          status=True)
        self.assertTrue(market_switcher_status, msg='Market switcher is disabled for Cricket sport')
        self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.cricket_config.category_id,
                                                       disp_sort_names='MR,HH,WH,HL',
                                                       primary_markets='|Match Betting|,|Match Betting Head/Head|,|Total Sixes|,|Team Runs (Main)|,|Next Over Runs (Main)|,|Runs At Fall Of Next Wicket|')
        self.ob_config.add_autotest_cricket_event(markets=self.event_markets)
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.cricket_config.category_id)
        self.site.wait_content_state('Homepage')
        self.navigate_to_page(name='sport/cricket')
        self.site.wait_content_state(state_name='cricket')
        self.site.sports_page.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
        current_tab_name = self.site.competition_league.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab is "{current_tab_name}", instead of "{expected_tab_name}"')

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: Desktop:
        EXPECTED: • 'Market Selector' is displayed next to Day Selectors (Today/Tomorrow/Future) on the right side
        EXPECTED: • 'Match Result' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Match Result' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to 'Match Result' in 'Market selector' Coral
        """
        has_market_selector = self.site.sports_page.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Cricket Sport')
        dropdown = self.site.sports_page.tab_content.dropdown_market_selector
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
        selected_value = self.site.sports_page.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper(),
                         msg=f'Actual selected value: "{selected_value.upper()}" is not same as'
                             f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper()}"')

    def test_002_tap_on_the_change_button_in_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Tap on the 'Change' button in 'Market Selector' dropdown list
        EXPECTED: • 'Market Selector' dropdown list opens
        EXPECTED: • List of markets are displayed
        EXPECTED: • The chevron near 'Change' button is pointed upwards
        """
        self.__class__.list_of_drop_down = self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict
        self.assertTrue(self.list_of_drop_down, msg=f'"Market Selector" dropdown list not opened')
        self.__class__.expected_list = [vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.title(),
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.total_sixes.title()]
        actual_list = list(self.list_of_drop_down.keys())
        self.assertListEqual(actual_list, self.expected_list,
                             msg=f'Actual list : "{actual_list}" is not same as '
                                 f'Expected list : "{self.expected_list}"')

    def test_003_verify_the_behavior_of_the_market_drop_down_list(self):
        """
        DESCRIPTION: Verify the behavior of the market drop down list
        EXPECTED: User should be able to mouse over the markets in the list,The market which is in focus will get highlighted.
        """
        if self.device_type == 'desktop':
            dropdown = self.site.sports_page.tab_content.dropdown_market_selector
            for option, element in self.list_of_drop_down.items():
                element.mouse_over()
                # when mouse over, color is not reflecting immediately
                sleep(2)
                actual_bg_color = element.background_color_value
                self.assertEqual(actual_bg_color, vec.colors.MARKET_SWITCHER_HIGHLIGHTED_COLOR,
                                 msg=f'Actual background color: "{actual_bg_color}" is not same as'
                                     f'Expected background color: "{vec.colors.MARKET_SWITCHER_HIGHLIGHTED_COLOR}"')
                dropdown.select_value(value=option)
                dropdown = self.site.sports_page.tab_content.dropdown_market_selector
                selected_value = dropdown.selected_market_selector_item
                self.assertEqual(selected_value.upper(), option.upper(),
                                 msg=f'Actual selected value: "{selected_value}" is not same as '
                                     f'Expected selected value: "{option}"')

    def test_004_click_on_the_market_which_is_highlighted(self):
        """
        DESCRIPTION: Click on the market which is highlighted
        EXPECTED: Highlighted market should be displayed
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
            dropdown_expanded = self.site.sports_page.tab_content.dropdown_market_selector.is_expanded()
            self.assertTrue(dropdown_expanded, msg=f'"Market Selector" dropdown list is not opened')
            actual_list = list(self.list_of_drop_down.keys())
            self.assertListEqual(actual_list, self.expected_list, msg=f'Actual list : "{actual_list}" is not same as'
                                                                      f'Expected list : "{self.expected_list}"')