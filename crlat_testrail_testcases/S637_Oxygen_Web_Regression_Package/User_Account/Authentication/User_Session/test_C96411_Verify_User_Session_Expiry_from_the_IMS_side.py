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
class Test_C96411_Verify_User_Session_Expiry_from_the_IMS_side(Common):
    """
    TR_ID: C96411
    NAME: Verify User Session Expiry from the IMS side
    DESCRIPTION: This test case verifies cases according to which user will be logged out from the application
    PRECONDITIONS: - User has valid account
    PRECONDITIONS: - Make sure session token expiry on the Play Tech side is more that 2 hours (please contact UAT team for checking/updating this info on IMS side) - this is for test environments where the token live time is different
    PRECONDITIONS: NOTE, the default values of Play Tech session token live time are the following:
    PRECONDITIONS: - 50 mins for TST2 environment
    PRECONDITIONS: - 180 mins for STG2 environment
    PRECONDITIONS: The live time of a BPP token = 12 hours
    PRECONDITIONS: Also IMS session token expiry time can be checked in WebSocket 31002 notification, 'sessionTokenExpirationTime' attribute
    """
    keep_browser_open = True

    def test_001_load_oxygen(self):
        """
        DESCRIPTION: Load Oxygen
        EXPECTED: App is loaded
        """
        pass

    def test_002_log_in_with_user_who_has_session_limits_set_as_not_defined(self):
        """
        DESCRIPTION: Log in with user who has session limits set as **Not Defined**
        EXPECTED: User is logged in
        """
        pass

    def test_003_put_the_app_into_background_for_more_that_2_hours(self):
        """
        DESCRIPTION: Put the app into background for more that 2 hours
        EXPECTED: 
        """
        pass

    def test_004_open_app_after_the_time_from_step_3_and_check_user_session(self):
        """
        DESCRIPTION: Open app after the time from step #3 and check user session
        EXPECTED: User is logged in
        """
        pass

    def test_005_make_sure_that_play_tech_session_token_is_expired_contact_uat_for_checking_its_live_time(self):
        """
        DESCRIPTION: Make sure that Play Tech session token is expired (contact UAT for checking its live time)
        EXPECTED: User session token is expired
        """
        pass

    def test_006_check_the_front___end(self):
        """
        DESCRIPTION: Check the front - end
        EXPECTED: User is logged out from the IMS side
        EXPECTED: See DEV console -> Network tab ->  Web Sockets section -> request  ID 31009
        """
        pass

    def test_007_log_in_with_user_who_has_set_its_session_limit_set_as_not_defined_and_make_sure_that_pl_session_token_is_valid_for_more_than_12_hours_please_contact_uat_to_find_out_whether_its_possible(self):
        """
        DESCRIPTION: Log In with user who has set its session limit set as **Not Defined** and make sure that PL session token is valid for more than 12 hours (please contact UAT to find out whether its possible)
        EXPECTED: User is logged in
        """
        pass

    def test_008_wait_for_more_than_12_hours_and_check_the_user_state_put_app_in_background_lock_the_phone_etc(self):
        """
        DESCRIPTION: Wait for more than 12 hours and check the user state (put app in background, lock the phone etc.)
        EXPECTED: - User is logged out
        EXPECTED: - User is logged out from the BPP side due to BPP token expiration (12 hours) - see errors in the DEV console
        EXPECTED: - PT token is still active
        """
        pass
