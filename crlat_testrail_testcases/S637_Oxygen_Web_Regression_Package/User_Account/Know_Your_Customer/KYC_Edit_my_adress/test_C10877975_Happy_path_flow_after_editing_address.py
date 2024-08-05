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
class Test_C10877975_Happy_path_flow_after_editing_address(Common):
    """
    TR_ID: C10877975
    NAME: Happy path flow after editing address
    DESCRIPTION: This test case verifies happy path flow after editing address
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: **Playtech IMS**:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: **To find & edit user details in IMS** go to: 'Player Management' tab > Player Search > Enter 'Username' & press 'Enter'
    PRECONDITIONS: **User Age Verification Result status** is received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab)
    PRECONDITIONS: - User with **IMS Age verification status** = *Active grace period* AND **Player tag** = *'AGP_Success_Upload < 5'* OR *POA_Required & AGP_Success_Upload < 5* (i.e failed 1+1 verification for ID and address) has edited his address inside **'Review details'** pop up
    PRECONDITIONS: - The number of edits for the address is less than 3('Review my details' link is available)
    """
    keep_browser_open = True

    def test_001_before_a_user_clicks_update_address_button_on_review_details_pop_upin_ims__find_a_just_registered_user__change_age_verification_result_to_under_review__tap_update_info(self):
        """
        DESCRIPTION: Before a user clicks "Update address" button on Review details pop up:
        DESCRIPTION: In IMS:
        DESCRIPTION: - Find a just registered user
        DESCRIPTION: - Change 'Age verification result' to **'Under Review'**
        DESCRIPTION: - Tap 'Update Info'
        EXPECTED: - Changes are saved in IMS
        EXPECTED: - Age Verification Result is **'Under Review'**
        """
        pass

    def test_002_click_on_the_update_address_button(self):
        """
        DESCRIPTION: Click on the "Update address" button
        EXPECTED: - Overlay with verification spinner displayed
        EXPECTED: - Title "VERIFYING YOUR DETAILS" text: "Just a few more seconds, please wait" and loading spinner.
        """
        pass

    def test_003_after_a_user_clicks_update_address_button_on_review_details_pop_upin_app_devtools__verify_response_in_openapi_websocket(self):
        """
        DESCRIPTION: After a user clicks "Update address" button on Review details pop up:
        DESCRIPTION: In app (devtools):
        DESCRIPTION: - Verify response in "openapi" websocket
        EXPECTED: In "openapi" websocket:
        EXPECTED: - 'ageVerificationStatus' = **"review"** is received (in response with "ID":31083)
        """
        pass

    def test_004_verify_displaying_the_popup_to_deposit_money(self):
        """
        DESCRIPTION: Verify displaying the popup to deposit money
        EXPECTED: The popup to deposit money is displayed
        """
        pass
