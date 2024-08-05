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
class Test_C44870342_User_has_finished_the_registration_flow_and_is_auto_logged_in_or_has_logged_in_to_application_as_already_existing_user_User_is_on_Home_page_and_is_able_to_browse_the_site_and_account_is_under_verification_Verify_user_sees_Check_status_button_on(Common):
    """
    TR_ID: C44870342
    NAME: "User has finished the registration flow and is auto logged in or has logged in to application as already existing user User is on Home page and is able to browse the site and  account is under verification  Verify user sees 'Check status' button on
    DESCRIPTION: "User has finished the registration flow and is auto logged in or has logged in to application as already existing user
    DESCRIPTION: User is on Home page and is able to browse the site and  account is under verification
    DESCRIPTION: Verify user sees 'Check status' button on review ribbon on Home page and sees overlay as below upon clicking on 'Check status'
    DESCRIPTION: -'Account in review' title
    DESCRIPTION: - close button in the upper left corner
    DESCRIPTION: - 'Welcome 'user name' (logout)' text under overlay header
    DESCRIPTION: - message for the user (CMS configurable)
    DESCRIPTION: - icon in the middle of the overlay
    DESCRIPTION: - message for the user at the bottom of the overlay (CMSable)
    DESCRIPTION: - 'If you need help contact customer support 24/7' text lower the previous one at the left corner
    DESCRIPTION: - 'Live chat' button in the right bottom corner (can be turned on/off in CMS)
    DESCRIPTION: "
    PRECONDITIONS: User has finished the registration process.
    PRECONDITIONS: User should be logged in
    """
    keep_browser_open = True

    def test_001_user_is_on_home_page(self):
        """
        DESCRIPTION: User is on home page
        EXPECTED: User should able to navigations b/w the sports
        EXPECTED: Note: when his account under verification
        """
        pass

    def test_002_verify_check_status_button_for_under_verification_user(self):
        """
        DESCRIPTION: Verify 'check status' button for under verification user
        EXPECTED: 'Check status' button should be displayed on home page.
        """
        pass

    def test_003_click_on_check_status_button(self):
        """
        DESCRIPTION: Click on 'check status' button
        EXPECTED: check the overlay as below upon clicking on 'check status'
        EXPECTED: -'Account in review' title
        EXPECTED: - close button in the upper left corner
        EXPECTED: - 'Welcome 'user name' (logout)' text under overlay header
        EXPECTED: - message for the user (CMS configurable)
        EXPECTED: - icon in the middle of the overlay
        EXPECTED: - message for the user at the bottom of the overlay (CMSable)
        EXPECTED: - 'If you need help contact customer support 24/7' text lower the previous one at the left corner
        EXPECTED: - 'Live chat' button in the right bottom corner (can be turned on/off in CMS)
        """
        pass
