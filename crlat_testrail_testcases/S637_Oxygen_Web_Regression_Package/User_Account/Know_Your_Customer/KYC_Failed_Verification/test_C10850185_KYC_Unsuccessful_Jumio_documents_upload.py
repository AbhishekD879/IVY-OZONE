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
class Test_C10850185_KYC_Unsuccessful_Jumio_documents_upload(Common):
    """
    TR_ID: C10850185
    NAME: KYC. Unsuccessful Jumio documents upload
    DESCRIPTION: Test case verifies Verification Failed screen after redirect from Jumio as a result of document upload failure
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: Playtech IMS:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: User Age Verification Result status and user tags are received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab. In WS Active Grace Period = “inprocess”
    PRECONDITIONS: **User has received IMS status = Active grace period and tag** (AGP_Success_Upload < 5) OR (POA_Required AND AGP_Success_Upload < 5) OR (POA_Required) **and was navigated to Verification failed screen**
    """
    keep_browser_open = True

    def test_001_tap_on_verify_me_verify_my_address_button_and_on_jumio_service_upload_incorrect_document_3_times_in_a_row(self):
        """
        DESCRIPTION: Tap on VERIFY ME (VERIFY MY ADDRESS) button and on Jumio service upload incorrect document (3 times in a row)
        EXPECTED: User is redirected from Jumio to the screen with Try Again button
        """
        pass

    def test_002_verify_overlay(self):
        """
        DESCRIPTION: Verify overlay
        EXPECTED: - header with Coral label
        EXPECTED: - text Welcome, (first name)
        EXPECTED: - log out button
        EXPECTED: - text from static block **KYC - Upload unsuccessful**
        EXPECTED: Current text set: "It has not been possible to upload your documents"
        EXPECTED: - text from static block **KYC - Retry Upload** Current text set: "Please try again by clicking the button below, or contact Customer Support"
        EXPECTED: - TRY AGAIN button
        EXPECTED: - LIVE CHAT button
        EXPECTED: - text "If you need help contact customer support 24/7”
        """
        pass

    def test_003_tap_on_try_again_button(self):
        """
        DESCRIPTION: Tap on TRY AGAIN button
        EXPECTED: User is redirected to Jumio service
        """
        pass

    def test_004_on_jumio_screen_switch_internet_offon_during_upload_minimize_kill__restore_app(self):
        """
        DESCRIPTION: On Jumio screen switch internet off/on during upload, minimize, kill / restore app
        EXPECTED: Jumio service is loaded after interruptions are finished
        """
        pass

    def test_005_on_jumio_service_upload_incorrect_document_3_times_in_a_row(self):
        """
        DESCRIPTION: On Jumio service upload incorrect document (3 times in a row)
        EXPECTED: User is redirected from Jumio to the screen with Try Again button
        """
        pass
