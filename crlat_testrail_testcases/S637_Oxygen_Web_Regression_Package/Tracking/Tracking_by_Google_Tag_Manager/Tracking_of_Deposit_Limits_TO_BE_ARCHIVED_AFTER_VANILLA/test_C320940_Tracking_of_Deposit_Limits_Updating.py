import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C320940_Tracking_of_Deposit_Limits_Updating(Common):
    """
    TR_ID: C320940
    NAME: Tracking of Deposit Limits Updating
    DESCRIPTION: This Test Case verified tracking in the Google Analytics data Layer when user updates Deposit Limits.
    DESCRIPTION: Jira ticket:
    DESCRIPTION: BMA-15962 Deposit Limits - Updating
    PRECONDITIONS: * Test case should be run on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: * Browser console should be opened
    PRECONDITIONS: * User is Logged In
    PRECONDITIONS: * User has set 'daily/weekly/monthly' balances
    PRECONDITIONS: **Note**
    PRECONDITIONS: Failure from step 18 is possible only in the following case:
    PRECONDITIONS: * E.g., user had daily limit set to 1000, and weekly and monthly limits set to 5000
    PRECONDITIONS: * User changes daily limit to 5000 (this becomes a waiting limit)
    PRECONDITIONS: * After that, user tries to change weekly limit to 1000
    PRECONDITIONS: In such case we receive an error from IMS after tapping 'Update Limits' button (this also applies for all similar cases).
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: 
        """
        pass

    def test_002_log_in(self):
        """
        DESCRIPTION: Log in
        EXPECTED: User is logged in
        """
        pass

    def test_003_navigate_to_my_limits_page(self):
        """
        DESCRIPTION: Navigate to 'My Limits' page
        EXPECTED: * 'My Limits' page is opened
        EXPECTED: * 'Deposit Limits' section is present
        """
        pass

    def test_004_select_value_in_the_deposit_limits_section_from_the_dropdown_from_default_values_for_daily_deposit_limit_weekly_deposit_limit_monthly_deposit_limit(self):
        """
        DESCRIPTION: Select value in the 'Deposit Limits' section from the dropdown (from default values) for:
        DESCRIPTION: * Daily Deposit Limit
        DESCRIPTION: * Weekly Deposit Limit
        DESCRIPTION: * Monthly Deposit Limit
        EXPECTED: Values are selected
        """
        pass

    def test_005_tap_on_update_deposit_limits_button(self):
        """
        DESCRIPTION: Tap on 'Update Deposit Limits' button
        EXPECTED: * Message about 'Your deposit limits have been updated successfully.' is shown
        EXPECTED: * Limits are set successfully
        EXPECTED: * 'Update Deposit Limits' button is disabled
        """
        pass

    def test_006_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'deposit limits',
        EXPECTED: 'eventAction' : 'update',
        EXPECTED: 'eventLabel' : 'success',
        EXPECTED: 'dailyValue' : '<value>',
        EXPECTED: 'weeklyValue' : '<value>',
        EXPECTED: 'monthlyValue' : '<value>'
        EXPECTED: });
        """
        pass

    def test_007_verify_parameters_that_are_present_in_current_object_in_datalayer(self):
        """
        DESCRIPTION: Verify parameters that are present in current object in 'dataLayer'
        EXPECTED: * 'dailyValue' = equal to the value that was selected in the 'Daily Deposit Limit' dropdown
        EXPECTED: * 'weeklyValue' = equal to the value that was selected in the 'Weekly Deposit Limit' dropdown
        EXPECTED: * 'monthlyValue' = equal to the value that was selected in the 'Monthly Deposit Limit' dropdown
        """
        pass

    def test_008_navigate_to_my_limits_page_again(self):
        """
        DESCRIPTION: Navigate to 'My Limits' page again
        EXPECTED: 
        """
        pass

    def test_009_select_other_value_from_the_dropdown_for_daily_deposit_limit_weekly_deposit_limit_monthly_deposit_limit(self):
        """
        DESCRIPTION: Select 'Other' value from the dropdown for:
        DESCRIPTION: * Daily Deposit Limit
        DESCRIPTION: * Weekly Deposit Limit
        DESCRIPTION: * Monthly Deposit Limit
        EXPECTED: Text fields for entering amounts appear near 'Other' dropdowns
        """
        pass

    def test_010_enter_amounts_in_the_corresponding_fields(self):
        """
        DESCRIPTION: Enter amounts in the corresponding fields
        EXPECTED: 
        """
        pass

    def test_011_repeat_steps_5_6(self):
        """
        DESCRIPTION: Repeat steps 5-6
        EXPECTED: 
        """
        pass

    def test_012_verify_parameters_that_are_present_in_current_object_in_datalayer(self):
        """
        DESCRIPTION: Verify parameters that are present in current object in 'dataLayer'
        EXPECTED: * 'dailyValue' = equal to the value that was entered in the amound field in the 'Daily Deposit Limit' field
        EXPECTED: * 'weeklyValue' = equal to the value that was entered in the amound field in the 'Weekly Deposit Limit' field
        EXPECTED: * 'monthlyValue' = equal to the value that was entered in the amound field in the 'Monthly Deposit Limit' field
        """
        pass

    def test_013_navigate_to_my_limits_page_again(self):
        """
        DESCRIPTION: Navigate to 'My Limits' page again
        EXPECTED: 
        """
        pass

    def test_014_change_value_in_the_deposit_limits_section_for_only__daily_deposit_limit_weekly_deposit_limit_not_changed_monthly_deposit_limit_not_changed(self):
        """
        DESCRIPTION: Change value in the 'Deposit Limits' section for only ' Daily Deposit Limit'
        DESCRIPTION: * Weekly Deposit Limit (not changed)
        DESCRIPTION: * Monthly Deposit Limit (not changed)
        EXPECTED: 
        """
        pass

    def test_015_repeat_steps_5_6(self):
        """
        DESCRIPTION: Repeat steps 5-6
        EXPECTED: 
        """
        pass

    def test_016_verify_parameters_that_are_present_in_current_object_in_datalayer(self):
        """
        DESCRIPTION: Verify parameters that are present in current object in 'dataLayer'
        EXPECTED: * 'dailyValue' = equal to the value that was selected for 'Daily Deposit Limit'
        EXPECTED: * 'weeklyValue' = '-'
        EXPECTED: * 'monthlyValue' = '-'
        """
        pass

    def test_017_navigate_to_my_limits_page_again(self):
        """
        DESCRIPTION: Navigate to 'My Limits' page again
        EXPECTED: Values are selected
        """
        pass

    def test_018_trigger_the_following_situation_user_clicks_on_update_deposit_limits_button_from_the_my_account_section_and_the_submission_is_not_successful_please_see_note_from_preconditions(self):
        """
        DESCRIPTION: Trigger the following situation:
        DESCRIPTION: * user clicks on 'Update Deposit Limits' button from the 'My Account' section and the submission is not successful (please see **Note** from Preconditions)
        EXPECTED: 
        """
        pass

    def test_019_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'deposit limits',
        EXPECTED: 'eventAction' : 'update',
        EXPECTED: 'eventLabel' : 'failure',
        EXPECTED: 'dailyValue' : '<value>',
        EXPECTED: 'weeklyValue' : '<value>',
        EXPECTED: 'monthlyValue' : '<value>',
        EXPECTED: 'errorMessage' : '<error message>',
        EXPECTED: 'errorCode' : '<error code>'
        EXPECTED: });
        """
        pass

    def test_020_verify_parameters_that_are_present_in_current_object_in_datalayer(self):
        """
        DESCRIPTION: Verify parameters that are present in current object in 'dataLayer'
        EXPECTED: * 'errorMessage' = equal to the front end error message that a customer sees (the whole text of the message should be fired to the data layer)
        EXPECTED: * 'errorCode' = should equal the back end error code (from the WebSockets)
        """
        pass
