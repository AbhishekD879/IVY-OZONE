import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C10850262_Verify_happy_KYC_verification_journey_after_user_refreshes_GDPR_screen_upon_registration(Common):
    """
    TR_ID: C10850262
    NAME: Verify happy KYC verification journey after user refreshes GDPR screen upon registration
    DESCRIPTION: This test case verifies happy KYC verification journey after a user refreshes the page on GDPR screen after registration
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: - Oxygen app is loaded
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - Link to access IMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: - To find & edit user details in IMS go to: 'Player Management' tab > Player Search > Enter 'Username' & press 'Enter'
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

    def test_002_in_ims__find_a_just_registered_user__change_age_verification_result_to_under_review__tap_update_info(self):
        """
        DESCRIPTION: In IMS:
        DESCRIPTION: - Find a just registered user
        DESCRIPTION: - Change 'Age verification result' to 'Under review'
        DESCRIPTION: - Tap 'Update Info'
        EXPECTED: Changes are saved in IMS
        """
        pass

    def test_003_in_app_refresh_the_page_on_gdpr_screen(self):
        """
        DESCRIPTION: In app: Refresh the page on GDPR screen
        EXPECTED: - 'Deposit' page is opened
        EXPECTED: In "openapi" websocket:
        EXPECTED: - 'ageVerificationStatus' = "review" is received (in response with "ID":31083)
        """
        pass
