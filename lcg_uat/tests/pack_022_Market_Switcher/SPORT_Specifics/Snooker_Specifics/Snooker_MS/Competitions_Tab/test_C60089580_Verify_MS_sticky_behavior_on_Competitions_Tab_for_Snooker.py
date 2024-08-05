import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - Event creation can not be done on PROD
@pytest.mark.market_switcher
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C60089580_Verify_MS_sticky_behavior_on_Competitions_Tab_for_Snooker(Common):
    """
    TR_ID: C60089580
    NAME: Verify MS sticky behavior on Competitions Tab for Snooker
    DESCRIPTION: This test case verifies 'Market Selector' sticky behavior on Snooker Competition page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Match Betting|,|Handicap|,|Total Frames|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: Load the app
    PRECONDITIONS: Go to the Snooker Landing Page -> 'Click on Competition Tab'
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: |Match Betting (WW)| - "Match Result"
    PRECONDITIONS: |Match Handicap (Handicap)| - "Handicap"
    PRECONDITIONS: |Total Frames Over/Under (Over/Under)| - "Total Frames"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    markets = [('total_frames_over_under',), ('match_handicap',)]

    def verify_sticky_behavior(self, market):
        is_sticky = self.site.sports_page.tab_content.is_market_selector_sticky
        self.assertTrue(is_sticky, msg='"Market Selector" is not sticky in Snooker league')
        self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(market).click()
        selected_market = self.site.sports_page.tab_content.dropdown_market_selector.value
        self.assertEqual(selected_market, market, msg=f'Actual Market: "{selected_market}" is not same as'
                                                      f'Expected Market: "{market}" , Market selector functionality is not same')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Load the app
        PRECONDITIONS: Go to the Snooker Landing Page -> 'Click on Competition Tab'
        """
        all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                     status=True)
        self.assertTrue(all_sports_status, msg='Market switcher is disabled for All Sports')
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='snooker', status=True)
        self.assertTrue(market_switcher_status, msg='Market switcher is disabled for Snooker sport')
        self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.backend.ti.snooker.category_id,
                                                       disp_sort_names='HH,MH,WH,HL',
                                                       primary_markets='|Match Result|,|Match Betting|,|Handicap Match Result|,'
                                                                       '|Total Frames Over/Under|,|Match Handicap|')
        self.ob_config.add_snooker_event_to_snooker_all_snooker(markets=self.markets)

        self.navigate_to_page(name='sport/snooker')
        self.site.wait_content_state('Snooker')
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                    self.ob_config.snooker_config.category_id)
        self.site.sports_page.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
        current_tab_name = self.site.sports_page.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as Expected Tab: "{expected_tab_name}"')
        has_market_selector = self.site.sports_page.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg='"Market Selector" drop-down is not displayed on Competitions tab')

    def test_001_verify_that_market_selector_is_sticky_when_scrolling_the_page_down(self):
        """
        DESCRIPTION: Verify that 'Market Selector' is sticky when scrolling the page down
        EXPECTED: Tablet/Mobile:
        EXPECTED: • 'Market Selector' is sticky. It remains at the top of the scrolling page
        EXPECTED: • Market selector functionality remains the same
        EXPECTED: **Note:**
        EXPECTED: For the Desktop 'Market Selector' is NOT sticky. It becomes hidden together with Date Selector panel
        """
        self.site.sports_page.scroll_to_bottom()
        self.__class__.markets = list(
            self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        self.assertTrue(self.markets, msg='No markets available in the market switcher dropdown')
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
        self.site.sports_page.scroll_to_top()
        self.verify_sticky_behavior(self.markets[2])
