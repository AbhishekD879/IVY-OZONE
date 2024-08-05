import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C23229012_Vanilla__Quick_Bet_Verify_Quick_Deposit_section_for_users_without_payment_methods(Common):
    """
    TR_ID: C23229012
    NAME: [Vanilla] - [Quick Bet] Verify Quick Deposit section for users without payment methods
    DESCRIPTION: This test case verifies Quick Deposit section within Quick Bet for users without payment methods
    DESCRIPTION: AUTOTEST [C49357308]
    PRECONDITIONS: 1. Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
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

    def test_003_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        EXPECTED: * Quick Bet is displayed at the bottom of the page
        EXPECTED: * Added selection and all data are displayed in Quick Bet
        EXPECTED: * 'Make a Deposit' button is displayed and disabled
        """
        pass

    def test_004_enter_some_value_in_stake_field_manually_or_use_quick_stake__buttons(self):
        """
        DESCRIPTION: Enter some value in 'Stake' field manually or use 'Quick Stake ' buttons
        EXPECTED: * 'Stake' field is populated with entered value
        EXPECTED: * 'Make a Deposit' is enabled
        """
        pass

    def test_005_tap_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap 'Make a Deposit' button
        EXPECTED: User is redirected to 'Deposit' page
        """
        pass

    def test_006_add_any_card_as_payment_method_fill_in_all_required_fieldstap_deposit_button(self):
        """
        DESCRIPTION: Add any card as payment method, fill in all required fields
        DESCRIPTION: Tap Deposit button
        EXPECTED: 'Your deposit has been successful' message appears
        """
        pass

    def test_007_tap_ok_button(self):
        """
        DESCRIPTION: Tap 'OK' button
        EXPECTED: User is redirected to Quick Bet
        EXPECTED: Place Bet button is available and active
        """
        pass
