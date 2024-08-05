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
class Test_C16425280_TO_BE_REMOVED_Vanilla_No_limit_Daily_Weekly_Monthly_Deposit_Limit_section_on_the_second_last_step_of_registration(Common):
    """
    TR_ID: C16425280
    NAME: TO BE REMOVED [Vanilla] 'No limit/Daily/Weekly/Monthly Deposit Limit' section on the second last step of registration
    DESCRIPTION: This test case verifies 'Daily/Weekly/Monthly Deposit Limit' fields entering on the second last step of registration
    DESCRIPTION: NO MORE SUPPORTED ON GVC PLATFORM, TEST CASE TO BE REMOVED
    PRECONDITIONS: - Oxygen application is loaded
    PRECONDITIONS: - User is not logged in
    """
    keep_browser_open = True

    def test_001_tap_join_button(self):
        """
        DESCRIPTION: Tap 'Join' button
        EXPECTED: Registration form is opened
        """
        pass

    def test_002_navigate_to_the_second_last_registration_page(self):
        """
        DESCRIPTION: Navigate to the second last registration page
        EXPECTED: Page with the second last registration step is opened
        """
        pass

    def test_003_verify_content_of_set_your_deposit_limits_page(self):
        """
        DESCRIPTION: Verify content of 'Set Your Deposit Limits' page
        EXPECTED: - *'You can request limits for the amount of money you will be able to deposit per day, week or month.'* message is displayed above.
        EXPECTED: - 4 'No limit', 'Daily', 'Weekly' & 'Monthly' tab period headers are displayed below.
        EXPECTED: - *'Due to UK online gaming regulations, you must review the following information:
        EXPECTED: Accept our Fund Protection policy. Customer funds are kept in bank accounts separate from other business bank accounts but they form part of the assets of the business in the event of insolvency. This meets the Gambling Commission's requirements for the segregation of customer funds at the level: Basic segregation.'* message is displayed below.
        """
        pass

    def test_004_verify_permitted_values_in_daily_deposit_limit(self):
        """
        DESCRIPTION: Verify permitted values in Daily deposit limit
        EXPECTED: - Drop down with the following default text 'Please select a limit' is displayed below if no data is in amount tab.
        EXPECTED: - *'You can set your limit to a maximum of 9999999 GBP.'* is displayed if you set limit to bigger value than 9999999 GBP.
        """
        pass

    def test_005_set_permitted_value(self):
        """
        DESCRIPTION: Set permitted value
        EXPECTED: Selected value is shown in the 'Amount(GBR)' field
        """
        pass

    def test_006_tap_no_limit(self):
        """
        DESCRIPTION: Tap 'No limit'
        EXPECTED: - No tab 'Amount(GBR)' is shown
        EXPECTED: - 'Accept our Fund Protection policy' message is shown
        EXPECTED: - 'Submit' button present
        """
        pass

    def test_007_repeat_steps_4_5_for_weekly_and_monthly_deposit_limit_tabs(self):
        """
        DESCRIPTION: Repeat steps #4-5 for 'Weekly' and 'Monthly' deposit limit tabs
        EXPECTED: Values are set only for 1 period (eg. Daily or Weekly or Monthly)
        """
        pass

    def test_008_fill_in_valid_information_for_all_required_registration_fieldsset_all_limits_fields_eg_daily___to_some_value_weekly__monthly___no_limits(self):
        """
        DESCRIPTION: Fill in valid information for all required registration fields.
        DESCRIPTION: Set all Limits fields: e.g. 'Daily' - to some value, 'Weekly' & Monthly - No Limits.
        EXPECTED: - All entered data is displayed correctly
        EXPECTED: - No error messages are displayed
        """
        pass

    def test_009_tap_submit_button(self):
        """
        DESCRIPTION: Tap 'Submit' button
        EXPECTED: - 'Deposit' page is shown
        """
        pass

    def test_010_tap_x_button(self):
        """
        DESCRIPTION: Tap 'X' button
        EXPECTED: User is redirected to main page
        """
        pass

    def test_011_tap_my_account_menu___settings_item___gambling_controls(self):
        """
        DESCRIPTION: Tap 'My Account' menu -> 'Settings' item -> 'Gambling Controls'
        EXPECTED: 'Gambling Controls' page is opened
        """
        pass

    def test_012_tap_deposit_limits___choose(self):
        """
        DESCRIPTION: Tap 'Deposit Limits' -> Choose
        EXPECTED: 'Deposit Limits' page is opened
        """
        pass

    def test_013_verify_dailyweeklymonthly_deposit_limit_field(self):
        """
        DESCRIPTION: Verify 'Daily/Weekly/Monthly Deposit Limit' field
        EXPECTED: Field values correspond to the values which were set during registration
        """
        pass
