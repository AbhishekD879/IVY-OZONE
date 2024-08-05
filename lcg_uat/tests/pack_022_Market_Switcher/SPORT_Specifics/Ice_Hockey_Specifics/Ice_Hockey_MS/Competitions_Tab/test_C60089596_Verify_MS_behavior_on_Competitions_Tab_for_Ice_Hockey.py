import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Events with specific markets cannot created in Prod/Beta
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.market_switcher
@pytest.mark.desktop
@vtest
class Test_C60089596_Verify_MS_behavior_on_Competitions_Tab_for_Ice_Hockey(BaseSportTest):
    """
    TR_ID: C60089596
    NAME: Verify MS behavior on Competitions Tab for Ice Hockey
    DESCRIPTION: This test case verifies the behavior of 'Market Selector' dropdown list in competition page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Money Line|,|60 Minute betting|,|Total Goals 2-way|,|Puck Line|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: Load the app
    PRECONDITIONS: Go to the Ice Hockey Landing Page -> 'Click on Competition Tab'
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: *|Money Line (WW)|- Money Line
    PRECONDITIONS: *|60 Minutes Betting (WDW)|- 60 Minute Betting
    PRECONDITIONS: *|Puck Line (Handicap)| - "Puck Line"
    PRECONDITIONS: *|Total Goals 2-way (Over/Under)| - "Total Goals 2-way"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    expected_market_selector_options = [vec.siteserve.EXPECTED_MARKETS_NAMES.money_line,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.sixty_minutes_betting,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.puck_line,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_2_way
                                        ]

    event_markets = [
        ('sixty_minutes_betting',),
        ('puck_line',),
        ('total_goals_2_way',)
    ]

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Ice Hockey event with scores
        EXPECTED: Event is successfully created
        """
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='icehockey',
                                                                                          status=True)
        self.assertTrue(market_switcher_status, msg='"Market Switcher" is disabled for IceHockey sport')
        all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                     status=True)
        self.assertTrue(all_sports_status, msg='"All Sports" is disabled')
        self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.backend.ti.ice_hockey.category_id,
                                                       disp_sort_names='HH,WH,MR,HL',
                                                       primary_markets='|Money Line|,|Total Goals 2-way|,|Puck Line|,|60 Minutes Betting|')
        self.ob_config.add_ice_hockey_event_to_ice_hockey_usa(markets=self.event_markets)
        self.__class__.market_selector_default_value = vec.siteserve.EXPECTED_MARKETS_NAMES.money_line

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: • Market Selector' is displayed next to (Matches/Outrights) on the right side
        EXPECTED: • 'Money Line' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Money Line' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to 'Money Line' in 'Market selector' Coral
        """
        self.navigate_to_page(name='sport/ice-hockey')
        self.site.wait_content_state(state_name='IceHockey')
        self.site.ice_hockey.tabs_menu.click_button(self.expected_sport_tabs.competitions)
        current_tab_name = self.site.ice_hockey.tabs_menu.current
        self.assertEqual(current_tab_name, self.expected_sport_tabs.competitions,
                         msg=f'Expected tab: "{current_tab_name}", Actual Tab: "{self.expected_sport_tabs.competitions}"')
        self.__class__.ice_hockey_tab_content = self.site.ice_hockey.tab_content
        self.assertTrue(self.ice_hockey_tab_content.has_dropdown_market_selector(),
                        msg='"Market Selector" drop-down is not displayed on IceHockey landing page')
        market_selector_default_value = self.market_selector_default_value.upper() \
            if self.brand == 'ladbrokes' and self.device_type == 'desktop' else self.market_selector_default_value
        self.assertEqual(self.ice_hockey_tab_content.dropdown_market_selector.selected_market_selector_item,
                         market_selector_default_value,
                         msg=f'Incorrect market name is selected by default:\n'
                             f'Actual: "{self.ice_hockey_tab_content.dropdown_market_selector.selected_market_selector_item}"\n'
                             f'Expected: "{market_selector_default_value}"')
        dropdown = self.ice_hockey_tab_content.dropdown_market_selector
        if self.brand == 'bma' and self.device_type == 'desktop':
            self.assertTrue(dropdown.has_up_arrow, msg='Market selector up arrow is not displayed')
            self.assertTrue(dropdown.has_down_arrow, msg='Market selector down arrow is not displayed')
        elif self.device_type == 'mobile' or self.brand == 'ladbrokes':
            dropdown.click()
            wait_for_result(lambda: dropdown.is_expanded() is not True,
                            name=f'Market switcher expanded/collapsed',
                            timeout=5)
            self.assertFalse(dropdown.is_expanded(), msg=f'dropdown arrow is not pointing downwards')

    def test_002_click_on_the_change_button_in_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Click on the 'Change' button in 'Market Selector' dropdown list
        EXPECTED: • 'Market Selector' dropdown list opens
        EXPECTED: • List of markets are displayed
        EXPECTED: • The chevron near 'Change' button is pointed upwards
        """
        self.__class__.available_markets = self.ice_hockey_tab_content.dropdown_market_selector.available_options
        self.assertListEqual(sorted(self.available_markets), sorted(self.expected_market_selector_options),
                             msg=f'Incorrect list/order of markets in Market Selector drop-down.\n'
                                 f'Actual: "{self.available_markets}"\nExpected: "{self.expected_market_selector_options}"')
        dropdown = self.site.contents.tab_content.dropdown_market_selector
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(dropdown.change_button, msg=f'"Change button" is not displayed')
            dropdown.click()
            self.assertFalse(dropdown.is_expanded(), msg=f'dropdown arrow is not pointing upwards')

    def test_003_verify_the_behavior_of_the_market_drop_down_list(self):
        """
        DESCRIPTION: Verify the behavior of the market drop down list
        EXPECTED: User should be able to mouse over the markets in the list,The market which is in focus will get highlighted.
        """
        drop_down = self.ice_hockey_tab_content.dropdown_market_selector
        list_of_drop_down = drop_down.items_as_ordered_dict
        result = wait_for_result(lambda: drop_down.is_expanded(),
                                 name='Market switcher to be expanded',
                                 timeout=5)
        if not result:
            drop_down.expand()
        if self.device_type == 'desktop':
            for element in list(list_of_drop_down.values()):
                element.mouse_over()
                # when mouse over, color is not reflecting immediately
                sleep(1)
                actual_bg_color = element.background_color_value
                self.assertEqual(actual_bg_color, vec.colors.MARKET_SWITCHER_HIGHLIGHTED_COLOR,
                                 msg=f'Actual background color: "{actual_bg_color}" is not same as'
                                     f'Expected background color: "{vec.colors.MARKET_SWITCHER_HIGHLIGHTED_COLOR}"')

    def test_004_click_on_market_which_is_highlighted(self):
        """
        DESCRIPTION: Click on market which is highlighted
        EXPECTED: Selected market should be displayed
        """
        options = self.ice_hockey_tab_content.dropdown_market_selector
        for market in self.available_markets:
            options.expand()
            options.value = market
            wait_for_result(lambda: options.selected_market_selector_item == market,
                            name=f'Current selector market to be equal '
                                 f'to expected market "{market}"',
                            timeout=5)
            if self.brand == 'ladbrokes' and self.device_type == 'desktop':
                market = market.upper()
            self.assertEqual(options.selected_market_selector_item,
                             market, msg=f'Incorrect market name is selected by default: '
                                         f'Actual: "{options.selected_market_selector_item}" Expected: "{market}"')

    def test_005_click_on_the_change_button_again_and_mouse_over_the_content(self):
        """
        DESCRIPTION: Click on the 'Change' button again and mouse over the content
        EXPECTED: • 'Market Selector' dropdown list opens
        EXPECTED: • List the Markets will be displayed
        EXPECTED: • The chevron near 'Change' button is pointed to upwards
        """
        self.ice_hockey_tab_content.dropdown_market_selector.expand()
        self.test_002_click_on_the_change_button_in_market_selector_dropdown_list()
