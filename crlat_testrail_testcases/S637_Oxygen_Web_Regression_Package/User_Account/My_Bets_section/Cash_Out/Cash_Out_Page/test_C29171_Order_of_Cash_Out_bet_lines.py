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
class Test_C29171_Order_of_Cash_Out_bet_lines(Common):
    """
    TR_ID: C29171
    NAME: Order of Cash Out bet lines
    DESCRIPTION: This test case verifies the order of Cash Out bets on 'Cash Out' tab when the user is logged in.
    DESCRIPTION: **JIRA tickets**:
    DESCRIPTION: * BMA-3249
    DESCRIPTION: * [BMA-17632 (Investigate and improve the sorting order of Cash Out bets)][1]
    DESCRIPTION: [1]:https://jira.egalacoral.com/browse/BMA-17632
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   Place simultaneous a few bets (multiples and singles) (in order to get the same Bet Placement Time)
    PRECONDITIONS: *   Place a few bets (multiples and singles) at different time (in order to get bet lines with different Bet Placement Time)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_open_my_bets_page(self):
        """
        DESCRIPTION: Open 'My Bets' page
        EXPECTED: 'My Bets' page is opened
        """
        pass

    def test_003_tap_cash_out_tab(self):
        """
        DESCRIPTION: Tap 'Cash Out' tab
        EXPECTED: 'Cash Out' page is opened
        """
        pass

    def test_004_verify_order_of_cash_out_bet_lines(self):
        """
        DESCRIPTION: Verify order of Cash Out bet lines
        EXPECTED: Cash Out bets are ordered chronologically by bet placement time/date (the most recent - first)
        """
        pass

    def test_005_verify_order_of_cash_out_bet_lines_with_the_same_bet_placement_time(self):
        """
        DESCRIPTION: Verify order of Cash Out bet lines with the same bet placement time
        EXPECTED: *   Bet lines are ordered by Event Start Time (with the earliest start time first)
        EXPECTED: *   In case of the same Event Start Time - in the order they come back from betplacement API (getbetDetails response)
        """
        pass
