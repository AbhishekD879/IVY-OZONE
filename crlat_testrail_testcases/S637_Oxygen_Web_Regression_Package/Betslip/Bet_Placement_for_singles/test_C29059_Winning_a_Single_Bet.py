import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C29059_Winning_a_Single_Bet(Common):
    """
    TR_ID: C29059
    NAME: Winning a Single Bet
    DESCRIPTION: This test case verifies Winning a Bet for single selection
    DESCRIPTION: AUTOTEST C2552884
    PRECONDITIONS: 1. User should be Log in
    PRECONDITIONS: 2. User should have sufficient funds to place a bet
    PRECONDITIONS: 3. How to trigger the situation when user wins a bet https://confluence.egalacoral.com/pages/viewpage.action?pageId=96150627
    """
    keep_browser_open = True

    def test_001_add_one_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add one selection to the Bet Slip
        EXPECTED: 
        """
        pass

    def test_002_go_to_the_bet_slip(self):
        """
        DESCRIPTION: Go to the Bet Slip
        EXPECTED: Added selection is displayed
        """
        pass

    def test_003_enter_correct_stake_in_stake_field_and_tap_bet_now(self):
        """
        DESCRIPTION: Enter correct Stake in 'Stake' field and tap 'Bet Now'
        EXPECTED: *  Bet is placed successfully
        EXPECTED: *  User 'Balance' is decreased by value entered in 'Stake' field
        EXPECTED: *  Bet Slip is replaced with a Bet Receipt view
        """
        pass

    def test_004_trigger_the_situation_when_user_wins_a_bet(self):
        """
        DESCRIPTION: Trigger the situation when user wins a bet
        EXPECTED: User balance is increased on bet win amount immediately
        """
        pass

    def test_005_go_to_bet_history(self):
        """
        DESCRIPTION: Go to Bet History
        EXPECTED: * 'Won' label is present on the Singles header
        EXPECTED: *  'You won <currency sign and value>' label right under header, on top of event card is shown
        EXPECTED: * Green tick is shown on the left of the bet
        """
        pass
