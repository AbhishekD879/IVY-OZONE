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
class Test_C13828778_Ladbrokes_Verify_user_is_redirected_to_AccountOne_on_refreshing_the_page_when_verification_is_failed(Common):
    """
    TR_ID: C13828778
    NAME: Ladbrokes. Verify user is redirected to AccountOne on refreshing the page when verification is failed
    DESCRIPTION: This test case verifies redirection to AccountOne KYC-entry-point when a new user with 'unknown' Age Verification Result refreshes the page during Verification Spinner overlay displayed.
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: - Playtech IMS:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Ladbrokes+Environments
    PRECONDITIONS: - To find & edit user details in IMS go to: 'Player Management' tab > Player Search > Enter 'Username' & press 'Enter'
    PRECONDITIONS: - User Age Verification Result status is received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab)
    """
    keep_browser_open = True

    def test_001_log_in_as_a_user_with_age_verification_result__unknown_in_ims(self):
        """
        DESCRIPTION: Log in as a user with 'Age verification result' = 'unknown' in IMS
        EXPECTED: * User is logged in successfully
        EXPECTED: * Overlay with verification spinner displayed. Title "VERIFYING YOUR DETAILS", text: "Just a few more seconds, please wait" and loading spinner.
        EXPECTED: * Spinner display time equals to the time set in CMS
        """
        pass

    def test_002_refresh_page_while_verification_spinner_displayed(self):
        """
        DESCRIPTION: Refresh page while verification spinner displayed
        EXPECTED: - In "openapi" websocket: 'ageVerificationStatus' = "unknown" is received (in response with "ID":31083)
        EXPECTED: - Verification spinner displayed (5-7 seconds (CMSable))
        EXPECTED: - User is redirected to AccountOne KYC-entry-point
        """
        pass
