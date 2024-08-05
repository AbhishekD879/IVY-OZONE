import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C59482938_Verify_that_Forgot_Password_page_is_not_accessible_for_logged_in_users(Common):
    """
    TR_ID: C59482938
    NAME: Verify that 'Forgot Password' page is not accessible for logged in users
    DESCRIPTION: This test case verifies that logged in user is not able to access 'Forgot Password' page
    DESCRIPTION: Should be repeated on Desktop, Tablet and Mobile
    PRECONDITIONS: User is not logged in
    PRECONDITIONS: Oxygen application is loaded
    PRECONDITIONS: **Choosing the password should include following rules:**
    PRECONDITIONS: * At least 8 characters;
    PRECONDITIONS: * Uppercase and lowercase letters;
    PRECONDITIONS: * Numbers and symbols
    """
    keep_browser_open = True

    def test_001_tap_log_in_button_in_the_app_header(self):
        """
        DESCRIPTION: Tap 'Log in' button in the app header
        EXPECTED: 'Log in' pop-up appears
        """
        pass

    def test_002_tap_i_forgot_my_usernamepassword_link_on_password_part(self):
        """
        DESCRIPTION: Tap 'I Forgot My Username/Password' link on 'Password' part.
        EXPECTED: 'Forgotten Password' page is opened
        """
        pass

    def test_003_navigate_back_in_the_browser(self):
        """
        DESCRIPTION: Navigate back in the browser
        EXPECTED: User is redirected to Home page
        """
        pass

    def test_004_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        EXPECTED: 'Forgotten Password' page is opened
        """
        pass

    def test_005_enter_valid_credentials_and_log_in(self):
        """
        DESCRIPTION: Enter valid credentials and log in
        EXPECTED: User is logged in
        EXPECTED: After login, user is redirected to Home page
        """
        pass

    def test_006_using_browser_buttonsswipes_try_navigate_back_to_previous_page_forgot_password_page(self):
        """
        DESCRIPTION: Using browser buttons/swipes, try navigate back to previous page ('Forgot Password' page)
        EXPECTED: 'Forgot Password' page is not opened
        EXPECTED: User is redirected to home page
        """
        pass

    def test_007_enter_the_forgot_password_page_link_directly_into_the_browser_httpenvironment_urlenmobileportallostpassword_and_follow_the_link_while_logged_in(self):
        """
        DESCRIPTION: Enter the 'Forgot Password' page link directly into the browser (http://<environment_URL>/en/mobileportal/lostpassword) and follow the link while logged in
        EXPECTED: 'Forgot Password' page is not opened
        EXPECTED: User is redirected to home page
        """
        pass
