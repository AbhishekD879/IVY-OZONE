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
class Test_C10841437_Verify_new_user_is_redirected_to_Happy_flow_on_refreshing_Verification_overlay(Common):
    """
    TR_ID: C10841437
    NAME: Verify new user is redirected to Happy flow on refreshing Verification overlay
    DESCRIPTION: This test case verifies redirection to Happy Flow when new user with 'unknown' Age Verification Result refreshes page during Verification Spinner overlay displayed and Age Verification Result changes to 'Under Review'
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: - Playtech IMS:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: - To find & edit user details in IMS go to: 'Player Management' tab > Player Search > Enter 'Username' & press 'Enter'
    PRECONDITIONS: - To be able to receive needed 'ageVerificationStatus' value right after registration > ask a developer to make a delay for a few seconds between registration and auto-login and change user status in IMS
    PRECONDITIONS: - User Age Verification Result status is received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab)
    PRECONDITIONS: - STG CMS:
    PRECONDITIONS: https://cms-api-ui-stg0.coralsports.nonprod.cloud.ladbrokescoral.com/
    PRECONDITIONS: creds: qa@coral.co.uk/qas1234
    PRECONDITIONS: Navigate to CMS  -> System Configuration -> Structure -> KYC -> pendingDialogTimeout
    PRECONDITIONS: Change display time (value set in ms, e.g."5000" equals 5 sec) and save changes
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

    def test_004_in_oxygen_app__click_on_save_my_preferences_button(self):
        """
        DESCRIPTION: In Oxygen app:
        DESCRIPTION: - Click on Save My Preferences button
        EXPECTED: Overlay with verification spinner displayed
        """
        pass

    def test_005_within_spinner_displaying_time__in_ims__find_a_just_registered_user__change_age_verification_result_to_under_review__tap_update_infonote_that_spinner_displaying_time_can_be_extended_in_cms_if_needed(self):
        """
        DESCRIPTION: Within Spinner displaying time > In IMS:
        DESCRIPTION: - Find a just registered user
        DESCRIPTION: - Change 'Age verification result' to 'Under Review'
        DESCRIPTION: - Tap 'Update Info'
        DESCRIPTION: Note! that spinner displaying time can be extended in CMS (if needed)
        EXPECTED: - Changes are saved in IMS
        EXPECTED: - Newly registered user Age Verification Result is 'Under Review'
        """
        pass

    def test_006_return_to_oxygen_app__while_verification_spinner_is_displayed__reload_page(self):
        """
        DESCRIPTION: Return to Oxygen app > while Verification spinner is displayed > Reload page
        EXPECTED: - User is redirected to Happy Flow (Deposit page)
        EXPECTED: - In "openapi" websocket: 'ageVerificationStatus' = "review" is received (in response with "ID":31083)
        """
        pass
