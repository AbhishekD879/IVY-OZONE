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
class Test_C28159_Set_Limits_after_Logout(Common):
    """
    TR_ID: C28159
    NAME: Set Limits after Logout
    DESCRIPTION: This test scenario verifies that user is logged out by server automatically when his/her session is over on the server.
    DESCRIPTION: **Jira tickets:** BMA-5678 (Handle HTTP Error 401)
    PRECONDITIONS: User should be logged in, but session should be OVER on the server
    PRECONDITIONS: To trigger event when session is over on the server please perform the following steps:
    PRECONDITIONS: *   Login to Invictus in one browser tab and open 'My Limits' page
    PRECONDITIONS: *   Login to Invictus in second browser tab, logout -> session is over on the server
    PRECONDITIONS: *   Navigate back to the first browser tab where user is still logged in, however there is no active session already
    """
    keep_browser_open = True

    def test_001_make_steps_from_preconditions_and_verify_my_limits_page(self):
        """
        DESCRIPTION: Make steps from Preconditions and verify 'My Limits' page
        EXPECTED: - User is logged out from the application automatically without performing any actions
        EXPECTED: - User is not able to see the content of '**My Limits**' page
        EXPECTED: - User is redirected to the Homepage where he logged out, login pop up is shown in a tab where he was logged out automatically
        """
        pass

    def test_002_make_steps_from_preconditions_and_changedailyweeklymonthly_deposit_limits(self):
        """
        DESCRIPTION: Make steps from Preconditions and change Daily/Weekly/Monthly  Deposit limits
        EXPECTED: 
        """
        pass

    def test_003_try_to_tap_update_deposit_limits_button(self):
        """
        DESCRIPTION: Try to tap 'Update Deposit Limits' button
        EXPECTED: - User is logged out from the application automatically without performing any actions
        EXPECTED: - User is not able to see the content of '**My Limits**' page
        EXPECTED: - User is redirected to the Homepage where he logged out, login pop up is shown in a tab where he was logged out automatically
        """
        pass

    def test_004_make_steps_from_preconditions_and_try_to_changeset_session_limit(self):
        """
        DESCRIPTION: Make steps from Preconditions and try to change/set Session Limit
        EXPECTED: - User is logged out from the application automatically without performing any actions
        EXPECTED: - User is not able to see the content of '**My Limits**' page
        EXPECTED: - User is redirected to the Homepage where he logged out, login pop up is shown in a tab where he was logged out automatically
        """
        pass

    def test_005_make_steps_from_preconditions_and_changeset_game_play_reminder_frequency(self):
        """
        DESCRIPTION: Make steps from Preconditions and change/set Game Play Reminder Frequency
        EXPECTED: 
        """
        pass

    def test_006_try_to_tap_confirm_button(self):
        """
        DESCRIPTION: Try to tap 'Confirm' button
        EXPECTED: - User is logged out from the application automatically without performing any actions
        EXPECTED: - User is not able to see the content of '**My Limits**' page
        EXPECTED: - User is redirected to the Homepage where he logged out, login pop up is shown in a tab where he was logged out automatically
        """
        pass
