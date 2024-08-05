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
class Test_C1500795_Tracking_of_successful_deposit_limits_submitting_on_registration_form(Common):
    """
    TR_ID: C1500795
    NAME: Tracking of successful deposit limits submitting on registration form
    DESCRIPTION: This test case verifies GA tracking of deposit limits submitted successfully on registration form
    PRECONDITIONS: 1.	Test Case should be executed on  mobile, tablet & desktop platforms
    PRECONDITIONS: 2.	Dev Tools -> Console should be opened
    PRECONDITIONS: 3.	Instruction for real mobile devices/ wrappers debugging: https://confluence.egalacoral.com/display/SPI/How+to+debug+emulator%2C+real+iOS+and+Android+devices
    """
    keep_browser_open = True

    def test_001_tap_join_us_button_and_fill_in_all_info_on_registration_form_untill_last_registration_page_account_details(self):
        """
        DESCRIPTION: Tap 'Join Us' button and fill in all info on registration form untill last registration page (Account Details)
        EXPECTED: Registration form is opened on last registration step
        """
        pass

    def test_002_on_deposit_limit_section_of_last_reg_page_set_all_fields_on_daily_weekly__monthly_tabs_correctlyfill_in_valid_information_for_all_remaining_required_registration_fields(self):
        """
        DESCRIPTION: On deposit limit section of last reg. page, set all fields on 'Daily', 'Weekly' & 'Monthl'y tabs correctly.
        DESCRIPTION: Fill in valid information for all remaining required registration fields.
        EXPECTED: All entered data is displayed correctly
        EXPECTED: No error messages are displayed
        """
        pass

    def test_003_tap_complete_registration_button(self):
        """
        DESCRIPTION: Tap 'Complete Registration' button
        EXPECTED: User is successfully registered
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter"
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'deposit limits',
        EXPECTED: 'eventAction' : 'set',
        EXPECTED: 'eventLabel' : 'success',
        EXPECTED: 'dailyValue' : '<< DAILY VALUE >>',
        EXPECTED: 'weeklyValue' : '<< WEEKLY VALUE >>',
        EXPECTED: 'monthlyValue' : '<< MONTHLY VALUE>>'
        EXPECTED: });
        """
        pass
