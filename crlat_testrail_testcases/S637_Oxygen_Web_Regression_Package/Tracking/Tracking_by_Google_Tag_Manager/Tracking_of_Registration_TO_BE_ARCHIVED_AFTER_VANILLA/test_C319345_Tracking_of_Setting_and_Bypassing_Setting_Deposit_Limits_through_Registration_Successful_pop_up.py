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
class Test_C319345_Tracking_of_Setting_and_Bypassing_Setting_Deposit_Limits_through_Registration_Successful_pop_up(Common):
    """
    TR_ID: C319345
    NAME: Tracking of Setting and Bypassing Setting Deposit Limits through 'Registration Successful!' pop-up
    DESCRIPTION: This Test Case verifies tracking in the Google Analytic's data Layer when user clicks on "Set Deposit Limits" button during the registration process in the 'Registration Successful!' pop-up.
    DESCRIPTION: Jira tickets:
    DESCRIPTION: * BMA-15810 Deposit Limits - Setting
    DESCRIPTION: * BMA-15963 Deposit Limits - Bypassing - no longer required due to story BMA-22619 [RG Toolkit DL016] Deposit Limits Default
    PRECONDITIONS: * Test case should be run on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: * Browser console should be opened
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: 
        """
        pass

    def test_002_tap_on_join_now_button(self):
        """
        DESCRIPTION: Tap on 'Join now' button
        EXPECTED: * Page 'Registration - Step 1 of 2' is shown on Desktop/ Tablet
        EXPECTED: * Page 'Registration - Step 1 of 3' is shown on Mobile devices
        """
        pass

    def test_003_fill_all_required_data_and_register_new_user(self):
        """
        DESCRIPTION: Fill all required data and register new user
        EXPECTED: * User is registered successfully and logged in automatically
        EXPECTED: * 'Registration Successful!' pop-up is shown
        EXPECTED: * 'Set deposit limits' button is disabled by default
        """
        pass

    def test_004_select_value_from_the_dropdown_from_default_values_for_daily_deposit_limit_weekly_deposit_limit_monthly_deposit_limit(self):
        """
        DESCRIPTION: Select value from the dropdown (from default values) for:
        DESCRIPTION: * Daily Deposit Limit
        DESCRIPTION: * Weekly Deposit Limit
        DESCRIPTION: * Monthly Deposit Limit
        EXPECTED: * Values are selected
        EXPECTED: * 'Set deposit limits' button becomes enabled
        """
        pass

    def test_005_tap_on_set_deposit_limits_button(self):
        """
        DESCRIPTION: Tap on 'Set deposit limits' button
        EXPECTED: * 'Successful Registration' pop-up is closed
        EXPECTED: * Limits are set successfully
        """
        pass

    def test_006_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'deposit limits',
        EXPECTED: 'eventAction' : 'set',
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
        EXPECTED: * 'dailyValue' = equal to the value that was selected in the 'Registration Successful!' pop-up
        EXPECTED: * 'weeklyValue' = equal to the value that was selected in the 'Registration Successful!' pop-up
        EXPECTED: * 'monthlyValue' = equal to the value that was selected in the 'Registration Successful!' pop-up
        """
        pass

    def test_008_repeat_steps_1_3(self):
        """
        DESCRIPTION: Repeat steps 1-3
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
        EXPECTED: * 'dailyValue' = equal to the value that was entered in the amound field in the 'Registration Successful!' pop-up
        EXPECTED: * 'weeklyValue' =  equal to the value that was entered in the amound field in the 'Registration Successful!' pop-up
        EXPECTED: * 'monthlyValue' =  equal to the value that was entered in the amound field in the 'Registration Successful!' pop-up
        """
        pass
