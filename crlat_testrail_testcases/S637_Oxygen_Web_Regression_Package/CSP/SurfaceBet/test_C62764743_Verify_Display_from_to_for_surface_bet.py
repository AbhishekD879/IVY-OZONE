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
class Test_C62764743_Verify_Display_from_to_for_surface_bet(Common):
    """
    TR_ID: C62764743
    NAME: Verify Display from/to for surface bet
    DESCRIPTION: This test case verified date/time settings for showing and hiding surface bet
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages >home page> surface bet
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_go_to_sports_pages___surface_bet_section___click_create_surface_bet_button(self):
        """
        DESCRIPTION: Go to Sports Pages -> surface bet section -> click 'Create surface bet' button
        EXPECTED: User should be navigated successfully and New surface bet' pop-up is present
        """
        pass

    def test_003_verify_display_from_date_and_time(self):
        """
        DESCRIPTION: Verify 'Display from' date and time
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

    def test_008_verify_display_to_date_and_time(self):
        """
        DESCRIPTION: Verify 'Display to' date and time
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

    def test_013_enter_valid_display_from_and_display_to_and_save_changes(self):
        """
        DESCRIPTION: Enter valid 'Display from' and 'Display to' and save changes
        EXPECTED: The changes are saved and the data stored accordingly
        """
        pass

    def test_014_load_oxygen_and_verify_surface_bet(self):
        """
        DESCRIPTION: Load Oxygen and verify surface bet
        EXPECTED: surface bet is displayed in the app as current date and time belong to time box set by Display from and Display to date and time fields
        """
        pass

    def test_015_go_to_cms_set_display_from_and_display_to_date_and_time_as_time_range_from_the_past_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS, set 'Display from' and 'Display to' date and time as time range from the past and save changes
        EXPECTED: The changes are saved and the data stored accordingly
        """
        pass

    def test_016_load_oxygen_and_verify_surface_bet(self):
        """
        DESCRIPTION: Load Oxygen and verify surface bet
        EXPECTED: surface bet is NOT displayed in the app
        """
        pass

    def test_017_go_to_cms_and_set_display_from_and_display_to_date_and_time_as_time_range_from_the_future(self):
        """
        DESCRIPTION: Go to CMS and set 'Display from' and 'Display to' date and time as time range from the future
        EXPECTED: The changes are saved and the data stored accordingly
        """
        pass

    def test_018_load_oxygen_and_verify_surface_bet(self):
        """
        DESCRIPTION: Load Oxygen and verify surface bet
        EXPECTED: surface bet is NOT displayed in the app
        """
        pass

    def test_019_go_to_cms_set_display_from_from_the_past_and_display_to_in_a_few_mins_from_the_current_time_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS, set 'Display from' from the past and 'Display to' in a few mins from the current time and save changes
        EXPECTED: The changes are saved and the data stored accordingly
        """
        pass

    def test_020_load_oxygen___wait_till_time_set_in_display_to_is_passed(self):
        """
        DESCRIPTION: Load Oxygen -> Wait till time set in 'Display to' is passed
        EXPECTED: After time set in 'Display to' is passed verified surface bet is no more shown within the application
        """
        pass

    def test_021_go_to_cms_set_display_from_in_a_few_mins_from_current_time_and_display_to_from_the_future_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS, set 'Display from' in a few mins from current time and 'Display to' from the future and save changes
        EXPECTED: The changes are saved and the data stored accordingly
        """
        pass

    def test_022_load_oxygen___wait_till_time_set_in_display_from_is_passed(self):
        """
        DESCRIPTION: Load Oxygen -> Wait till time set in 'Display from' is passed
        EXPECTED: After time set in 'Display from' is passed verified surface bet appears to be shown within the application
        """
        pass

    def test_023_go_to_cms_and_try_to_set_display_from_from_the_future_and_display_to_from_the_past(self):
        """
        DESCRIPTION: Go to CMS and try to set 'Display from' from the future and 'Display to' from the past
        EXPECTED: Its NOT possible to set 'Display from' from the future and 'Display to' from the past
        """
        pass
