import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C59491115_Vanilla_Verify_automatic_balance_updating_on_Banking_menu(Common):
    """
    TR_ID: C59491115
    NAME: [Vanilla] Verify automatic balance updating on 'Banking' menu
    DESCRIPTION: This test case verifies automatic balance updating in Banking menu
    PRECONDITIONS: User should have at least one payment method registered for his/her account (e.g. credit/debit card with money) to have ability to perform Deposit and Withdraw actions
    PRECONDITIONS: 1. Login into application with user who has positive balance
    PRECONDITIONS: 2. Navigate to My Account > 'Banking'/'Banking & Balances' menu > 'My Balance'
    """
    keep_browser_open = True

    def test_001_place_a_bet_and_verify_balance_info_displayed_in_banking_menu(self):
        """
        DESCRIPTION: Place a bet and verify balance info displayed in 'Banking' menu
        EXPECTED: Balance is updated automatically after successful bet placement, it is decremented by entered stake
        """
        pass

    def test_002_verify_balance_in_case_you_win_a_bet(self):
        """
        DESCRIPTION: Verify Balance in case you win a bet
        EXPECTED: Balance is updated automatically in Banking menu, it is incremented by 'Total Estimated Return'
        """
        pass

    def test_003_make_a_deposit_to_your_account_and_verify_balance_info_displayed_in_banking_menu(self):
        """
        DESCRIPTION: Make a deposit to your account and verify balance info displayed in Banking menu
        EXPECTED: Balance is updated immediately in Banking menu, it is incremented by entered Deposit amount
        """
        pass

    def test_004_perform_withdraw_action_from_users_account_and_verify_balance_info_displayed_in_banking_menu(self):
        """
        DESCRIPTION: Perform Withdraw action from user's account and verify balance info displayed in Banking menu
        EXPECTED: Balance is updated immediately in Banking menu, it is incremented by entered Withdrawal amount
        """
        pass
