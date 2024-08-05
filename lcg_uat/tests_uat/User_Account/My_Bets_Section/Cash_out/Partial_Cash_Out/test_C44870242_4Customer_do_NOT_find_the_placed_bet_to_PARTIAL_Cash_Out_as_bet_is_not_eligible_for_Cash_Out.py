import pytest
import tests
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.environments import constants as vec
from collections import OrderedDict


@pytest.mark.p1
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.uat
@pytest.mark.medium
@pytest.mark.cash_out
@pytest.mark.mobile_only
@vtest
class Test_C44870242_4Customer_do_NOT_find_the_placed_bet_to_PARTIAL_Cash_Out_as_bet_is_not_eligible_for_Cash_Out(BaseBetSlipTest):
    """
    TR_ID: C44870242
    NAME: 4.Customer do NOT find the placed bet to PARTIAL Cash Out as bet is not eligible for Cash Out
    """
    keep_browser_open = True
    prices = OrderedDict([('odds_home', '33/1'), ('odds_draw', '33/1'), ('odds_away', '33/1')])

    def test_001_place_a_low_stake_bet_on_a_selection_which_has_high_odds_from_a_cash_out_market_eg_10p_bet_on_a_selection_which_has_odds_of_331_or_greater(self):
        """
        DESCRIPTION: Place a low stake bet on a selection which has high odds from a cash out market e.g. 10p bet on a selection which has odds of 33/1 or greater
        EXPECTED: You should have placed the bet
        """
        self.site.login()
        if tests.settings.backend_env == 'prod':
            cashout_filter = simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         additional_filters=cashout_filter, all_available_events=True, in_play_event=False)
            highest_odd = 0
            for event in events:
                match_result_market = next((market['market'] for market in event['event']['children'] if
                                            market.get('market').get('templateMarketName') == 'Match Betting'), None)
                outcomes = match_result_market['children']
                for outcome in outcomes:
                    outcome_id = outcome['outcome']['id']
                    price_num = float(outcome['outcome']['children'][0]['price']['priceNum'])
                    price_den = float(outcome['outcome']['children'][0]['price']['priceDen'])
                    self.odd_value = price_num / price_den
                    if highest_odd < self.odd_value:
                        highest_odd = self.odd_value
                        self.__class__.selection_id = outcome_id
        else:
            events = self.ob_config.add_autotest_premier_league_football_event(in_play_event=False, lp=self.prices)
            self.selection_id = list(events.selection_ids.values())[0]
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.place_and_validate_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.close_betreceipt()

    def test_002_go_to_my_bets_open_bets_and_verify_that_you_see_a_cash_out_button_but_no_partial_cash_out_button(self):
        """
        DESCRIPTION: Go to My Bets->Open Bets and verify that you see a Cash Out button, but no Partial Cash Out button
        EXPECTED: You should only see a Cash Out button and no Partial Cash Out button
        """
        self.site.open_my_bets_open_bets()
        _, bet = self.site.open_bets.tab_content.accordions_list. \
            get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, selection_ids=self.selection_id)
        self.assertTrue(bet.buttons_panel.has_full_cashout_button(), msg=f'"{vec.bet_history.CASH_OUT_TAB_NAME}" button is not present')
        self.assertFalse(bet.buttons_panel.has_partial_cashout_button(expected_result=False),
                         msg=f'"{vec.bet_history.PARTIAL_CASH_OUT_BTN_TEXT}" button is present')
