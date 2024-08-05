import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


@pytest.mark.crl_prod
@pytest.mark.crl_hl
@pytest.mark.crl_tst2  # Coral only, test case is not applicable for Ladbrokes
@pytest.mark.crl_stg2
@pytest.mark.high
@pytest.mark.mobile_only
@pytest.mark.popup
@pytest.mark.login
@pytest.mark.user_account
@pytest.mark.safari
@vtest
class Test_C2211708_C16268964_Accessing_Log_In_popup_Mobile_Mode(BaseUserAccountTest):
    """
    TR_ID: C2211708
    TR_ID: C16268964
    VOL_ID: C9698473
    NAME: Accessing Log In popup Mobile mode
    DESCRIPTION: This test case verifies accessing Log In popup from different places of the application
    PRECONDITIONS: Oxygen app is opened. User is logged out
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Check if Cashout tab is configured in CMS
        """
        initial_data = self.cms_config.get_initial_data(cached=True)
        cashout_cms = initial_data.get('CashOut', {})
        if not cashout_cms:
            system_config = initial_data.get('systemConfiguration', {})
            cashout_cms = system_config.get('CashOut')
        self.__class__.is_cashout_tab_enabled = cashout_cms.get('isCashOutTabEnabled')

    def test_001_check_log_in_button_present_on_the_header(self):
        """
        DESCRIPTION: Check "LOG IN" button is displayed on the screen
        EXPECTED: "LOG IN" button must be displayed on the screen
        """
        self.assertTrue(self.site.header.sign_in.is_displayed(), msg='"LOG IN" button is not displayed on site header')
        self.site.header.sign_in.click()

    def test_002_check_log_in_pop_up_is_displayed(self):
        """
        DESCRIPTION: Check 'Log In' pop-up is displayed on the screen
        EXPECTED: 'Log In' pop-up must be displayed on the screen
        """
        dialog = self.site._wait_for_login_dialog(15)
        self.assertTrue(dialog, '"Log In" pop-up is not displayed')
        dialog.close_dialog()
        self.assertFalse(vec.dialogs.DIALOG_MANAGER_LOG_IN in self.site.dialog_manager.items_as_ordered_dict,
                         msg='"Log In" dialog should not be displayed on the screen')

    def test_003_check_log_in_button_present_on_cash_out(self):
        """
        DESCRIPTION: Check "Log In" button is displayed at "CASH OUT" page
        EXPECTED: "Log In" button must be displayed at "CASH OUT" page
        """
        if not self.is_cashout_tab_enabled:
            self._logger.warning('CashOut tab is not switched on in CMS config')
        else:
            self.navigate_to_page(name='cashout')
            self.site.wait_content_state(state_name='CashOut')
            log_in_button = self.site.cashout.tab_content.login_button
            self.assertTrue(log_in_button.is_displayed(), msg='"Log In" button is not displayed at "CASH OUT" page')
            log_in_button.click()

    def test_004_repeat_step_2_for_cash_out(self):
        """
        DESCRIPTION: Repeat step #2 for 'Cash Out' page
        EXPECTED: Results are the same
        """
        if not self.is_cashout_tab_enabled:
            self._logger.warning('CashOut tab is not switched on in CMS config')
        else:
            self.test_002_check_log_in_pop_up_is_displayed()

    def test_005_check_log_in_button_present_on_open_bets(self):
        """
        DESCRIPTION: Check "Log In" button is displayed at "OPEN BETS" page
        EXPECTED: "Log In" button must be displayed at "OPEN BETS" page
        """
        self.navigate_to_page(name='open-bets')
        self.site.wait_content_state(state_name='OpenBets')
        log_in_button = self.site.open_bets.tab_content.login_button
        self.assertTrue(log_in_button.is_displayed(), msg='"Log In" button is not displayed at "OPEN BETS" page')
        log_in_button.click()

    def test_006_repeat_step_2_for_open_bets(self):
        """
        DESCRIPTION: Repeat step #2 for 'Open Bets' page
        EXPECTED: Results are the same
        """
        self.test_002_check_log_in_pop_up_is_displayed()

    def test_007_check_log_in_button_present_on_bet_history(self):
        """
        DESCRIPTION: Check "Log In" button is displayed at "Settled Bets" page
        EXPECTED: "Log In" button must be displayed at "Settled Bets" page
        """
        self.navigate_to_page(name='bet-history')
        self.site.wait_content_state(state_name='BetHistory')
        log_in_button = self.site.bet_history.login_button
        self.assertTrue(log_in_button.is_displayed(), msg='"Log In" button is not shown at "Settled Bets" page')
        log_in_button.click()

    def test_008_repeat_step_2_for_bet_history(self):
        """
        DESCRIPTION: Repeat step #2 for 'Settled Bets' page
        EXPECTED: Results are the same
        """
        self.test_002_check_log_in_pop_up_is_displayed()

    def test_009_check_log_in_button_present_on_favorite_matches(self):
        """
        DESCRIPTION: Check "Log In" button is displayed at "FAVOURITE MATCHES" page
        EXPECTED: "Log In" button must be displayed at the "FAVOURITE MATCHES" page
        """
        self.navigate_to_page(name='favourites')
        self.site.wait_content_state(state_name='Favourites')
        log_in_button = self.site.favourites.login_button
        self.assertTrue(log_in_button.is_displayed(),
                        msg='"Log In" button is not shown at "FAVOURITE MATCHES" page')
        log_in_button.click()

    def test_010_repeat_step_2_for_favourite_matches(self):
        """
        DESCRIPTION: Repeat step #2 for 'Favourite Matches' page
        EXPECTED: Results are the same
        """
        self.test_002_check_log_in_pop_up_is_displayed()
