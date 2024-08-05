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
class Test_C9726423_Verify_that_partial_cash_out_journey_stops_when_EDIT_MY_ACCA_Bet_button_is_tapped(Common):
    """
    TR_ID: C9726423
    NAME: Verify that partial cash out journey stops when 'EDIT MY ACCA/Bet' button is tapped
    DESCRIPTION: This test case verifies that Partial cash out journey stops and not shown when 'EDIT MY ACCA' button is tapped
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: Login and place a multiple bet with Partial Cash Out available
    PRECONDITIONS: Navigate to My Bets page
    PRECONDITIONS: NOTE: Verifications should be done on Cash Out and on Open Bets tabs
    """
    keep_browser_open = True

    def test_001_tap_partial_cash_out_button_for_placed_betverify_that_edit_my_accabet_button_and_partial_cash_out_bar_are_shown(self):
        """
        DESCRIPTION: Tap 'Partial Cash Out' button for placed bet
        DESCRIPTION: Verify that 'EDIT MY ACCA/Bet' button and Partial Cash Out bar are shown
        EXPECTED: - 'EDIT MY ACCA/Bet' button is shown and enable
        EXPECTED: - Partial Cash Out bar is shown
        """
        pass

    def test_002_move_partial_cash_out_slider_to_change_partial_cash_out_valueverify_that_value_is_changing_and_edit_my_accabet_button_is_shown(self):
        """
        DESCRIPTION: Move partial cash out slider to change partial cash out value
        DESCRIPTION: Verify that value is changing and 'EDIT MY ACCA/Bet' button is shown
        EXPECTED: - 'EDIT MY ACCA/Bet' button is shown and enable
        EXPECTED: - Partial Cash Out value is changing
        """
        pass

    def test_003_tap_edit_my_accabet_buttonthat_partial_cash_out_journey_is_not_shown_and_edit_mode_for_acca_is_opened(self):
        """
        DESCRIPTION: Tap 'EDIT MY ACCA/Bet' button
        DESCRIPTION: that Partial cash out journey is not shown and edit mode for ACCA is opened
        EXPECTED: - Partial Cash Out journey is closed and not shown
        EXPECTED: - Cash Out and Partial Cash Out button is not shown at all
        EXPECTED: - Edit mode for ACCA is opened
        """
        pass

    def test_004_tap_cancel_editing_buttonverify_that_edit_mode_for_acca_is_closed_and_cash_out_and_partial_cash_out_button_is_shown(self):
        """
        DESCRIPTION: Tap 'Cancel Editing' button
        DESCRIPTION: Verify that edit mode for ACCA is closed and Cash Out and Partial Cash Out button is shown
        EXPECTED: - Edit mode for ACCA is closed
        EXPECTED: - Cash Out and Partial Cash Out button is shown
        """
        pass
