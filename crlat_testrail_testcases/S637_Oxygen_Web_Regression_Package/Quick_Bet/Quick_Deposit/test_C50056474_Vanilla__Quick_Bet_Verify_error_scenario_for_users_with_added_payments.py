import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.quick_bet
@vtest
class Test_C50056474_Vanilla__Quick_Bet_Verify_error_scenario_for_users_with_added_payments(Common):
    """
    TR_ID: C50056474
    NAME: [Vanilla]   [Quick Bet] Verify error scenario for users with added payments
    DESCRIPTION: This test case verifies error scenario for users with added payment method
    DESCRIPTION: SCENARIO
    DESCRIPTION: GIVEN User have registered payment methods
    DESCRIPTION: AND He adds selection to a betslip/quickbet
    DESCRIPTION: THAN Vanilla API call is triggered (AC 1) before opening Quick Deposit
    DESCRIPTION: AND returns ERROR (AC 1)
    DESCRIPTION: THAN Oxygen app should redirect User to a deposit page using Cashier link (AC 2)
    DESCRIPTION: AND QD iframe should not be opened
    PRECONDITIONS: Charles is installed and configured
    PRECONDITIONS: Instruction is here:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Charles+-+HTTP%28S%29+Debugging
    """
    keep_browser_open = True

    def test_001_configure_breakpoints_for_quickdepositenabled_response_in_charlesindexphpattachmentsget62756859(self):
        """
        DESCRIPTION: Configure Breakpoints for QuickDepositEnabled response in Charles
        DESCRIPTION: ![](index.php?/attachments/get/62756859)
        EXPECTED: Breakpoints are configured
        """
        pass

    def test_002_add_selection_to_the_quick_betenter_value_bigger_than_users_balance_into_stake_field(self):
        """
        DESCRIPTION: Add selection to the Quick Bet
        DESCRIPTION: Enter value bigger than user's balance into Stake field
        EXPECTED: Selection is added
        EXPECTED: Make a Deposit button is displayed
        """
        pass

    def test_003_tap_on_make_a_deposit_buttonat_the_same_time_open_charles(self):
        """
        DESCRIPTION: Tap on Make a Deposit button
        DESCRIPTION: At the same time open Charles
        EXPECTED: Edit Breakpoints page is opened
        EXPECTED: ![](index.php?/attachments/get/62758464)
        """
        pass

    def test_004_tap_on_edit_response_and_enter_404_instead_of_200_okindexphpattachmentsget62758465tap_execute(self):
        """
        DESCRIPTION: Tap on Edit Response and enter 404 instead of 200 OK
        DESCRIPTION: ![](index.php?/attachments/get/62758465)
        DESCRIPTION: Tap Execute
        EXPECTED: At once second Edit Breakpoints page is opened
        """
        pass

    def test_005_tap_execute_with_200_ok_status_codeobserve_application(self):
        """
        DESCRIPTION: Tap Execute with 200 OK status code
        DESCRIPTION: Observe application
        EXPECTED: Deposit page is opened
        """
        pass

    def test_006_enter_any_amount_of_money_cvv_codetap_deposit_page(self):
        """
        DESCRIPTION: Enter any amount of money, CVV code
        DESCRIPTION: Tap Deposit page
        EXPECTED: Deposit is successfully processed
        """
        pass
