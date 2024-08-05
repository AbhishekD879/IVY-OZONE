import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C9608413_VerifyStake_and_Est_Returns_when_any_Selection_is_Removed(Common):
    """
    TR_ID: C9608413
    NAME: Verify Stake and Est. Returns when any Selection is Removed
    DESCRIPTION: This test case verifies Stake and Potential Return when any Selection is Removed
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: Login into App
    PRECONDITIONS: Place Multiple bet
    PRECONDITIONS: Navigate to the Bet History from Right/User menu
    PRECONDITIONS: Go to 'Open Bets' Tab -> verify that 'Edit My Acca/Bet' button is available
    PRECONDITIONS: Go to 'Cash Out' Tab -> verify that 'Edit My Acca/Bet' button is available
    PRECONDITIONS: Tap on 'Edit My Acca/Bet' button in 'Open Bets' Tab -> verify that user is in 'My Acca Edit' mode
    PRECONDITIONS: NOTE: 'Edit My ACCA/Bet' button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    """
    keep_browser_open = True

    def test_001_remove_one_or_more_selection_in_the_acca(self):
        """
        DESCRIPTION: Remove one or more selection in the Acca
        EXPECTED: The selection (-ions) is removed
        """
        pass

    def test_002_verify_that_new_stake_is_shown_as_the_cashout_value_of_the_acca_with_removed_selection(self):
        """
        DESCRIPTION: Verify that 'New Stake' is shown as the 'Cashout' Value of the Acca with removed Selection
        EXPECTED: The 'New Stake' is shown as the 'Cashout' Value of the Acca with removed Selection. 'New Stake' Value are taken from *ValidateBet* request and 'Cashout' Value - from *readBet* request
        """
        pass

    def test_003_verify_that_potential_return_is_shown_asnew_potential_returns(self):
        """
        DESCRIPTION: Verify that 'Potential Return' is shown as
        DESCRIPTION: "New Potential Returns"
        EXPECTED: 'Potential Return' is shown as "New Potential Returns"
        """
        pass

    def test_004_repeat_all_case_in_cashout_tab(self):
        """
        DESCRIPTION: Repeat all case in 'Cashout' Tab
        EXPECTED: 
        """
        pass
