import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C9608049_Verify_Potential_return_increase_during_bet_placement_of_the_new_Acca(Common):
    """
    TR_ID: C9608049
    NAME: Verify Potential return increase during bet placement of the new Acca
    DESCRIPTION: This test case verifies Potential return increase during bet placement of the new Acca
    PRECONDITIONS: **Configurations:
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: **Preconditions:**
    PRECONDITIONS: Login into App
    PRECONDITIONS: Place Multiple bet
    PRECONDITIONS: Navigate to the Bet History from Right/User menu
    PRECONDITIONS: Go to 'Open Bets' Tab -> verify that 'Edit My Acca' button is available
    PRECONDITIONS: Go to 'Cash Out' Tab -> verify that 'Edit My Acca' button is available
    PRECONDITIONS: Tap on 'Edit My Acca' button in 'Open Bets' Tab -> verify that user is in 'My Acca Edit' mode
    PRECONDITIONS: Remove the selection from 'My Acca Edit' mode
    PRECONDITIONS: NOTE: 'Edit My ACCA' button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    """
    keep_browser_open = True

    def test_001_change_price_increasedecrease_for_one_of_selection_from_my_acca_edit_mode(self):
        """
        DESCRIPTION: Change price (increase/decrease) for one of selection from 'My Acca Edit' mode
        EXPECTED: Price is increased/decreased
        EXPECTED: The new potential returns increased/decreased
        """
        pass

    def test_002_tap_confirm_button_and_verify_that_the_new_acca_is_successfully_placed_at_the_new_potential_returns(self):
        """
        DESCRIPTION: Tap 'Confirm' button and verify that the new Acca is successfully placed at the new potential returns
        EXPECTED: The new Acca is successfully placed at the new potential returns
        """
        pass

    def test_003_verify_that_updated_prices_are_shown_against_each_open_selections(self):
        """
        DESCRIPTION: Verify that updated prices are shown against each Open Selections
        EXPECTED: Updated prices are shown against each Open Selections
        """
        pass

    def test_004_verify_that_new_stake_information_is_shown(self):
        """
        DESCRIPTION: Verify that New stake information is shown
        EXPECTED: New stake information is taken from *ValidateBet* request ('NewBetStake' attribute) and is displayed
        """
        pass

    def test_005_verify_that_new_potential_returns_are_shown(self):
        """
        DESCRIPTION: Verify that New Potential Returns are shown
        EXPECTED: New Potential Returns are taken from *ValidateBet* request ('BetPotentialWin' attribute) and displayed
        """
        pass
