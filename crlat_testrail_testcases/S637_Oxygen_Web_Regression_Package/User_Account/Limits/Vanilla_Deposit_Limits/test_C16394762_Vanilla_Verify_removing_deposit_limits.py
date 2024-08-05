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
class Test_C16394762_Vanilla_Verify_removing_deposit_limits(Common):
    """
    TR_ID: C16394762
    NAME: [Vanilla] Verify removing deposit limits
    DESCRIPTION: This test case verifies removing Daily/Weekly/Monthly deposit limits
    PRECONDITIONS: User has deposit limit set up.
    """
    keep_browser_open = True

    def test_001_log_in_as_a_user_with_deposit_limits_set(self):
        """
        DESCRIPTION: Log in as a user with deposit limits set
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
        EXPECTED: 'DEPOSIT LIMITS' page is open and there are already Daily/Weekly/Monthly limits set up.
        """
        pass

    def test_005_tab_remove_limits_button(self):
        """
        DESCRIPTION: Tab 'REMOVE LIMITS' button
        EXPECTED: 'Confirmation sent. Your requested limits will be available within 24 hours.' message and link 'Cancel my request' is shown.
        EXPECTED: Current limit is not updated.
        """
        pass

    def test_006_within_24_hours_go_back_to_the_main_page_of_application_and_try_to_do_deposit_that_is_greater_than_dailyweeklymonthly_limit_that_had_been_set_up_from_precondition(self):
        """
        DESCRIPTION: Within 24 hours go back to the main page of application and try to do deposit that is greater than Daily/Weekly/Monthly limit that had been set up (from precondition)
        EXPECTED: Error message: **"SELF-SET DEPOSIT LIMIT EXCEEDED You have exceeded the Daily/Weekly/Monthly deposit limit previously set by you." ** is shown.
        """
        pass

    def test_007_log_out_from_application(self):
        """
        DESCRIPTION: Log out from application
        EXPECTED: User is logged out
        """
        pass

    def test_008_log_in_to_the_application_after_24_hours_after_remove_limit_request_had_been_done(self):
        """
        DESCRIPTION: Log in to the application after 24 hours after remove limit request had been done.
        EXPECTED: Pop-up about changes in deposit limits appears.
        """
        pass

    def test_009_tab_confirm_new_limits_in_deposit_limits_page_go_to_account_gambling_controls_deposit_limits_and_check_limits_for_dailyweeklymonthly(self):
        """
        DESCRIPTION: Tab 'CONFIRM NEW LIMITS' in 'DEPOSIT LIMITS' page. Go to Account->GAMBLING CONTROLS->'Deposit limits' and check limits for Daily/Weekly/Monthly.
        EXPECTED: Limits should not be set up (value: None).
        """
        pass

    def test_010_go_back_to_the_main_page_of_application_and_do_deposit_that_is_greater_than_dailyweeklymonthly_limit_that_has_been_set_up_in_preconditions(self):
        """
        DESCRIPTION: Go back to the main page of application and do deposit that is greater than Daily/Weekly/Monthly limit that has been set up in preconditions.
        EXPECTED: Deposit action is done without problem and amount is updated on user's account.
        """
        pass
