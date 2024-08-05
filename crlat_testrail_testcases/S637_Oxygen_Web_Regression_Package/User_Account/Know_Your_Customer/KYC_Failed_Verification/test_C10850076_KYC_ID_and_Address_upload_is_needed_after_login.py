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
class Test_C10850076_KYC_ID_and_Address_upload_is_needed_after_login(Common):
    """
    TR_ID: C10850076
    NAME: KYC. ID and Address upload is needed after login
    DESCRIPTION: Test case verifies "Verification failed" overlay with documents options for ID and Address verification when IMS status Active grace period AND Player tag = AGP_Success_Upload < 5 are received after user login
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: Playtech IMS:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: User Age Verification Result status and user tags are received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab). In WS Active Grace Period = “inprocess”
    """
    keep_browser_open = True

    def test_001_login_as_a_user_with_ims_age_verification_status__active_grace_period_and_player_tag__agp_success_upload__5(self):
        """
        DESCRIPTION: Login as a user with IMS Age verification status = Active grace period AND Player tag = AGP_Success_Upload < 5
        EXPECTED: “Verification failed” without verify my address CTA overlay is displayed
        """
        pass

    def test_002_verify_elements_of_the_overlay(self):
        """
        DESCRIPTION: Verify elements of the overlay
        EXPECTED: - header VERIFICATION FAILED
        EXPECTED: - text Welcome, (first name) text
        EXPECTED: - log out button
        EXPECTED: - text from static block **KYC - Upload Required Documents** . Current text: "In order to prevent under-age gambling, protect the vulnerable and provide you with a better experience, new legislation requires us to verify your identify before continuing. Please upload one of the following documents"
        EXPECTED: - **Text from CMC static block "KYC - ID Verification Documents"** Current document options offered:
        EXPECTED: 1) UK Driving Licence (Highly Recommended)
        EXPECTED: 2) Passport Photo Page OR
        EXPECTED: National ID Card (front and back)
        EXPECTED: AND
        EXPECTED: Utility Bill OR Bank Statement
        EXPECTED: (issued within the last 3 months)
        EXPECTED: - VERIFY ME button
        EXPECTED: - REVIEW MY DETAILS link
        EXPECTED: - LIVE CHAT button
        EXPECTED: - Text "If you need help contact customer support 24/7”
        """
        pass

    def test_003_verify_the_state_of_review_my_details_link(self):
        """
        DESCRIPTION: Verify the state of “Review my details” link
        EXPECTED: The link is enabled if user has made < 3 attempts to edit details before (variable in local storage)
        """
        pass

    def test_004_tap_on_verify_me_button(self):
        """
        DESCRIPTION: Tap on VERIFY ME button
        EXPECTED: User is redirected to Jumio service for documents upload
        """
        pass
