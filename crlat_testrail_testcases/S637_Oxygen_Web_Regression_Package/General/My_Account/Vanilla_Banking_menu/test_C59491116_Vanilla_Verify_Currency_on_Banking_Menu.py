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
class Test_C59491116_Vanilla_Verify_Currency_on_Banking_Menu(Common):
    """
    TR_ID: C59491116
    NAME: [Vanilla] Verify Currency on 'Banking' Menu
    DESCRIPTION: This test case verifies Currency displaying on 'Banking'/'Banking & Balances' Menu
    PRECONDITIONS: 1) Make sure you have registered users with different currency settings:
    PRECONDITIONS: GBP, AUD, EUR, NOK, NZD, CHF, USD - for Ladbrokes
    PRECONDITIONS: EUR, GBP, USD - for Coral
    PRECONDITIONS: 2) In order to verify currency symbol use:
    PRECONDITIONS: 'GBP': symbol = £
    PRECONDITIONS: 'AUD': symbol = AUD
    PRECONDITIONS: 'EUR': symbol = €
    PRECONDITIONS: 'NOK': symbol = NOK
    PRECONDITIONS: 'NZD': symbol = NZD
    PRECONDITIONS: 'CHF': symbol = CHF
    PRECONDITIONS: 'USD': symbol = $
    """
    keep_browser_open = True

    def test_001_log_in_with_user_with_gbp_currency(self):
        """
        DESCRIPTION: Log in with user with **GBP** currency
        EXPECTED: User is logged in successfully
        """
        pass

    def test_002_navigate_to_my_account__bankingbanking__balances_my_balance(self):
        """
        DESCRIPTION: Navigate to My Account > 'Banking'/'Banking & Balances'> 'My Balance'
        EXPECTED: 'My Balance' item is opened
        """
        pass

    def test_003_verify_currency_symbol_next_to_the_user_balances(self):
        """
        DESCRIPTION: Verify currency symbol next to the user balances
        EXPECTED: Currency symbol matches with the currency symbol as per user's settings set during registration
        """
        pass

    def test_004_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: User is logged out successfully
        """
        pass

    def test_005_repeat_steps_1_4_for_user_with_aud_currency(self):
        """
        DESCRIPTION: Repeat steps 1-4 for user with **AUD** currency
        EXPECTED: Currency symbol properly displayed
        """
        pass

    def test_006_repeat_steps_1_4_for_user_with_eur_currency(self):
        """
        DESCRIPTION: Repeat steps 1-4 for user with **EUR** currency
        EXPECTED: Currency symbol properly displayed
        """
        pass

    def test_007_repeat_steps_1_4_for_user_with_nok_currency(self):
        """
        DESCRIPTION: Repeat steps 1-4 for user with **NOK** currency
        EXPECTED: Currency symbol properly displayed
        """
        pass

    def test_008_repeat_steps_1_4_for_user_with_nzd_currency(self):
        """
        DESCRIPTION: Repeat steps 1-4 for user with **NZD** currency
        EXPECTED: Currency symbol properly displayed
        """
        pass

    def test_009_repeat_steps_1_4_for_user_with_chf_currency(self):
        """
        DESCRIPTION: Repeat steps 1-4 for user with **CHF** currency
        EXPECTED: Currency symbol properly displayed
        """
        pass

    def test_010_repeat_steps_1_4_for_user_with_usd_currency(self):
        """
        DESCRIPTION: Repeat steps 1-4 for user with **USD** currency
        EXPECTED: Currency symbol properly displayed
        """
        pass
