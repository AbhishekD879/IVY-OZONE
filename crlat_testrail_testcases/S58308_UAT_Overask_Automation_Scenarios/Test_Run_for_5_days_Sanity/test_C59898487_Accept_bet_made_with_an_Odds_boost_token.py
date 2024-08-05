import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C59898487_Accept_bet_made_with_an_Odds_boost_token(Common):
    """
    TR_ID: C59898487
    NAME: Accept bet made with an Odds boost token
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_add_a_selection_to_quick_bet_or_bet_slip_click_on_odds_boost_and_trigger_overask(self):
        """
        DESCRIPTION: Add a selection to Quick Bet or bet slip, click on Odds Boost and trigger Overask.
        EXPECTED: Your bet should have gone through to Overask
        """
        pass

    def test_002_in_the_ti_accept_the_bet(self):
        """
        DESCRIPTION: In the TI, accept the bet.
        EXPECTED: You should see the bet receipt and it should have the Odds Boost signposting.
        """
        pass

    def test_003_check_my_bets_open_bets_and_verify_that_you_see_your_bet_there_and_that_it_has_the_odds_boost_signposting(self):
        """
        DESCRIPTION: Check My Bets->Open Bets and verify that you see your bet there and that it has the Odds Boost signposting.
        EXPECTED: Your bet should be in My Bets->Open Bets and it should have the Odds Boost signposting.
        """
        pass
