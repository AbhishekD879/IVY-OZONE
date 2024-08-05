import pytest
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # #Events with specific markets cannot created in Prod/Beta
@pytest.mark.mobile_only
@pytest.mark.market_switcher
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C60089564_Verify_MS_sticky_behavior_on_Competitions_Tab_for_Golf(BaseSportTest):
    """
    TR_ID: C60089564
    NAME: Verify MS sticky behavior on Competitions Tab for Golf
    DESCRIPTION: This test case verifies 'Market Selector' sticky behavior on Golf Competitions page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) Is Outright sport should be ‘enabled’ and Odds card Header type should be ‘None’
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Golf Competitions page -> 'Matches' tab
    PRECONDITIONS: 3. Make sure that 'Market Selector' is present on the page
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: |3 Ball Betting| - "3 Ball Betting"
    PRECONDITIONS: |2 Ball Betting| - "2 Ball Betting"
    """
    keep_browser_open = True
    event_markets = [('2_ball_betting',)]

    def verify_sticky_behavior(self, market):
        is_sticky = self.golf_tab_content.is_market_selector_sticky
        self.assertTrue(is_sticky, msg='"Market Selector" is not sticky in Golf league')
        drop_down_list = self.golf_tab_content.dropdown_market_selector
        drop_down_list.items_as_ordered_dict.get(market).click()
        selected_market = self.golf_tab_content.dropdown_market_selector.value
        self.assertEqual(selected_market, market, msg=f'Actual Market: "{selected_market}" is not same as'
                                                      f'Expected Market: "{market}", Market selector functionality is not same')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Go to the Golf Landing page -> 'Competition' tab
        PRECONDITIONS: 3. Make sure that 'Market Selector' is present on the page
        """
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='golf',
                                                                                          status=True)
        self.assertTrue(market_switcher_status, msg='Market switcher is disabled for Golf sport')
        all_sport_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                             status=True)
        self.assertTrue(all_sport_switcher_status, msg='"All Sports" is disabled')
        self.ob_config.add_golf_event_to_golf_all_golf(markets=self.event_markets)

        self.navigate_to_page(name='sport/golf')
        self.site.wait_content_state('golf')
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                    self.ob_config.golf_config.category_id)
        self.site.contents.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
        current_tab_name = self.site.contents.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab is "{current_tab_name}", instead of "{expected_tab_name}"')
        self.__class__.golf_tab_content = self.site.competition_league.tab_content
        has_market_selector = self.golf_tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Golf')

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
        self.__class__.markets = list(
            self.golf_tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        self.assertTrue(self.markets, msg='Markets not found')
        self.verify_sticky_behavior(self.markets[0])

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
        self.verify_sticky_behavior(self.markets[1])
