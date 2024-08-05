import voltron.environments.constants as vec
import pytest
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.crl_tst2  # it is always disabled for Ladbrokes
@pytest.mark.crl_stg2
@pytest.mark.crl_prod
@pytest.mark.crl_hl
@pytest.mark.cash_out
@pytest.mark.portal_dependant
@pytest.mark.desktop
@pytest.mark.low
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C146507_Cash_Out_tab_when_there_are_no_bets_available_for_cash_out(BaseUserAccountTest):
    """
    TR_ID: C146507
    NAME: 'Cash Out' tab when there are no bets available for cash out
    DESCRIPTION: This test case verifies 'Cash Out' tab when the customer has no bets available for cash out.
    DESCRIPTION: Design:
    DESCRIPTION: Coral: https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3/screen/5c4f0e0933fdc7bf07d0508e
    DESCRIPTION: Ladbrokes: https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b/screen/5c4f1ce6e3b4a8bf92cfcf5f
    PRECONDITIONS: *   User is logged in;
    PRECONDITIONS: *   User has no bets available for cash out.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Verify CashOut tab configuration in CMS
        DESCRIPTION: Load Oxygen application and login as user with no bets available for cash out
        """
        system_config = self.get_initial_data_system_configuration()
        cashout_cms = system_config.get('CashOut')
        if not cashout_cms:
            cashout_cms = self.cms_config.get_system_configuration_item('CashOut')
        if not cashout_cms:
            raise CmsClientException('CashOut section not found in System Configuration')
        self.__class__.is_cashout_tab_enabled = cashout_cms.get('isCashOutTabEnabled')
        if not self.is_cashout_tab_enabled:
            raise CmsClientException('CashOut tab is not enabled in CMS')

        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username, close_all_banners=False, timeout_close_dialogs=3, async_close_dialogs=False)
        self.site.wait_content_state('Homepage', timeout=30)

    def test_001_navigate_to_cash_out_tab_on_my_bets_page_bet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/ 'Bet Slip' widget
        EXPECTED: 'Cash out' tab has opened
        """
        self.site.open_my_bets_cashout()

    def test_002_verify_cash_out_tab(self):
        """
        DESCRIPTION: Verify 'Cash Out' tab
        EXPECTED: * Text 'You currently have no cash out bets '(Coral)/ You currently have no bets available for cash out(Ladbrokes) is present
        EXPECTED: * Button 'Start betting'(Coral)/'Go betting'(Ladbrokes) is displayed according to design - Available from OX99
        """
        self.__class__.cashout = self.site.cashout.tab_content.accordions_list
        self.assertTrue(self.cashout.no_bets_text, msg='"You have no Cash Out bets available" text is not present')
        self.assertEqual(self.cashout.no_bets_text, vec.bet_history.NO_CASHOUT_BETS,
                         msg=f'Message "{self.cashout.no_bets_text}" does not match expected '
                             f'"{vec.bet_history.NO_CASHOUT_BETS}"')
        if self.device_type == 'mobile':
            self.assertTrue(self.cashout.start_betting_button, msg='"Start beating" button is not displayed')

    def test_003_tap_start_betting_go_betting_button(self):
        """
        DESCRIPTION: Tap 'Start betting'/'Go betting' button
        EXPECTED: User is redirected to the Home page
        """
        if self.device_type == 'mobile':
            self.cashout.start_betting_button.click()
            self.site.wait_content_state('HomePage')
