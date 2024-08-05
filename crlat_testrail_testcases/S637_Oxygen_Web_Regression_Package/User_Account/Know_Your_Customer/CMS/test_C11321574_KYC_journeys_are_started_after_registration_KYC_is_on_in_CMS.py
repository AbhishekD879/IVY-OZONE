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
class Test_C11321574_KYC_journeys_are_started_after_registration_KYC_is_on_in_CMS(Common):
    """
    TR_ID: C11321574
    NAME: KYC journeys are started after registration (KYC is on in CMS)
    DESCRIPTION: This test case verifies that KYC flows are started after registration if KYC feature toggle is on in CMS
    DESCRIPTION: Note: cannot automate, we cannot set some of statuses by script, the rest of statuses are covered in other test cases
    PRECONDITIONS: 1. In CMS > System Configuration > Config:
    PRECONDITIONS: - 'KYC' group is created
    PRECONDITIONS: - Field added in 'KYC' group: 'Field Name' = "enabled; 'Field Type' = "checkbox"
    PRECONDITIONS: 2. In CMS > System Configuration > Structure:
    PRECONDITIONS: - Checkbox "enabled" in 'KYC' table is ON
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
        EXPECTED: KYC journey is started:
        EXPECTED: - 'Pending' verification pop up is shown
        EXPECTED: (when 'ageVerificationStatus' = "unknown" is received (in response with "ID":31083)
        EXPECTED: OR/AND
        EXPECTED: - 'Verification Needed' pop up (when 'ageVerificationStatus' = "inprocess" is received in response with "ID":31083)
        EXPECTED: OR/AND
        EXPECTED: - User is redirected to 'Deposit' page,
        EXPECTED: "KYC_Success" is set (in request "SetPlayerTags"), when 'ageVerificationStatus' = "review"
        """
        pass
