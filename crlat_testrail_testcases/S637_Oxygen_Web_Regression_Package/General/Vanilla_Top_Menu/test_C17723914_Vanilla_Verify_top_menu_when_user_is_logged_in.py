import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.navigation
@vtest
class Test_C17723914_Vanilla_Verify_top_menu_when_user_is_logged_in(Common):
    """
    TR_ID: C17723914
    NAME: [Vanilla] Verify top menu when user is logged in
    DESCRIPTION: This test case is to verify top menu when user is logged in
    DESCRIPTION: AUTOTEST [C48896797]
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
        pass

    def test_002_coral_clicktap_login_buttonladbrokes_clicktap_log_injoin_in_buttonfor_mobile__ladbrokes_has_1_button_log_injoin__coral_has_2_buttons_log_in_and_joinfor_desktop__ladbrokes_and_coral_has_2_buttons_log_in_and_join(self):
        """
        DESCRIPTION: Coral: Click/tap Login button
        DESCRIPTION: Ladbrokes: Click/tap Log in/Join in button
        DESCRIPTION: For **Mobile**:
        DESCRIPTION: - Ladbrokes has 1 button Log in/Join
        DESCRIPTION: - Coral has 2 buttons Log in and Join
        DESCRIPTION: For **Desktop**:
        DESCRIPTION: - Ladbrokes and Coral has 2 buttons Log in and Join
        EXPECTED: Login form appears
        """
        pass

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
        EXPECTED: - My Bets; (Only Coral)
        EXPECTED: - 'Balance' button with user`s balance;
        EXPECTED: -  My account;
        EXPECTED: - 'Betslip' icon with a number of added selections in a bubble or without bubble if no selections are added to betslip
        """
        pass

    def test_004_click_deposit_button_desktop(self):
        """
        DESCRIPTION: Click Deposit button (Desktop)
        EXPECTED: User is taken to deposit/add payment method page
        """
        pass

    def test_005_tap_my_bets_mobile(self):
        """
        DESCRIPTION: Tap My bets (mobile)
        EXPECTED: User is taken to Open Bets tab
        """
        pass

    def test_006_clicktap_my_inbox_button_desktop(self):
        """
        DESCRIPTION: Click/tap My Inbox button (Desktop)
        EXPECTED: My Inbox window opens with the list of user's messages
        """
        pass

    def test_007_close_my_inbox_window_and_clicktap_my_account_button(self):
        """
        DESCRIPTION: Close My Inbox window and click/tap My Account button
        EXPECTED: Right menu is opened
        """
        pass
