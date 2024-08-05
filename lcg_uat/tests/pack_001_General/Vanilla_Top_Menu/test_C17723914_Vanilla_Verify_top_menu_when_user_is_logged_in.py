import pytest
from tests.base_test import vtest
from tests.Common import Common


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.portal_only_test
@pytest.mark.high
@pytest.mark.navigation
@pytest.mark.desktop
@pytest.mark.top_menu
@pytest.mark.login
@vtest
class Test_C17723914_Vanilla_Verify_top_menu_when_user_is_logged_in(Common):
    """
    TR_ID: C17723914
    NAME: [Vanilla] Verify top menu when user is logged in
    DESCRIPTION: This test case is to verify top menu when user is logged in
    PRECONDITIONS: User has an account on QA environment
    """
    keep_browser_open = True

    def test_001_verify_top_menu_when_user_is_not_logged_in(self):
        """
        DESCRIPTION: Verify top menu when user is not logged in
        EXPECTED: Top menu contains following menu options:
        EXPECTED: - Join
        EXPECTED: - Login
        """
        self.site.wait_content_state(state_name='HomePage')
        self.assertTrue(self.site.header.sign_in.is_displayed(), msg='Top menu does not contain "Login" option')
        self.assertTrue(self.site.header.join_us.is_displayed(), msg='Top menu does not contain "Join" option')

    def test_002_click_login_button(self):
        """
        DESCRIPTION: Click/tap login button
        EXPECTED: Login form appears
        """
        self.site.login(async_close_dialogs=False)

    def test_003_enter_valid_credentials_and_click_log_in_button(self):
        """
        DESCRIPTION: Enter valid credentials and click Log in button
        EXPECTED: User is logged in.
        EXPECTED: Top menu items are changed to:
        EXPECTED: For **Desktop**:
        EXPECTED: - Deposit;
        EXPECTED: - 'Balance' button with user`s balance;
        EXPECTED: - My Inbox;
        EXPECTED: - My Account
        EXPECTED: For **Mobile**:
        EXPECTED: - My Bets;(Only Coral)
        EXPECTED: - 'Balance' button with user`s balance;
        EXPECTED: - My account;
        EXPECTED: - 'Betslip' icon with a number of added selections in a bubble or without bubble if no selections are added to betslip
        """
        self.assertTrue(self.site.header.has_right_menu(),
                        msg='Top menu does not contain "My Account" option')
        self.assertTrue(self.site.header.user_panel.balance.is_displayed(),
                        msg='Top menu does not contain "Balance" option')
        if self.device_type == 'mobile':
            self.assertTrue(self.site.header.has_bet_slip_counter(),
                            msg='Top menu does not contain "Betslip" option')
            if self.brand == 'bma':
                self.assertTrue(self.site.header.my_bets.is_displayed(),
                                msg='Top menu does not contain "My Bets" option')
        else:
            self.assertTrue(self.site.header.user_panel.deposit_button.is_displayed(),
                            msg='Top menu does not contain "Deposit" option')
            self.assertTrue(self.site.header.user_panel.my_inbox_button.is_displayed(),
                            msg='Top menu does not contain "My Inbox" option')

    def test_004_click_deposit_button_desktop(self):
        """
        DESCRIPTION: Click Deposit button (Desktop)
        EXPECTED: User is taken to deposit/add payment method page
        """
        if self.device_type != 'mobile':
            self.site.header.user_panel.deposit_button.click()
            self.assertTrue(self.site.deposit.is_displayed(), msg=f'"Deposit" is not opened')

    def test_005_tap_my_bets_mobile(self):
        """
        DESCRIPTION: Tap My bets (mobile)
        EXPECTED: User is taken to Open Bets tab
        """
        if self.device_type == 'mobile':
            self.site.open_my_bets_open_bets()

    def test_006_click_my_inbox_button_desktop(self):
        """
        DESCRIPTION: Click/tap My Inbox button (Desktop)
        EXPECTED: My Inbox window opens with the list of user's messages
        """
        if self.device_type != 'mobile':
            self.site.deposit.close_button.click()
            self.site.wait_content_state(state_name='HomePage')
            self.site.header.user_panel.my_inbox_button.click()
            self.assertTrue(self.site.my_inbox.is_displayed(),
                            msg='"My Inbox" window is not displayed')

    def test_007_close_my_inbox_window_and_click_my_account_button(self):
        """
        DESCRIPTION: Close My Inbox window and click/tap My Account button
        EXPECTED: Right menu is opened
        """
        if self.device_type != 'mobile':
            self.site.my_inbox.close_button.click()
            self.site.header.right_menu_button.click()
            self.assertTrue(self.site.right_menu.is_displayed(),
                            msg='"Right menu" is not displayed')
