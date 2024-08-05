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
class Test_C11250802_Verify_account_in_review_info_bar_in_My_Account_menu(Common):
    """
    TR_ID: C11250802
    NAME: Verify 'account in review' info bar in My Account menu
    DESCRIPTION: This test case verifies 'account in review info bar' appearance in My Account page when user's account is still under review and restricted.
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: - User has finished the registration flow and is auto logged in or has logged in to application as already existing one
    PRECONDITIONS: - User is on Home page and is able to browse the site
    PRECONDITIONS: - User account is under verification (Check for IMS 'age verification result' status = Active Grace period and Player tags = "AGP_Success_Upload < 5 & Verfication_Review") Playtech IMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS User Age Verification Result status is received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab) Player tags (in IMS) are documented here and are key sensitive : https://docs.google.com/spreadsheets/d/1RM5-9MnsmsSErdENXQUrBzDJAzsroIfpYblObwnrqG8/edit#gid=0
    """
    keep_browser_open = True

    def test_001_click_on_user_right_menu_my_account(self):
        """
        DESCRIPTION: Click on user right menu: 'My Account'
        EXPECTED: User is navigated to 'My Account' menu page
        """
        pass

    def test_002_verify_the_review_info_bar(self):
        """
        DESCRIPTION: Verify the review info bar
        EXPECTED: Review info bar is placed at the top of the menu (below app header, above 'My account' menu header) and consists of:
        EXPECTED: - 'Account in review' text placed on the left of the ribbon
        EXPECTED: - 'Check status' clickable link on the right (underlinged)
        EXPECTED: - Clock icon placed after  'Check status' link
        """
        pass

    def test_003_scroll_my_account_menu_page_up_and_down(self):
        """
        DESCRIPTION: Scroll my account menu page up and down
        EXPECTED: Review ribbon and 'My Account' header are sticky and are not hidden while scrolling
        """
        pass

    def test_004_click_on_check_status_link_on_the_review_ribbon(self):
        """
        DESCRIPTION: Click on 'Check status' link on the review ribbon
        EXPECTED: - 'Check status' link becomes greyed out
        EXPECTED: - Spinner is loading inside the clock icon
        EXPECTED: - When response from IMS is received, user is shown 'Account in review' overlay
        """
        pass

    def test_005_navigate_to_any_other_accessible_page_except_home_page(self):
        """
        DESCRIPTION: Navigate to any other accessible page (except home page)
        EXPECTED: Review ribbon is not shown
        """
        pass

    def test_006_navigate_back_to_my_account_page(self):
        """
        DESCRIPTION: Navigate back to 'My Account' page
        EXPECTED: Review ribbon is displayed
        """
        pass

    def test_007_change_tags_in_ims_for_the_user_to_age_verification_result_status__under_review_user_passed_verification_and_click_check_status_link(self):
        """
        DESCRIPTION: Change tags in IMS for the user to 'age verification result' status = Under Review (user passed verification) and click 'Check status' link
        EXPECTED: - 'Check status' link becomes greyed out
        EXPECTED: - Spinner is loading inside the clock icon
        EXPECTED: - After response is received the ribbon disappears
        EXPECTED: - 'My Account' menu header is placed just below the app header
        """
        pass
