import pytest
import tests
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C1377332_Verify_Settled_Bets_tab_when_user_is_logged_out(Common):
    """
    TR_ID: C1377332
    NAME: Verify 'Settled Bets' tab when user is logged out
    DESCRIPTION: This test case verifies login from 'Settled Bets' tab
    PRECONDITIONS:
    """
    keep_browser_open = True

    def test_001_open_settled_bets_tabmobile_my_bets_page___settled_betstabletdesktop_bet_slip_widget___settled_betsuse_direct_url_bet_history(self):
        """
        DESCRIPTION: Open 'Settled Bets' tab
        DESCRIPTION: Mobile: 'My Bets' page -> 'Settled Bets'
        DESCRIPTION: Tablet/Desktop: 'Bet Slip' widget -> 'Settled Bets'
        DESCRIPTION: (Use direct URL: .../Bet-history)
        EXPECTED: * 'Settled Bets' tab is opened
        EXPECTED: * "Please log in to see your Settled Bets." message is displayed
        EXPECTED: * "Log In" button is shown below the message
        """
        self.site.wait_content_state('Homepage', timeout=5)
        if self.device_type == 'mobile':
            self.navigate_to_page(name='bet-history')
            self.site.wait_content_state(state_name='BetHistory')
        else:
            self.site.open_my_bets_settled_bets()
        self.__class__.settled_bets = self.site.bet_history.tab_content
        self.assertEqual(self.settled_bets.please_login_text, vec.BetHistory.SETTLED_BETS_PLEASE_LOGIN_MESSAGE,
                         msg=f'Actual: "{self.settled_bets.please_login_text}" is not equal '
                             f'to expected: "{vec.BetHistory.SETTLED_BETS_PLEASE_LOGIN_MESSAGE}"')
        # For ladbrokes: login button is not available
        if self.brand == 'bma':
            self.assertTrue(self.settled_bets.has_login_button(), msg=f'"{vec.bma.LOGIN}"button not displayed.')

    def test_002_log_in_from_settled_bets_tab(self):
        """
        DESCRIPTION: Log in from 'Settled Bets' tab
        EXPECTED: *   User is logged in
        EXPECTED: *   Content of page is visible
        """
        if self.brand == 'bma':
            self.settled_bets.login_button.click()
            self.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
            self.assertTrue(self.dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not displayed')
            self.dialog.username = tests.settings.default_username
            self.dialog.password = tests.settings.default_password
            self.dialog.click_login()
            sleep(3)
            settled_bets_item = self.settled_bets.accordions_list.items_as_ordered_dict
            if len(settled_bets_item) > 0:
                self.assertTrue(settled_bets_item, msg='SETTLED BETS tab has no bets to display.')
            else:
                no_settled_bets_text = self.settled_bets.accordions_list.no_bets_text
                self.assertEqual(no_settled_bets_text, vec.bet_history. NO_HISTORY_INFO,
                                 msg=f'Actual text: "{no_settled_bets_text}" is not equal with the'
                                     f'Expected text: "{vec.bet_history. NO_HISTORY_INFO}"')
