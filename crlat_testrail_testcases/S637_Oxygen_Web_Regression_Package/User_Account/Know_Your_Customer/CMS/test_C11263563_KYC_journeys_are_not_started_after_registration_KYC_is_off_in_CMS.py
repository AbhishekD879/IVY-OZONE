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
class Test_C11263563_KYC_journeys_are_not_started_after_registration_KYC_is_off_in_CMS(Common):
    """
    TR_ID: C11263563
    NAME: KYC journeys are not started after registration (KYC is off in CMS)
    DESCRIPTION: This test case verifies that KYC flows are not started after registration if KYC feature toggle is off in CMS
    DESCRIPTION: Note: cannot automate, we won't disable KYC in automation tests because it can affect other testers.
    PRECONDITIONS: 1. In CMS > System Configuration > Config:
    PRECONDITIONS: - 'KYC' group is created
    PRECONDITIONS: - Field added in 'KYC' group: 'Field Name' = "enabled; 'Field Type' = "checkbox"
    PRECONDITIONS: 2. In CMS > System Configuration > Structure:
    PRECONDITIONS: - Checkbox "enabled" in 'KYC' table is OFF
    PRECONDITIONS: NOTE:
    PRECONDITIONS: Link to CMS:
    PRECONDITIONS: - DEV0: https://cms-api-ui-dev0.coralsports.dev.cloud.ladbrokescoral.com/
    PRECONDITIONS: Login details: test.admin@coral.co.uk/admin
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

    def test_002_tap_on_save_my_preferences_button(self):
        """
        DESCRIPTION: Tap on 'Save My Preferences' button
        EXPECTED: User is navigated to 'Deposit' page
        """
        pass

    def test_003_verify_whether_kyc_journey_is_started(self):
        """
        DESCRIPTION: Verify whether KYC journey is started
        EXPECTED: KYC journey is NOT started:
        EXPECTED: - No 'Pending' verification pop up
        EXPECTED: (when 'ageVerificationStatus' = "unknown" is received (in response with "ID":31083)
        EXPECTED: -  No 'Verification Needed' pop up (when 'ageVerificationStatus' = "inprocess" is received in response with "ID":31083)
        EXPECTED: -  No "KYC_Success" is set (in request "SetPlayerTags"), when 'ageVerificationStatus' = "review"
        """
        pass
