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
class Test_C10877928_Verify_Account_in_review_overlay_appearance(Common):
    """
    TR_ID: C10877928
    NAME: Verify 'Account in review' overlay appearance
    DESCRIPTION: This test case verifies the user is shown corresponding overlay when his account is still under review and restricted.
    PRECONDITIONS: 1. KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: 2. User has finished the registration flow and is auto logged in or has logged in to application as already existing user
    PRECONDITIONS: 3. User is on Home page and is able to browse the site
    PRECONDITIONS: 4. User account is under verification (Check for IMS 'age verification result' status = Active Grace period and Player tags = "AGP_Success_Upload < 5
    PRECONDITIONS: & Verfication_Review")
    PRECONDITIONS: - Playtech IMS:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Ladbrokes+Environments
    PRECONDITIONS: - User Age Verification Result status is received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab)
    PRECONDITIONS: - Player tags (in IMS) are documented here and are key sensitive : https://docs.google.com/spreadsheets/d/1RM5-9MnsmsSErdENXQUrBzDJAzsroIfpYblObwnrqG8/edit#gid=0
    """
    keep_browser_open = True

    def test_001_click_on_check_status_button_on_review_ribbon_on_home_page(self):
        """
        DESCRIPTION: Click on 'Check status' button on review ribbon on Home page
        EXPECTED: Spinner appears, status check is in process
        """
        pass

    def test_002_wait_till_the_response_is_received_account_is_still_under_review(self):
        """
        DESCRIPTION: Wait till the response is received (account is still under review)
        EXPECTED: User is shown an overlay with:
        EXPECTED: **Mobile**
        EXPECTED: - 'Account in review' title
        EXPECTED: - close button in the upper left corner
        EXPECTED: - 'Welcome 'user name' (logout)' text under overlay header
        EXPECTED: - message for the user (CMS configurable)
        EXPECTED: -  icon in the middle of the overlay
        EXPECTED: - message for the user at the bottom of the overlay (CMSable)
        EXPECTED: - 'If you need help contact customer support 24/7' text lower the previous one at the left corner
        EXPECTED: - 'Live chat' button in the right bottom corner (can be turned on/off in CMS)
        EXPECTED: **Desktop**
        EXPECTED: - 'Coral' title
        EXPECTED: -  'Account in review' , 'Welcome 'user name' (logout)' text under the overlay title
        EXPECTED: - message for the user (CMS configurable)
        EXPECTED: - message for the user (CMS configurable) under the previous one
        EXPECTED: -  icon in the middle of the overlay
        EXPECTED: - 'To update your date of birth or name please contact customer support' text in the bottom left corner
        EXPECTED: -  'Live chat' button in the right bottom corner (can be turned on/off in CMS)
        """
        pass

    def test_003_click_on_the_close_button_on_the_overlay(self):
        """
        DESCRIPTION: Click on the close button on the overlay
        EXPECTED: - Overlay is closed
        EXPECTED: - User is on the same page he was before
        """
        pass

    def test_004_click_on_check_status_button_on_review_ribbon_in_user_account_menu_account_still_under_review(self):
        """
        DESCRIPTION: Click on 'Check status' button on review ribbon in user Account Menu (account still under review)
        EXPECTED: User is shown an overlay as described above
        """
        pass

    def test_005_click_several_times_on_the_check_status_button(self):
        """
        DESCRIPTION: Click several times on the 'Check status' button
        EXPECTED: If user account is still under review (same player tags are received from preconditions) user will be shown the overlay over and over till the new status is received
        """
        pass
