import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C60060307_Verify_that_one_SS_response_is_received_after_placing_Bet(Common):
    """
    TR_ID: C60060307
    NAME: Verify that one SS response is received after placing Bet
    DESCRIPTION: Test case verifies that EventToOutomeForEvent is replaced with EventToOutcomeForOutcome in SS responce after Betslip receipt
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Make sure the user is logged into their account
    PRECONDITIONS: 3. The User's account balance is sufficient to cover a bet stake
    PRECONDITIONS: 4. Make bet placement
    PRECONDITIONS: 5. Make sure Bet is placed successfully
    """
    keep_browser_open = True

    def test_001_check_ss_response__for_bet_receipt__in_devtools__network__xhr___search_outcome(self):
        """
        DESCRIPTION: Check SS response  for Bet receipt  in devTools-> Network ->XHR -> search 'outcome'
        EXPECTED: Verify betslip receipt with EventToOutomeForOutcome, example of request: EventToOutcomeForOutcome/582071908?
        EXPECTED: no EventToOutomeForEvent requests should be made from betslip receipt
        """
        pass

    def test_002_make_multiply_stakecheck_ss_response_for_bet_receipt_in_devtools__network__xhr___search_outcome(self):
        """
        DESCRIPTION: Make multiply Stake
        DESCRIPTION: Check SS response for Bet receipt in devTools-> Network ->XHR -> search 'outcome'
        EXPECTED: Verify betslip receipt with EventToOutomeForOutcome, example of request: EventToOutcomeForOutcome/582071908?
        EXPECTED: no EventToOutomeForEvent requests should be made from betslip receipt
        """
        pass
