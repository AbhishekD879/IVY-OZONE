import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.mobile_only
@pytest.mark.lad_uat
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C44870236_Clicking_Cash_Out_Terms_Conditions_link_should_take_you_to_Cash_Out_Terms_Conditions(BaseBetSlipTest):
    """
    TR_ID: C44870236
    NAME: Clicking Cash Out Terms & Conditions link should take you to Cash Out Terms & Conditions
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find/Create events
        DESCRIPTION: Login with user
        DESCRIPTION: Place a bet with cashout available
        """
        self.site.login()
        if tests.settings.backend_env == 'prod':
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                        additional_filters=cashout_filter)[0]
            match_result_market = next((market['market'] for market in event['event']['children'] if
                                        market.get('market').get('templateMarketName') == 'Match Betting'), None)
            outcomes = match_result_market['children']
            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            selection_ids = event.selection_ids
        self.open_betslip_with_selections(selection_ids=list(selection_ids.values())[0])
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

    def test_001_log_in_and_go_to_my_bets_open_bets(self):
        """
        DESCRIPTION: Log in and go to My Bets->Open Bets
        EXPECTED: You should be on My Bets->Open Bets
        """
        self.site.open_my_bets_open_bets()

    def test_002_scroll_to_the_bottom_of_the_page_to_where_the_cash_out_terms__conditions_link_is(self):
        """
        DESCRIPTION: Scroll to the bottom of the page to where the Cash Out Terms & Conditions link is
        EXPECTED: You should be at the Cash Out Terms & Conditions link
        """
        cashoutTC = self.site.open_bet.verify_CashOut_TC
        self.assertTrue(cashoutTC.is_displayed(), msg='"Cashout Terms and Conditions" link is not displayed')

    def test_003_click_on_the_link_and_verify_that_you_are_taken_to_the_cash_out_terms__conditions_page(self):
        """
        DESCRIPTION: Click on the link and verify that you are taken to the Cash Out Terms & Conditions page
        EXPECTED: You should be on the Cash Out Terms & Conditions page
        """
        self.site.open_bet.verify_CashOut_TC.click()
        actual_header = self.site.cashout.header_line.page_title.text
        expected_header = vec.ema._terms_cashout.upper() if self.brand == 'bma' else vec.ema._terms_cashout
        self.assertEqual(actual_header, expected_header, msg=f'Actual header "{actual_header}" is not same as '
                                                                    f'Expected header "{expected_header}"')
