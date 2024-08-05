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
class Test_C16367452_Vanilla_Verify_Increasing_of_Users_Limits(Common):
    """
    TR_ID: C16367452
    NAME: [Vanilla] Verify Increasing of User's Limits
    DESCRIPTION: This test case verifies increasing of Daily/Weekly/Monthly deposit limits
    DESCRIPTION: Note: Cannot be automated as we cannot wait 24 h for new limits to change
    PRECONDITIONS: User has already deposit limits set up.
    """
    keep_browser_open = True

    def test_001_log_in_as_a_user_who_has_already_deposit_limits_set_up(self):
        """
        DESCRIPTION: Log in as a user who has already deposit limits set up.
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
        EXPECTED: 'DEPOSIT LIMITS' page is open and there is set up for Daily/Weekly/Monthly limits
        """
        pass

    def test_005_increase_daily_deposit_limit_and_tap_save_button(self):
        """
        DESCRIPTION: Increase **Daily** Deposit Limit and tap 'SAVE' button
        EXPECTED: 'Confirmation sent. Your requested limits will be available within 24 hours.' message and link 'Cancel my request' is shown.
        EXPECTED: Current limit is not updated
        """
        pass

    def test_006_increase_weekly_deposit_limit_and_tap_save_button(self):
        """
        DESCRIPTION: Increase **Weekly** Deposit Limit and tap 'SAVE' button
        EXPECTED: 'Confirmation sent. Your requested limits will be available within 24 hours.' message and link 'Cancel my request' is shown.
        EXPECTED: Current limit is not updated
        """
        pass

    def test_007_increase_monthly_deposit_limit_and_tap_save_button(self):
        """
        DESCRIPTION: Increase **Monthly** Deposit Limit and tap 'SAVE' button
        EXPECTED: 'Confirmation sent. Your requested limits will be available within 24 hours.' message and link 'Cancel my request' is shown.
        EXPECTED: Current limit is not updated
        """
        pass

    def test_008_increase_daily_weekly_and_monthly_deposit_limits_and_tap_save_button(self):
        """
        DESCRIPTION: Increase **Daily**, **Weekly** and **Monthly** Deposit Limits and tap 'SAVE' button
        EXPECTED: 'Confirmation sent. Your requested limits will be available within 24 hours.' message and link 'Cancel my request' is shown.
        EXPECTED: Current limit is not updated
        """
        pass

    def test_009_open_deposit_limits_within_24_hours_after_change_limit_request_was_done_and_check_current_limits(self):
        """
        DESCRIPTION: Open 'DEPOSIT LIMITS' within 24 hours after change limit request was done and check current limits
        EXPECTED: 'Confirmation sent. Your requested limits will be available within 24 hours.' message and link 'Cancel my request' is shown.
        EXPECTED: Current limit is not updated
        """
        pass

    def test_010__login_to_application_after_24_hours_after_change_limit_is_requested_when_confirmation_of_deposit_limit_changes_pop_up_appears_accept_limits_changes_go_to_deposit_limits_page_and_verify_limits(self):
        """
        DESCRIPTION: * Login to application after 24 hours after change limit is requested.
        DESCRIPTION: * When confirmation of deposit limit changes pop-up appears accept limits changes
        DESCRIPTION: * Go to 'DEPOSIT LIMITS' page and verify limits
        EXPECTED: New values of deposit limits are set up and there is no message about pending change request.
        """
        pass

    def test_011_go_to_main_page_and_do_deposit_that_is_greater_that_current_daily_limit_but_lower_than_new_values_that_was_set_up(self):
        """
        DESCRIPTION: Go to main page and do deposit that is greater that current Daily limit but lower than new values that was set up
        EXPECTED: Deposit is done successfully.
        """
        pass
