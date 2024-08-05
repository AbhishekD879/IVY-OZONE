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
class Test_C10922791_Verify_failed_user_overlay(Common):
    """
    TR_ID: C10922791
    NAME: Verify failed user overlay
    DESCRIPTION: This test case verifies the failed user is shown the overlay after he fails the document upload for 5 times.
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: - User has failed all the 5 attempts for uploading his documents for verification (in Jumio screen)
    PRECONDITIONS: - the IMS response of the player tag has AGP_Success_Upload >5 AND IMS age verification result = Active grace period
    PRECONDITIONS: - Playtech IMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: - User Age Verification Result status is received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab)
    PRECONDITIONS: - Player tags (in IMS) are documented here and are key sensitive : https://docs.google.com/spreadsheets/d/1RM5-9MnsmsSErdENXQUrBzDJAzsroIfpYblObwnrqG8/edit#gid=0
    """
    keep_browser_open = True

    def test_001_in_ims_set_corresponding_status_for_failed_user_from_precondition_and_login_to_the_oxygen_app(self):
        """
        DESCRIPTION: In IMS set corresponding status for failed user (from precondition) and login to the Oxygen app
        EXPECTED: - User is logged in
        EXPECTED: - User is shown the overlay
        """
        pass

    def test_002_verify_the_overlay(self):
        """
        DESCRIPTION: Verify the Overlay
        EXPECTED: Overlay consists of such components:
        EXPECTED: **Mobile**
        EXPECTED: - 'Verification failed' title
        EXPECTED: - 'Welcome |user name| (logout)' text below title on the right
        EXPECTED: - 'You have reached the maximum limit of verification attempts' text  (CMS configurable) centered at the upper part of overlay
        EXPECTED: - icon in the middle of the overlay
        EXPECTED: - 'If you need help contact customer support 24/7' text at the left bottom corner
        EXPECTED: - 'Live Chat' button in the right bottom corner (can be turned on/off in CMS)
        EXPECTED: **Desktop**
        EXPECTED: - 'Coral' title
        EXPECTED: - 'Verification failed' , 'Welcome 'user name' (logout)' text under the overlay title
        EXPECTED: - icon
        EXPECTED: - 'You have reached the maximum limit of verification attempts' message (CMS configurable)
        EXPECTED: - 'To update your date of birth or name please contact customer support' text in the bottom left corner
        EXPECTED: - 'Live chat' button in the right bottom corner (can be turned on/off in CMS)
        """
        pass

    def test_003_try_to_close_the_overlay(self):
        """
        DESCRIPTION: Try to close the overlay
        EXPECTED: Overlay has no close button and user is not able to close the overlay (even through page refresh)
        """
        pass
