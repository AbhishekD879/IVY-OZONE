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
class Test_C10877959_KYC_Successful_documents_upload_for_Address_verification(Common):
    """
    TR_ID: C10877959
    NAME: KYC. Successful documents upload for Address verification
    DESCRIPTION: Test case verifies "Account in Review" overlay which user sees after successful upload of Address documents for verification
    DESCRIPTION: Note: cannot automate as we are not able to set IMS tags and upload documents via scripts
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: Playtech IMS:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: User Age Verification Result status and user tags are received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab). In WS Active Grace Period = “inprocess”.
    PRECONDITIONS: **User has received IMS status = Active grace period and IMS tags** (POA_Required, AGP_Success_Upload < 5) OR (POA_Required) **and was navigated to "Verification failed" screen**
    """
    keep_browser_open = True

    def test_001_tap_on_verify_my_address_button_and_on_jumio_service_upload_correct_document(self):
        """
        DESCRIPTION: Tap on VERIFY MY ADDRESS button and on Jumio service upload correct document
        EXPECTED: User is redirected from Jumio to "Account in Review" overlay (without Verify Me button)
        """
        pass

    def test_002_verify_data_is_sent_to_ims_over_openapi_websocket_and_refresh_ims_user_account_page(self):
        """
        DESCRIPTION: Verify data is sent to IMS over openapi websocket, and refresh IMS user account page
        EXPECTED: Tags are sent over openapi websocket and are present in IMS
        EXPECTED: - increment +1 for "AGP_Success_Upload" value
        EXPECTED: - "Verification Review" is added (if not already existing)
        """
        pass

    def test_003_verify_account_in_review_overlay(self):
        """
        DESCRIPTION: Verify "Account in Review" overlay
        EXPECTED: - header ACCOUNT IN REVIEW
        EXPECTED: - text Welcome, (first name)
        EXPECTED: - log out button
        EXPECTED: - text from static block **KYC - Uploaded documents being reviewed**. Current text: "You have successfully uploaded your documents, they will now be reviewed"
        EXPECTED: - text from static block **KYC - Feel Free To Close Popup**. Current text: "We aim to get back to you within 2 hours. You’ll receive an email and onsite message. Feel free to close this screen when you are ready."
        EXPECTED: - LIVE CHAT button
        EXPECTED: - Close button
        EXPECTED: - text "If you need help contact customer support 24/7”
        """
        pass

    def test_004_tap_close_button(self):
        """
        DESCRIPTION: Tap Close button
        EXPECTED: Overlay is closed
        """
        pass
