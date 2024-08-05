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
class Test_C13848751_Ladbrokes_Verify_login_of_frozen_user_after_failed_verification(Common):
    """
    TR_ID: C13848751
    NAME: Ladbrokes. Verify login of frozen user after failed verification
    DESCRIPTION: This test case verifies the failed user is navigated to AccountOne page with no back URL after he performs document upload for >5 times and tries to login
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: - User has failed all the 5 attempts for uploading his documents for verification (in Jumio screen)
    PRECONDITIONS: - the IMS response of the player tag has AGP_Success_Upload >5 AND IMS age verification result = Active grace period
    PRECONDITIONS: - Playtech IMS Ladbrokes: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Ladbrokes+Environments
    PRECONDITIONS: - User Age Verification Result status is received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab)
    """
    keep_browser_open = True

    def test_001_in_ims_set_corresponding_status_for_failed_user_from_precondition_and_login_to_the_oxygen_app(self):
        """
        DESCRIPTION: In IMS set corresponding status for failed user (from precondition) and login to the Oxygen app
        EXPECTED: * User is logged in
        EXPECTED: * User is redirected to Account one page (with no back URL)
        """
        pass

    def test_002_try_to_close_the_overlay(self):
        """
        DESCRIPTION: Try to close the overlay
        EXPECTED: The overlay has no close button and user is not able to close the overlay (even through page refresh)
        """
        pass

    def test_003_try_to_use_back_button_to_get_back_to_roxanne_app(self):
        """
        DESCRIPTION: Try to use 'back' button to get back to Roxanne app
        EXPECTED: User is not able to close the overlay
        """
        pass
