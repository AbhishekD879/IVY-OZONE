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
class Test_C10850079_KYC_ID_and_Address_upload_is_needed_after_registration(Common):
    """
    TR_ID: C10850079
    NAME: KYC. ID and Address upload is needed after registration
    DESCRIPTION: Test case verifies "Verification failed" overlay with documents options for ID and Address verification when IMS status Active grace period AND Player tag = AGP_Success_Upload < 5  are received after user registration
    DESCRIPTION: Note: Cannot automate as we are not able to set  “Active Grace Period” and Player tag AGP_Success_Upload < 5   for the user in IMS via scripts
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: Playtech IMS:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: User Age Verification Result status and user tags are received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab). In WS Active Grace Period = “inprocess”
    """
    keep_browser_open = True

    def test_001_start_new_user_registration_flow_until_gdpr_screen(self):
        """
        DESCRIPTION: Start new user registration flow until GDPR screen
        EXPECTED: GDPR screen displayed with ability to select and Save Preferences
        """
        pass

    def test_002_before_user_is_auto_logged_innavigate_to_ims_and_set_age_verification_result_to_active_grace_period_and_player_tag_agp_success_upload__5_for_the_user(self):
        """
        DESCRIPTION: Before user is auto logged in:
        DESCRIPTION: Navigate to IMS and set Age Verification Result to “Active Grace Period” and Player tag AGP_Success_Upload < 5   for the user
        EXPECTED: User IMS status is set
        """
        pass

    def test_003_after_user_is_auto_logged_intap_on_save_my_preferences_button_in_the_app(self):
        """
        DESCRIPTION: After user is auto logged in:
        DESCRIPTION: tap on Save My Preferences button in the app
        EXPECTED: “Verification failed” without verify my address CTA overlay is displayed
        """
        pass

    def test_004_verify_elements_of_the_overlay(self):
        """
        DESCRIPTION: Verify elements of the overlay
        EXPECTED: - header VERIFICATION FAILED
        EXPECTED: - text Welcome, (first name)
        EXPECTED: - log out button
        EXPECTED: - text from static block **KYC - Upload Required Documents** . Current text: "In order to prevent underage gambling, protect the vulnerable and provide you with a better experience, new legislation requires us to verify your identity before continuing.
        EXPECTED: Please upload one of the following documents"
        EXPECTED: - **Text from CMS static block "KYC - ID Verification Documents"**. Current documents options set:
        EXPECTED: 1. Driving Licence	Highly recommended
        EXPECTED: 2. Passport / National ID Card & Utility bill / Bank Statement	You might be required to upload extra documents at later stage
        EXPECTED: - VERIFY ME button
        EXPECTED: - REVIEW MY DETAILS link
        EXPECTED: - LIVE CHAT button
        EXPECTED: - text "If you need help contact customer support 24/7”
        """
        pass

    def test_005_tap_on_verify_me_button(self):
        """
        DESCRIPTION: Tap on VERIFY ME button
        EXPECTED: User is redirected to Jumio service for documents upload
        """
        pass
