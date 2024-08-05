import pytest

import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.currency
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.navigation
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C28085_Verify_Currency_on_the_Global_Header_for_Desktop(BaseUserAccountTest):
    """
    TR_ID: C28085
    VOL_ID: C9698162
    NAME: Verify Currency on the Global Header for Desktop
    DESCRIPTION: This test case verifies Currency on the Universal Header for Desktop.
    PRECONDITIONS: *   Make sure you have 4 registered users with different currency settings: **GBP**, **EUR**, **USD**
    PRECONDITIONS: In order to verify currency symbol use:
    PRECONDITIONS: *   'GBP': symbol = ' **£** ';
    PRECONDITIONS: *   'USD': symbol = ' **$** ';
    PRECONDITIONS: *   'EUR': symbol = ' **€** ';
    """
    currency_GBP = 'GBP'
    currency_USD = 'USD'
    currency_EUR = 'EUR'
    keep_browser_open = True
    device_name = tests.desktop_default

    def check_currency_symbol(self, currency):
        currency_symbol = {'GBP': '£', 'USD': '$', 'EUR': '€'}
        actual_currency = self.site.header.user_balance_section.currency_symbol
        expected_currency = currency_symbol[currency]

        self.assertEqual(actual_currency, expected_currency,
                         msg=f'Actual currency symbol is "{actual_currency}". '
                             f'Expected currency symbol "{currency_symbol}" is not shown.')

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        self.__class__.user_EUR = tests.settings.user_with_euro_currency_and_card
        self.__class__.user_USD = tests.settings.user_with_usd_currency_and_card
        self.__class__.user_GBP = tests.settings.betplacement_user
        self.site.wait_content_state('Homepage')

    def test_002_log_in_user_with_gbp_currency(self):
        """
        DESCRIPTION: Log in user with **GBP** currency
        EXPECTED: User is logged in successfully
        """
        self.site.login(username=self.user_GBP)

    def test_003_verify_currency_symbol_near_the_user_balance(self):
        """
        DESCRIPTION: Verify currency symbol near the user balance
        EXPECTED: Currency symbol displayed matches users' currency
        """
        self.check_currency_symbol(self.currency_GBP)

    def test_004_log_out_from_application(self):
        """
        DESCRIPTION: Log out from application
        EXPECTED: User is logged out successfully
        """
        self.site.logout()

    def test_005_log_in_user_with_eur_currency(self):
        """
        DESCRIPTION: Log in user with '**EUR** ' currency
        EXPECTED: User is logged in successfully
        """
        self.site.login(username=self.user_EUR, async_close_dialogs=False, timeout_close_dialogs=5)

    def test_006_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps 3-4
        EXPECTED: The same as on the steps 3-4
        """
        self.check_currency_symbol(self.currency_EUR)
        self.site.logout()

    def test_007_log_in_user_with_usd_currency(self):
        """
        DESCRIPTION: Log in user with '**USD** ' currency
        EXPECTED: User is logged in successfully
        """
        self.site.login(username=self.user_USD, async_close_dialogs=False, timeout_close_dialogs=5)

    def test_008_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps 3-4
        EXPECTED: The same as on the steps 3-4
        """
        self.check_currency_symbol(self.currency_USD)
        self.site.logout()
