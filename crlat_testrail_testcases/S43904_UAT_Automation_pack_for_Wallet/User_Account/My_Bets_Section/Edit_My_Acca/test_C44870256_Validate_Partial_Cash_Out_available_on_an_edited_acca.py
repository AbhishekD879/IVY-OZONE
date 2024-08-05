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
class Test_C44870256_Validate_Partial_Cash_Out_available_on_an_edited_acca(Common):
    """
    TR_ID: C44870256
    NAME: Validate  Partial Cash Out available on an edited acca
    DESCRIPTION: 
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMB -> Enabled
    PRECONDITIONS: Login and place a multiple bet with Partial Cash Out available
    PRECONDITIONS: Navigate to My Bets page
    """
    keep_browser_open = True

    def test_001_tap_partial_cash_out_button_for_placed_betverify_that_edit_my_bet_button_and_partial_cash_out_bar_are_shown(self):
        """
        DESCRIPTION: Tap 'Partial Cash Out' button for placed bet
        DESCRIPTION: Verify that 'EDIT MY BET' button and Partial Cash Out bar are shown
        EXPECTED: 'EDIT MY BET' button is shown and enable
        EXPECTED: Partial Cash Out bar is shown
        """
        pass

    def test_002_move_partial_cash_out_slider_to_change_partial_cash_out_valueverify_that_value_is_changing_and_edit_my_bet_button_is_shown(self):
        """
        DESCRIPTION: Move partial cash out slider to change partial cash out value
        DESCRIPTION: Verify that value is changing and 'EDIT MY BET' button is shown
        EXPECTED: 'EDIT MY BET' button is shown and enable
        EXPECTED: Partial Cash Out value is changing
        """
        pass

    def test_003_tap_edit_my_bet_buttonthat_partial_cash_out_journey_is_not_shown_and_edit_mode_for_acca_is_opened(self):
        """
        DESCRIPTION: Tap 'EDIT MY BET' button
        DESCRIPTION: that Partial cash out journey is not shown and edit mode for ACCA is opened
        EXPECTED: Partial Cash Out journey is closed and not shown
        EXPECTED: Cash Out and Partial Cash Out button is not shown at all
        EXPECTED: Edit mode for ACCA is opened
        """
        pass

    def test_004_tap_cancel_editing_buttonverify_that_edit_mode_for_acca_is_closed_and_cash_out_and_partial_cash_out_button_is_shown(self):
        """
        DESCRIPTION: Tap 'Cancel Editing' button
        DESCRIPTION: Verify that edit mode for ACCA is closed and Cash Out and Partial Cash Out button is shown
        EXPECTED: Edit mode for ACCA is closed
        EXPECTED: Cash Out and Partial Cash Out button is shown
        """
        pass
