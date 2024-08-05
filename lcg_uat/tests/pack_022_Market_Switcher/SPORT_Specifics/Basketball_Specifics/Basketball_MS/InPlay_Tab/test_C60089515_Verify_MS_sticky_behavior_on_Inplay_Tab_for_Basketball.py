import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.medium
@pytest.mark.in_play
# @pytest.mark.prod #Events with specific markets cannot be created in Prod/Beta
@pytest.mark.market_switcher
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C60089515_Verify_MS_sticky_behavior_on_Inplay_Tab_for_Basketball(BaseSportTest):
    """
    TR_ID: C60089515
    NAME: Verify MS sticky behavior on Inplay Tab for Basketball
    DESCRIPTION: This test case verifies the sticky behavior of 'Market Selector'
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the Basketball -> In-Play page and Inplay from Sports Ribbon menu -> Basketball
    PRECONDITIONS: **Note:**
    PRECONDITIONS: Be aware that the Market selector becomes unsticky when the user reaches the Upcoming section
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB using the following market Templates:
    PRECONDITIONS: |Money Line (WW)| - "Money Line"
    PRECONDITIONS: |Total Points (Over/Under)| - "Total Points"
    PRECONDITIONS: |Handicap 2-way (Handicap)| - "Handicap"
    PRECONDITIONS: |Half Total Points (Over/Under)| - "Current Half Total Points"
    PRECONDITIONS: |Quarter Total Points (Over/Under)| - "Current Quarter Total Points"
    PRECONDITIONS: 2) Be aware that market switching using 'Market Selector' is applied only for events from the 'Live Now' section
    """
    keep_browser_open = True

    event_markets = [
        ('total_points',),
        ('handicap_2_way',),
        ('half_total_points',),
        ('quarter_total_points',)]

    def verify_sticky_behavior(self, market):
        is_sticky = self.basketball_tab_content.is_market_selector_sticky
        self.assertTrue(is_sticky, msg='"Market Selector" is not sticky in Basketball Sport Page')
        drop_down_list = self.basketball_tab_content.dropdown_market_selector
        drop_down_list.items_as_ordered_dict.get(market).click()
        selected_market = self.basketball_tab_content.dropdown_market_selector.value
        self.assertEqual(selected_market, market, msg=f'Actual Market: "{selected_market}" is not same as'
                                                      f'Expected Market: "{market}", Market selector functionality is not same')

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
        start_time = self.get_date_time_formatted_string(seconds=20)
        self.cms_config.verify_and_update_sport_config(
            sport_category_id=self.ob_config.backend.ti.basketball.category_id,
            disp_sort_names='HL,WH,HH',
            primary_markets='|Money Line|,|Total Points|,'
                            '|Home team total points|,|Away team total points|,'
                            '|Half Total Points|,|Quarter Total Points|,'
                            '|Handicap 2-way|')
        self.ob_config.add_basketball_event_to_us_league(is_live=True, markets=self.event_markets, start_time=start_time)
        self.__class__.market_selector_default_value = vec.siteserve.EXPECTED_MARKETS_NAMES.money_line
        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state(state_name='basketball')
        expected_tab = self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play
        self.site.basketball.tabs_menu.click_button(self.expected_sport_tabs.in_play)
        expected_tab_name = self.get_sport_tab_name(expected_tab, self.ob_config.basketball_config.category_id)
        current_tab_name = self.site.contents.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as'
                             f'Expected tab: "{expected_tab_name}".')
        self.__class__.basketball_tab_content = self.site.basketball.tab_content
        self.assertTrue(self.basketball_tab_content.has_dropdown_market_selector(),
                        msg='"Market Selector" drop-down is not displayed on basketball landing page')

    def test_001_verify_that_market_selector_is_sticky_when_scrolling_the_page_down(self):
        """
        DESCRIPTION: Verify that 'Market Selector' is sticky when scrolling the page down
        EXPECTED: Mobile/Tablet:
        EXPECTED: • Market selector remains at the top of the scrolling page
        EXPECTED: • Market selector functionality remains the same
        EXPECTED: **Note:**
        EXPECTED: For the Desktop 'Market Selector' is NOT sticky. It becomes hidden together with Date Selector panel
        """
        self.site.contents.scroll_to_bottom()
        self.__class__.markets = list(
            self.basketball_tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        self.assertTrue(self.markets, msg='Markets not found')
        self.verify_sticky_behavior(self.markets[1])

    def test_002_verify_that_market_selector_is_sticky_when_scrolling_the_page_up(self):
        """
        DESCRIPTION: Verify that 'Market Selector' is sticky when scrolling the page up
        EXPECTED: • Market selector remains at the top of the scrolling page
        EXPECTED: • Market selector functionality remains the same
        EXPECTED: **Note:**
        EXPECTED: For the Desktop 'Market Selector' is NOT sticky. It becomes hidden together with Date Selector panel
        """
        self.site.contents.scroll_to_top()
        self.verify_sticky_behavior(self.markets[2])
