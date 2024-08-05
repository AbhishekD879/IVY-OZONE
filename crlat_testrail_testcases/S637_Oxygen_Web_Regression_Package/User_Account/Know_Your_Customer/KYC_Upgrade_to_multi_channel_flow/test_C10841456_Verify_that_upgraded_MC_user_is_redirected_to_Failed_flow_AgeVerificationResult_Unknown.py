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
class Test_C10841456_Verify_that_upgraded_MC_user_is_redirected_to_Failed_flow_AgeVerificationResult_Unknown(Common):
    """
    TR_ID: C10841456
    NAME: Verify that upgraded MC user is redirected to Failed flow (AgeVerificationResult = "Unknown")
    DESCRIPTION: This test case verifies that the user who has just finished upgrading process and has 'Age verification result' = "Unknown" in IMS is redirected to failed flow
    PRECONDITIONS: * Make sure Upgrade feature is turned on in CMS: System configuration -> Connect -> upgrade
    PRECONDITIONS: * In-shop user should be logged in and upgraded. [How to create In-Shop user](https://confluence.egalacoral.com/display/SPI/Create+In-Shop+user)
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - Link to access IMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: - To find & edit user details in IMS go to: 'Player Management' tab > Player Search > Enter 'Username' & press 'Enter'
    PRECONDITIONS: * User Age Verification Result status is received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab)
    """
    keep_browser_open = True

    def test_001___open_connect_from_header_ribbon__tap_use_connect_online__fill_all_required_fields_correctly_use_unique_data_for_mail_and_phone_number__tap_confirm_button(self):
        """
        DESCRIPTION: - Open 'Connect' from header ribbon
        DESCRIPTION: - Tap 'Use Connect Online'
        DESCRIPTION: - Fill all required fields correctly (use unique data for mail and phone number)
        DESCRIPTION: - Tap 'Confirm' button
        EXPECTED: * The in-shop user is upgraded to the multichannel user successfully
        EXPECTED: * 'Success Upgrade' pop up with verification spinner appears
        """
        pass

    def test_002_before_a_user_is_auto_logged_inin_ims_find_just_updated_user_by_his_username_if_needed_change_age_verification_result_to_unknown_tap_update_info(self):
        """
        DESCRIPTION: Before a user is auto-logged in:
        DESCRIPTION: In IMS:
        DESCRIPTION: * Find just updated user by his username
        DESCRIPTION: * If needed, change 'Age verification result' to "unknown"
        DESCRIPTION: * Tap 'Update Info'
        EXPECTED: - Changes are saved in IMS
        EXPECTED: - 'Age verification result' = "unknown"
        """
        pass

    def test_003_in_appverify_that_user_is_navigated_to_failed_flow_right_after_login(self):
        """
        DESCRIPTION: In app:
        DESCRIPTION: Verify that user is navigated to 'Failed' flow right after login
        EXPECTED: 'Verification Failed' page is shown with 'Verify Me' button
        """
        pass
