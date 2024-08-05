import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C28376_Verify_Self_Exclusion_Functionality(Common):
    """
    TR_ID: C28376
    NAME: Verify 'Self Exclusion' Functionality
    DESCRIPTION: This test case verifies 'Self Exclusion' functionality according the story **BMA-3952 **LCCP Auto Self-Exclude Requirement
    PRECONDITIONS: User should be logged in to view the 'Self Exclusion' form
    PRECONDITIONS: On order to check whether user if frozen in IMS side follow the steps:
    PRECONDITIONS: 1. Load IMS system (https://admin-tst2.egalacoral.com/ims/playeredit/10483912?clearPlayerCache=false - for tst2 env)
    PRECONDITIONS: 2. Find teh needed user
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_right_menu_icon(self):
        """
        DESCRIPTION: Tap Right Menu Icon
        EXPECTED: Right Menu slides in from the right
        """
        pass

    def test_003_tap_my_account_item(self):
        """
        DESCRIPTION: Tap 'My account' item
        EXPECTED: 'My account' page is opened with full list of items
        """
        pass

    def test_004_tap_responsible_gambling(self):
        """
        DESCRIPTION: Tap 'Responsible Gambling'
        EXPECTED: The 'Responsible Gambling' page is opened
        """
        pass

    def test_005_tap_read_more_about_self_exclusion_button(self):
        """
        DESCRIPTION: Tap 'Read More About Self Exclusion' button
        EXPECTED: 'Self Exclusion' page is opened
        """
        pass

    def test_006_tap_requestself_exclusion_link(self):
        """
        DESCRIPTION: Tap 'Request Self Exclusion' link
        EXPECTED: The 'Self Exclusion' pop-up is shown
        """
        pass

    def test_007_verify_click_here_to_confirm_that_you_wish_to_self_exclude_link(self):
        """
        DESCRIPTION: Verify 'CLICK HERE to confirm that you wish to Self-Exclude' link
        EXPECTED: 'CLICK HERE to confirm that you wish to Self-Exclude' link is disabled by default
        """
        pass

    def test_008_select_the_period_for_self_exclusion_from_drop_down_for_example_6_months(self):
        """
        DESCRIPTION: Select the period for Self Exclusion from drop down (for example 6 Months)
        EXPECTED: * The value is selected
        EXPECTED: * 'CLICK HERE to confirm that you wish to Self-Exclude' link is become enabled
        """
        pass

    def test_009_enter_a_invalid_password_into_password_field_and_tap_click_here_to_confirm_that_you_wish_to_self_exclude_link(self):
        """
        DESCRIPTION: Enter a invalid password into "Password" field and tap 'CLICK HERE to confirm that you wish to Self-Exclude' link
        EXPECTED: * Error message "Your password is invalid.Please try again" is displayed under "Password" field (field is highlighted with red color)
        EXPECTED: * User is not logged out and user account is not frozen
        """
        pass

    def test_010_enter_a_valid_password_into_password_link(self):
        """
        DESCRIPTION: Enter a valid password into "Password" link
        EXPECTED: 
        """
        pass

    def test_011_tap_click_here_to_confirm_that_you_wish_to_self_exclude_link(self):
        """
        DESCRIPTION: Tap 'CLICK HERE to confirm that you wish to Self-Exclude' link
        EXPECTED: *   User`s account is frozen
        EXPECTED: *   User is logged out automatically
        EXPECTED: *   The confirmation pop up message is shown
        EXPECTED: *   The 'Self Exclusion Request' letter is sent to user`s email
        """
        pass

    def test_012_verify_the_confirmation_sent_to_users_email_automatically(self):
        """
        DESCRIPTION: Verify the confirmation sent to user`s email automatically
        EXPECTED: The confirmation is received to user`s email
        """
        pass

    def test_013_try_to_log_in_with_the_same_credentials1_10(self):
        """
        DESCRIPTION: Try to log in with the same credentials #1-10
        EXPECTED: *   User can not log in
        EXPECTED: *   'Please contact Customer Support. We apologise for any inconvenience caused' message is shown
        EXPECTED: *    Message 'Player is frozen <username>' message is shown in data section in request 31009 in Network tab -> Web Sockets section
        """
        pass

    def test_014_repeat_all_previous_steps_for_the_next_values___from_period_drop_down__1_year__2_years__3_years__4_years__5_years(self):
        """
        DESCRIPTION: Repeat all previous steps for the next values   from period drop down:
        DESCRIPTION: - 1 Year
        DESCRIPTION: - 2 Years
        DESCRIPTION: - 3 Years
        DESCRIPTION: - 4 Years
        DESCRIPTION: - 5 Years
        EXPECTED: *   User`s account is frozen
        EXPECTED: *   User is logged out automatically
        EXPECTED: *   The confirmation pop up message is shown
        EXPECTED: *   The 'Self Exclusion Request' letter is sent to user`s email
        """
        pass
