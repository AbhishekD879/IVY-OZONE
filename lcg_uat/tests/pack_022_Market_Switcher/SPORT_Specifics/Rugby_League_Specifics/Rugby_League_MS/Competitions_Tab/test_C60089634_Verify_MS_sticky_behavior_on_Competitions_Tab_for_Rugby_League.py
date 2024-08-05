import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Events with specific markets cannot created in Prod/Beta
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.mobile_only
@pytest.mark.market_switcher
@vtest
class Test_C60089634_Verify_MS_sticky_behavior_on_Competitions_Tab_for_Rugby_League(Common):
    """
    TR_ID: C60089634
    NAME: Verify MS sticky behavior on Competitions Tab for Rugby League
    DESCRIPTION: This test case verifies 'Market Selector' sticky behavior on Rugby League Competition page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Rugby League Landing page -> 'Competition' tab
    PRECONDITIONS: 3. Make sure that 'Market Selector' is present on the page
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Match Betting (WDW)| - "Match Result"
    PRECONDITIONS: * |Handicap 2-way (Handicap)| - "Handicap 2-way"
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
        ('handicap_2_way',),
        ('total_match_points',)]

    def verify_sticky_behavior(self, market):
        is_sticky = self.site.contents.tab_content.is_market_selector_sticky
        self.assertTrue(is_sticky, msg='"Market Selector" is not sticky in Rugby league')
        self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(market).click()
        selected_market = self.site.competition_league.tab_content.dropdown_market_selector.value
        self.assertEqual(selected_market, market, msg=f'Actual Market: "{selected_market}" is not same as'
                                                      f'Expected Market: "{market}", Market selector functionality is not same')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Go to the Rugby League Landing page -> 'Competition' tab
        PRECONDITIONS: 3. Make sure that 'Market Selector' is present on the page
        """
        all_sports = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports', status=True)
        self.assertTrue(all_sports, msg='"Allsports" is not enabled')
        status = self.cms_config.verify_and_update_market_switcher_status(sport_name='rugbyleague', status=True)
        self.assertTrue(status, msg='"Rugby league" is not enabled')
        self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.rugby_league_config.category_id,
                                                       disp_sort_names='MR,WH,HL',
                                                       primary_markets='|Match Betting|,|Handicap 2-way|,'
                                                                       '|Total Match Points|')
        self.ob_config.add_rugby_league_event_to_rugby_league_all_rugby_league(markets=self.event_markets)

        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                    self.ob_config.rugby_league_config.category_id)
        self.navigate_to_page("sport/rugby-league")
        self.site.wait_content_state_changed(timeout=15)
        self.site.contents.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
        self.site.wait_content_state_changed()
        current_tab_name = self.site.contents.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab is "{current_tab_name}", instead of "{expected_tab_name}"')
        has_market_selector = self.site.competition_league.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Rugby Leauge')

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
        self.__class__.markets = list(self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
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
