import pytest
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.event_details
@pytest.mark.markets
@pytest.mark.cash_out
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.safari
@vtest
class Test_C29173_Markets_with_Cash_Out_option_available(BaseCashOutTest, BaseSportTest):
    """
    TR_ID: C29173
    NAME: Markets with Cash Out option available
    DESCRIPTION: This test case verifies Markets with Cash Out option available on Event Details Pages
    """
    keep_browser_open = True
    markets = None
    markets_params = [('extra_time_result', {'cashout': True}),
                      ('both_teams_to_score', {'cashout': False}),
                      ('over_under_total_goals', {'cashout': True, 'over_under': 2.5}),
                      ('over_under_total_goals', {'cashout': False, 'over_under': 1.5})]
    racing_event_with_cashout = None
    racing_event_without_cashout = None
    ew_terms = {'ew_places': 2, 'ew_fac_num': 1, 'ew_fac_den': 16}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        self.__class__.racing_event_with_cashout = self.ob_config.add_UK_greyhound_racing_event(
            number_of_runners=1, cashout=True, ew_terms=self.ew_terms)
        self.__class__.racing_event_without_cashout = self.ob_config.add_UK_greyhound_racing_event(
            number_of_runners=1, cashout=False, ew_terms=self.ew_terms)
        self.__class__.event = self.ob_config.add_autotest_premier_league_football_event(markets=self.markets_params)

    def test_001_go_to_event_details_page(self):
        """
        DESCRIPTION: Go to Event Details page
        EXPECTED: <Sport> Event Details page is opened
        """
        self.navigate_to_edp(event_id=self.event.event_id)

    def test_002_verify_cash_out_icon_for_market_with_cashoutavail_y_attribute_on_market_level(self):
        """
        DESCRIPTION: Verify 'CASH OUT' icon for market with **cashoutAvail="Y"** attribute on Market level
        EXPECTED: 'CASH OUT' icon is displayed from the right side on corresponding market accordion
        """
        self.assertTrue(self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.all_markets),
                        msg='"ALL MARKETS" is not active tab')
        self.__class__.markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.markets, msg='No markets are shown')

        extra_time_result_market = self.markets.get(self.expected_market_sections.extra_time_result)
        self.assertTrue(extra_time_result_market, msg='"Extra-Time Result" market is not shown')
        self.assertTrue(extra_time_result_market.market_section_header.has_cash_out_mark(),
                        msg='"Extra-Time Result" market have no cashout indicator')

    def test_003_verify_cash_out_icon_for_market_with_cashoutavail_n_attribute_on_market_level(self):
        """
        DESCRIPTION: Verify 'CASH OUT' icon for market with **cashoutAvail="N"** attribute on Market level
        EXPECTED: 'CASH OUT' icon is NOT displayed from the right side on corresponding market accordion
        """
        both_teams_to_score_market = self.markets.get(self.expected_market_sections.both_teams_to_score)
        self.assertTrue(both_teams_to_score_market, msg='"Both Teams to Score" market is not shown')
        self.assertFalse(both_teams_to_score_market.market_section_header.has_cash_out_mark(expected_result=False),
                         msg='"Both Teams to Score" market have cashout indicator')

    def test_004_verify_cash_out_icon_for_combined_markets(self):
        """
        DESCRIPTION: Verify 'CASH OUT' icon for **combined** markets
        DESCRIPTION: (<Football>: Scorecast/Popular Goalscorer Markets etc.)
        EXPECTED: If one of combined markets has **cashoutAvail="Y"** then 'Cash out' icon should be displayed from the right side on corresponding market accordion
        """
        over_under_total_goals_market = self.markets.get(self.expected_market_sections.over_under_total_goals)
        self.assertTrue(over_under_total_goals_market, msg='Over/Under Total Goals market is not shown')
        self.assertTrue(over_under_total_goals_market.market_section_header.has_cash_out_mark(),
                        msg='Over/Under Total Goals market have no cashout indicator')

    def test_005_go_to_racing_event_details_page_with_cashout(self):
        """
        DESCRIPTION: Go to Racing Event Details page for market with **cashoutAvail="Y"**
        DESCRIPTION: Verify 'CASH OUT' icon for market with **cashoutAvail="Y"** attribute on Market level
        EXPECTED: <Race> Event Details page is opened
        EXPECTED: 'CASH OUT' icon is displayed in the same line as the Each-way terms below <Race> Event markets tabs
        """
        self.navigate_to_edp(event_id=self.racing_event_with_cashout.event_id, sport_name='greyhound-racing')

        markets = self.site.greyhound_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets found')
        market = list(markets.values())[0]
        self.assertTrue(market.section_header.has_cashout_label(), msg='Cashout label is not shown')

    def test_006_verify_cash_out_icon_for_market_with_cashoutavail_n_attribute_on_market_level(self):
        """
        DESCRIPTION: Go to Racing Event Details page for market with **cashoutAvail="N"**
        EXPECTED: <Race> Event Details page is opened
        DESCRIPTION: Verify 'CASH OUT' icon for market with **cashoutAvail="N"** attribute on Market level
        EXPECTED: 'CASH OUT' icon is NOT displayed in the same line as the Each-way terms below <Race> Event markets tabs
        """
        self.navigate_to_edp(event_id=self.racing_event_without_cashout.event_id, sport_name='greyhound-racing')

        markets = self.site.greyhound_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets found')
        market = list(markets.values())[0]

        has_cashout = market.section_header.has_cashout_label()
        self.assertFalse(has_cashout, msg='Cashout label is shown for market without cashout available')
