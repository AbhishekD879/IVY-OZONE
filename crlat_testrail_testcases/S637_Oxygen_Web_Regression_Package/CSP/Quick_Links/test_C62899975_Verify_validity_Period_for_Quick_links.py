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
class Test_C62899975_Verify_validity_Period_for_Quick_links(Common):
    """
    TR_ID: C62899975
    NAME: Verify validity Period for Quick links
    DESCRIPTION: This test case verified date/time settings for showing and hiding Quick links
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages >Home page > Quick links
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_go_to_sports_pages___quick_links_section___click_create_quick_links_button(self):
        """
        DESCRIPTION: Go to Sports Pages -> Quick links section -> click 'Create Quick links' button
        EXPECTED: User should be navigated successfully and New Quick links' pop-up is present
        """
        pass

    def test_003_verify_validity_period_start_date_and_time(self):
        """
        DESCRIPTION: Verify 'Validity Period Start' date and time
        EXPECTED: Date: MM/DD/YYYY
        """
        pass

    def test_004_(self):
        """
        DESCRIPTION: 
        EXPECTED: Time: HH:MM:SS
        """
        pass

    def test_005_(self):
        """
        DESCRIPTION: 
        EXPECTED: 'Today' button sets current date automatically
        """
        pass

    def test_006_(self):
        """
        DESCRIPTION: 
        EXPECTED: 'Tomorrow' button sets tomorrow's date automatically
        """
        pass

    def test_007_(self):
        """
        DESCRIPTION: 
        EXPECTED: NOTE time does not change automatically after tapping 'Today' / 'Tomorrow' button.
        """
        pass

    def test_008_verify_validity_period_end_date_and_time(self):
        """
        DESCRIPTION: Verify 'Validity Period End' date and time
        EXPECTED: Date: MM/DD/YYYY
        """
        pass

    def test_009_(self):
        """
        DESCRIPTION: 
        EXPECTED: Time: HH:MM:SS
        """
        pass

    def test_010_(self):
        """
        DESCRIPTION: 
        EXPECTED: 'Today' button sets current date automatically
        """
        pass

    def test_011_(self):
        """
        DESCRIPTION: 
        EXPECTED: 'Tomorrow' button sets tomorrow's date automatically
        """
        pass

    def test_012_(self):
        """
        DESCRIPTION: 
        EXPECTED: NOTE time does not change automatically after tapping 'Today' / 'Tomorrow' button
        """
        pass

    def test_013_enter_valid_validity_period_start_and_validity_period_end_and_save_changes(self):
        """
        DESCRIPTION: Enter valid 'Validity Period Start' and 'Validity Period End' and save changes
        EXPECTED: The changes are saved and the data stored accordingly
        """
        pass

    def test_014_load_oxygen_and_verify_quick_links(self):
        """
        DESCRIPTION: Load Oxygen and verify Quick links
        EXPECTED: Quick links is displayed in the app as current date and time belong to time box set by Validity Period Start and Validity Period End date and time fields
        """
        pass

    def test_015_go_to_cms_set_validity_period_start_and_validity_period_end_date_and_time_as_time_range_from_the_past_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS, set 'Validity Period Start' and 'Validity Period End' date and time as time range from the past and save changes
        EXPECTED: The changes are saved and the data stored accordingly
        """
        pass

    def test_016_load_oxygen_and_verify_quick_links(self):
        """
        DESCRIPTION: Load Oxygen and verify Quick links
        EXPECTED: Quick links is NOT displayed in the app
        """
        pass

    def test_017_go_to_cms_and_set_validity_period_start_and_validity_period_end_date_and_time_as_time_range_from_the_future(self):
        """
        DESCRIPTION: Go to CMS and set 'Validity Period Start' and 'Validity Period End' date and time as time range from the future
        EXPECTED: The changes are saved and the data stored accordingly
        """
        pass

    def test_018_load_oxygen_and_verify_quick_links(self):
        """
        DESCRIPTION: Load Oxygen and verify Quick links
        EXPECTED: Quick links is NOT displayed in the app
        """
        pass

    def test_019_go_to_cms_set_validity_period_start_from_the_past_and_validity_period_end_in_a_few_mins_from_the_current_time_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS, set 'Validity Period Start' from the past and 'Validity Period End' in a few mins from the current time and save changes
        EXPECTED: The changes are saved and the data stored accordingly
        """
        pass

    def test_020_load_oxygen___wait_till_time_set_in_validity_period_end_is_passed(self):
        """
        DESCRIPTION: Load Oxygen -> Wait till time set in 'Validity Period End' is passed
        EXPECTED: After time set in 'Validity Period End' is passed verified Quick links is no more shown within the application
        """
        pass

    def test_021_go_to_cms_set_validity_period_start_in_a_few_mins_from_current_time_and_validity_period_end_from_the_future_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS, set 'Validity Period Start' in a few mins from current time and 'Validity Period End' from the future and save changes
        EXPECTED: The changes are saved and the data stored accordingly
        """
        pass

    def test_022_load_oxygen___wait_till_time_set_in_validity_period_start_is_passed(self):
        """
        DESCRIPTION: Load Oxygen -> Wait till time set in 'Validity Period Start' is passed
        EXPECTED: After time set in 'Validity Period Start' is passed verified Quick links appears to be shown within the application
        """
        pass

    def test_023_go_to_cms_and_try_to_set_validity_period_start_from_the_future_and_validity_period_end_from_the_past(self):
        """
        DESCRIPTION: Go to CMS and try to set 'Validity Period Start' from the future and 'Validity Period End' from the past
        EXPECTED: Its NOT possible to set 'Validity Period Start' from the future and 'Validity Period End' from the past
        """
        pass
