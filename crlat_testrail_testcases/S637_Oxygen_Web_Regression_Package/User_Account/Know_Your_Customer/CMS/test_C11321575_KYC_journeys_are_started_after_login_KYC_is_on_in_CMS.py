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
class Test_C11321575_KYC_journeys_are_started_after_login_KYC_is_on_in_CMS(Common):
    """
    TR_ID: C11321575
    NAME: KYC journeys are started after login (KYC is on in CMS)
    DESCRIPTION: This test case verifies that KYC flows are started after login if KYC feature toggle is on in CMS
    DESCRIPTION: Note: cannot automate, we cannot set some of statuses by script, the rest of statuses are covered in other test cases
    PRECONDITIONS: 1. In CMS > System Configuration > Config:
    PRECONDITIONS: - 'KYC' group is created
    PRECONDITIONS: - Field added in 'KYC' group: 'Field Name' = "enabled; 'Field Type' = "checkbox"
    PRECONDITIONS: 2. In CMS > System Configuration > Structure:
    PRECONDITIONS: - Checkbox "enabled" in 'KYC' table is ON
    PRECONDITIONS: 3. In IMS: 'Age verification result' is set to 'Unknown' for a user
    PRECONDITIONS: 4. Oxygen app is loaded
    PRECONDITIONS: NOTE:
    PRECONDITIONS: Link to CMS:
    PRECONDITIONS: - DEV0: https://cms-api-ui-dev0.coralsports.dev.cloud.ladbrokescoral.com/
    PRECONDITIONS: Login details: test.admin@coral.co.uk/admin
    PRECONDITIONS: - Link to access IMS:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Ladbrokes+Environments
    PRECONDITIONS: - To find & edit user details in IMS go to: 'Player Management' tab > Player Search > Enter 'Username' & press 'Enter'
    """
    keep_browser_open = True

    def test_001_login_with_a_user_from_step_3_in_preconditions(self):
        """
        DESCRIPTION: Login with a user (from step 3 in Preconditions)
        EXPECTED: 'Pending Verification' KYC journey is started:
        EXPECTED: - 'Pending' verification pop up is shown
        EXPECTED: (when 'ageVerificationStatus' = "unknown" is received (in response with "ID":31083)
        """
        pass

    def test_002_in_ims__find_a_user__change_age_verification_result_to_active_grace_period__tap_update_info(self):
        """
        DESCRIPTION: In IMS:
        DESCRIPTION: - Find a user
        DESCRIPTION: - Change 'Age verification result' to 'Active grace period'
        DESCRIPTION: - Tap 'Update Info'
        EXPECTED: Changes are saved in IMS
        """
        pass

    def test_003_in_app_refresh_the_page(self):
        """
        DESCRIPTION: In app: Refresh the page
        EXPECTED: 'Failed Verification' KYC journey is started:
        EXPECTED: - 'Verification Needed' page
        EXPECTED: ('ageVerificationStatus' = "inprocess" is received (in response with "ID":31083)
        """
        pass

    def test_004_in_ims__find_a_user__change_age_verification_result_to_under_review__tap_update_info(self):
        """
        DESCRIPTION: In IMS:
        DESCRIPTION: - Find a user
        DESCRIPTION: - Change 'Age verification result' to 'Under review'
        DESCRIPTION: - Tap 'Update Info'
        EXPECTED: Changes are saved in IMS
        """
        pass

    def test_005_in_app_refresh_the_page(self):
        """
        DESCRIPTION: In app: Refresh the page
        EXPECTED: - 'Happy' KYC journey is started
        EXPECTED: - User is able to deposit/place bet
        """
        pass
