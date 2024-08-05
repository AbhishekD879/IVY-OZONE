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
class Test_C14835390_Ladbrokes_KYC_Verify_end_to_end_flow_with_document_upload_for_in_process_user(Common):
    """
    TR_ID: C14835390
    NAME: Ladbrokes. KYC. Verify end-to-end flow with document upload for 'in process' user
    DESCRIPTION: This test case verifies end-to-end flow with document upload for a user with IMS.'Age verification result' = "Active grace period" (redirect to AccOne > redirect NetVerify > Redirect to Roxanne app)
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: - Playtech IMS:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Ladbrokes+Environments
    PRECONDITIONS: - To find & edit user details in IMS go to: 'Player Management' tab > Player Search > Enter 'Username' & press 'Enter'
    PRECONDITIONS: - User Age Verification Result status is received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab)
    """
    keep_browser_open = True

    def test_001_log_in_as_a_user_with_ims_age_verification_status__active_grace_period_and_without_tags__agp_success_upload_verfication_review(self):
        """
        DESCRIPTION: Log in as a user with IMS 'Age verification status' = "Active grace period" and without tags  'AGP_Success_Upload', 'Verfication_Review'
        EXPECTED: - A user is redirected to Account one page
        EXPECTED: - 'Please double-check your details' page is open
        """
        pass

    def test_002_change_some_details__tap_update_details_buttonortap_skip_to_next_step_button(self):
        """
        DESCRIPTION: Change some details > tap 'Update details' button
        DESCRIPTION: OR
        DESCRIPTION: Tap 'Skip to next step' button
        EXPECTED: 'A bit more info needed' page is opened after pop-up with a progress bar
        """
        pass

    def test_003_tap_upload_documentation_button(self):
        """
        DESCRIPTION: Tap 'Upload Documentation' button
        EXPECTED: Netverify site is opened
        """
        pass

    def test_004_tap_start_button__choose_a_country_eg_united_kingdom__select_id_type_eg_driving_licence__tap_take_photo__take_photo_of_driving_licence_tap_complee_button(self):
        """
        DESCRIPTION: Tap 'Start' button > Choose a country (e.g., United Kingdom) > Select ID type (e.g., Driving licence) > Tap 'Take photo' > Take photo of driving licence >
        DESCRIPTION: Tap 'Complee' button
        EXPECTED: * After photo uploading, user is redirected to AccountOne page where information about successful uploading of documents is displayed
        EXPECTED: **IMS:**
        EXPECTED: * tags are added: 'AGP_Success_Upload' = [successful upload attempts, e.g.1], 'Verfication_Review'
        EXPECTED: * 'Age verification result' = "Active grace period"
        """
        pass

    def test_005_tap_close_button_x(self):
        """
        DESCRIPTION: Tap Close button ('X')
        EXPECTED: * User is redirected back to Roxanne app
        EXPECTED: * User is logged in
        EXPECTED: * 'Account In Review' bar appeared
        """
        pass
