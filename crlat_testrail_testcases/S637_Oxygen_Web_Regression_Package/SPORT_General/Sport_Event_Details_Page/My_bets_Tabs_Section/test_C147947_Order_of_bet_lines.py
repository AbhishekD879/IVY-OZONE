import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C147947_Order_of_bet_lines(Common):
    """
    TR_ID: C147947
    NAME: Order of bet lines
    DESCRIPTION: This test case verifies the order of bets on 'My bets' tab on Event Details page when the user is logged in.
    DESCRIPTION: AUTOMATED [C9697702] [C10581807]
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   Place simultaneous a few bets for the same sport event (multiples and singles) (in order to get the same Bet Placement Time)
    PRECONDITIONS: *   Place a few bets (multiples and singles) for the same sport event at different time (in order to get bet lines with different Bet Placement Time)
    """
    keep_browser_open = True

    def test_001_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_bets_from_preconditions(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed bets from preconditions
        EXPECTED: 
        """
        pass

    def test_002_verify_order_of_bet_lines(self):
        """
        DESCRIPTION: Verify order of bet lines
        EXPECTED: Bets are ordered chronologically by bet placement time/date (the most recent - first)
        """
        pass

    def test_003_verify_order_of_cash_out_bet_lines_with_the_same_bet_placement_time(self):
        """
        DESCRIPTION: Verify order of Cash Out bet lines with the same bet placement time
        EXPECTED: Bets are shown in the order they come back from betplacement API (getbetPlaced response)
        """
        pass
