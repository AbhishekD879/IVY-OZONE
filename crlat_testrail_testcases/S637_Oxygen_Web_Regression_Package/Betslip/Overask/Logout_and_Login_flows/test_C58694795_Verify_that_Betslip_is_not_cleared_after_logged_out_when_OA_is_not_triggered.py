import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C58694795_Verify_that_Betslip_is_not_cleared_after_logged_out_when_OA_is_not_triggered(Common):
    """
    TR_ID: C58694795
    NAME: Verify that Betslip is not cleared after logged out when OA is not triggered
    DESCRIPTION: This test case verifies that Betslip is not cleared after user is logged out when OA is not triggered
    PRECONDITIONS: Overask is enabled for User1 and for event which will be added to Betslip (see doc: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983)
    PRECONDITIONS: 1. Login with User1 (without 'Remember Me' option) and add selection available for Overask to Betslip
    PRECONDITIONS: Check parameters in Local Storage:
    PRECONDITIONS: OX.BetSelections
    PRECONDITIONS: ![](index.php?/attachments/get/106948322)
    """
    keep_browser_open = True

    def test_001_trigger_log_out_from_appon_desktop_tap_logout_button_in_account_menuon_web_mobile_refresh_page_then_tap_logout_button_in_the_account_menuon_wrappers_kill_and_reopen_the_app(self):
        """
        DESCRIPTION: Trigger log out from app:
        DESCRIPTION: On Desktop: Tap 'Logout' button in account menu
        DESCRIPTION: On Web mobile: Refresh page then tap 'Logout' button in the account menu
        DESCRIPTION: On wrappers: Kill and reopen the app
        EXPECTED: - User is logged out
        EXPECTED: - Homepage is shown (for mobile web and wrappers)
        """
        pass

    def test_002_go_to_betslip(self):
        """
        DESCRIPTION: Go to Betslip
        EXPECTED: Selection added in preconditions is shown in Betslip
        """
        pass

    def test_003_check_local_storage(self):
        """
        DESCRIPTION: Check Local Storage
        EXPECTED: OX.BetSelections is NOT cleared
        """
        pass

    def test_004_tap_login_buttonlogin_with_user1_from_preconditions(self):
        """
        DESCRIPTION: Tap 'Login' button
        DESCRIPTION: Login with user1 from preconditions
        EXPECTED: - User is logged in
        EXPECTED: - Selection added in preconditions is shown in Betslip
        """
        pass
