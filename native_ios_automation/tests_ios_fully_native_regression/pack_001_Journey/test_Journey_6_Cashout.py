import pytest
import tests_ios_fully_native_regression as tests
from time import sleep
from tests_ios_fully_native_regression.base_test import BaseTest


@pytest.mark.native
class Test_Journey_6_Cash_Out(BaseTest):
    """
    NAME: Cashout
    DESCRIPTION: This test case verifies cash out functionality
    """

    def test_001_open_app(self):
        """
        Open The Native App
        """
        homepage = self.native_app.home_page
        self.assertTrue(homepage, msg="App not opened")

    def test_002_login_into_app(self):
        """
        Click on Login CTA
        Enter Credentials
        Click On Login Button to Confirm Login
        """
        if tests.settings.brand != 'bma':
            self.native_app.login(username="testgvcld_RT2JIW")
        else:
            self.native_app.login(username="testgvccl-U3AW6E")
        sleep(5)
        buttons = self.native_app.home_page.bet_buttons
        buttons.pop().click()
        self.native_app.home_page.quick_bet_stake_input = "0.1"
        self.native_app.home_page.quick_bet_place_bet.click()
        self.native_app.home_page.quick_bet_receipt_close_button.click()

    def test_003_navigate_to_my_bets(self):
        """
        Click MY BETS in the footer items
        """
        self.native_app.home_page.my_bets_footer_item.click()
        sleep(5)

    def test_004_verify_cashout(self):
        """
        Click on Cash out
        Click on Confirm Cash out
        Cash out is succsessful
        """
        self.native_app.home_page.cash_out.click()  # Cash out
        sleep(1)
        self.native_app.home_page.cash_out.click()  # Confirm Cash out
        self.assertTrue(self.native_app.home_page.cash_out_successful, msg='Cash out is not successful')
