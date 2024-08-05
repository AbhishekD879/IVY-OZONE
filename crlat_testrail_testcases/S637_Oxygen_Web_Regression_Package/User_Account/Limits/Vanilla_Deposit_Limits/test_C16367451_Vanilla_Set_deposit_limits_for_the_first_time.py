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
class Test_C16367451_Vanilla_Set_deposit_limits_for_the_first_time(Common):
    """
    TR_ID: C16367451
    NAME: [Vanilla] Set deposit limits for the first time
    DESCRIPTION: This test case verifies set up of Daily/Weekly/Monthly deposit limits for the first time
    PRECONDITIONS: User has never set up deposit limits.
    """
    keep_browser_open = True

    def test_001_log_in_as_a_user_without_deposit_limits(self):
        """
        DESCRIPTION: Log in as a user without deposit limits
        EXPECTED: User is logged in successfully
        """
        pass

    def test_002_tap_right_menu_icon___my_account_menu_item(self):
        """
        DESCRIPTION: Tap Right menu icon -> 'My Account' menu item
        EXPECTED: Tap Right menu icon -> 'My Account' menu item
        """
        pass

    def test_003_tap_gambling_controls(self):
        """
        DESCRIPTION: Tap 'GAMBLING CONTROLS'
        EXPECTED: Tap 'GAMBLING CONTROLS'
        """
        pass

    def test_004_check_deposit_limits_image_and_tap_choose__button(self):
        """
        DESCRIPTION: Check 'Deposit Limits' image and tap 'CHOOSE ' button
        EXPECTED: 'DEPOSIT LIMITS' page is open and the is no set up for Daily/Weekly/Monthly limits
        """
        pass

    def test_005_set_daily_limits_and_tap_save_button(self):
        """
        DESCRIPTION: Set **Daily** limits and tap 'SAVE' button
        EXPECTED: There is a message that says that limits has been set up successfully: 'DAILY DEPOSIT LIMIT: Your limits have been changed.'
        """
        pass

    def test_006_set_weekly_limits_and_tap_save_button(self):
        """
        DESCRIPTION: Set **Weekly** limits and tap 'SAVE' button
        EXPECTED: There is a message that says that limits has been set up successfully: 'WEEKLY DEPOSIT LIMIT: Your limits have been changed.'
        """
        pass

    def test_007_set_monthly_limits_and_tap_save_button(self):
        """
        DESCRIPTION: Set **Monthly** limits and tap 'SAVE' button
        EXPECTED: There is a message that says that limits has been set up successfully: 'MONTHLY DEPOSIT LIMIT: Your limits have been changed.'
        """
        pass

    def test_008_go_back_to_the_main_page_of_application_and_do_deposit_that_is_greater_than_dailyweeklymonthly_limit_that_has_been_set_up_in_steps_6_7(self):
        """
        DESCRIPTION: Go back to the main page of application and do deposit that is greater than Daily/Weekly/Monthly limit that has been set up in Steps 6-7
        EXPECTED: Error message: **"SELF-SET DEPOSIT LIMIT EXCEEDED You have exceeded the daily deposit limit previously set by you." ** is shown.
        """
        pass

    def test_009_log_out_and_log_in_with_the_another_user_that_has_no_limits_set_yet(self):
        """
        DESCRIPTION: Log out and log in with the another user that has no limits set yet.
        EXPECTED: User is logged in successfully.
        """
        pass

    def test_010_repeat_step_from_2_5_and_set_dailyweeklymonthly_limits_and_tap_save_button(self):
        """
        DESCRIPTION: Repeat step from 2-5 and set **Daily/Weekly/Monthly** limits and tap 'SAVE' button
        EXPECTED: There is a message that says that limits has been set up successfully: 'DAILY DEPOSIT LIMIT,WEEKLY DEPOSIT LIMIT,MONTHLY DEPOSIT LIMIT: Your limits have been changed.'
        """
        pass

    def test_011_go_back_to_the_main_page_of_application_and_do_deposit_that_is_greater_than_dailyweeklymonthly_limit_that_has_been_set_up_in_step_11(self):
        """
        DESCRIPTION: Go back to the main page of application and do deposit that is greater than Daily/Weekly/Monthly limit that has been set up in Step 11
        EXPECTED: Error message: **"SELF-SET DEPOSIT LIMIT EXCEEDED You have exceeded the daily deposit limit previously set by you." ** is shown.
        """
        pass
