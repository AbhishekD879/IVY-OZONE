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
class Test_C9608067_Verify_Stake_and_Potential_Return_when_No_Selection_is_Removed(Common):
    """
    TR_ID: C9608067
    NAME: Verify Stake and Potential Return when No Selection is Removed
    DESCRIPTION: This test case verifies Stake and Potential Return when No Selection is Removed
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: Login into App
    PRECONDITIONS: Place Multiple bet on pre-match events
    PRECONDITIONS: Navigate to the Bet History from Right/User menu
    PRECONDITIONS: Go to 'Open Bets' Tab -> verify that 'Edit My Acca/Bet' button is available
    PRECONDITIONS: Go to 'Cash Out' Tab -> verify that 'Edit My Acca/Bet' button is available
    PRECONDITIONS: Tap on 'Edit My Acca/Bet' button in 'Open Bets' Tab -> verify that user is in 'My Acca Edit' mode
    PRECONDITIONS: NOTE: 'Edit My ACCA' button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    PRECONDITIONS: Test case should be discussed and edited https://jira.egalacoral.com/browse/BMA-46789
    """
    keep_browser_open = True

    def test_001_verify_that_no_selection_is_removed(self):
        """
        DESCRIPTION: Verify that No Selection is removed
        EXPECTED: No Selection is removed
        """
        pass

    def test_002_verify_that_stake_is_available(self):
        """
        DESCRIPTION: Verify that Stake is available
        EXPECTED: Stake is available
        """
        pass

    def test_003_verify_that_potential_returnest_returns_is_shown_as_na(self):
        """
        DESCRIPTION: Verify that 'Potential Return'/'Est. Returns' is shown as N/A
        EXPECTED: 'Potential Return'/'Est. Returns' is shown as N/A
        """
        pass

    def test_004_change_price_for_one_of_selections_in_my_acca_edit_modeverify_that_any_change_in_the_prices_is_not_shown(self):
        """
        DESCRIPTION: Change price for one of selections in 'My Acca' Edit mode
        DESCRIPTION: Verify that any change in the Prices is NOT shown
        EXPECTED: - Est. Returns is shown as N/A
        EXPECTED: - Price is not updated on UI
        """
        pass

    def test_005_remove_one_selection_other_than_that_for_which_price_was_changed(self):
        """
        DESCRIPTION: Remove one selection other than that for which price was changed
        EXPECTED: - New Est. Returns is shown according to ValidateBet request
        """
        pass

    def test_006_tap_confirm_buttonverify_that_updated_price_is_shown_for_selection_for_which_price_was_changed_in_a_step_4(self):
        """
        DESCRIPTION: Tap 'Confirm' button
        DESCRIPTION: Verify that updated price is shown for selection for which price was changed in a step #4
        EXPECTED: Updated price is shown for selection for which price was changed in a step #4
        EXPECTED: or
        EXPECTED: message "Sorry, editing was unsuccessful, please try again." is displayed for the first click on the 'Confirm' button and after second click changes are successfully saved
        """
        pass

    def test_007_repeat_all_case_in_cashout_tab(self):
        """
        DESCRIPTION: Repeat all case in 'Cashout' Tab
        EXPECTED: 
        """
        pass
