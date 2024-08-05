import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C16761013_Vanilla__Cashier_Withdraw_issuing_for_insufficient_funds_on_the_account_general_flow(Common):
    """
    TR_ID: C16761013
    NAME: [Vanilla] - Cashier Withdraw  issuing for insufficient funds on the account (general flow)
    DESCRIPTION: The purpose of TC is verification that the user cannot withdraw more funds that are placed to the wallet.
    PRECONDITIONS: 1. User logged to the application;
    PRECONDITIONS: 2. User has a positive balance;
    PRECONDITIONS: 3. Payment method added;
    """
    keep_browser_open = True

    def test_001_open_withdrawal_menu__user_avatar_icon__cashier__withdrawal(self):
        """
        DESCRIPTION: Open Withdrawal menu:
        DESCRIPTION: - User "Avatar" icon > Cashier > Withdrawal;
        EXPECTED: The withdrawal menu page is opened;
        """
        pass

    def test_002_select_payment_method_eg_visa(self):
        """
        DESCRIPTION: Select payment method (e.g. VISA)
        EXPECTED: Payment method is selected and withdrawal page is opened;
        """
        pass

    def test_003_enter_sum_that_exceeds_user_ballance_and_perform_withdrawal(self):
        """
        DESCRIPTION: Enter sum that exceeds user ballance and perform Withdrawal
        EXPECTED: Error message is displayed:
        EXPECTED: - "The Withdrawal amount can not be greater than your available balance."
        """
        pass
