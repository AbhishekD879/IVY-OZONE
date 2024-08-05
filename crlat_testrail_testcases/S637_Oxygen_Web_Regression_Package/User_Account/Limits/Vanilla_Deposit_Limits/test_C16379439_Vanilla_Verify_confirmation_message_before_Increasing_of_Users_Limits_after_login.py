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
class Test_C16379439_Vanilla_Verify_confirmation_message_before_Increasing_of_Users_Limits_after_login(Common):
    """
    TR_ID: C16379439
    NAME: [Vanilla] Verify confirmation message before Increasing of User's Limits after login
    DESCRIPTION: his test case verifies appearing of confirmation message after the 24 hours has elapsed before Increasing of Users' Limits after user loggs in.
    PRECONDITIONS: - Users' limits are lower than 99 00000
    PRECONDITIONS: - Two users changed their Deposit Limits less than 24 hours ago
    PRECONDITIONS: NOTE: if other pop-up messages are expected after log in then the order of pop-up appearing should be the following:
    PRECONDITIONS: Terms and Conditions -> Verify Your Account (Netverify) -> Deposit Limits -> Quick Deposit -> Casino bonuses
    """
    keep_browser_open = True

    def test_001_wait_till_24_hours_elapse_from_the_moment_ofincreasing_of_users_limits(self):
        """
        DESCRIPTION: Wait till 24 hours elapse from the moment of Increasing of User's Limits
        EXPECTED: 
        """
        pass

    def test_002_log_in_with_the_first_user(self):
        """
        DESCRIPTION: Log in with the first user
        EXPECTED: *  User is logged in
        EXPECTED: *  'DEPOSIT LIMITS' pop-up appears
        """
        pass

    def test_003_verify_deposit_limits_pop_up(self):
        """
        DESCRIPTION: Verify 'DEPOSIT LIMITS' pop-up
        EXPECTED: 'DEPOSIT LIMITS' pop-up consists of the following:
        EXPECTED: 1.  TITLE: **'DEPOSIT LIMITS'** with close 'X button' available
        EXPECTED: 2.  BODY:
        EXPECTED: - **'Please confirm your new deposit limits to be changed'** text displayed
        EXPECTED: - Information about new and current limits with currency symbol and amount for: DAILY LIMIT, WEEKLY LIMIT, MONTHLY LIMIT
        EXPECTED: 3.  BUTTONS: **CONFIRM NEW LIMITS** and **CANCEL REQUEST** and **Remind me later**
        """
        pass

    def test_004_verify_cancel_request_button(self):
        """
        DESCRIPTION: Verify 'CANCEL REQUEST' button
        EXPECTED: After tapping 'CANCEL REQUEST' button:
        EXPECTED: *   user's limit is not increased
        EXPECTED: *   pop-up disappears
        """
        pass

    def test_005_log_out_with_the_first_user_and_log_in_with_second_one_given_that_there_is_some_time_left_before_24_hours_pass(self):
        """
        DESCRIPTION: Log out with the first user and log in with second one (given that there is some time left before 24 hours pass)
        EXPECTED: 2nd user is logged in
        """
        pass

    def test_006_wait_till_24_hours_elapse_from_the_moment_ofincreasing_of_users_limits_while_staying_in_the_app(self):
        """
        DESCRIPTION: Wait till 24 hours elapse from the moment of Increasing of Users' Limits while staying in the app
        EXPECTED: 
        """
        pass

    def test_007_verify_appearing_of_deposit_limits_pop_up(self):
        """
        DESCRIPTION: Verify appearing of 'DEPOSIT LIMITS' pop-up
        EXPECTED: Pop-up is displayed right after the 24 hours have elapsed
        """
        pass

    def test_008_verify_deposit_limits_pop_up(self):
        """
        DESCRIPTION: Verify 'DEPOSIT LIMITS' pop-up
        EXPECTED: 'DEPOSIT LIMITS' pop-up consists of the following:
        EXPECTED: 1.  TITLE: **'DEPOSIT LIMITS'** with close 'X button' available
        EXPECTED: 2.  BODY:
        EXPECTED: - **'Please confirm your new deposit limits to be changed'** text displayed
        EXPECTED: - Information about new and current limits with currency symbol and amount for: DAILY LIMIT, WEEKLY LIMIT, MONTHLY LIMIT
        EXPECTED: 3.  BUTTONS: **CONFIRM NEW LIMITS** and **CANCEL REQUEST** and **Remind me later**
        """
        pass

    def test_009_verify_confirm_new_limits_button(self):
        """
        DESCRIPTION: Verify 'CONFIRM NEW LIMITS' button
        EXPECTED: After tapping 'CONFIRM NEW LIMITS' button:
        EXPECTED: *   user's limit is increased to value, which was set 24 hours ago
        EXPECTED: *   pop-up disappears
        """
        pass

    def test_010_navigate_to_my_limits_page_and_check_whether_the_users_limit_has_changed(self):
        """
        DESCRIPTION: Navigate to 'My Limits' page and check whether the user's limit has changed
        EXPECTED: User's limit is increased on 'My Limits' page in 'GAMBLING CONTROLS' section
        """
        pass
