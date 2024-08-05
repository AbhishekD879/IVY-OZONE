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
class Test_C14835392_Ladbrokes_KYC_Verify_end_to_end_flow_with_document_upload_for_registered_in_process_user(Common):
    """
    TR_ID: C14835392
    NAME: Ladbrokes. KYC. Verify end-to-end flow with document upload for registered 'in process' user
    DESCRIPTION: This test case verifies end-to-end flow with document upload for a just registered user with IMS.'Age verification result' = "Active grace period" (redirect to AccOne > redirect NetVerify > Redirect to Roxanne app)
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: - Playtech IMS:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Ladbrokes+Environments
    PRECONDITIONS: - To find & edit user details in IMS go to: 'Player Management' tab > Player Search > Enter 'Username' & press 'Enter'
    PRECONDITIONS: - User Age Verification Result status is received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab)
    """
    keep_browser_open = True

    def test_001_mobiletap_loginjoin_button__join_us_here_buttondesktopclick_join_now_buttonfor_ladbrokes_mobile_and_desktopclick_on_register_button(self):
        """
        DESCRIPTION: **Mobile:**
        DESCRIPTION: Tap 'Login/Join' button > 'Join us here' button
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Click 'Join now' button
        DESCRIPTION: **For Ladbrokes (Mobile and Desktop)**:
        DESCRIPTION: Click on 'Register' button
        EXPECTED: Account One Registration page is displayed
        """
        pass

    def test_002_complete_the_3_step_registration_processand_tap_the_button_open_accountfor_test_env_email__testplaytechcom(self):
        """
        DESCRIPTION: Complete the 3 step registration process
        DESCRIPTION: and tap the button 'Open account'
        DESCRIPTION: (for test env. 'email' = "test@playtech.com")
        EXPECTED: 'Save my preferences' page is opened
        """
        pass

    def test_003_before_a_user_is_auto_logged_inin_ims__find_a_just_registered_user__change_age_verification_result_value_to_active_grace_period__tap_update_info__ensure_tags_are_absent_agp_success_upload_verfication_review(self):
        """
        DESCRIPTION: Before a user is auto logged in:
        DESCRIPTION: In IMS:
        DESCRIPTION: - Find a just registered user
        DESCRIPTION: - Change 'Age verification result' value to "Active grace period"
        DESCRIPTION: - Tap 'Update Info'
        DESCRIPTION: - Ensure tags are absent: 'AGP_Success_Upload', 'Verfication_Review'
        EXPECTED: Changes are saved in IMS
        """
        pass

    def test_004_fill_the_contact_preference_page__tap_save_my_preferences_button(self):
        """
        DESCRIPTION: Fill the 'Contact Preference Page' > tap 'Save my preferences' button
        EXPECTED: * A user is redirected to Account one page
        EXPECTED: * 'Please double-check your details' page is open
        """
        pass

    def test_005_change_some_details__tap_update_details_buttonortap_skip_to_next_step_button(self):
        """
        DESCRIPTION: Change some details > tap 'Update details' button
        DESCRIPTION: OR
        DESCRIPTION: Tap 'Skip to next step' button
        EXPECTED: 'A bit more info needed' page is opened after pop-up with a progress bar
        """
        pass

    def test_006_tap_upload_documentation_button(self):
        """
        DESCRIPTION: Tap 'Upload Documentation' button
        EXPECTED: Netverify site is opened
        """
        pass

    def test_007_tap_start_button__choose_a_country_eg_united_kingdom__select_id_type_eg_driving_licence__tap_take_photo__take_photo_of_driving_licence_tap_complee_button(self):
        """
        DESCRIPTION: Tap 'Start' button > Choose a country (e.g., United Kingdom) > Select ID type (e.g., Driving licence) > Tap 'Take photo' > Take photo of driving licence >
        DESCRIPTION: Tap 'Complee' button
        EXPECTED: * After photo uploading, user is redirected to AccountOne page about successful upload of documents
        EXPECTED: **IMS:**
        EXPECTED: * tags are added: 'AGP_Success_Upload' > 0, 'Verfication_Review'
        EXPECTED: * 'Age verification result' = "Active grace period"
        """
        pass

    def test_008_tap_close_button_x(self):
        """
        DESCRIPTION: Tap Close button ('X')
        EXPECTED: * User is redirected back to Roxanne app
        EXPECTED: * User is logged in
        EXPECTED: * 'Account In Review' bar appeared
        """
        pass
