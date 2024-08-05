import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C16367453_Vanilla_View_Limits_after_Logout(Common):
    """
    TR_ID: C16367453
    NAME: [Vanilla] View Limits after Logout
    DESCRIPTION: This test scenario verifies that user is logged out by server automatically when his/her session is over on the server.
    DESCRIPTION: Jira tickets:
    DESCRIPTION: BMA-5678 (Handle HTTP Error 401)
    DESCRIPTION: BMA-18752 Deposit Limits Refactoring
    PRECONDITIONS: User should be logged in, but session should be OVER on the server
    PRECONDITIONS: To trigger event when session is over on the server please perform the following steps:
    PRECONDITIONS: *   Login to application in one browser tab and open 'DEPOSIT LIMITS' page
    PRECONDITIONS: *   Login to application in second browser tab, logout -> session is over on the server
    PRECONDITIONS: *   Navigate back to the first browser tab where user is still logged in, however there is no active session already
    """
    keep_browser_open = True

    def test_001_log_in_to_application_in_one_browser_tab_and_navigate_to_deposit_limitsmy_account_menu_item_settings_gambling_controls_deposit_limits(self):
        """
        DESCRIPTION: Log in to application in one browser tab and navigate to 'DEPOSIT LIMITS'
        DESCRIPTION: ('My Account' menu item->SETTINGS'->'GAMBLING CONTROLS'->'Deposit Limits')
        EXPECTED: 'DEPOSIT LIMITS' page is open
        """
        pass

    def test_002_login_to_application_in_second_browser_tab_and_then_logout___session_is_over_on_the_server(self):
        """
        DESCRIPTION: Login to application in second browser tab and then logout -> session is over on the server
        EXPECTED: User is logged out
        """
        pass

    def test_003_navigate_back_to_the_first_browser_tab_where_user_is_still_logged_in_however_there_is_no_active_session_already(self):
        """
        DESCRIPTION: Navigate back to the first browser tab where user is still logged in, however there is no active session already
        EXPECTED: 
        """
        pass

    def test_004_verify_deposit_limits_page(self):
        """
        DESCRIPTION: Verify 'DEPOSIT LIMITS' page
        EXPECTED: * "Your session expired. Please log in again."pop-up message appears.
        EXPECTED: * User is logged out from the application automatically without performing any action
        EXPECTED: * User is not able to see the content of '**DEPOSIT LIMITS**' page
        EXPECTED: * User is redirected to login page
        """
        pass

    def test_005_navigate_to_my_limits_page_via_direct_link_as_a_logged_out_userlink_httpsenvironmentenmobileportaldepositlimits(self):
        """
        DESCRIPTION: Navigate to 'My Limits' page via direct link as a logged out user
        DESCRIPTION: (Link: https://<ENVIRONMENT>/en/mobileportal/depositlimits)
        EXPECTED: * User is not able to see the content of '**DEPOSIT LIMITS**' page
        EXPECTED: * User is redirected to the login page
        """
        pass
