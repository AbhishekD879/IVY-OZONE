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
class Test_C9337877_Verify_the_flow_after_tapping_the_Confirm_button_in_My_Bet_Acca_Edit_mode(Common):
    """
    TR_ID: C9337877
    NAME: Verify the flow after tapping the 'Confirm' button in My Bet/Acca Edit mode
    DESCRIPTION: This test case verifies the flow after tapping the 'Confirm' button in My Bet/Acca Edit mode
    DESCRIPTION: Ladbrokes : https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b?seid=5c4f1e8c4def2a015bb81cea
    DESCRIPTION: Coral : https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3?seid=5be15e2ea472811f68583124
    DESCRIPTION: AUTOMATED [C12861507] [C12996539]
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: Login into App
    PRECONDITIONS: Place Multiple bet
    PRECONDITIONS: Navigate to the Bet History from Right/User menu
    PRECONDITIONS: Go to 'Open Bets' Tab -> verify that 'Edit My Bet/Acca' button is available
    PRECONDITIONS: Go to 'Cash Out' Tab -> verify that 'Edit My Bet/Acca' button is available
    PRECONDITIONS: Tap on 'Edit My  Bet/Acca' button -> verify that user is in 'My  Bet/Acca Edit' mode
    PRECONDITIONS: NOTE: 'Edit My BET/ACCA' button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    """
    keep_browser_open = True

    def test_001_tap_on_the_selection_removal_button_to_remove_a_selection_from_their_original_acca(self):
        """
        DESCRIPTION: Tap on the 'Selection Removal' button to remove a selection from their original Acca
        EXPECTED: The selection is removed from their original Acca
        """
        pass

    def test_002_verify_that_the_confirm_button_is_displayed_and_click_able(self):
        """
        DESCRIPTION: Verify that the Confirm button is displayed and click-able
        EXPECTED: The 'Confirm' button is displayed and click-able
        """
        pass

    def test_003_make_sure_that_there_are_no_price_updates_to_any_open_selections_from_the_original_acca_and_there_are_no_suspended_selections_on_the_original_acca(self):
        """
        DESCRIPTION: Make sure that there are no price updates to any open selections from the original Acca and there are no suspended selections on the original Acca
        EXPECTED: 
        """
        pass

    def test_004_click_the_confirm_button_and_verify_that_the_original_bet_is_cashed_out(self):
        """
        DESCRIPTION: Click the 'Confirm' button and verify that the original bet is cashed out
        EXPECTED: The original bet is cashed out
        """
        pass

    def test_005_verify_that_no_funds_are_sent_or_requested_from_the_users_account(self):
        """
        DESCRIPTION: Verify that no funds are sent or requested from the users account
        EXPECTED: No funds are sent or requested from the users account
        """
        pass

    def test_006_verify_that_the_successful_confirmation_message_is_shown_under_the_confirm_button(self):
        """
        DESCRIPTION: Verify that the successful confirmation message is shown under the 'Confirm' button
        EXPECTED: Successful confirmation message is shown under the 'Confirm' button
        """
        pass

    def test_007_verify_content_of_confirmation_message(self):
        """
        DESCRIPTION: Verify content of confirmation message
        EXPECTED: Text: 'Acca Edited Successfully' is displayed
        """
        pass
