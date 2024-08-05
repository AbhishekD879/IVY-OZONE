import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C18249840_Vanilla_Verify_User_Session_termination_after_password_changing(Common):
    """
    TR_ID: C18249840
    NAME: [Vanilla] Verify User Session termination after password changing
    DESCRIPTION: This test case verifies user session termination after password changing
    PRECONDITIONS: Private mode is switched off on device browser
    """
    keep_browser_open = True

    def test_001_load_to_vanilla_evn_eg_httpqa2sportscoralcouk(self):
        """
        DESCRIPTION: Load to Vanilla evn (e.g. http://qa2.sports.coral.co.uk)
        EXPECTED: The main page should be displayed
        """
        pass

    def test_002_specify__valid_login__valid_password__tick_remember_me_checkbox(self):
        """
        DESCRIPTION: Specify:
        DESCRIPTION: - valid Login
        DESCRIPTION: - valid Password
        DESCRIPTION: - tick "Remember me" checkbox
        EXPECTED: All fields /UI controls fulfilled
        EXPECTED: ![](index.php?/attachments/get/35829)
        """
        pass

    def test_003_click_on_login(self):
        """
        DESCRIPTION: Click on Login
        EXPECTED: User Should be successfully logged in
        """
        pass

    def test_004_click_on_my_account_icon____settings__change_password(self):
        """
        DESCRIPTION: Click on "My Account" icon --> "Settings"--"Change Password"
        EXPECTED: Change Password Page should be opened
        EXPECTED: ![](index.php?/attachments/get/35959)
        """
        pass

    def test_005_specify_old_and_new_password_and_click_on_submit_button(self):
        """
        DESCRIPTION: Specify Old and New password and click on "Submit" button
        EXPECTED: "Password changed successfully!" message should appear
        """
        pass

    def test_006_close_browser(self):
        """
        DESCRIPTION: Close browser
        EXPECTED: n/a
        """
        pass

    def test_007_open_browser_and_load_to_vanilla_evn_eg_httpqa2sportscoralcouk(self):
        """
        DESCRIPTION: Open browser and load to Vanilla evn (e.g. http://qa2.sports.coral.co.uk)
        EXPECTED: According to VANO-1078:
        EXPECTED: user session should be terminated
        EXPECTED: user should NOT be Logged in
        EXPECTED: Login button should be displayed
        """
        pass
