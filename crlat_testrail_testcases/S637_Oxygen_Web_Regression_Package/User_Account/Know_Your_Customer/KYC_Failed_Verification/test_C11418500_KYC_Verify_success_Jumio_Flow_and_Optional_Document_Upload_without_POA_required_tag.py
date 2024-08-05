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
class Test_C11418500_KYC_Verify_success_Jumio_Flow_and_Optional_Document_Upload_without_POA_required_tag(Common):
    """
    TR_ID: C11418500
    NAME: KYC. Verify success Jumio Flow and Optional Document Upload (without POA_required tag)
    DESCRIPTION: This test case verifies that user can upload documents multiple times (WITHOUT POA_required tag)
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: **Playtech IMS**:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: **To find & edit user details in IMS** go to: 'Player Management' tab > Player Search > Enter 'Username' & press 'Enter'
    PRECONDITIONS: **User Age Verification Result status** is received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab)
    PRECONDITIONS: - User with IMS **Age verification status** = *Active grace period* AND **Player tag** = *'AGP_Success_Upload < 5'&'Verification Review'* and has uploaded the documents **(WITHOUT POA_required tag)**
    PRECONDITIONS: - **User is displayed the pop-up 'Account in Review' WITH 'VERIFY MY ADDRESS button'**
    """
    keep_browser_open = True

    def test_001_tap_on_verify_my_address_button_and_on_jumio_service_upload_document(self):
        """
        DESCRIPTION: Tap on VERIFY MY ADDRESS button and on Jumio service upload document
        EXPECTED: - Documents are uploaded successfully
        EXPECTED: - User is redirected on Account in Review' WITHOUT 'VERIFY MY ADDRESS button'
        """
        pass

    def test_002_verify_account_in_review_overlay_without_verify_my_address_button(self):
        """
        DESCRIPTION: Verify "Account in Review" overlay **WITHOUT** 'VERIFY MY ADDRESS' button
        EXPECTED: -Header ACCOUNT IN REVIEW
        EXPECTED: - "Welcome <first name> (logout)"(link)
        EXPECTED: - Text from static block **KYC - Successfully Uploaded Documents**. Current text: "Your documents have successfully been uploaded and are now being reviewed.".
        EXPECTED: - Text from static block **KYC - Get Back Within Time**. Current text: "You will receive an email and onsite message once complete. We aim to do this in just a few minutes but it could take up to 24 hours."
        EXPECTED: - LIVE CHAT(yellow) button  surrounded by text "If you need help contact customer support 24/7”
        EXPECTED: - Close button
        """
        pass

    def test_003_verify_devtool___application___local_storage_are_updated(self):
        """
        DESCRIPTION: Verify Devtool -> Application -> Local Storage are updated
        EXPECTED: Key ***OX.kycOptionalUploadStatus*** is present with value 'username': "Performed"
        """
        pass

    def test_004_verify_ims_tags_are_updated(self):
        """
        DESCRIPTION: Verify IMS tags are updated
        EXPECTED: In IMS:
        EXPECTED: "AGP_Success_Upload" value has **NOT** been incremented on 1
        """
        pass

    def test_005_tap_close_button(self):
        """
        DESCRIPTION: Tap Close button
        EXPECTED: Overlay is closed
        """
        pass
