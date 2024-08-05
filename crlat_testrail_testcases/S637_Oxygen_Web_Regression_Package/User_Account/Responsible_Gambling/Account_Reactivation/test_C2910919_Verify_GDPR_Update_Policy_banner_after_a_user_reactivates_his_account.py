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
class Test_C2910919_Verify_GDPR_Update_Policy_banner_after_a_user_reactivates_his_account(Common):
    """
    TR_ID: C2910919
    NAME: Verify GDPR 'Update Policy' banner after a user reactivates his account
    DESCRIPTION: This test case verifies appearing of GDPR 'Update Policy' banner after a user reactivates his account
    DESCRIPTION: AUTOTEST [C9272859]
    PRECONDITIONS: - User's Account is closed (Navigate to Right Menu -> My Account -> select Responsible Gambling item -> Tap/click 'I want to close my Account' link within 'Account Closure' section)
    PRECONDITIONS: - Player Tags: 'Account_Closed_By_Player' is set to 'True' & 'mrktpref_status_seen' is set to 'yes' in IMS
    PRECONDITIONS: - User is logged in
    PRECONDITIONS: - My Account > Reactivation page is opened
    PRECONDITIONS: NOTE: Use STG IMS and STG endpoints for testing
    """
    keep_browser_open = True

    def test_001_enter_valid_value_into_password_field__tap_confirm__tap_ok(self):
        """
        DESCRIPTION: Enter valid value into 'Password' field > Tap 'Confirm' > Tap 'Ok'
        EXPECTED: - User account is reactivated
        EXPECTED: NOTE: In openapi websocket response with ID: 35548, "mrktpref_status_seen"="no" tag is received
        """
        pass

    def test_002_verify_availability_of_update_policy_banner(self):
        """
        DESCRIPTION: Verify availability of 'Update Policy' banner
        EXPECTED: - 'Update Policy' banner appears
        EXPECTED: Note: In next openapi websocket response with ID: 35545, "mrktpref_status_seen"="yes" tag is received
        """
        pass
