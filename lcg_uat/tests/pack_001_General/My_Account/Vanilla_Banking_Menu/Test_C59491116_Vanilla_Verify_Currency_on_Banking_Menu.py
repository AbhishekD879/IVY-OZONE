import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.user_account
@vtest
class Test_C59491116_Vanilla_Verify_Currency_on_Banking_Menu(BaseUserAccountTest):
    """
    TR_ID: C59491116
    NAME: [Vanilla] Verify Currency on 'Banking' Menu
    DESCRIPTION: This test case verifies Currency displaying on 'Banking'/'Banking & Balances' Menu
    PRECONDITIONS: 1) Make sure you have registered users with different currency settings:
    PRECONDITIONS: GBP, AUD, EUR, NOK, NZD, CHF, USD - for Ladbrokes
    PRECONDITIONS: EUR, GBP, USD - for Coral
    PRECONDITIONS: 2) In order to verify currency symbol use:
    PRECONDITIONS: 'GBP': symbol =
    PRECONDITIONS: 'AUD': symbol = AUD
    PRECONDITIONS: 'EUR': symbol =
    PRECONDITIONS: 'NOK': symbol = NOK
    PRECONDITIONS: 'NZD': symbol = NZD
    PRECONDITIONS: 'CHF': symbol = CHF
    PRECONDITIONS: 'USD': symbol =
    """
    currency_GBP = 'GBP'
    currency_USD = 'USD'
    currency_EUR = 'EUR'

    keep_browser_open = True

    def check_currency_symbol(self, currency):
        actual_currency = self.site.right_menu.my_balance.currency_symbol
        if self.brand != 'bma' and currency == "USD":
            expected_currency = "US$"
        else:
            expected_currency = self.currency_symbols[currency]
        self.assertEqual(actual_currency, expected_currency,
                         msg=f'Actual currency symbol is "{actual_currency}". '
                             f'Expected currency symbol "{self.currency_symbols}" is not shown.')

    def test_001_log_in_with_user_with_gbp_currency(self):
        """
        DESCRIPTION: Log in with user with **GBP** currency
        EXPECTED: User is logged in successfully
        """
        self.__class__.user_EUR = tests.settings.user_with_euro_currency_and_card
        self.__class__.user_USD = tests.settings.user_with_usd_currency_and_card
        self.__class__.user_GBP = tests.settings.betplacement_user
        self.site.wait_content_state('Homepage')
        self.site.login(username=self.user_GBP)

    def test_002_navigate_to_my_account__bankingbanking__balances_my_balance(self):
        """
        DESCRIPTION: Navigate to My Account > 'Banking'/'Banking & Balances'> 'My Balance'
        EXPECTED: 'My Balance' item is opened
        """
        self.assertTrue(self.site.header.right_menu_button.is_displayed(),
                        msg='[My Account] button is not displayed on Header')
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open My Account Menu')
        my_balance_text = self.site.window_client_config.get_gvc_config_item_text(key_title='name',
                                                                                  value_title='balance')
        cashier_menu_title = self.site.window_client_config.cashier_menu_title
        self.site.right_menu.click_item(item_name=cashier_menu_title)
        self.site.wait_content_state_changed(timeout=5)
        self.site.right_menu.click_item(item_name=my_balance_text)

        sections = self.site.right_menu.my_balance.items_names
        right_menu_deposit_items = self.site.window_client_config.get_gvc_config_item(key_title='menuRoute',
                                                                                      value_title='menu/balance')
        my_balance_items = self.site.window_client_config.get_gvc_config_item(key_title='name',
                                                                              value_title='balanceitems',
                                                                              context=right_menu_deposit_items)
        expected_my_balance_title = []
        for item in my_balance_items.get('children'):
            if item.get('name') != 'inplay' and item.get('name') != 'withdrawableinshop' and \
                    item.get('name') != 'negative' and item.get('name') != 'restricted':
                expected_my_balance_title.append(item.get('text').upper() if self.brand == 'bma' else item.get('text'))
        # 'restricted' item is skipped as we cannot identify whether it'll be displayed
        status = all(item in sections for item in expected_my_balance_title)

        self.assertTrue(status,
                        msg=f'Actual Menu items "{set(sections)}" != Expected "{set(expected_my_balance_title)}')

        self.assertTrue(self.site.right_menu.my_balance.deposit_button.is_displayed(),
                        msg='Deposit button is not present')
        self.assertTrue(self.site.right_menu.my_balance.available_to_use.is_displayed(),
                        msg='Available to use on table is not present')

    def test_003_verify_currency_symbol_next_to_the_user_balances(self, currency=currency_GBP):
        """
        DESCRIPTION: Verify currency symbol next to the user balances
        EXPECTED: Currency symbol matches with the currency symbol as per user's settings set during registration
        """
        self.check_currency_symbol(currency)

    def test_004_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: User is logged out successfully
        """
        self.navigate_to_page('Homepage')
        self.site.wait_content_state('Homepage')
        self.site.logout()

    def test_005_repeat_steps_1_4_for_user_with_aud_currency(self):
        """
        DESCRIPTION: Repeat steps 1-4 for user with **AUD** currency
        EXPECTED: Currency symbol properly displayed
        """
        # TODO as of now we are not able to create users with this currency

    def test_006_repeat_steps_1_4_for_user_with_eur_currency(self):
        """
        DESCRIPTION: Repeat steps 1-4 for user with **EUR** currency
        EXPECTED: Currency symbol properly displayed
        """
        self.site.login(username=self.user_EUR)
        self.test_002_navigate_to_my_account__bankingbanking__balances_my_balance()
        self.test_003_verify_currency_symbol_next_to_the_user_balances(currency=self.currency_EUR)
        self.test_004_log_out()

    def test_007_repeat_steps_1_4_for_user_with_nok_currency(self):
        """
        DESCRIPTION: Repeat steps 1-4 for user with **NOK** currency
        EXPECTED: Currency symbol properly displayed
        """
        # TODO as of now we are not able to create users with this currency

    def test_008_repeat_steps_1_4_for_user_with_nzd_currency(self):
        """
        DESCRIPTION: Repeat steps 1-4 for user with **NZD** currency
        EXPECTED: Currency symbol properly displayed
        """
        # TODO as of now we are not able to create users with this currency

    def test_009_repeat_steps_1_4_for_user_with_chf_currency(self):
        """
        DESCRIPTION: Repeat steps 1-4 for user with **CHF** currency
        EXPECTED: Currency symbol properly displayed
        """
        # TODO as of now we are not able to create users with this currency

    def test_010_repeat_steps_1_4_for_user_with_usd_currency(self):
        """
        DESCRIPTION: Repeat steps 1-4 for user with **USD** currency
        EXPECTED: Currency symbol properly displayed
        """
        self.site.login(username=self.user_USD)
        self.test_002_navigate_to_my_account__bankingbanking__balances_my_balance()
        self.test_003_verify_currency_symbol_next_to_the_user_balances(currency=self.currency_USD)
        self.test_004_log_out()
