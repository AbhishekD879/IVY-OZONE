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
class Test_C44870140_Need_To_UpdateVerify_self_excluded_customer_error_message_and_user_cant_login_to_the_site(Common):
    """
    TR_ID: C44870140
    NAME: [Need To Update]Verify self excluded customer error message and user can't login to the site.
    DESCRIPTION: 
    PRECONDITIONS: User should be logged in to view the 'Self Exclusion' form
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_my_account_item(self):
        """
        DESCRIPTION: Tap 'My account' item
        EXPECTED: 'My account' page is opened with full list of items
        """
        pass

    def test_003_tap_gambling_controls(self):
        """
        DESCRIPTION: Tap 'Gambling controls'
        EXPECTED: The 'Gambling controls' page is opened
        """
        pass

    def test_004_select_account_closure__reopening___choose(self):
        """
        DESCRIPTION: Select 'Account Closure & Reopening'  & Choose
        EXPECTED: Account Closure & Reopening page  is displayed
        EXPECTED: With two options
        EXPECTED: 1. I want to close my account or sections of it
        EXPECTED: 2. I'd like to take an irreversible time-out or exclude myself from gaming.
        """
        pass

    def test_005_verify_cancel_button(self):
        """
        DESCRIPTION: Verify Cancel button
        EXPECTED: Cancel button is active and user is redirected to the previous page (Gambling controls) when clicks on Cancel
        """
        pass

    def test_006_select_account_closure__reopening___choose(self):
        """
        DESCRIPTION: Select 'Account Closure & Reopening'  & Choose
        EXPECTED: Account Closure & Reopening page  is displayed
        EXPECTED: With two options
        EXPECTED: 1. I want to close my account or sections of it
        EXPECTED: 2. I'd like to take an irreversible time-out or exclude myself from gaming.
        """
        pass

    def test_007_select_id_like_to_take_an_irreversible_time_out_or_exclude_myself_from_gaming(self):
        """
        DESCRIPTION: Select 'I'd like to take an irreversible time-out or exclude myself from gaming.
        EXPECTED: Option is selected and Continue button becomes active
        """
        pass

    def test_008_verify_continue_button(self):
        """
        DESCRIPTION: Verify Continue button
        EXPECTED: User is taken to Take a short time-out page with options & reason for taking break
        EXPECTED: Note: For 'Self-Exclusion' the user has to click the 'Self-exclusion' link at the bottom.
        """
        pass

    def test_009_click_on_the_self_exclusion_link(self):
        """
        DESCRIPTION: Click on the Self Exclusion link
        EXPECTED: The user is taken to next page with Self-exclusion & Gamstop options
        """
        pass

    def test_010_select_self_exclusion_and_choose(self):
        """
        DESCRIPTION: Select 'Self-exclusion' and Choose
        EXPECTED: Self-exclusion page is opened with options of select the Period to be excluded and brand to select with drop down.
        """
        pass

    def test_011_verify_select_the_brand_you_wish_to_exclude_from_from_the_drop_down_a(self):
        """
        DESCRIPTION: Verify 'Select the brand you wish to exclude from' from the drop down a
        EXPECTED: User is able to select the brand from where they want to be excluded
        EXPECTED: Once selected, the "Continue" button becomes active.
        """
        pass

    def test_012_select_continue_after_choosing_time_brand_to_be_self_exculded__tick_box(self):
        """
        DESCRIPTION: Select "Continue" after choosing time, brand to be self-exculded & tick box
        EXPECTED: User is taken to the next page asking to enter "Password"
        EXPECTED: "Self-exclude" tab is inactive when no password is entered.
        """
        pass

    def test_013_enter_a_invalid_password_into_password_field_and_select_self_exclude(self):
        """
        DESCRIPTION: Enter a invalid password into "Password" field and select "Self-Exclude"
        EXPECTED: Error message "Incorrect password" (field is highlighted with red colour)
        """
        pass

    def test_014_enter_a_valid_password_into_password_link_and_select_self_exclude(self):
        """
        DESCRIPTION: Enter a valid password into "Password" link and select "Self-exclude"
        EXPECTED: Confirmation of self exclusion box is opened with
        EXPECTED: two tick boxes
        EXPECTED: 1. I confirm that I wish to self-exclude.......
        EXPECTED: 2. I understand that during this period...........
        EXPECTED: with "YES" button inactive
        """
        pass

    def test_015_select_both_the_tick_boxes_and_tap_yes(self):
        """
        DESCRIPTION: Select both the tick boxes and tap "Yes"
        EXPECTED: The confirmation pop up message is shown
        EXPECTED: "You have successfully excluded from all our products"
        EXPECTED: User is not logged out of the app.
        """
        pass

    def test_016_navigate_to_the_homepage_and_try_placing_any_bets(self):
        """
        DESCRIPTION: Navigate to the Homepage and try placing any bets
        EXPECTED: User will not be able to place bets.
        """
        pass

    def test_017_log_off_and_try_to_log_in_with_the_same_credentials(self):
        """
        DESCRIPTION: Log off and try to log in with the same credentials
        EXPECTED: User cannot log in
        EXPECTED: error message shown stating
        EXPECTED: "Your account is locked because you have chosen to self-exclude......."
        """
        pass
