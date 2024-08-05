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
class Test_C17328964_Vanilla_Verify_that_Forgot_Username_page_is_not_accessible_for_logged_in_users(Common):
    """
    TR_ID: C17328964
    NAME: [Vanilla] Verify that 'Forgot Username' page is not accessible for logged in users
    DESCRIPTION: This test case verifies that logged in user is not able to access 'Forgot Username' page
    DESCRIPTION: Should be repeated on Desktop, Tablet and Mobile
    PRECONDITIONS: User is not logged in
    PRECONDITIONS: Oxygen application is loaded
    """
    keep_browser_open = True

    def test_001_tap_login_button_in_the_app_header(self):
        """
        DESCRIPTION: Tap 'LOGIN' button in the app header
        EXPECTED: 'LOGIN' pop-up appears
        """
        pass

    def test_002_tap_i_forgot_my_username_link(self):
        """
        DESCRIPTION: Tap 'I forgot my Username' link
        EXPECTED: 'FORGOTTEN USERNAME' page is opened
        """
        pass

    def test_003_tap_login_button_in_the_header_again(self):
        """
        DESCRIPTION: Tap 'LOGIN' button in the header again
        EXPECTED: 'Log in' pop-up appears
        """
        pass

    def test_004_enter_valid_credentials_and_log_in(self):
        """
        DESCRIPTION: Enter valid credentials and log in
        EXPECTED: User is logged in
        EXPECTED: After login, user is redirected to Home page
        """
        pass

    def test_005_using_browser_buttonsswipes_try_navigate_back_to_previous_page_forgotten_username_page(self):
        """
        DESCRIPTION: Using browser buttons/swipes, try navigate back to previous page ('FORGOTTEN USERNAME' page)
        EXPECTED: 'FORGOTTEN USERNAME' page is not opened
        EXPECTED: User is redirected to home page
        """
        pass

    def test_006_enter_the_forgotten_username_page_link_directly_into_the_browser_httpsenvironmentcoralcoukenmobileportalverifyuserdetails_and_follow_the_link_while_logged_in(self):
        """
        DESCRIPTION: Enter the 'FORGOTTEN USERNAME' page link directly into the browser (https://<environment>.coral.co.uk/#/en/mobileportal/verifyuserdetails) and follow the link while logged in
        EXPECTED: 'FORGOTTEN USERNAME' page is not opened
        EXPECTED: User is redirected to home page
        """
        pass
