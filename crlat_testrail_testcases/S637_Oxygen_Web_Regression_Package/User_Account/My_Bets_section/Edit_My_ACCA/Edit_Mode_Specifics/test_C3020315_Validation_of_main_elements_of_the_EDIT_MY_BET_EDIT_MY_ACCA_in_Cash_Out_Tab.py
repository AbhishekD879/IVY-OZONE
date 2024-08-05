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
class Test_C3020315_Validation_of_main_elements_of_the_EDIT_MY_BET_EDIT_MY_ACCA_in_Cash_Out_Tab(Common):
    """
    TR_ID: C3020315
    NAME: Validation of main elements of the 'EDIT MY BET' /'EDIT MY ACCA' in 'Cash Out' Tab
    DESCRIPTION: This test case verifies removing selection(s) in edit acca
    DESCRIPTION: Ladbrokes : https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b?seid=5c4f1e8c4def2a015bb81cea
    DESCRIPTION: Coral : https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3?seid=5be15e2ea472811f68583124
    DESCRIPTION: AUTOTEST [C12587640]
    PRECONDITIONS: 1. Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: 2. Login into App
    PRECONDITIONS: 3. Place Multiple bet
    PRECONDITIONS: 4. Navigate to the Bet History from Right/User menu
    PRECONDITIONS: 5. Go to 'Cash Out' tab -> verify that 'EDIT MY BET'/'EDIT MY ACCA' button is available
    PRECONDITIONS: NOTE: 'EDIT MY BET/ACCA' button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    """
    keep_browser_open = True

    def test_001_tap_edit_my_bet_coraledit_my_acca_ladbrokes_button(self):
        """
        DESCRIPTION: Tap 'EDIT MY BET' (Coral)/EDIT MY ACCA' (Ladbrokes) button
        EXPECTED: Edit mode of the Acca is available
        """
        pass

    def test_002_click_on_selections_removal_button_to_remove_selections_from_their_original_acca(self):
        """
        DESCRIPTION: Click on Selection(s) Removal button to remove selection(s) from their original Acca
        EXPECTED: - The selection(s) are removed
        EXPECTED: - The selection name(s) for the removed selection is displayed
        EXPECTED: - UNDO button is displayed
        """
        pass

    def test_003_verify_that_new_stake_and_new_est_returnscoral_new_potential_returns_ladbrokes_are_shown(self):
        """
        DESCRIPTION: Verify that 'New Stake' and 'New Est. Returns'(Coral) 'New Potential Returns' (Ladbrokes) are shown
        EXPECTED: 'New Stake' and and 'New Est. Returns'(Coral) 'New Potential Returns' (Ladbrokes) is displayed
        """
        pass

    def test_004_verify_that_cancel_editing_button_is_displayed(self):
        """
        DESCRIPTION: Verify that 'Cancel Editing' Button is displayed
        EXPECTED: 'Cancel Editing' Button is displayed
        """
        pass

    def test_005_verify_that_confirm_button_is_displayed(self):
        """
        DESCRIPTION: Verify that 'Confirm' Button is displayed
        EXPECTED: 'Confirm' Button is displayed
        """
        pass

    def test_006_verify_that_message_is_shown_in_the_bottom(self):
        """
        DESCRIPTION: Verify that message is shown in the bottom
        EXPECTED: Message "Edit My Acca uses the cash out value of this bet and the latest odds of each selection" is shown
        """
        pass
