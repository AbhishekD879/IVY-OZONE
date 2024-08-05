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
class Test_C10841491_Verify_happy_KYC_verification_journey_after_registration(Common):
    """
    TR_ID: C10841491
    NAME: Verify happy KYC verification journey after registration
    DESCRIPTION: This test case verifies happy KYC verification journey after a new user is registered
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: - Oxygen app is loaded
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - Link to access IMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: - To find & edit user details in IMS go to: 'Player Management' tab > Player Search > Enter 'Username' & press 'Enter'
    PRECONDITIONS: - To be able to receive 'ageVerificationStatus' = "review" right after registration > ask a developer to make a delay for a few seconds between registration and auto-login and change user status in IMS.
    """
    keep_browser_open = True

    def test_001___tap_join_now__fill_out_required_fields_on_each_registration_page__tap_complete_registration_on_registration___account_details_page(self):
        """
        DESCRIPTION: - Tap 'Join Now'
        DESCRIPTION: - Fill out required fields on each 'Registration' page
        DESCRIPTION: - Tap 'Complete Registration' on 'Registration - Account Details' page
        EXPECTED: 'Marketing Preferences' screen is shown
        """
        pass

    def test_002_before_a_user_is_auto_logged_inin_ims__find_a_just_registered_user__change_age_verification_result_to_under_review__tap_update_info(self):
        """
        DESCRIPTION: Before a user is auto logged in:
        DESCRIPTION: In IMS:
        DESCRIPTION: - Find a just registered user
        DESCRIPTION: - Change 'Age verification result' to 'Under review'
        DESCRIPTION: - Tap 'Update Info'
        EXPECTED: Changes are saved in IMS
        """
        pass

    def test_003_after_a_user_is_auto_logged_in__verify_response_in_openapi_websocket(self):
        """
        DESCRIPTION: After a user is auto logged in:
        DESCRIPTION: - Verify response in "openapi" websocket
        EXPECTED: In "openapi" websocket:
        EXPECTED: - 'ageVerificationStatus' = "review" is received (in response with "ID":31083)
        EXPECTED: - Tag 'name': "KYC_Success" is set (in request "SetPlayerTags")
        """
        pass

    def test_004_in_app__tap_on_save_my_preferences_button(self):
        """
        DESCRIPTION: In app:
        DESCRIPTION: - Tap on 'Save My Preferences' button
        EXPECTED: 'Deposit' page is opened
        """
        pass
