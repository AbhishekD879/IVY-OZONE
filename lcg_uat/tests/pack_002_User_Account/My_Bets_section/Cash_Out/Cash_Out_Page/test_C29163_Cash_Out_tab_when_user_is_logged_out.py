import voltron.environments.constants as vec
import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.crl_tst2  # it is always disabled for Ladbrokes
@pytest.mark.crl_stg2
@pytest.mark.crl_prod
@pytest.mark.crl_hl
@pytest.mark.user_account
@pytest.mark.cash_out
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C29163_Cash_Out_tab_when_user_is_logged_out(BaseCashOutTest):
    """
    TR_ID: C29163
    NAME: Cash Out tab when user is logged out
    DESCRIPTION: This test case verifies 'Cash Out' tab when the user is logged out
    PRECONDITIONS: **JIRA ticket:** BMA-3925, BMA-17728
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Verify CashOut tab configuration in CMS
        """
        system_config = self.get_initial_data_system_configuration()
        cashout_cms = system_config.get('CashOut')
        if not cashout_cms:
            cashout_cms = self.cms_config.get_system_configuration_item('CashOut')
        if not cashout_cms:
            raise CmsClientException('CashOut section not found in System Configuration')
        if not cashout_cms.get('isCashOutTabEnabled'):
            raise CmsClientException('CashOut tab is not enabled in CMS')

    def test_001_go_to_my_bets_page_bet_slip_widget(self):
        """
        DESCRIPTION: Go to 'My Bets' page / 'Bet Slip' widget
        EXPECTED: 'My Bets' page / 'Bet Slip' widget is opened
        """
        if self.device_type == 'desktop':
            self.site.open_my_bets_cashout()
        else:
            footer_items = self.site.navigation_menu.items_as_ordered_dict
            footer_items.get(self.my_bets_tab_name).click()
            self.site.cashout.tabs_menu.click_item(vec.bet_history.CASHOUT)

    def test_002_observe_cash_out_tab(self):
        """
        DESCRIPTION: Observe 'Cash Out' tab
        EXPECTED: **"Please log in to see your Cash Out bets."** message is displayed
        EXPECTED: **'Log In'** button is shown below the message
        """
        if self.device_type == 'mobile':
            active_tab = self.site.cashout.tabs_menu.current
            self.assertEqual(active_tab, vec.bet_history.CASHOUT,
                             msg=f'Current tab is: "{active_tab}", not the same as expected: "{vec.bet_history.CASHOUT}"')
        cashout = self.site.cashout.tab_content
        self.assertTrue(cashout.please_login_text, msg='"Please login" text is not shown')
        self.assertEqual(cashout.please_login_text, vec.bet_history.CASHOUT_PLEASE_LOGIN_MESSAGE,
                         msg=f'Actual "Please login text": "{cashout.please_login_text}" is not equal '
                             f'to expected: "{vec.bet_history.CASHOUT_PLEASE_LOGIN_MESSAGE}"')
        if self.brand != 'ladbrokes':
            self.assertTrue(cashout.has_login_button(), msg='Login button is not shown')

    def test_003_log_in_from_cash_out_tab(self):
        """
        DESCRIPTION: Log in from 'Cash Out' tab
        EXPECTED: User is logged in
        EXPECTED: Content of page is visible
        """
        if self.brand != 'ladbrokes':
            self.site.cashout.tab_content.login_button.click()
            username = tests.settings.betplacement_user
            self.site.login(username=username, timeout_wait_for_dialog=2)
            self.assertTrue(self.site.cashout.tab_content.accordions_list,
                            msg='Cashout content is not visible after login')
