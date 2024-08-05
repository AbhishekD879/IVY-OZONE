import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.mobile_only
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870349_Verify_that_user_balance_is_displayed_on_the_header_in_the_right_menu_when_user_does_not_hide_the_balance(Common):
    """
    TR_ID: C44870349
    NAME: Verify that user balance is displayed on the header in the right menu when user does not hide the balance.
    DESCRIPTION: Not applicable for Desktop
    PRECONDITIONS: User is logged in the application.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: login to application
        """
        self.site.login()

    def test_001_click_on_betslip__balance__xxxxx_(self):
        """
        DESCRIPTION: Click on Betslip > Balance (£ XXX.XX) >
        EXPECTED: Hide Balance / Deposit
        EXPECTED: options are available
        """
        self.site.open_betslip()
        self.assertTrue(self.site.has_betslip_opened(), msg='Failed to open Betslip')
        self.assertTrue(self.get_betslip_content().header.user_balance_amount,
                        msg='User Balance is not displayed on Betslip Header')
        self.assertTrue(self.get_betslip_content().hide_balance_option.is_displayed(),
                        msg='"Hide Balance" option is not available in balance dropdown')
        self.get_betslip_content().balance_button.click()
        self.assertTrue(self.get_betslip_content().quick_deposit_link.is_displayed(),
                        msg='"Deposit" option is not availale in balance dropdown')
        self.get_betslip_content().balance_button.click()

    def test_002_click_on_hide_balance_and_verify(self):
        """
        DESCRIPTION: Click on Hide balance and verify.
        EXPECTED: The user's account balance is not displayed in the header area. Thus, the user's balance is hidden displayed as BALANCE
        """
        self.get_betslip_content().hide_balance_option.click()
        actual_result = self.get_betslip_content().header.user_balance_amount
        self.assertEqual(actual_result, vec.betslip.BALANCE,
                         msg=f'User balance is not displayed as "{vec.betslip.BALANCE}" word. Actual: "{actual_result}"')

    def test_003_close_the_betslip_and_againclick_on_betslip__balance__xxxxx(self):
        """
        DESCRIPTION: Close the 'Betslip' and again
        DESCRIPTION: Click on Betslip > Balance (£ XXX.XX)
        EXPECTED: Show Balance / Deposit
        EXPECTED: options are available
        """
        self.site.close_betslip()
        self.assertFalse(self.site.has_betslip_opened(expected_result=False),
                         msg='Betslip is not closed')
        self.site.open_betslip()
        self.assertTrue(self.site.has_betslip_opened(), msg='Failed to open Betslip')
        actual_result = self.get_betslip_content().header.user_balance_amount
        self.assertEqual(actual_result, vec.betslip.BALANCE,
                         msg=f'User balance is not displayed as "{vec.betslip.BALANCE}" word. Actual: "{actual_result}"')
        self.assertTrue(self.get_betslip_content().hide_balance_option.is_displayed(),
                        msg='"Show Balance" option is not available in balance dropdown')
        self.get_betslip_content().balance_button.click()
        self.assertTrue(self.get_betslip_content().quick_deposit_link.is_displayed(),
                        msg='"Deposit" option is not availale in balance dropdown')
        self.get_betslip_content().balance_button.click()

    def test_004_click_on_show_balance_and_verify(self):
        """
        DESCRIPTION: Click on Show balance and verify.
        EXPECTED: The user's account balance is displayed in the header area along with the corresponding currency symbol.
        """
        self.get_betslip_content().hide_balance_option.click()
        self.assertTrue(self.get_betslip_content().header.user_balance_amount,
                        msg='User Balance is not displayed on Betslip Header')
