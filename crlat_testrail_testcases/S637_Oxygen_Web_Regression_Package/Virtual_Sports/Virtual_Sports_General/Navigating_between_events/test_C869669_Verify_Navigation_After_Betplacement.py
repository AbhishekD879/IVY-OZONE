import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.virtual_sports
@vtest
class Test_C869669_Verify_Navigation_After_Betplacement(Common):
    """
    TR_ID: C869669
    NAME: Verify Navigation After Betplacement
    DESCRIPTION: This test case verifies navigation after bet placement when user selects outcome from Virtuals Sports
    DESCRIPTION: Jira ticket: BMA-5233, BMA-11096
    PRECONDITIONS: User should be logged in to place a bet.
    """
    keep_browser_open = True

    def test_001_go_to_virtual_sports(self):
        """
        DESCRIPTION: Go to "Virtual Sports"
        EXPECTED: Virtual Sports successfully opened
        EXPECTED: Next or current event is shown
        """
        pass

    def test_002_go_to_virtual_football_sport_page(self):
        """
        DESCRIPTION: Go to 'Virtual Football' sport page
        EXPECTED: 'Virtual Football' sport page is opened
        """
        pass

    def test_003_add_selection_to_the_bet_slip___open_bet_slip(self):
        """
        DESCRIPTION: Add selection to the Bet Slip -> open Bet Slip
        EXPECTED: *   Betslip is opened
        EXPECTED: *   Selection is present
        """
        pass

    def test_004_enter_stake_in_stake_field_and_tap_bet_now_button(self):
        """
        DESCRIPTION: Enter stake in 'Stake' field and tap 'Bet Now' button
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   Bet Receipt is shown
        """
        pass

    def test_005_tap_done_button_on_bet_receipt_page(self):
        """
        DESCRIPTION: Tap 'Done' button on Bet Receipt page
        EXPECTED: *   Bet Receipt is not shown anymore and Bets Slip closes
        EXPECTED: *   User stays on same page.
        """
        pass

    def test_006_repeat_this_test_case_for_the_following_virtual_sports_greyhounds_football_motorsports_cycling_speedway_tennis_grand_national(self):
        """
        DESCRIPTION: Repeat this test case for the following Virtual Sports:
        DESCRIPTION: * Greyhounds
        DESCRIPTION: * Football,
        DESCRIPTION: * Motorsports,
        DESCRIPTION: * Cycling,
        DESCRIPTION: * Speedway,
        DESCRIPTION: * Tennis
        DESCRIPTION: * Grand National
        EXPECTED: 'Virtual Horse Racing' sport page is opened
        """
        pass
