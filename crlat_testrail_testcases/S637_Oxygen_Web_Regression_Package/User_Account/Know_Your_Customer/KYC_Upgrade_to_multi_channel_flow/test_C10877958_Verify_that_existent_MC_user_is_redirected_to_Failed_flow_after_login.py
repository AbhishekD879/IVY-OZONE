import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C10877958_Verify_that_existent_MC_user_is_redirected_to_Failed_flow_after_login(Common):
    """
    TR_ID: C10877958
    NAME: Verify that existent MC user is redirected to Failed flow after login
    DESCRIPTION: This test case verifies existent MC user redirection to Failed Flow after login with AVR 'unknown' or 'Active Grace Period'
    PRECONDITIONS: - MC User is NOT logged in
    PRECONDITIONS: - Playtech IMS:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: - To find & edit user details in IMS go to: 'Player Management' tab > Player Search > Enter 'Username' & press 'Enter'
    PRECONDITIONS: - User Age Verification Result status is received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab)
    """
    keep_browser_open = True

    def test_001_in_ims_find_mc_user_by_his_username_if_needed_change_age_verification_result_to_unknown_tap_update_info(self):
        """
        DESCRIPTION: In IMS:
        DESCRIPTION: * Find MC user by his username
        DESCRIPTION: * If needed, change 'Age verification result' to "unknown"
        DESCRIPTION: * Tap 'Update Info'
        EXPECTED: 'Age verification result' = "unknown"
        """
        pass

    def test_002_log_in_to_oxygen_app_as_multichannel_user(self):
        """
        DESCRIPTION: Log in to Oxygen app as multichannel user
        EXPECTED: * 'Verify your details' pop-up with spinner is shown
        EXPECTED: * User is redirected to Failed Flow (docs upload)
        EXPECTED: * In "openapi" websocket: 'ageVerificationStatus' = "unknown" is received (in response with "ID":31083)
        """
        pass

    def test_003_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: 
        """
        pass

    def test_004_in_ims_find_mc_user_by_his_username_change_age_verification_result_to_active_grace_period_tap_update_info(self):
        """
        DESCRIPTION: In IMS:
        DESCRIPTION: * Find MC user by his username
        DESCRIPTION: * Change 'Age verification result' to "Active Grace Period"
        DESCRIPTION: * Tap 'Update Info'
        EXPECTED: 'Age verification result' = "Active Grace Period"
        """
        pass

    def test_005_log_in_to_oxygen_app_as_multichannel_user(self):
        """
        DESCRIPTION: Log in to Oxygen app as multichannel user
        EXPECTED: * User is redirected to Failed Flow (docs upload)
        EXPECTED: * In "openapi" websocket: 'ageVerificationStatus' = "inprocess" is received (in response with "ID":31083)
        """
        pass
