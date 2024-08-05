import pytest
import tests
from tests.Common import Common
from tests.base_test import vtest
import voltron.environments.constants as vec


# @pytest.mark.tst2  # disabled as manual test case is not up to date
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.prod_incident
@pytest.mark.medium
@pytest.mark.user_account
@pytest.mark.desktop
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C28221_Verify_Order_of_Pop_ups_after_LogIn(Common):
    """
    TR_ID: C28221
    NAME: Verify Order of Pop-ups after LogIn
    DESCRIPTION: Verify ordering of pop-ups after successful log in
    PRECONDITIONS: *   The pop-ups appear in a sequence (see step 2) **ONLY IF** appropriate conditions are true (see steps 3-9)
    PRECONDITIONS: *   If a necessary condition is false, an appropriate pop-up does not appear
    PRECONDITIONS: *   Instruction how to grand bonuses: https://confluence.egalacoral.com/display/MOB/How+to+trigger+casino+bonuses
    PRECONDITIONS: The expected sequence of pop-ups after successful login :
    PRECONDITIONS: 1.  Terms and Conditions
    PRECONDITIONS: 2.  Login messages (received from IMS, in open Api websocket: ID: 31027)
    PRECONDITIONS: 3.  Verify Your Account (Netverify)
    PRECONDITIONS: 4.  Deposit Limits
    PRECONDITIONS: 5.  Quick Deposit
    PRECONDITIONS: 6.  Free Bet
    PRECONDITIONS: 7. Odds Boost
    PRECONDITIONS: 8. Free Bet Expiry Message (starting from 99)
    PRECONDITIONS: 9. Casino bonuses
    PRECONDITIONS: For Verifying Your Account (Netverify) specific user is needed, with the following attributes set in IMS system: "suspended":"true" **and **"ageVerificationStatus":"Active Grace period"
    """
    keep_browser_open = True
    dialog = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Verify if KYC is on in CMS
        """
        self.__class__.username = tests.settings.betplacement_user
        kyc_info = self.get_initial_data_system_configuration().get('KYC', {})
        if not kyc_info:
            kyc_info = self.cms_config.get_system_configuration_item('KYC')
        self.__class__.kyc_status = kyc_info.get('enabled')

    def test_001_clicktap_log_in_button(self):
        """
        DESCRIPTION: Click/Tap 'Log In' button
        EXPECTED: 'Log In' form is displayed
        """
        self.site.header.sign_in.click()
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(self.dialog, msg='Login dialog is not present on page')

    def test_002_enter_valid_credentials_and_taplog_in_button(self):
        """
        DESCRIPTION: Enter valid credentials and tap 'Log In' button
        EXPECTED: *   User is logged in successfully
        EXPECTED: *   Welcome 'Sign In successful' pop-up message is NOT displayed
        EXPECTED: *   'Terms and Conditions' pop-up appears
        """
        self._logger.info(f'*** Trying to login with user {self.username}')
        self.dialog.username = self.username
        self.dialog.password = tests.settings.default_password
        self.dialog.click_login()
        dialog_closed = self.dialog.wait_dialog_closed()
        self.assertTrue(dialog_closed, msg='Login dialog was not closed')

    def test_003_verify_the_pop_up_terms_and_conditions(self):
        """
        DESCRIPTION: Verify the pop-up 'Terms and Conditions'
        EXPECTED: The pop-up 'Terms and Conditions' appears in case Terms and Conditions have changed
        """
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_TERMS_AND_CONDITIONS, timeout=3)
        if dialog:
            dialog.default_action()

    def test_004_verify_the_log_in_message_pop_up(self):
        """
        DESCRIPTION: Verify the 'Log In Message' pop up
        EXPECTED: The pop-up 'Log In Message' appears if any
        """
        # We can't do it because it is IMS configurable

    def test_005_verify_appearing__the_very_pop_up_verify_your_account_netverify(self):
        """
        DESCRIPTION: Verify appearing & the very pop-up 'Verify Your Account (Netverify)'
        EXPECTED: The pop-up appears if the user has not been verified by 'NetVerify' service yet
        """
        if not self.kyc_status:
            dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_VERIFY_YOUR_ACCOUNT, timeout=5)
            self.assertTrue(dialog, msg='"Verify Your Account" dialog is not shown')
            dialog.close_dialog()

    def test_006_verify_appearing__the_very_pop_up_deposit_limits(self):
        """
        DESCRIPTION: Verify appearing & the very pop-up 'Deposit Limits'
        EXPECTED: The pop-up 'Deposit Limits' appears if the user has changed deposit limits 24 or more hours ago (during his first LogIn after that)
        """
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_YOU_HAVE_A_PENDING_DEPOSIT_LIMIT_INCREASE, timeout=3)
        if dialog:
            dialog.close_dialog()

    def test_007_verify_appearing__the_very_pop_up_quick_deposit(self):
        """
        DESCRIPTION: Verify appearing & the very pop-up 'Quick Deposit'
        EXPECTED: The pop-up appears if the logged in user's balance is equal to '0'
        """
        if not self.kyc_status:
            user_balance = float(self.site.header.user_balance)
            self._logger.info(f'*** User balance is {user_balance}')
            if not user_balance > 0:
                dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_QUICK_DEPOSIT, timeout=3)
                self.assertTrue(dialog, msg='Quick Deposit dialog is not shown')
                dialog.close_dialog()

    def test_008_verify_appearing__the_very_pop_up_free_bet(self):
        """
        DESCRIPTION: Verify appearing & the very pop-up 'Free Bet'
        EXPECTED: The pop-up appears if only the logged in user's free bet balance is > '0'
        """
        if not self.kyc_status and self.site.header.has_freebets(expected_result=True, timeout=0):
            dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_FREE_BETS_TOKEN_DESCRIPTION, timeout=3)
            self.assertTrue(dialog, msg='FREE BETS TOKEN DESCRIPTION dialog is not shown')
            dialog.close_dialog()

    def test_009_verify_appearing__the_very_pop_up_odds_boost(self):
        """
        DESCRIPTION: Verify appearing & the very pop-up 'Odds Boost'
        EXPECTED: The pop-up appears if new 'Odds boost' token has been awarded. Only for NEW tokens
        """
        if not self.kyc_status:
            dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_ODDS_BOOST, timeout=3)
            self.assertTrue(dialog, msg='"ODDS BOOST" dialog is not shown')
            dialog.close_dialog()

    def test_010_verify_appearing__the_very_free_bet_expiry_message_starting_from_99(self):
        """
        DESCRIPTION: Verify appearing & the very Free Bet Expiry message (starting from 99)
        EXPECTED: The message appears if User has Free Bet expiring within 24 hours
        """
        # Will add it for 99

    def test_011_verify_appearing__the_very_pop_up_casino_bonuses(self):
        """
        DESCRIPTION: Verify appearing & the very pop-up 'Casino bonuses'
        EXPECTED: The pop-up appears if casino bonuses have been added to user`s account.
        """
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CONGRATULATIONS_EX, timeout=3)
        if dialog:
            dialog.decline_button.click()

    def test_012_verify_whether_the_following_sequence_of_pop_ups_is_kept_1__terms_and_conditions2__login_messages_received_from_ims_in_open_api_websocket_id_310273__verify_your_account_netverify4__deposit_limits5__quick_deposit6__free_bet7_odds_boost8_free_bet_expiry_message_starting_from_999_casino_bonuseson_the_login_journey_this_should_be_last_in_the_queue_to_appearif_one_of_the_pop_ups_is_missed_the_next_one_from_the_above_sequence_is_displayed_instead(self):
        """
        DESCRIPTION: Verify whether the following sequence of pop-ups is kept :
        DESCRIPTION: 1.  Terms and Conditions
        DESCRIPTION: 2.  Login messages (received from IMS, in open Api websocket: ID: 31027)
        DESCRIPTION: 3.  Verify Your Account (Netverify)
        DESCRIPTION: 4.  Deposit Limits
        DESCRIPTION: 5.  Quick Deposit
        DESCRIPTION: 6.  Free Bet
        DESCRIPTION: 7. Odds Boost
        DESCRIPTION: 8. Free Bet Expiry Message (starting from 99)
        DESCRIPTION: 9. Casino bonuses
        DESCRIPTION: On the login journey, this should be last in the queue to appear
        DESCRIPTION: If one of the pop-ups is missed, the next one from the above sequence is displayed instead
        EXPECTED:
        """
        # All previous steps do it
