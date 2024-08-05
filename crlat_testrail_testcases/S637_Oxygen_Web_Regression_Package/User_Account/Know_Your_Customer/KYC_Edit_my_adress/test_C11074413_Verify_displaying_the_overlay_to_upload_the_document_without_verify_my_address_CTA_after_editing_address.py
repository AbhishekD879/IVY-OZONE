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
class Test_C11074413_Verify_displaying_the_overlay_to_upload_the_document_without_verify_my_address_CTA_after_editing_address(Common):
    """
    TR_ID: C11074413
    NAME: Verify displaying the overlay to upload the document without verify my address CTA after editing address
    DESCRIPTION: This test case verifies displaying the overlay to upload the document without verify my address CTA after editing address
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: **Playtech IMS**:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: **To find & edit user details in IMS** go to: 'Player Management' tab > Player Search > Enter 'Username' & press 'Enter'
    PRECONDITIONS: **User Age Verification Result status** is received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab)
    PRECONDITIONS: - User with **IMS Age verification status** = *Active grace period* AND **Player tag** = *'AGP_Success_Upload < 5'& POA_Required* has edited his address inside **'Review my details'** pop up
    PRECONDITIONS: - The number of edits for the address is less than 3('Review my details' link is available)
    """
    keep_browser_open = True

    def test_001_before_a_user_clicks_update_address_button_on_review_details_pop_upin_ims__find_a_just_registered_user__delete_player_tags_poa_required__tap_update_info(self):
        """
        DESCRIPTION: Before a user clicks "Update address" button on Review details pop up:
        DESCRIPTION: In IMS:
        DESCRIPTION: - Find a just registered user
        DESCRIPTION: - Delete Player tags “POA required”
        DESCRIPTION: - Tap 'Update Info'
        EXPECTED: - Changes are saved in IMS
        EXPECTED: - Player tags “POA required” is deleted
        """
        pass

    def test_002_click_on_the_update_address_button(self):
        """
        DESCRIPTION: Click on the "Update address" button
        EXPECTED: -Overlay with verification spinner displayed.
        EXPECTED: -Title "VERIFYING YOUR DETAILS" text: "Just a few more seconds, please wait" and loading spinner.
        """
        pass

    def test_003_after_a_user_clicks_update_address_button_on_review_details_pop_upin_app_devtools__verify_response_in_openapi_websocket(self):
        """
        DESCRIPTION: After a user clicks "Update address" button on Review details pop up:
        DESCRIPTION: In app (devtools):
        DESCRIPTION: - Verify response in "openapi" websocket
        EXPECTED: In "openapi" websocket response:
        EXPECTED: - 'ageVerificationStatus' = **"inprocess"** is received (in response with "ID":31083)
        """
        pass

    def test_004_verify_displaying_the_overlay_to_verify_the_address_and_success_screen_without_verify_my_address_cta(self):
        """
        DESCRIPTION: Verify displaying the overlay to verify the address and success screen **without** verify my Address CTA
        EXPECTED: 'Verification failed' overlay is displayed with CMS configurable content:
        EXPECTED: e.g.
        EXPECTED: - Welcome Mark(logout)
        EXPECTED: - You are required to upload one of the following documents
        EXPECTED: - Driving License -> Highly recommended
        EXPECTED: - Passport/National ID card & Utility bill/Bank statement ->
        EXPECTED: If you use a passport or ID card you will ALSO need to provide a utility bill(gas, electric, phone bill OR bank statement issued within the last 3 months)
        EXPECTED: -Green button **"Verify me"** OR "Review my Details" link are present
        EXPECTED: - Yellow button "Live chat" surrounded by text "If you need help contact customer support 24/7"
        """
        pass
