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
class Test_C49918134_Vanilla__Quick_Bet_Verify_Quick_Deposit_section_for_users_with_0_balance_and_added_payment_method(Common):
    """
    TR_ID: C49918134
    NAME: [Vanilla] - [Quick Bet]  Verify Quick Deposit section for users with 0 balance and added payment method
    DESCRIPTION: This test case verifies Quick Deposit section within Quick Bet for users with 0 balance and added payment method
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

    def test_002_log_in_with_user_that_has_0_on_his_balance_and_added_payment_method_to_his_account(self):
        """
        DESCRIPTION: Log in with user that has 0 on his balance and added payment method to his account
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
        EXPECTED: * 'Make a Deposit' becomes enabled
        """
        pass

    def test_005_tap_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap 'Make a Deposit' button
        EXPECTED: Quick Deposit iFrame opens
        """
        pass

    def test_006_enter_cvvtap_deposit_and_place_bet_button(self):
        """
        DESCRIPTION: Enter CVV
        DESCRIPTION: Tap 'Deposit and Place Bet' button
        EXPECTED: Quick Bet is opened
        EXPECTED: Bet is successfully placed
        """
        pass
