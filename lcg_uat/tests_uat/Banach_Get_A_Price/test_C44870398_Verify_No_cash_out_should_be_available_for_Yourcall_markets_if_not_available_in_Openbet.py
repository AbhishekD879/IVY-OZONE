import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870398_Verify_No_cash_out_should_be_available_for_Yourcall_markets_if_not_available_in_Openbet(Common):
    """
    TR_ID: C44870398
    NAME: Verify No cash out should be available for Yourcall markets if not available in Openbet
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_find_an_event_on_the_site_which_has_a_banache_market_which_is_not_displaying_a_cash_out_icon(self):
        """
        DESCRIPTION: Find an event on the site which has a Banache market which is not displaying a cash out icon
        EXPECTED: You should have found a Banache market which does not have a cash out icon
        """
        pass

    def test_002_verify_in_openbet_that_cash_out_is_not_enabled_for_this_market(self):
        """
        DESCRIPTION: Verify in Openbet that cash out is not enabled for this market
        EXPECTED: Cash out should not have been enabled for this market
        """
        pass

    def test_003_place_a_bet_on_a_selection_from_the_market_and_verify_that_the_bet_receipt_and_my_bets_open_bets_does_not_show_cash_out_signposting(self):
        """
        DESCRIPTION: Place a bet on a selection from the market and verify that the bet receipt and My Bets->Open Bets does not show Cash Out signposting
        EXPECTED: The bet receipt and My Bets->Open Bets should not show Cash Out signposting
        """
        pass
