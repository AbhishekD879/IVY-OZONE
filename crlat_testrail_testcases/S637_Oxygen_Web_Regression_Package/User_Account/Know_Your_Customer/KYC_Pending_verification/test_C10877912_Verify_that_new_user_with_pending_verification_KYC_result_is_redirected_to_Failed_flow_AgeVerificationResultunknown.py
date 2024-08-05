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
class Test_C10877912_Verify_that_new_user_with_pending_verification_KYC_result_is_redirected_to_Failed_flow_AgeVerificationResultunknown(Common):
    """
    TR_ID: C10877912
    NAME: Verify that new user with pending verification KYC result is redirected to Failed flow (AgeVerificationResult="unknown")
    DESCRIPTION: This test case verifies new user with 'unknown' Age Verification Result redirection to Failed KYC flow (docs upload)
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: - Playtech IMS:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: - To find & edit user details in IMS go to: 'Player Management' tab > Player Search > Enter 'Username' & press 'Enter'
    PRECONDITIONS: - To be able to receive needed 'ageVerificationStatus' value right after registration > ask a developer to make a delay for a few seconds between registration and auto-login and change user status in IMS
    PRECONDITIONS: - User Age Verification Result status is received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab)
    """
    keep_browser_open = True

    def test_001___navigate_to_oxygen_app__tap_join_now__fill_out_required_fields_on_each_registration_page__tap_complete_registration_on_registration___account_details_page(self):
        """
        DESCRIPTION: - Navigate to Oxygen app
        DESCRIPTION: - Tap 'Join Now'
        DESCRIPTION: - Fill out required fields on each 'Registration' page
        DESCRIPTION: - Tap 'Complete Registration' on 'Registration - Account Details' page
        EXPECTED: 'Marketing Preferences' (GDPR) screen displayed with ability to select and Save Preferences
        """
        pass

    def test_002_before_a_user_is_auto_logged_inin_ims__find_a_just_registered_user__if_needed___change_age_verification_result_to_unknown__tap_update_info(self):
        """
        DESCRIPTION: Before a user is auto logged in:
        DESCRIPTION: In IMS:
        DESCRIPTION: - Find a just registered user
        DESCRIPTION: - If needed - change 'Age verification result' to 'unknown'
        DESCRIPTION: - Tap 'Update Info'
        EXPECTED: - Changes are saved in IMS
        EXPECTED: - Newly registered user Age Verification Result is 'unknown'
        """
        pass

    def test_003_after_a_user_is_auto_logged_inin_app_devtools__verify_response_in_openapi_websocket(self):
        """
        DESCRIPTION: After a user is auto logged in:
        DESCRIPTION: In app (devtools):
        DESCRIPTION: - Verify response in "openapi" websocket
        EXPECTED: In "openapi" websocket:
        EXPECTED: - 'ageVerificationStatus' = "unknown" is received (in response with "ID":31083)
        """
        pass

    def test_004___in_oxygen_app_and_click_on_save_my_preferences_button__note_make_sure_that_users_ageverificationstatus_remains_unknown_in_response_with_id31083(self):
        """
        DESCRIPTION: - In Oxygen app and click on Save My Preferences button
        DESCRIPTION: - Note! Make sure that user's 'ageVerificationStatus' remains "unknown" (in response with "ID":31083)
        EXPECTED: - Overlay with verification spinner displayed
        """
        pass

    def test_005_wait_until_verification_spinner_display_time_ends(self):
        """
        DESCRIPTION: Wait until verification spinner display time ends
        EXPECTED: User is redirected to Failed Flow (docs upload)
        """
        pass
