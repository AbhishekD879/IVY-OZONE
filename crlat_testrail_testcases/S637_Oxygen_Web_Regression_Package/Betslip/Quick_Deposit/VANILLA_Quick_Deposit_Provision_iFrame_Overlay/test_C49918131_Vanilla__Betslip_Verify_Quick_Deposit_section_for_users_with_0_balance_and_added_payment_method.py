import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C49918131_Vanilla__Betslip_Verify_Quick_Deposit_section_for_users_with_0_balance_and_added_payment_method(Common):
    """
    TR_ID: C49918131
    NAME: [Vanilla] - [Betslip] Verify Quick Deposit section for users with 0 balance and added payment method
    DESCRIPTION: This test case verifies Quick Deposit section within Betslip for users with 0 balance and added payment method
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_the_application(self):
        """
        DESCRIPTION: Load the application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_log_in_with_user_that_has_0_on_his_balance_and_added_payment_method_to_his_account(self):
        """
        DESCRIPTION: Log in with user that has 0 on his balance and added payment method to his account
        EXPECTED: User is logged in
        """
        pass

    def test_003_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip
        EXPECTED: Selection is added
        """
        pass

    def test_004_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: Quick Deposit iFrame is automatically opened in Betslip
        """
        pass

    def test_005_enter_any_value_in_deposit_amount_fieldenter_cvvclicktap_deposit_and_place_bet_button(self):
        """
        DESCRIPTION: Enter any value in Deposit amount field
        DESCRIPTION: Enter CVV
        DESCRIPTION: Click/Tap 'Deposit and Place Bet' button
        EXPECTED: For Coral 'Please Enter A Stake For At Least One Bet' message appears above the Total Stake
        EXPECTED: For Ladbrokes 'Please Enter A Stake For At Least One Bet' message appears in the top for few seconds
        EXPECTED: Deposit is successful
        """
        pass
