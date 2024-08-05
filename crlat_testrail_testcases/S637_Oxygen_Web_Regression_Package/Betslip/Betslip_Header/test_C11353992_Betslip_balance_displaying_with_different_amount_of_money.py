import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C11353992_Betslip_balance_displaying_with_different_amount_of_money(Common):
    """
    TR_ID: C11353992
    NAME: Betslip: balance displaying with different amount of money
    DESCRIPTION: This test case verifies balance displaying when user has low or huge account balance
    PRECONDITIONS: - You should have 2 users:
    PRECONDITIONS: 1) User with low account balance (e.g. 1-100)
    PRECONDITIONS: 2) User with huge account balance (e.g. 123,321,123.00)
    PRECONDITIONS: - You should be logged in with user with low account balance and betslip should be opened
    """
    keep_browser_open = True

    def test_001_verify_betslip_label_and_balance_displaying(self):
        """
        DESCRIPTION: Verify 'Betslip' label and balance displaying
        EXPECTED: 'Betslip' label is centered within betslip header
        EXPECTED: **Coral**
        EXPECTED: - Balance is displayed and centered within the dark blue account balance area at the top right corner
        EXPECTED: **Ladbrokes**
        EXPECTED: - Balance is displayed and centered within the dark red account balance area at the top right corner
        """
        pass

    def test_002_make_a_bet_and_verify_bet_receipt_label_and_balance_displaying(self):
        """
        DESCRIPTION: Make a bet and verify 'Bet Receipt' label and balance displaying
        EXPECTED: 'Bet Receipt' label is centered within betslip header
        EXPECTED: **Coral**
        EXPECTED: - Balance is displayed and centered within the dark blue account balance area at the top right corner
        EXPECTED: **Ladbrokes**
        EXPECTED: - Balance is displayed and centered within the dark red account balance area at the top right corner
        """
        pass

    def test_003___logout_and_login_with_user_with_huge_account_balance__open_betslip_and_verify_balance_displaying(self):
        """
        DESCRIPTION: - Logout and login with user with huge account balance
        DESCRIPTION: - Open betslip and verify balance displaying
        EXPECTED: Account balance area is respectively extended
        EXPECTED: 'Betslip' label is respectively moved to the left within betslip header not to overlap with account balance
        EXPECTED: **Coral**
        EXPECTED: - Balance is displayed and centered within the dark blue account balance area at the top right corner
        EXPECTED: **Ladbrokes**
        EXPECTED: - Balance is displayed and centered within the dark red account balance area at the top right corner
        """
        pass

    def test_004_make_a_bet_and_verify_bet_receipt_label_and_balance_displaying(self):
        """
        DESCRIPTION: Make a bet and verify 'Bet Receipt' label and balance displaying
        EXPECTED: Account balance area is respectively extended
        EXPECTED: 'Bet Receipt' label is respectively moved to the left within betslip header not to overlap with account balance
        EXPECTED: **Coral**
        EXPECTED: - Balance is displayed and centered within the dark blue account balance area at the top right corner
        EXPECTED: **Ladbrokes**
        EXPECTED: - Balance is displayed and centered within the dark red account balance area at the top right corner
        """
        pass
