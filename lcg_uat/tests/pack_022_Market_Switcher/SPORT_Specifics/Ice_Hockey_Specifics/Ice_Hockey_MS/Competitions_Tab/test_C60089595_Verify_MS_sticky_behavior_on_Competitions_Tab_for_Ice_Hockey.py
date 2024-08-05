import pytest
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Events with specific markets cannot created in Prod/Beta
@pytest.mark.medium
@pytest.mark.sports
@vtest
@pytest.mark.market_switcher
@pytest.mark.mobile_only
class Test_C60089595_Verify_MS_sticky_behavior_on_Competitions_Tab_for_Ice_Hockey(BaseSportTest):
    """
    TR_ID: C60089595
    NAME: Verify MS sticky behavior on Competitions Tab for Ice Hockey
    DESCRIPTION: This test case verifies 'Market Selector' sticky behavior on Ice Hockey Competition page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Money Line|,|Puck line|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Ice Hockey sport -> 'Competition' tab
    PRECONDITIONS: 3. Make sure that 'Market Selector' is present on the page
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
    event_markets = [
        ('total_goals_2_way',),
        ('puck_line',),
        ('sixty_minutes_betting',)
    ]

    def verify_sticky_behavior(self, market):
        is_sticky = self.ice_hockey_tab_content.is_market_selector_sticky
        self.assertTrue(is_sticky, msg='"Market Selector" is not sticky in Ice Hockey')
        drop_down_list = self.ice_hockey_tab_content.dropdown_market_selector
        drop_down_list.items_as_ordered_dict.get(market).click()
        selected_market = self.ice_hockey_tab_content.dropdown_market_selector.value
        self.assertEqual(selected_market, market, msg=f'Actual Market: "{selected_market}" is not same as'
                                                      f'Expected Market: "{market}", Market selector functionality is not same')

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Go to the Ice Hockey landing page -> 'Competition' tab
        PRECONDITIONS: 3. Make sure that 'Market Selector' is present on the page
        """
        ice_hockey_category_id = self.ob_config.ice_hockey_config.category_id
        self.cms_config.verify_and_update_market_switcher_status(sport_name='icehockey', status=True)
        all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                     status=True)
        self.assertTrue(all_sports_status, msg='"All Sports" is disabled')
        self.cms_config.verify_and_update_sport_config(sport_category_id=ice_hockey_category_id,
                                                       disp_sort_names='HH,WH,MR,HL',
                                                       primary_markets='|Money Line|,|Total Goals 2-way|,|Puck Line|,|60 Minutes Betting|')
        self.ob_config.add_ice_hockey_event_to_ice_hockey_usa(markets=self.event_markets)
        self.site.wait_content_state('Homepage')
        self.navigate_to_page("sport/ice-hockey")
        self.site.wait_content_state(state_name='IceHockey')
        self.site.ice_hockey.tabs_menu.click_button(self.expected_sport_tabs.competitions)
        current_tab_name = self.site.ice_hockey.tabs_menu.current
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                    ice_hockey_category_id)
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual Tab : "{current_tab_name}" Expected Tab : "{expected_tab_name}"')
        self.__class__.ice_hockey_tab_content = self.site.ice_hockey.tab_content
        has_market_selector = self.ice_hockey_tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Ice Hockey')

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
            self.ice_hockey_tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        self.assertTrue(self.markets, msg='Markets not found')
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
