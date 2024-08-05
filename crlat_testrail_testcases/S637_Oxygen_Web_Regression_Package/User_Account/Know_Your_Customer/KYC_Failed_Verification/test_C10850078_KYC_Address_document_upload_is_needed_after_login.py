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
class Test_C10850078_KYC_Address_document_upload_is_needed_after_login(Common):
    """
    TR_ID: C10850078
    NAME: KYC. Address document upload is needed after login
    DESCRIPTION: Test case verifies "Verification failed" overlay with documents options for Address verification when (IMS status Active grace period AND Player tags are POA_Required, AGP_Success_Upload < 5) OR (IMS Age verification status: Active grace period AND Player tags: POA_Required) are received after user login
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: Playtech IMS:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: User Age Verification Result status and user tags are received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab. In WS Active Grace Period = “inprocess”
    PRECONDITIONS: User tags are received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 35548
    """
    keep_browser_open = True

    def test_001_login_as_a_user_with_ims_age_verification_status_is_active_grace_period_and_player_tags_are_poa_required_agp_success_upload__5(self):
        """
        DESCRIPTION: Login as a user with IMS Age verification status is Active grace period AND Player tags are POA_Required, AGP_Success_Upload < 5
        EXPECTED: “Verification failed” with verify my address CTA overlay is displayed
        """
        pass

    def test_002_verify_elements_of_the_overlay(self):
        """
        DESCRIPTION: Verify elements of the overlay
        EXPECTED: - header VERIFICATION FAILED
        EXPECTED: - text Welcome, (first name) text
        EXPECTED: - log out button
        EXPECTED: - text from static block **KYC - Upload Required Documents** . Current text: "In order to prevent under-age gambling, protect the vulnerable and provide you with a better experience, new legislation requires us to verify your identify before continuing. Please upload one of the following documents"
        EXPECTED: - Text from CMS static block **"KYC - Address Verification Documents"**. Current documents options offered:
        EXPECTED: 1) UK Driving Licence (Highly Recommended)  2) Utility Bill OR Bank Statement
        EXPECTED: (issued within the last 3 months)
        EXPECTED: - VERIFY MY ADDRESS button
        EXPECTED: - REVIEW MY DETAILS link
        EXPECTED: - LIVE CHAT button
        EXPECTED: - text "If you need help contact customer support 24/7”
        """
        pass

    def test_003_verify_the_state_of_review_my_details_link(self):
        """
        DESCRIPTION: Verify the state of “Review my details” link
        EXPECTED: The link is enabled if user had made < 3 attempts to edit details before (variable in local storage)
        """
        pass

    def test_004_tap_on_verify_my_address_button(self):
        """
        DESCRIPTION: Tap on VERIFY MY ADDRESS button
        EXPECTED: User is redirected to Jumio service for documents upload
        """
        pass

    def test_005_repeat_steps_1_4_for_user_with_ims_age_verification_status_active_grace_period_and_player_tags_poa_required(self):
        """
        DESCRIPTION: Repeat Steps 1-4 for user with (IMS Age verification status: Active grace period AND Player tags: POA_Required)
        EXPECTED: Same as above
        """
        pass
