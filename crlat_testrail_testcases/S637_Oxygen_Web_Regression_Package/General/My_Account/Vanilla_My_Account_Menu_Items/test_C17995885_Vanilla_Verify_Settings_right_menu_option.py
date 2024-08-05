import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C17995885_Vanilla_Verify_Settings_right_menu_option(Common):
    """
    TR_ID: C17995885
    NAME: [Vanilla] Verify Settings right menu option
    DESCRIPTION: This test case is to verify all option menus under Settings right menu option
    DESCRIPTION: Test case need to be updated as Settings menu buttons are different for Coral and Ladbrokes
    PRECONDITIONS: User has account on QA env
    """
    keep_browser_open = True

    def test_001_log_in_to_test_env(self):
        """
        DESCRIPTION: Log in to test env
        EXPECTED: User is logged in, My Account button appears
        """
        pass

    def test_002_clicktap_my_account_button(self):
        """
        DESCRIPTION: Click/tap My Account button
        EXPECTED: Right menu is displayed
        """
        pass

    def test_003_clicktap_settings_menu_option(self):
        """
        DESCRIPTION: Click/tap Settings menu option
        EXPECTED: Settings menu is displayed with the following options:
        EXPECTED: - My Account Details
        EXPECTED: - Change Password
        EXPECTED: - Marketing References
        EXPECTED: - Betting Settings
        """
        pass

    def test_004_clicktap_my_account_details_option(self):
        """
        DESCRIPTION: Click/tap My Account Details option
        EXPECTED: My Account Details page is displayed
        """
        pass

    def test_005_reopen_right_menu__settings_and_clicktap_change_password_option(self):
        """
        DESCRIPTION: Reopen right menu-> Settings and click/tap Change Password option
        EXPECTED: User is taken to Change Password page
        """
        pass

    def test_006_reopen_right_menu__settings_and_clicktap_marketing_references_option(self):
        """
        DESCRIPTION: Reopen right menu-> Settings and click/tap Marketing References option
        EXPECTED: User is taken to Communication Preferences page
        """
        pass

    def test_007_reopen_right_menu__settings_and_clicktap_betting_settings_option(self):
        """
        DESCRIPTION: Reopen right menu-> Settings and click/tap Betting Settings option
        EXPECTED: User is taken to Betting Settings page
        """
        pass
