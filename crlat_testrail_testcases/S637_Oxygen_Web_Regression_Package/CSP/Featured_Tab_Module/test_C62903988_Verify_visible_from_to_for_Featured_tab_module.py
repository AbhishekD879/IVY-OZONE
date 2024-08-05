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
class Test_C62903988_Verify_visible_from_to_for_Featured_tab_module(Common):
    """
    TR_ID: C62903988
    NAME: Verify visible from/to for Featured tab module
    DESCRIPTION: This test case verified date/time settings for showing and hiding Featured tab module
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > Featured tab module
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_go_to_sports_pages___featured_tab_module_section___click_create_featured_tab_module_button(self):
        """
        DESCRIPTION: Go to Sports Pages -> Featured tab module section -> click 'Create Featured tab module' button
        EXPECTED: User should be navigated successfully and New Featured tab module' pop-up is present
        """
        pass

    def test_003_verify_visible_from_date_and_time(self):
        """
        DESCRIPTION: Verify 'Visible from' date and time
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

    def test_008_verify_visible_to_date_and_time(self):
        """
        DESCRIPTION: Verify 'Visible to' date and time
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

    def test_013_enter_valid_visible_from_and_visible_to_and_save_changes(self):
        """
        DESCRIPTION: Enter valid 'Visible from' and 'Visible to' and save changes
        EXPECTED: The changes are saved and the data stored accordingly
        """
        pass

    def test_014_load_oxygen_and_verify_featured_tab_module(self):
        """
        DESCRIPTION: Load Oxygen and verify Featured tab module
        EXPECTED: Featured tab module is displayed in the app as current date and time belong to time box set by Visible from and Visible to date and time fields
        """
        pass

    def test_015_go_to_cms_set_visible_from_and_visible_to_date_and_time_as_time_range_from_the_past_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS, set 'Visible from' and 'Visible to' date and time as time range from the past and save changes
        EXPECTED: The changes are saved and the data stored accordingly
        """
        pass

    def test_016_load_oxygen_and_verify_featured_tab_module(self):
        """
        DESCRIPTION: Load Oxygen and verify Featured tab module
        EXPECTED: Featured tab module is NOT displayed in the app
        """
        pass

    def test_017_go_to_cms_and_set_visible_from_and_visible_to_date_and_time_as_time_range_from_the_future(self):
        """
        DESCRIPTION: Go to CMS and set 'Visible from' and 'Visible to' date and time as time range from the future
        EXPECTED: The changes are saved and the data stored accordingly
        """
        pass

    def test_018_load_oxygen_and_verify_featured_tab_module(self):
        """
        DESCRIPTION: Load Oxygen and verify Featured tab module
        EXPECTED: Featured tab module is NOT displayed in the app
        """
        pass

    def test_019_go_to_cms_set_visible_from_from_the_past_and_visible_to_in_a_few_mins_from_the_current_time_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS, set 'Visible from' from the past and 'Visible to' in a few mins from the current time and save changes
        EXPECTED: The changes are saved and the data stored accordingly
        """
        pass

    def test_020_load_oxygen___wait_till_time_set_in_visible_to_is_passed(self):
        """
        DESCRIPTION: Load Oxygen -> Wait till time set in 'Visible to' is passed
        EXPECTED: After time set in 'Visible to' is passed verified Featured tab module is no more shown within the application
        """
        pass

    def test_021_go_to_cms_set_visible_from_in_a_few_mins_from_current_time_and_visible_to_from_the_future_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS, set 'Visible from' in a few mins from current time and 'Visible to' from the future and save changes
        EXPECTED: The changes are saved and the data stored accordingly
        """
        pass

    def test_022_load_oxygen___wait_till_time_set_in_visible_from_is_passed(self):
        """
        DESCRIPTION: Load Oxygen -> Wait till time set in 'Visible from' is passed
        EXPECTED: After time set in 'Visible from' is passed verified Featured tab module appears to be shown within the application
        """
        pass

    def test_023_go_to_cms_and_try_to_set_visible_from_from_the_future_and_visible_to_from_the_past(self):
        """
        DESCRIPTION: Go to CMS and try to set 'Visible from' from the future and 'Visible to' from the past
        EXPECTED: Its NOT possible to set 'Visible from' from the future and 'Visible to' from the past
        """
        pass
