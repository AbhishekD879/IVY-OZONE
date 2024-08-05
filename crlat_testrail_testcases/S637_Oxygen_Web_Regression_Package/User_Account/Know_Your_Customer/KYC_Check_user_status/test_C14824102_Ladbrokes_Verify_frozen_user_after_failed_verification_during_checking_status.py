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
class Test_C14824102_Ladbrokes_Verify_frozen_user_after_failed_verification_during_checking_status(Common):
    """
    TR_ID: C14824102
    NAME: Ladbrokes. Verify frozen user after failed verification during checking status
    DESCRIPTION: This test case verifies the failed user is navigated to AccountOne page with no back URL after he performs document upload for >5 times during checking status
    PRECONDITIONS: 1. KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: 2. User has finished the registration flow and is auto logged in or has logged in to the application as already existing user
    PRECONDITIONS: 3. User is on Home page and is able to browse the site
    PRECONDITIONS: 4. User account is under verification (Check for IMS 'age verification result' status = Active Grace period and Player tags = "AGP_Success_Upload = 5
    PRECONDITIONS: & Verfication_Review")
    PRECONDITIONS: - Playtech IMS:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Ladbrokes+Environments
    PRECONDITIONS: - User Age Verification Result status is received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab)
    PRECONDITIONS: - Player tags (in IMS) are documented here and are key sensitive : https://docs.google.com/spreadsheets/d/1RM5-9MnsmsSErdENXQUrBzDJAzsroIfpYblObwnrqG8/edit#gid=0
    """
    keep_browser_open = True

    def test_001_in_imsset_tag_agp_success_upload_5_eg_6_for_the_logged_in_user(self):
        """
        DESCRIPTION: In IMS:
        DESCRIPTION: Set tag AGP_Success_Upload >5 (e.g., 6) for the logged in user
        EXPECTED: Tag is successfully set
        """
        pass

    def test_002_in_apptap_check_status_on_account_in_review_bar(self):
        """
        DESCRIPTION: In app:
        DESCRIPTION: Tap 'Check Status' on 'Account in review' bar
        EXPECTED: * User is redirected to Account one page (with no back URL)
        """
        pass

    def test_003_try_to_close_the_overlay(self):
        """
        DESCRIPTION: Try to close the overlay
        EXPECTED: The overlay has no close button and the user is not able to close the overlay (even through page refresh)
        """
        pass

    def test_004_try_to_use_back_button_to_get_back_to_roxanne_app(self):
        """
        DESCRIPTION: Try to use 'back' button to get back to Roxanne app
        EXPECTED: User is not able to close the overlay
        """
        pass
