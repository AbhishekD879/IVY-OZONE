import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.uat
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870165_Check_user_sees_message_as_Please_log_in_to_see_your_settled_bets_when_not_logged_in_to_system_and_on_Betslip__Settled_bets_section_Log_in_button_is_available(Common):
    """
    TR_ID: C44870165
    NAME: Check user sees message as 'Please log in to see your settled bets..' when not logged in to system and on Betslip -> Settled bets section. Log in button is available
    DESCRIPTION: Check user sees message as 'Please log in to see your Cashout' when not logged in to system
    DESCRIPTION: Desktop:  Navigate to 'My Bets'
    DESCRIPTION: Mobile: Navigate to 'My bets' via 'Cashout' from the Footer menu
    DESCRIPTION: Log in button is available
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load Application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state("Homepage")

    def test_002_for_mobile__navigate_to_my_bets_via_cashout_from_the_footer_menulog_in_button_is_available(self):
        """
        DESCRIPTION: For mobile:  Navigate to 'My bets' via 'Cashout' from the Footer menu
        DESCRIPTION: Log in button is available
        EXPECTED: My Bets page should open with Cashout page opened by default & check the user sees message as 'Please log in to see your Cashout' when not logged in to system with Log button is available
        """
        # For ladbrokes: open-bets tab is by default
        if self.brand == 'ladbrokes':
            if self.device_type == 'mobile':
                self.navigate_to_page(name='open-bets', test_automation=False)
                self.site.wait_content_state(state_name='OpenBets')
                current_tab = self.site.cashout.tabs_menu.current
            else:
                self.site.open_my_bets()
                self.site.open_my_bets_open_bets()
                current_tab = self.site.betslip.tabs_menu.current

            self.assertEqual(current_tab, vec.bet_history.OPEN_BETS_TAB_NAME,
                             msg=f'Actual text: "{current_tab}" is not as'
                             f'Expected text: "{vec.bet_history.OPEN_BETS_TAB_NAME}"')
            actual_text = self.site.open_bets.tab_content.please_login_text
            self.assertEqual(actual_text, vec.bet_history.OPEN_BETS_PLEASE_LOGIN_MESSAGE,
                             msg=f'Actual text: "{actual_text}" is not equal with the'
                             f'Expected text: "{vec.bet_history.OPEN_BETS_PLEASE_LOGIN_MESSAGE}"')
        else:
            if self.device_type == 'mobile':
                self.navigate_to_page('/cashout', test_automation=False)
                self.site.wait_content_state(state_name='Cashout')
                current_tab = self.site.cashout.tabs_menu.current
            else:
                self.site.open_my_bets_cashout()
                current_tab = self.site.cashout.tab_content.grouping_buttons.current

            self.assertEqual(current_tab, vec.bet_history.CASH_OUT_TAB_NAME,
                             msg=f'Actual text: "{current_tab}" is not as'
                                 f'Expected text: "{vec.bet_history.CASH_OUT_TAB_NAME}"')
            cash_outs = self.site.cashout.tab_content
            actual_text = cash_outs.please_login_text
            self.assertEqual(actual_text, vec.bet_history.CASHOUT_PLEASE_LOGIN_MESSAGE,
                             msg=f'Actual text: "{actual_text}" is not equal with the'
                                 f'Expected text: "{vec.bet_history.CASHOUT_PLEASE_LOGIN_MESSAGE}"')
            self.assertTrue(cash_outs.has_login_button(), msg=f'"{vec.bma.LOGIN}" button not displayed.')

    def test_003_for_desktop__tabletsnavigate_to_my_bets_section___(self):
        """
        DESCRIPTION: For Desktop & Tablets:
        DESCRIPTION: Navigate to My Bets section -->
        EXPECTED: My Bets page should open with Cashout page opened by default & check user sees message as 'Please log in to see your Cashout' when not logged in to system with Log in button available
        """
        # This step is covered in step2.

    def test_004_tap_on_settled_bets_tab(self):
        """
        DESCRIPTION: Tap on Settled bets tab
        EXPECTED: Check 'Please login to see your Settled bets' message is displayed once the user navigates to Settled tabs.
        EXPECTED: Log in button is available
        """
        if self.device_type == 'mobile':
            self.navigate_to_page(name='bet-history')
            self.site.wait_content_state(state_name='BetHistory')
        else:
            self.site.open_my_bets_settled_bets()

        settled_bets = self.site.bet_history.tab_content
        actual_text = settled_bets.please_login_text
        self.assertEqual(actual_text, vec.bet_history.SETTLED_BETS_PLEASE_LOGIN_MESSAGE,
                         msg=f'Actual text: "{actual_text}" is not equal with the'
                             f'Expected text: "{vec.bet_history.SETTLED_BETS_PLEASE_LOGIN_MESSAGE}"')
        # For ladbrokes: login button is not available
        if self.brand == 'bma':
            self.assertTrue(settled_bets.has_login_button(), msg=f'"{vec.bma.LOGIN}"button not displayed.')
