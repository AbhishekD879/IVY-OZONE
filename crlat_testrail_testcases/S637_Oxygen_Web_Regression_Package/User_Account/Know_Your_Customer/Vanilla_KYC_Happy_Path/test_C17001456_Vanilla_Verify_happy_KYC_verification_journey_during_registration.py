import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C17001456_Vanilla_Verify_happy_KYC_verification_journey_during_registration(Common):
    """
    TR_ID: C17001456
    NAME: [Vanilla] Verify happy KYC verification journey during registration
    DESCRIPTION: This test case verifies happy KYC verification journey while a new user is registered
    PRECONDITIONS: Link to internal GVC IMS: https://localreports.ivycomptech.co.in/pls/trunkiaezecash/ezeindex
    PRECONDITIONS: NOTE:
    PRECONDITIONS: Verification is required only for users whose country of residence is **United Kingdom**
    PRECONDITIONS: P.S. You may use attached documents:
    PRECONDITIONS: ![](index.php?/attachments/get/35346)
    PRECONDITIONS: ![](index.php?/attachments/get/35348)
    PRECONDITIONS: ![](index.php?/attachments/get/35347)
    PRECONDITIONS: ![](index.php?/attachments/get/35349)
    """
    keep_browser_open = True

    def test_001___tap_join_on_vanilla_app__fill_out_required_fields_on_each_registration_page__tap_create_my_account__set_your_deposit_limits___tap_submit(self):
        """
        DESCRIPTION: - Tap 'Join' on Vanilla app
        DESCRIPTION: - Fill out required fields on each 'Registration' page
        DESCRIPTION: - Tap 'Create my account'
        DESCRIPTION: - Set your deposit limits -> Tap 'Submit'
        EXPECTED: **'Verification required'** page is opened
        """
        pass

    def test_002_verify_verification_required_page_1(self):
        """
        DESCRIPTION: Verify 'Verification required' page 1
        EXPECTED: Please Double-check Your Details
        EXPECTED: *'As part of new UK gaming regulations, we are required to verify your account details. Please check that the information below is correct and amend if necessary.'* message is shown
        EXPECTED: - First Name;
        EXPECTED: - Surname;
        EXPECTED: - Date of birth;
        EXPECTED: - Your address
        EXPECTED: - 'Continue' button
        EXPECTED: - 'Live chat' button
        """
        pass

    def test_003_tap_continue_button(self):
        """
        DESCRIPTION: Tap 'Continue' button
        EXPECTED: 'Verification required' page 2 is opened:
        EXPECTED: *'Only one more step to go
        EXPECTED: We recommend using your driving licence as it confirms both your identity and address. Alternatively, you can provide a passport and utility bill.'* message is shown
        EXPECTED: Two options are offered to confirm your identity:
        EXPECTED: - 'Use driving licence';
        EXPECTED: - 'Passport & Utility Bill';
        EXPECTED: - 'Live chat' button is present
        EXPECTED: ![](index.php?/attachments/get/34781)
        """
        pass

    def test_004_tap_on_passport__utility_bill_button(self):
        """
        DESCRIPTION: Tap on 'Passport & Utility Bill' button
        EXPECTED: 'Verification required' page 3 is opened:
        EXPECTED: ![](index.php?/attachments/get/34782)
        """
        pass

    def test_005___choose_issuing_country__select_id_type_eg_passport(self):
        """
        DESCRIPTION: - Choose issuing country;
        DESCRIPTION: - Select ID type (e.g. passport)
        EXPECTED: Verification required' page 3 is opened:
        EXPECTED: ![](index.php?/attachments/get/34783)
        """
        pass

    def test_006___tap_on_choose_file__upload_a_color_image_of_the_entire_document__click_confirm(self):
        """
        DESCRIPTION: - Tap on 'Choose file'
        DESCRIPTION: - Upload a color image of the entire document
        DESCRIPTION: - Click 'Confirm'
        EXPECTED: 'Checking image quality for ID verification' page is opened:
        EXPECTED: ![](index.php?/attachments/get/34792)
        EXPECTED: - 'Verification' window is shown:
        EXPECTED: ![](index.php?/attachments/get/34793)
        """
        pass

    def test_007_tap_continue_button(self):
        """
        DESCRIPTION: Tap 'Continue' button
        EXPECTED: 'Verification required' page 4 is opened:
        EXPECTED: ![](index.php?/attachments/get/34794)
        """
        pass

    def test_008_tap_use_other_document_button(self):
        """
        DESCRIPTION: Tap 'Use Other Document' button
        EXPECTED: 'Verification required' page 5 is opened:
        EXPECTED: ![](index.php?/attachments/get/34795)
        """
        pass

    def test_009___click_on_upload_files__tap_continue_button(self):
        """
        DESCRIPTION: - Click on 'Upload files'
        DESCRIPTION: - Tap 'Continue' button
        EXPECTED: ![](index.php?/attachments/get/34796)
        """
        pass

    def test_010_tap_continue_button(self):
        """
        DESCRIPTION: Tap 'Continue' button
        EXPECTED: 'Verification pending' page is opened:
        EXPECTED: ![](index.php?/attachments/get/34797)
        """
        pass

    def test_011_tap_continue_button(self):
        """
        DESCRIPTION: Tap 'Continue' button
        EXPECTED: - User is redirected to homepage
        EXPECTED: - Pop-up is shown at the top of app:
        EXPECTED: ![](index.php?/attachments/get/34798)
        """
        pass

    def test_012___go_to_gvc_ims__in_general_reports_search_for_a_new_registered_user_via_last_name__email__partial_account_name__click_on_eze_account_name_cl_usernameindexphpattachmentsget34799indexphpattachmentsget34800(self):
        """
        DESCRIPTION: - Go to GVC IMS;
        DESCRIPTION: - In 'General Reports' search for a new registered user via Last Name / Email / Partial Account Name;
        DESCRIPTION: - Click on 'Eze Account Name' (cl_username)
        DESCRIPTION: ![](index.php?/attachments/get/34799)
        DESCRIPTION: ![](index.php?/attachments/get/34800)
        EXPECTED: All account information is opened
        """
        pass

    def test_013_click_on_manually_verify_account_details(self):
        """
        DESCRIPTION: Click on 'Manually Verify Account Details'
        EXPECTED: Window for verification of account details is shown:
        EXPECTED: ![](index.php?/attachments/get/34801)
        """
        pass

    def test_014___change_all_statuses_to_verified_in_such_columnsa_id_and_age_verificationb_address_validationc_phone_verificationd_mobile_verificationnote_in_document_numberdetailscomments_list_any_information__tap_updatenote_needs_to_be_updated_separately___update_button_reloads_page(self):
        """
        DESCRIPTION: - Change all statuses to **verified** in such columns:
        DESCRIPTION: a) ID and Age Verification
        DESCRIPTION: b) Address Validation
        DESCRIPTION: c) Phone Verification
        DESCRIPTION: d) Mobile Verification
        DESCRIPTION: NOTE: in Document Number/Details/Comments/ list any information
        DESCRIPTION: - Tap 'Update'
        DESCRIPTION: NOTE: Needs to be updated separately - 'update' button reloads page
        EXPECTED: 
        """
        pass

    def test_015_go_back_to_vanilla_application(self):
        """
        DESCRIPTION: Go back to Vanilla application
        EXPECTED: 'Deposit' page is opened with congratulation pop-up:
        EXPECTED: ![](index.php?/attachments/get/34802)
        """
        pass
