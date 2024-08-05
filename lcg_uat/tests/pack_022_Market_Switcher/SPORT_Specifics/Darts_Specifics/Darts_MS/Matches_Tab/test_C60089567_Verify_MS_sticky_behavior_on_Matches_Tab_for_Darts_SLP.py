import pytest
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Events with specific markets cannot created in Prod/Beta
@pytest.mark.market_switcher
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C60089567_Verify_MS_sticky_behavior_on_Matches_Tab_for_Darts_SLP(BaseSportTest):
    """
    TR_ID: C60089567
    NAME: Verify MS sticky behavior on Matches Tab for Darts SLP
    DESCRIPTION: This test case verifies 'Market Selector' sticky behavior on Darts landing page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Darts landing page -> 'Matches' tab
    PRECONDITIONS: 3. Make sure that 'Market Selector' is present on the page
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: |Match Betting(WW/WDW)| - "Match Result"
    PRECONDITIONS: |Leg Handicap| - "Handicap"
    PRECONDITIONS: |Total 180s Over/Under (Over/Under)| - "Total 180s"
    PRECONDITIONS: |Most 180s (WDW)| - "Most 180s"
    """
    keep_browser_open = True
    market_selector_options = [('match_handicap',), ('total_180s_over_under',), ('most_180s',)]

    def verify_sticky_behavior(self, market):
        is_sticky = self.darts_tab_content.is_market_selector_sticky
        self.assertTrue(is_sticky, msg='"Market Selector" is not sticky on Darts Competition page ')
        drop_down_list = self.darts_tab_content.dropdown_market_selector
        drop_down_list.items_as_ordered_dict.get(market).click()
        selected_market = self.site.sports_page.tab_content.dropdown_market_selector.value
        self.assertEqual(selected_market, market,
                         msg=f'Actual Market: "{selected_market}" is not same as the'
                             f'Expected Market: "{market}"')

    def test_000_precondition(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Go to the Dart Landing page -> 'Matches' tab
        PRECONDITIONS: 3. Make sure that 'Market Selector' is present on the page
        """
        market_switcher_status = \
            self.cms_config.verify_and_update_market_switcher_status(sport_name='darts', status=True)
        self.assertTrue(market_switcher_status, msg=f'The "Darts" sport is disabled in CMS')
        all_sport_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports', status=True)
        self.assertTrue(all_sport_status, msg='"All Sport" Market switcher is disabled')
        self.cms_config.verify_and_update_sport_config(self.ob_config.backend.ti.darts.category_id,
                                                       disp_sort_names='MR,HL,WH,HH',
                                                       primary_markets='|Match Betting|,|Total 180s Over/Under|,'
                                                                       '|Most 180s|,|Leg Handicap|,|Leg Winner|,'
                                                                       '|Match Betting Head/Head|,|Match Handicap|')
        self.ob_config.add_darts_event_to_darts_all_darts(markets=self.market_selector_options)
        self.navigate_to_page(name='sport/darts')
        self.site.wait_content_state(state_name='Darts')
        self.site.darts.tabs_menu.click_button(self.expected_sport_tabs.matches)
        current_tab_name = self.site.sports_page.tabs_menu.current
        self.assertEqual(current_tab_name, self.expected_sport_tabs.matches,
                         msg=f'Actual Tab: "{current_tab_name}" is not same as the'
                             f'Expected Tab: "{self.expected_sport_tabs.matches}"')
        self.__class__.darts_tab_content = self.site.sports_page.tab_content
        self.assertTrue(self.darts_tab_content.has_dropdown_market_selector(),
                        msg='"Market Selector" drop-down is not displayed on Darts landing page')

    def test_001_verify_that_market_selector_is_sticky_when_scrolling_the_page_down(self):
        """
        DESCRIPTION: Verify that 'Market Selector' is sticky when scrolling the page down
        EXPECTED: Tablet/Mobile:
        EXPECTED: • 'Market Selector' is sticky. It remains at the top of the scrolling page
        EXPECTED: • Market selector functionality remains the same
        EXPECTED: **Note:**
        EXPECTED: For the Desktop 'Market Selector' is NOT sticky. It becomes hidden together with Date Selector panel
        """
        self.site.contents.scroll_to_bottom()
        self.__class__.markets = list(self.darts_tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        self.assertTrue(self.markets, msg='"Markets" are not available in the market switcher drop-down')
        self.verify_sticky_behavior(self.markets[1])

    def test_002_verify_that_market_selector_is_sticky_when_scrolling_the_page_up(self):
        """
        DESCRIPTION: Verify that 'Market Selector' is sticky when scrolling the page up
        EXPECTED: Tablet/Mobile:
        EXPECTED: • 'Market Selector' is sticky. It remains at the top of the scrolling page
        EXPECTED: • Market selector functionality remains the same
        EXPECTED: **Note:**
        EXPECTED: For the Desktop 'Market Selector' is NOT sticky. It becomes hidden together with Date Selector panel
        """
        self.site.contents.scroll_to_top()
        self.verify_sticky_behavior(self.markets[2])
