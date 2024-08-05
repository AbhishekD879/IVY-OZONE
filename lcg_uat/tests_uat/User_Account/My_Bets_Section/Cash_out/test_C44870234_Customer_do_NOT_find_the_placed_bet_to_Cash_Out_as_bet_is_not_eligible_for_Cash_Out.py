import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.constants import ATTRIBUTES, LEVELS, OPERATORS


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C44870234_Customer_do_NOT_find_the_placed_bet_to_Cash_Out_as_bet_is_not_eligible_for_Cash_Out(BaseBetSlipTest):
    """
    TR_ID: C44870234
    NAME: Customer do NOT find the placed bet to Cash Out as bet is not eligible for Cash Out
    """
    keep_browser_open = True

    def test_001_make_a_bet_from_a_market_that_does_not_have_cash_out(self):
        """
        DESCRIPTION: Make a bet from a market that does not have cash out.
        EXPECTED: You should have made a bet on a market which does not have cash out.
        """
        self.site.login()
        cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'N'), \
            simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'N')
        event = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                    all_available_events=True,
                                                    additional_filters=cashout_filter,
                                                    in_play_event=False, number_of_events=1)[0]
        self.__class__.event_name = event['event']['name']
        market = next((market for market in event['event']['children']), None)
        outcomes_resp = market['market']['children']
        all_selection_ids = {i['outcome']['name']: i['outcome']['id']
                             for i in outcomes_resp if 'Unnamed' not in i['outcome']['name']}
        self.open_betslip_with_selections(selection_ids=list(all_selection_ids.values())[0])
        self.place_and_validate_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.close_betreceipt()

    def test_002_check_that_this_bet_does_not_show_a_cash_out_button_in_my_bets_open_bets(self):
        """
        DESCRIPTION: Check that this bet does not show a Cash Out button in My Bets->Open Bets.
        EXPECTED: This bet should not show a Cash Out button in My Bets->Open Bets
        """
        self.site.open_my_bets_open_bets()
        _, bet = self.site.open_bets.tab_content.accordions_list. \
            get_bet(bet_type='SINGLE', event_names=self.event_name)
        self.assertFalse(bet.buttons_panel.has_full_cashout_button(),
                         msg=f'{vec.bet_history.CASH_OUT_TAB_NAME} was found for event : {self.event_name}')
