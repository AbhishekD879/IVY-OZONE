import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@pytest.mark.login
@pytest.mark.desktop
@vtest
class Test_C16268965_Vanilla_Successful_Log_Out(Common):
    """
    TR_ID: C16268965
    NAME: [Vanilla] Successful Log Out
    DESCRIPTION: This test case verifies user logging out
    PRECONDITIONS: User is logged In
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: User is logged In
        """
        self.site.login()

    def test_001_click_on_my_account_button__log_out_button(self):
        """
        DESCRIPTION: Click on 'My Account' button --> 'Log Out' button
        DESCRIPTION: ![](index.php?/attachments/get/34287) -->  ![](index.php?/attachments/get/34288)
        EXPECTED: * User is logged out
        EXPECTED: * 'JOIN' and 'LOG IN' buttons are displayed in the header
        EXPECTED: * User Balance is not shown any more
        EXPECTED: ![](index.php?/attachments/get/34256)
        EXPECTED: * User is not able to access Right Menu, User Account menu, Deposit, Withdrawal pages
        EXPECTED: * **FOR Desktop**'Log In' button is displayed on Cash Out, Open Bets, Bet History, Favourites page/widget
        """
        self.site.logout()
        self.assertTrue(self.site.header.join_us.is_displayed(),
                        msg='"JOIN" button is not visible on the screen')
        self.assertTrue(self.site.header.sign_in.is_displayed(),
                        msg='"LOG IN" button is not visible on the screen')

        self.assertFalse(self.site.header.has_right_menu(expected_result=False),
                         msg='User still able to access right menu button')

        if self.device_type == 'desktop':
            cashout_cms_tab = self.get_initial_data_system_configuration().get('CashOut', {})
            if not cashout_cms_tab:
                cashout_cms_tab = self.cms_config.get_system_configuration_item('CashOut')
            if cashout_cms_tab.get('isCashOutTabEnabled'):
                self.site.open_my_bets_cashout()
                result = self.site.betslip.tabs_menu.current
                self.assertEqual(result, vec.bet_history.CASH_OUT_TAB_NAME,
                                 msg=f'"{vec.bet_history.CASH_OUT_TAB_NAME}" was not opened. Was opened "{result}" tab')
                if self.brand != 'ladbrokes':
                    self.assertTrue(self.site.cashout.tab_content.has_login_button(),
                                    msg='"Log In" button is not shown at the "CASH OUT" tab')
            else:
                self._logger.warning('*** Cash out tab is disabled in CMS')

            self.site.open_my_bets_open_bets()
            result = self.site.betslip.tabs_menu.current
            self.assertEqual(result, vec.bet_history.OPEN_BETS_TAB_NAME,
                             msg=f'"{vec.bet_history.OPEN_BETS_TAB_NAME}" was not opened. Was opened "{result}" tab')

            if self.brand != 'ladbrokes':
                self.assertTrue(self.site.open_bets.tab_content.has_login_button(),
                                msg='"Log In" button is not shown at the "OPEN BETS" tab')

            self.site.open_my_bets_settled_bets()
            result = self.site.betslip.tabs_menu.current
            self.assertEqual(result, vec.bet_history.SETTLED_BETS_TAB_NAME,
                             msg=f'"{vec.bet_history.SETTLED_BETS_TAB_NAME}" was not opened. Was opened "{result}" tab')

            if self.brand != 'ladbrokes':
                self.assertTrue(self.site.bet_history.login_button.is_displayed(),
                                msg='"Log In" button is not shown at the "SETTLED BETS" tab')

            # this step is valid for Coral brand
            if not self.brand == 'ladbrokes':
                if not self.cms_config.get_widgets(widget_type='favourites')[0]['disabled']:
                    self.assertTrue(self.site.favourites.login_button.is_displayed(),
                                    msg='"Log In" button is not shown on the "FAVOURITES" widget')
