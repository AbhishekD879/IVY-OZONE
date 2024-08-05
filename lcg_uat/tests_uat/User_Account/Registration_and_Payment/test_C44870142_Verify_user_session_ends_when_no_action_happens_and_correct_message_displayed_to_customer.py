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
class Test_C44870142_Verify_user_session_ends_when_no_action_happens_and_correct_message_displayed_to_customer(Common):
    """
    TR_ID: C44870142
    NAME: Verify user session ends when no action happens and correct message displayed to customer
    DESCRIPTION: The user should be Logged in without ticking the 'REMEMBER ME' check box. And there should be no activity for 2 hours.
    PRECONDITIONS: Session limit set to 2 hours in API.
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_log_in_without_ticking_the_remember_me_check_box(self):
        """
        DESCRIPTION: Log in without ticking the 'REMEMBER ME' check box
        EXPECTED: User is logged in and on the Homepage.
        """
        pass

    def test_003_leave_the_app_ideal_for_2_hours(self):
        """
        DESCRIPTION: Leave the app ideal for 2 hours
        EXPECTED: The user should be logged off as there was no activity since two hours.
        EXPECTED: And should be notified stating session expired.
        """
        pass
