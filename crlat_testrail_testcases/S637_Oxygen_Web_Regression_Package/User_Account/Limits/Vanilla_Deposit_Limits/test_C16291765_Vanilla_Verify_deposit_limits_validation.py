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
class Test_C16291765_Vanilla_Verify_deposit_limits_validation(Common):
    """
    TR_ID: C16291765
    NAME: [Vanilla] Verify deposit limits validation
    DESCRIPTION: Test scenario verifies that Daily/Weekly/Monthly limits that are set up are properly validated when deposit exceeds those limits
    PRECONDITIONS: User has Daily/Weekly/Monthly limits set up in DEPOSIT LIMITS.
    """
    keep_browser_open = True

    def test_001_log_in_as_a_user_with_deposit_limits(self):
        """
        DESCRIPTION: Log in as a user with deposit limits
        EXPECTED: User is logged in successfully
        """
        pass

    def test_002_open_deposit_page(self):
        """
        DESCRIPTION: Open Deposit page
        EXPECTED: Deposit page is open
        """
        pass

    def test_003_select_any_payment_method_fill_required_fields_and_set_amount_higher_than_daily_users_limit_tap_deposit_button(self):
        """
        DESCRIPTION: Select any payment method, fill required fields and set Amount higher than Daily user's limit. Tap 'Deposit' button.
        EXPECTED: Error message: **"SELF-SET DEPOSIT LIMIT EXCEEDED You have exceeded the daily deposit limit previously set by you." ** is shown
        """
        pass

    def test_004_select_any_payment_method_fill_required_fields_and_set_amount_that_is_within_daily_users_limit_tap_deposit_button_repeat_operation_next_days_in_order_to_exceed_weekly_limit_that_is_set_up(self):
        """
        DESCRIPTION: Select any payment method, fill required fields and set Amount that is within Daily user's limit. Tap 'Deposit' button. Repeat operation next days in order to exceed Weekly limit that is set up.
        EXPECTED: Error message: **"SELF-SET DEPOSIT LIMIT EXCEEDED You have exceeded the daily deposit limit previously set by you." ** is shown
        """
        pass

    def test_005_select_any_payment_method_fill_required_fields_and_set_amount_that_is_within_daily_and_weekly_users_limit_tap_deposit_button_repeat_operation_next_weeks_in_order_to_exceed_monthly_limit_that_is_set_up(self):
        """
        DESCRIPTION: Select any payment method, fill required fields and set Amount that is within Daily and Weekly user's limit. Tap 'Deposit' button. Repeat operation next weeks in order to exceed Monthly limit that is set up.
        EXPECTED: Error message: **"SELF-SET DEPOSIT LIMIT EXCEEDED You have exceeded the daily deposit limit previously set by you." ** is shown
        """
        pass
