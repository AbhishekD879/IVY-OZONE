import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Events with specific markets cannot created in Prod/Beta
@pytest.mark.sports
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.market_switcher
@vtest
class Test_C60089549_Verify_MS_sticky_behavior_on_Matches_Tab_for_Volleyball_SLP(Common):
    """
    TR_ID: C60089549
    NAME: Verify MS sticky behavior on Matches Tab for Volleyball SLP
    DESCRIPTION: This test case verifies 'Market Selector' sticky behavior on Volleyball landing page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Match Betting|,|Total Points|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: Load the app
    PRECONDITIONS: Go to the Volleyball Landing Page -> 'Click on Matches Tab'
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Match Betting (WW)| - "Match Result"
    PRECONDITIONS: * |Set Handicap (Handicap)| - "Set Handicap"
    PRECONDITIONS: * |Total Match Points (Over/Under)| - "Total Points"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    event_markets = [
        ('match_set_handicap',),
        ('total_match_points',)]

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Go to the volleyball Landing page -> 'matches' tab
        PRECONDITIONS: 3. Make sure that 'Market Selector' is present on the page
        """
        all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports', status=True)
        self.assertTrue(all_sports_status, msg='"All Sports" is disabled')
        status = self.cms_config.verify_and_update_market_switcher_status(sport_name='volleyball', status=True)
        self.assertTrue(status, msg=f'The sport "volleyball" is not checked')
        self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.volleyball_config.category_id,
                                                       disp_sort_names='HH,MH,WH,HL,3W',
                                                       primary_markets='|Match Betting|,|Handicap Match Result|,|Match Set Handicap|,|Total Match Points|,|Set X Winner||Handicap 3-Way|')

        self.ob_config.add_volleyball_event_to_austrian_league(markets=self.event_markets)
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches, self.ob_config.volleyball_config.category_id)
        self.site.wait_content_state('Homepage')
        self.navigate_to_page("sport/volleyball")
        self.site.sports_page.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
        current_tab_name = self.site.contents.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Current tab:"{current_tab_name}", is not same as Expected tab:"{expected_tab_name}"')
        has_market_selector = self.site.sports_page.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for volleyball')

    def test_001_verify_that_market_selector_is_sticky_when_scrolling_the_page_down(self):
        """
        DESCRIPTION: Verify that 'Market Selector' is sticky when scrolling the page down
        EXPECTED: Tablet/Mobile:
        EXPECTED: • 'Market Selector' is sticky. It remains at the top of the scrolling page
        EXPECTED: • Market selector functionality remains the same
        EXPECTED: **Note:**
        EXPECTED: For the Desktop 'Market Selector' is NOT sticky. It becomes hidden together with Date Selector panel
        """
        markets = list(self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        self.assertTrue(markets, msg='Markets not found')
        for market in markets:
            is_sticky = self.site.sports_page.tab_content.is_market_selector_sticky
            self.assertTrue(is_sticky, msg='"Market Selector" is not sticky in volleyball')
            self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(market).click()
            selected_market = self.site.sports_page.tab_content.dropdown_market_selector.value
            self.assertEqual(selected_market, market, msg=f'Actual Market: "{selected_market}" is not same as'
                                                          f'Expected Market: "{market}", Market selector functionality is not same')

    def test_002_verify_that_market_selector_is_sticky_when_scrolling_the_page_up(self):
        """
        DESCRIPTION: Verify that 'Market Selector' is sticky when scrolling the page up
        EXPECTED: Tablet/Mobile:
        EXPECTED: • 'Market Selector' is sticky. It remains at the top of the scrolling page
        EXPECTED: • Market selector functionality remains the same
        EXPECTED: **Note:**
        EXPECTED: For the Desktop 'Market Selector' is NOT sticky. It becomes hidden together with Date Selector panel
        """
        # covered in step_001
