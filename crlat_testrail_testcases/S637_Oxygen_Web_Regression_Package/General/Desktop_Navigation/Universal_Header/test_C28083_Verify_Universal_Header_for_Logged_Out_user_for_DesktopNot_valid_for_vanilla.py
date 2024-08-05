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
class Test_C28083_Verify_Universal_Header_for_Logged_Out_user_for_DesktopNot_valid_for_vanilla(Common):
    """
    TR_ID: C28083
    NAME: Verify Universal Header for Logged Out user for Desktop(Not valid for vanilla)
    DESCRIPTION: Please note: this test case is not valid for Vanilla.
    DESCRIPTION: This test case verifies Universal Header UI and functionality when user is logged out on Desktop.
    DESCRIPTION: Need to check on Windows ( IE, Edge, Chrome, FireFox ) and Mac OS (Safari).
    PRECONDITIONS: 1. Oxygen app is loaded
    PRECONDITIONS: 2. User is logged out
    """
    keep_browser_open = True

    def test_001_verify_universal_header_displaying(self):
        """
        DESCRIPTION: Verify Universal Header displaying
        EXPECTED: Universal Header is displayed on every page across the app
        """
        pass

    def test_002_verify_universal_header_content(self):
        """
        DESCRIPTION: Verify Universal Header content
        EXPECTED: Following elements are displayed:
        EXPECTED: *   'Main Navigation' menu (CMS configurable)
        EXPECTED: *   'Sports Sub Navigation' menu (CMS configurable)
        EXPECTED: *   'Coral' logo
        EXPECTED: *   'Join Now' button
        EXPECTED: *   'Log in' button
        """
        pass

    def test_003_navigate_to_any_page_in_app_and_click_on_coral_logo(self):
        """
        DESCRIPTION: Navigate to any page in app and click on 'Coral' logo
        EXPECTED: User is navigated to Homepage after clicking 'Coral' logo
        """
        pass

    def test_004_click_on_join_now_button(self):
        """
        DESCRIPTION: Click on 'Join Now' button
        EXPECTED: 'Registration Step 1' page is opened
        """
        pass

    def test_005_click_on_log_in_button(self):
        """
        DESCRIPTION: Click on 'Log in' button
        EXPECTED: 'Log in' pop-up appears
        """
        pass
