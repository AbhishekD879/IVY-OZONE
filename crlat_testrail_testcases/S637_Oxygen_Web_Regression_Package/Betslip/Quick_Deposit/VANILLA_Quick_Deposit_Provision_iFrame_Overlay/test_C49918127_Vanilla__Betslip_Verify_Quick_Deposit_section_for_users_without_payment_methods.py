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
class Test_C49918127_Vanilla__Betslip_Verify_Quick_Deposit_section_for_users_without_payment_methods(Common):
    """
    TR_ID: C49918127
    NAME: [Vanilla] - [Betslip]  Verify Quick Deposit section for users without payment methods
    DESCRIPTION: This test case verifies Quick Deposit section within Betslip for users without payment methods
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_the_application(self):
        """
        DESCRIPTION: Load the application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_log_in_with_user_that_has_0_on_his_balance_and_no_payment_methods_added_to_his_account(self):
        """
        DESCRIPTION: Log in with user that has 0 on his balance and no payment methods added to his account
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
        EXPECTED: * Betslip is opened with added selection
        EXPECTED: * 'Make a Deposit' button is displayed and disabled
        """
        pass

    def test_005_enter_some_value_in_stake_field(self):
        """
        DESCRIPTION: Enter some value in 'Stake' field
        EXPECTED: * 'Stake' field is populated with entered value
        EXPECTED: * 'Make a Deposit' button becomes enabled
        """
        pass

    def test_006_clicktap_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Click/tap on 'Make a Deposit' button
        EXPECTED: Deposit page is opened
        """
        pass

    def test_007_add_any_card_as_payment_method_fill_in_all_required_fieldstap_deposit_button(self):
        """
        DESCRIPTION: Add any card as payment method, fill in all required fields.
        DESCRIPTION: Tap 'Deposit' button
        EXPECTED: 'Your deposit has been successful' message appears
        """
        pass

    def test_008_tap_ok_buttonopen_betslip(self):
        """
        DESCRIPTION: Tap 'OK' button
        DESCRIPTION: Open Betslip
        EXPECTED: 'Place Bet' button is available and active
        """
        pass
