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
class Test_C16367454_Vanilla_Verify_Decreasing_of_Users_Limits(Common):
    """
    TR_ID: C16367454
    NAME: [Vanilla ] Verify Decreasing of User's Limits
    DESCRIPTION: This test case verifies decreasing of Daily/Weekly/Monthly deposit limits
    PRECONDITIONS: User has deposit limits set up.
    """
    keep_browser_open = True

    def test_001_log_in_to_application(self):
        """
        DESCRIPTION: Log in to application
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

    def test_005_decrease_daily_deposit_limit_and_tap_save_button(self):
        """
        DESCRIPTION: Decrease **Daily** Deposit Limit and tap 'SAVE' button
        EXPECTED: *   **'DAILY DEPOSIT LIMIT: Your limits have been changed..'** success message is shown
        EXPECTED: *   Current limit is updated accordingly
        """
        pass

    def test_006_decrease_weekly_deposit_limit_and_tap_save_button(self):
        """
        DESCRIPTION: Decrease **Weekly** Deposit Limit and tap 'SAVE' button
        EXPECTED: *   **'WEEKLY DEPOSIT LIMIT: Your limits have been changed.'** success message is shown
        EXPECTED: *   Current limit is updated accordingly
        """
        pass

    def test_007_decrease_monthly_deposit_limit_and_tap_save_button(self):
        """
        DESCRIPTION: Decrease **Monthly** Deposit Limit and tap 'SAVE' button
        EXPECTED: *   **'MONTHLY DEPOSIT LIMIT: Your limits have been changed.'** success message is shown
        EXPECTED: *   Current limit is updated accordingly
        """
        pass

    def test_008_decrease_daily_and_monthly_and_monthly_deposit_limit_and_tap_save_button(self):
        """
        DESCRIPTION: Decrease **Daily** and **Monthly** and **Monthly** Deposit Limit and tap 'SAVE' button
        EXPECTED: *   **'DAILY DEPOSIT LIMIT,WEEKLY DEPOSIT LIMIT,MONTHLY DEPOSIT LIMIT: Your limits have been changed..'** success message is shown
        EXPECTED: *   Current limit is updated accordingly
        """
        pass

    def test_009_open_deposit_limits_and_verify_limits_from_point_6_9_by_doing_a_deposit_that_is_greater_than_dailyweeklymonthly_limits_but_lower_than_previous_limits(self):
        """
        DESCRIPTION: Open 'DEPOSIT LIMITS' and verify limits from point 6-9 by doing a deposit that is greater than Daily/Weekly/Monthly limits but lower than previous limits.
        EXPECTED: Error message: **"SELF-SET DEPOSIT LIMIT EXCEEDED You have exceeded the daily deposit limit previously set by you." ** is shown
        """
        pass
