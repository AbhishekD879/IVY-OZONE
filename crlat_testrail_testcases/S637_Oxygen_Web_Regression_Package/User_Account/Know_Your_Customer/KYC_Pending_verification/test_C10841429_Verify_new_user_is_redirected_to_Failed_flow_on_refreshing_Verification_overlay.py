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
class Test_C10841429_Verify_new_user_is_redirected_to_Failed_flow_on_refreshing_Verification_overlay(Common):
    """
    TR_ID: C10841429
    NAME: Verify new user is redirected to Failed flow on refreshing Verification overlay
    DESCRIPTION: This test case verifies redirection to Failed Flow (docs upload) when new user with 'unknown' Age Verification Result refreshes page during Verification Spinner overlay displayed.
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

    def test_004_in_oxygen_app__click_on_save_my_preferences_buttonnote_you_have_to_proceed_to_step_4_asap(self):
        """
        DESCRIPTION: In Oxygen app:
        DESCRIPTION: - Click on Save My Preferences button.
        DESCRIPTION: Note! You have to proceed to Step 4 asap.
        EXPECTED: Overlay with verification spinner displayed
        """
        pass

    def test_005_refresh_page_while_verification_spinner_displayed_step_3(self):
        """
        DESCRIPTION: Refresh page while verification spinner displayed (Step 3)
        EXPECTED: - In "openapi" websocket: 'ageVerificationStatus' = "unknown" is received (in response with "ID":31083)
        EXPECTED: - Verification spinner displayed (5-7 seconds (CMSable))
        EXPECTED: - User is redirected to Failed Flow (upload document overlay)
        """
        pass
