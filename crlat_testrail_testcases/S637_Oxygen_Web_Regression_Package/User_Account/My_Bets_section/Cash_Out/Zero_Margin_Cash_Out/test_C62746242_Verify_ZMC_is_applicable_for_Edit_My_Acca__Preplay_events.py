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
class Test_C62746242_Verify_ZMC_is_applicable_for_Edit_My_Acca__Preplay_events(Common):
    """
    TR_ID: C62746242
    NAME: Verify ZMC is applicable  for Edit My Acca _ Preplay events
    DESCRIPTION: This test case verifies ZMC is applicable  for  Edit My Acca (Preplay events)
    PRECONDITIONS: * 'No Loss' profile is configured in 'Cash out profile' field at category level in OB for respective sports
    PRECONDITIONS: * 'is Off': "NO" and "N/A" at event level in OB
    PRECONDITIONS: * Make sure no generic bet offers are running currently in OB
    PRECONDITIONS: * Login to application and place Multiple bets
    PRECONDITIONS: NOTE: 'Edit My ACCA' button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    PRECONDITIONS: NOTE: Should be run on:
    PRECONDITIONS: - Cash Out tab;
    PRECONDITIONS: - Open Bets tab;
    PRECONDITIONS: - Bet History;
    """
    keep_browser_open = True

    def test_001_navigate_to_open_bets_tab__gt_verify_that_edit_my_acca_button_is_available(self):
        """
        DESCRIPTION: Navigate to 'Open Bets' Tab -&gt; verify that 'Edit My Acca' button is available
        EXPECTED: 'Edit My Acca' button should be displayed
        """
        pass

    def test_002_tap_on_edit_my_acca_button(self):
        """
        DESCRIPTION: Tap on 'Edit My Acca' button
        EXPECTED: User should be on 'My Acca Edit' mode
        """
        pass

    def test_003_remove_selection_from_my_acca_edit_modetap_confirm_button(self):
        """
        DESCRIPTION: Remove selection from 'My Acca Edit' mode
        DESCRIPTION: Tap 'Confirm' button
        EXPECTED: user should successfully edited their Acca
        """
        pass

    def test_004_verify_that_the_new_bet_type_name_is_displayed(self):
        """
        DESCRIPTION: Verify that the new bet type name is displayed
        EXPECTED: The new bet type name should be displayed
        """
        pass

    def test_005_verify_that_the_stake_is_displayed(self):
        """
        DESCRIPTION: Verify that the stake is displayed
        EXPECTED: The stake is displayed
        EXPECTED: New stake value is received from validateBet request - 'newBetStake' parameter
        """
        pass

    def test_006_verify_the_cash_out_value(self):
        """
        DESCRIPTION: Verify the Cash Out value
        EXPECTED: Cash Out value should be same as New stake amount
        """
        pass

    def test_007_verify_the_network_call_in_ws(self):
        """
        DESCRIPTION: Verify the Network call in WS
        EXPECTED: WS call should consists of below attributes
        EXPECTED: * cash out Profile: "NO_LOSS"
        EXPECTED: * cash out Value: "X" (where X is the Total Stake amount)
        EXPECTED: * is Off: "-" or "N"
        """
        pass

    def test_008_tap_cash_out_buttonverify_that_green_confirm_cash_out_cta_is_shown(self):
        """
        DESCRIPTION: Tap 'CASH OUT' button
        DESCRIPTION: Verify that green 'CONFIRM CASH OUT' CTA is shown
        EXPECTED: 'CONFIRM CASH OUT' CTA with bet placed stake value should be displayed
        """
        pass

    def test_009_tap_confirm_cash_out_button_and_verify_user_balance(self):
        """
        DESCRIPTION: Tap 'CONFIRM CASH OUT' button and Verify user balance
        EXPECTED: Cash Out should be successful and User balance should be increased
        """
        pass
