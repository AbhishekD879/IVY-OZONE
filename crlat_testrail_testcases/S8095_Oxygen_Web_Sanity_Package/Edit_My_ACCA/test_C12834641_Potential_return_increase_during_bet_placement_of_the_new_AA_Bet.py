import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C12834641_Potential_return_increase_during_bet_placement_of_the_new_AA_Bet(Common):
    """
    TR_ID: C12834641
    NAME: Potential return increase during bet placement of the new AССA Bet
    DESCRIPTION: 
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: 1. Login into App
    PRECONDITIONS: 2. Place single bet and multiple bet with more than 4 selection (e.g. ACCA 5) (selections should have cash out available) NOTE: The button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    PRECONDITIONS: 3. Navigate to My Bets>Open Bets
    PRECONDITIONS: 4. Tap on 'Edit My Acca' button  -> verify that user is in 'My Acca Edit' mode
    """
    keep_browser_open = True

    def test_001_remove_one_or_more_selection_in_the_acca(self):
        """
        DESCRIPTION: Remove one or more selection in the Acca
        EXPECTED: The selection(s) is removed
        """
        pass

    def test_002_verify_that_new_stake_is_shown(self):
        """
        DESCRIPTION: Verify that 'New Stake' is shown
        EXPECTED: The 'New Stake' is shown. 'New Stake' Value is taken from ValidateBet request
        """
        pass

    def test_003_verify_that_potential_return_is_shown_as_new_potential_return(self):
        """
        DESCRIPTION: Verify that 'Potential Return' is shown as 'New Potential Return'
        EXPECTED: 'Potential Return' is shown as 'New Potential Return'
        """
        pass

    def test_004_stay_in_edit_mode_and_in_same_time_change_price_for_one_of_the_selectionsverify_that_any_changes_in_the_prices_is_reflected_on_the_stake_and_potential_returns(self):
        """
        DESCRIPTION: Stay in edit mode and in same time change price for one of the selections
        DESCRIPTION: Verify that any changes in the Prices is reflected on the Stake and Potential Returns
        EXPECTED: - New Stake and Potential Returns is taken from ValidateBet request
        """
        pass

    def test_005_repeat_steps_1_4_on_cashout_tab(self):
        """
        DESCRIPTION: Repeat steps 1-4 on 'Cashout' Tab
        EXPECTED: 
        """
        pass
