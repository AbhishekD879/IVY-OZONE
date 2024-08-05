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
class Test_C11088394_Verify_account_in_review_info_bar_on_Home_page(Common):
    """
    TR_ID: C11088394
    NAME: Verify account in review info bar on Home page
    DESCRIPTION: This test case verifies 'account in review info bar' appearance on Home page when user's account is still under review and restricted.
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: - User has finished the registration flow and is auto logged in or has logged in to application as already existing one
    PRECONDITIONS: - User is on Home page and is able to browse the site
    PRECONDITIONS: - User account is under verification (Check for IMS 'age verification result' status = Active Grace period and Player tags = "AGP_Success_Upload < 5 & Verfication_Review")
    PRECONDITIONS: Playtech IMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: User Age Verification Result status is received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab)
    PRECONDITIONS: Player tags (in IMS) are documented here and are key sensitive : https://docs.google.com/spreadsheets/d/1RM5-9MnsmsSErdENXQUrBzDJAzsroIfpYblObwnrqG8/edit#gid=0
    """
    keep_browser_open = True

    def test_001_verify_the_review_info_bar_on_home_page(self):
        """
        DESCRIPTION: Verify the review info bar on Home page
        EXPECTED: User sees the info bar below the AEM Banner & above module ribbon
        """
        pass

    def test_002_verify_the_review_info_bar_view(self):
        """
        DESCRIPTION: Verify the review info bar view
        EXPECTED: It consists of :
        EXPECTED: - 'Account in review' text placed on the left
        EXPECTED: - 'Check status' clickable link on the right
        EXPECTED: - Clock icon placed after  'Check status' link
        """
        pass

    def test_003_click_on_check_status_link(self):
        """
        DESCRIPTION: Click on 'Check status' link
        EXPECTED: - 'Check status' link becomes greyed out
        EXPECTED: - Spinner is loading inside the clock icon
        EXPECTED: - When response from IMS is received, user is shown 'Account in review' overlay
        """
        pass

    def test_004_change_tags_in_ims_for_the_user_to_age_verification_result_status__under_review_user_passed_verification_and_click_check_status_link(self):
        """
        DESCRIPTION: Change tags in IMS for the user to 'age verification result' status = Under Review (user passed verification) and click 'Check status' link
        EXPECTED: - 'Check status' link becomes greyed out
        EXPECTED: - Spinner is loading inside the clock icon
        EXPECTED: - After response is received the ribbon disappears
        """
        pass
