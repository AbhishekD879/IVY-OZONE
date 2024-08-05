import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C17410295_Vanilla__Verify_Withdraw_for_account_without_enough_funds_on_balance_for__Skrill1tap(Common):
    """
    TR_ID: C17410295
    NAME: [Vanilla] - Verify Withdraw for account without enough funds on balance for - Skrill1tap
    DESCRIPTION: The purpose of TC is verification that the user cannot withdraw more funds that are placed to the wallet.
    PRECONDITIONS: 1. User logged to the application;
    PRECONDITIONS: 2. User has a positive balance;
    PRECONDITIONS: 3. Visa direct (Through Safecharge) Payment method added;
    """
    keep_browser_open = True

    def test_001_open_withdrawal_menu__user_avatar_icon__cashier__withdrawal(self):
        """
        DESCRIPTION: Open Withdrawal menu:
        DESCRIPTION: - User "Avatar" icon > Cashier > Withdrawal;
        EXPECTED: The withdrawal menu page is opened;
        """
        pass

    def test_002_select_the_visa_direct_through_safecharge_payment_method(self):
        """
        DESCRIPTION: Select the Visa direct (Through Safecharge) payment method;
        EXPECTED: Payment method is selected and withdrawal page is opened;
        """
        pass

    def test_003_enter_sum_that_exceeds_user_ballance_and_perform_the_withdrawal(self):
        """
        DESCRIPTION: Enter sum that exceeds user ballance and perform the Withdrawal
        EXPECTED: Error message is displayed:
        EXPECTED: - "The Withdrawal amount can not be greater than your available balance."
        """
        pass