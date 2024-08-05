import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C96285_Verify_User_Session_Support_after_more_than_2_hours_of_inactivity(Common):
    """
    TR_ID: C96285
    NAME: Verify User Session Support after more than 2 hours of inactivity
    DESCRIPTION: This test case verifies the user session support after more that 2 hours of inactivity on the site
    PRECONDITIONS: - Make sure user session limit is set as 'not defined'
    PRECONDITIONS: - Make sure session token expiry on the Play Tech side is more than 2 hours (please contact UAT team for checking/updating this info on IMS side) - this is for test environments where the token live time is different
    PRECONDITIONS: NOTE, the default values of Play Tech session token live time are the following:
    PRECONDITIONS: - 50 mins for TST2 environment
    PRECONDITIONS: - 180 mins for STG2 environment
    PRECONDITIONS: Also IMS session token expiry time can be checked in WebSocket 31002 notification, 'sessionTokenExpirationTime' attribute
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: App is loaded
        """
        pass

    def test_002_log_in_as_a_user_with_valid_credentialsmake_sure_pre_conditions_are_met(self):
        """
        DESCRIPTION: Log in as a user with valid credentials
        DESCRIPTION: Make sure pre-conditions are met
        EXPECTED: User is logged in
        EXPECTED: User login time is detected
        EXPECTED: BPP session token is created
        """
        pass

    def test_003_leave_user_inactive_for_more_than_2_hours_2_hours_and_15_mins___eg_put_device_with_app_in_a_background_lock_the_phone_etc(self):
        """
        DESCRIPTION: Leave user inactive for more than 2 hours (~2 hours and 15 mins) - e.g put device with app in a background, lock the phone etc.
        EXPECTED: User is left as inactive
        """
        pass

    def test_004_open_app_after_time_from_the_step_3(self):
        """
        DESCRIPTION: Open app after time from the step #3
        EXPECTED: App is loaded
        """
        pass

    def test_005_check_the_user_session_state(self):
        """
        DESCRIPTION: Check the user session state
        EXPECTED: User session is active
        """
        pass

    def test_006_try_to_add_selection_to_the_bet_slip_and_place_a_bet_on_selected_bet(self):
        """
        DESCRIPTION: Try to add selection to the Bet Slip and place a bet on selected bet
        EXPECTED: Selection is added
        EXPECTED: placeBet is finished correctly (bet Api token is alive)
        """
        pass

    def test_007_try_to_reach_account_history_bet_history_etc(self):
        """
        DESCRIPTION: Try to reach account history (bet history etc)
        EXPECTED: Account history is displayed correctly (OXiApi token is alive)
        EXPECTED: User remains logged in
        """
        pass
