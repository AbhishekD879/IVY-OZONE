import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C15785353_Vanilla_User_is_logged_out_in_case_of_error_happening(Common):
    """
    TR_ID: C15785353
    NAME: [Vanilla] User is logged out in case of error happening
    DESCRIPTION: This test case verifies that user is logged out by the server automatically in case of error happening
    PRECONDITIONS: User is logged out in case:
    PRECONDITIONS: - **this.authService.isAuthenticated** is failed
    PRECONDITIONS: - **this.api.get('temporarytoken')** is failed
    """
    keep_browser_open = True

    def test_001_log_in(self):
        """
        DESCRIPTION: Log in
        EXPECTED: User is successfully logged in
        """
        pass

    def test_002_open_separate_tab_in_the_browser_load_oxygen_app_and_log_in_there_with_the_same_credentials(self):
        """
        DESCRIPTION: Open separate tab in the browser, load oxygen app and log in there with the same credentials
        EXPECTED: User is already logged in
        """
        pass

    def test_003_log_out_from_one_of_opened_tabs(self):
        """
        DESCRIPTION: Log out from one of opened tabs
        EXPECTED: Session is over on the server side
        """
        pass

    def test_004_go_to_another_tab(self):
        """
        DESCRIPTION: Go to another tab
        EXPECTED: Ladbrokes:
        EXPECTED: - User is logged out after page refresh
        EXPECTED: - 'Log out' pop-up shouldn't be displayed
        EXPECTED: Coral:
        EXPECTED: - User is logged out after page refresh
        EXPECTED: - 'Log out' pop-up is displayed
        """
        pass

    def test_005_log_in_again(self):
        """
        DESCRIPTION: Log in again
        EXPECTED: User is successfully logged in
        """
        pass

    def test_006_open_application_tab___cookies___delete_vauthnetwork_tab___offline___online(self):
        """
        DESCRIPTION: Open Application tab -> Cookies -> delete 'vauth'
        DESCRIPTION: Network tab -> Offline -> Online
        EXPECTED: - User is logged out
        EXPECTED: - 'Log out' pop-up is displayed
        """
        pass

    def test_007_log_in_again(self):
        """
        DESCRIPTION: Log in again
        EXPECTED: User is successfully logged in
        """
        pass

    def test_008_in_dev_tools___application___local_storage_select_app_url(self):
        """
        DESCRIPTION: In Dev Tools -> Application -> Local Storage select app url
        EXPECTED: 
        """
        pass

    def test_009_for_oxuser_parameter_change_bpptoken_value_and_save_changes(self):
        """
        DESCRIPTION: For OX.USER parameter change bppToken": value and save changes
        EXPECTED: 
        """
        pass

    def test_010_in_application_refresh_the_page_and_verify_that_user_is_still_logged_in(self):
        """
        DESCRIPTION: In application refresh the page and verify that user is still logged in
        EXPECTED: User is still logged in to application
        """
        pass
