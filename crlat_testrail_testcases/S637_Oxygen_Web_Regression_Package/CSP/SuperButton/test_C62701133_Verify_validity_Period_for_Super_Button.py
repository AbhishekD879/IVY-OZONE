import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C62701133_Verify_validity_Period_for_Super_Button(Common):
    """
    TR_ID: C62701133
    NAME: Verify validity Period for Super Button
    DESCRIPTION: This test case verified date/time settings for showing and hiding Super Button
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages > super button.
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_go_to_sports_pages__gt_super_button_section__gt_click_create_super_button_button(self):
        """
        DESCRIPTION: Go to Sports Pages -&gt; Super Button section -&gt; click 'Create Super Button' button
        EXPECTED: User should be navigated successfully and New Super Button' pop-up is present
        """
        pass

    def test_003_verify_validity_period_start_date_and_time(self):
        """
        DESCRIPTION: Verify 'Validity Period Start' date and time
        EXPECTED: Date: MM/DD/YYYY
        EXPECTED: Time: HH:MM:SS
        EXPECTED: 'Today' button sets current date automatically
        EXPECTED: 'Tomorrow' button sets tomorrow's date automatically
        EXPECTED: NOTE: time does not change automatically after tapping 'Today' / 'Tomorrow' button.
        """
        pass

    def test_004_enter_valid_validity_period_start_and_validity_period_end_and_save_changes(self):
        """
        DESCRIPTION: Enter valid 'Validity Period Start' and 'Validity Period End' and save changes
        EXPECTED: The changes are saved and the data stored accordingly
        """
        pass

    def test_005_load_oxygen_and_verify_super_button(self):
        """
        DESCRIPTION: Load Oxygen and verify Super Button
        EXPECTED: Super Button is displayed in the app as current date and time belong to time box set by Validity Period Start and Validity Period End date and time fields
        """
        pass

    def test_006_go_to_cms_set_validity_period_start_and_validity_period_end_date_and_time_as_time_range_from_the_past_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS, set 'Validity Period Start' and 'Validity Period End' date and time as time range from the past and save changes
        EXPECTED: The changes are saved and the data stored accordingly
        """
        pass

    def test_007_load_oxygen_and_verify_super_button(self):
        """
        DESCRIPTION: Load Oxygen and verify Super Button
        EXPECTED: Super Button is NOT displayed in the app
        """
        pass

    def test_008_go_to_cms_and_set_validity_period_start_and_validity_period_end_date_and_time_as_time_range_from_the_future(self):
        """
        DESCRIPTION: Go to CMS and set 'Validity Period Start' and 'Validity Period End' date and time as time range from the future
        EXPECTED: The changes are saved and the data stored accordingly
        """
        pass

    def test_009_load_oxygen_and_verify_super_button(self):
        """
        DESCRIPTION: Load Oxygen and verify Super Button
        EXPECTED: Super Button is NOT displayed in the app
        """
        pass

    def test_010_go_to_cms_set_validity_period_start_from_the_past_and_validity_period_end_in_a_few_mins_from_the_current_time_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS, set 'Validity Period Start' from the past and 'Validity Period End' in a few mins from the current time and save changes
        EXPECTED: The changes are saved and the data stored accordingly
        """
        pass

    def test_011_load_oxygen__gt_wait_till_time_set_in_validity_period_end_is_passed(self):
        """
        DESCRIPTION: Load Oxygen -&gt; Wait till time set in 'Validity Period End' is passed
        EXPECTED: After time set in 'Validity Period End' is passed verified Super Button is no more shown within the application
        """
        pass

    def test_012_go_to_cms_set_validity_period_start_in_a_few_mins_from_current_time_and_validity_period_end_from_the_future_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS, set 'Validity Period Start' in a few mins from current time and 'Validity Period End' from the future and save changes
        EXPECTED: The changes are saved and the data stored accordingly
        """
        pass

    def test_013_load_oxygen__gt_wait_till_time_set_in_validity_period_start_is_passed(self):
        """
        DESCRIPTION: Load Oxygen -&gt; Wait till time set in 'Validity Period Start' is passed
        EXPECTED: After time set in 'Validity Period Start' is passed verified Super Button appears to be shown within the application
        """
        pass

    def test_014_go_to_cms_and_try_to_set_validity_period_start_from_the_future_and_validity_period_end_from_the_past(self):
        """
        DESCRIPTION: Go to CMS and try to set 'Validity Period Start' from the future and 'Validity Period End' from the past
        EXPECTED: Its NOT possible to set 'Validity Period Start' from the future and 'Validity Period End' from the past
        """
        pass
