import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
# @pytest.mark.crl_hl  # can't grant freebets on prod
# @pytest.mark.crl_prod
@pytest.mark.user_account
@pytest.mark.freebets
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C28222_Verify_Freebet_Pop_up_content_and_appearance_after_LogIn(BaseUserAccountTest):
    """
    TR_ID: C28222
    NAME: Verify Freebet Pop-up content and appearance after LogIn
    """
    keep_browser_open = True
    dialog = None
    username = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create new user and add several freebet bonuses
        EXPECTED: User is created
        EXPECTED: Freebet bonuses are granted
        """
        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=self.username, async_close_dialogs=False)

        self.site.logout()
        [self.ob_config.grant_freebet(username=self.username) for _ in range(0, 5)]

    def test_001_tap_log_in_button(self):
        """
        DESCRIPTION: Tap 'Log In' button
        EXPECTED: 'Log In' pop-up is displayed
        """
        self.site.header.sign_in.click()
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(self.dialog, msg='Login dialog is not present on page')

    def test_002_enter_valid_user_with_positive_freebet_balance_credentials_and_tap_log_in_button(self):
        """
        DESCRIPTION: Enter valid user with positive freebet balance credentials and tap 'Log In' button
        EXPECTED: User is logged in successfully.
        EXPECTED: 'Free Bet' pop-up is shown (last in the queue of pop-up messages).
        """
        self.site.login(username=self.username,
                        ignored_dialogs=vec.dialogs.DIALOG_MANAGER_FREE_BETS_TOKEN_DESCRIPTION,
                        async_close_dialogs=False,
                        timeout_wait_for_dialog=1)

        freebet_token_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_FREE_BETS_TOKEN_DESCRIPTION)
        self.assertTrue(freebet_token_dialog, msg='Freebet dialog is not shown for user with freebets: "%s"' % self.username)
        self.__class__.dialog = freebet_token_dialog

    def test_003_compare_information_displayed_in_pop_up_with_data_received_from_preconditions(self):
        """
        DESCRIPTION: Compare information displayed in pop-up with data received from Preconditions
        EXPECTED: The data must match:
        EXPECTED: *   Free bet description = "freebetOfferName"
        EXPECTED: *   Expiry date = "freebetTokenExpiryDate"
        EXPECTED: *   Value = "freebetTokenValue"
        EXPECTED: *   Total sum of Free bets at the top of table
        """
        total_freebet_sum = 0
        tokens = self.dialog.items_as_ordered_dict
        self.assertTrue(tokens, msg='*** No one dialog token was found')
        for token_name, token in tokens.items():
            self._logger.debug('*** Freebet Token name "%s" value "%s" expiry date "%s"' %
                               (token.name, token.value, token.expiry_date))
            total_freebet_sum += float(token.value)

        self.assertEqual(float(self.dialog.freebet_sum), total_freebet_sum,
                         msg='Freebet sum from popup "%s" do not equal to sum of all Freebet Tokens "%s"' % (
                             self.dialog.freebet_sum, total_freebet_sum))

    def test_004_check_buttons_on_free_bet_pop_up(self):
        """
        DESCRIPTION: Check buttons on 'Free Bet' pop-up
        EXPECTED: Pop-up includes an X and an OK button to close the pop-up
        """
        self.assertTrue(self.dialog.has_close_button(), msg='"Close" Button is not shown')
        self.assertTrue(self.dialog.ok_button.is_displayed(), msg='"OK" Button is not shown')

    def test_005_close_the_pop_up_selecting_x_or_ok_button(self):
        """
        DESCRIPTION: Close the pop-up selecting X or OK button
        EXPECTED: Pop-up is closed
        """
        self.dialog.click_ok()
        dialog_closed = self.dialog.wait_dialog_closed()
        self.assertTrue(dialog_closed, msg='Dialog is not closed after pressing \'OK\' button')
        self.site.close_all_dialogs(async_close=False)

    def test_006_log_out_and_log_in_under_the_same_user(self):
        """
        DESCRIPTION: Log out and log in under the same user
        EXPECTED: User is logged in successfully.
        EXPECTED: Free Bet pop-up is not shown
        """
        self.site.logout()
        self.assertTrue(self.site.wait_logged_out(), msg='User is not logged out')
        self.site.login(username=self.username, ignored_dialogs=vec.dialogs.DIALOG_MANAGER_FREE_BETS_TOKEN_DESCRIPTION, async_close_dialogs=False)

        freebet_token_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_FREE_BETS_TOKEN_DESCRIPTION, timeout=5)
        self.assertFalse(freebet_token_dialog, msg='Freebet dialog is shown again for user "%s" after second login' % self.username)
        self.site.close_all_dialogs(async_close=False)

    def test_007_log_out_from_oxygen_application(self):
        """
        DESCRIPTION: Log out from Oxygen application
        EXPECTED: User is logged out successfully
        """
        self.site.logout()

    def test_008_add_new_freebet_for_user(self):
        """
        DESCRIPTION: Add new freebet for user
        EXPECTED: Free bet is received and shown on Header in freebet balance
        """
        self.ob_config.grant_freebet(username=self.username)

    def test_009_log_in_under_the_same_user(self):
        """
        DESCRIPTION: Log in under the same user
        EXPECTED: User is logged in successfully.
        EXPECTED: Free Bet pop-up is shown with information of all available for user freebets
        """
        self.site.login(username=self.username, ignored_dialogs=vec.dialogs.DIALOG_MANAGER_FREE_BETS_TOKEN_DESCRIPTION, async_close_dialogs=False)

        freebet_token_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_FREE_BETS_TOKEN_DESCRIPTION)
        self.assertTrue(freebet_token_dialog, msg='Freebet dialog is not shown for user with freebets: "%s"' % self.username)
