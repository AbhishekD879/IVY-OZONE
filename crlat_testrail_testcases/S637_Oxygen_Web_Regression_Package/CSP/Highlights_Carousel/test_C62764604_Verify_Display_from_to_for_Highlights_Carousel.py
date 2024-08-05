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
class Test_C62764604_Verify_Display_from_to_for_Highlights_Carousel(Common):
    """
    TR_ID: C62764604
    NAME: Verify Display from/to for Highlights Carousel
    DESCRIPTION: This test case verified date/time settings for showing and hiding Highlights Carousel
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages >home page> Highlights Carousel
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_go_to_sports_pages__gt_highlights_carousel_section__gt_click_create_highlights_carousel_button(self):
        """
        DESCRIPTION: Go to Sports Pages -&gt; Highlights Carousel section -&gt; click 'Create Highlights Carousel' button
        EXPECTED: User should be navigated successfully and New Highlights Carousel' pop-up is present
        """
        pass

    def test_003_verify_display_from_date_and_time(self):
        """
        DESCRIPTION: Verify 'Display from' date and time
        EXPECTED: Date: MM/DD/YYYY
        EXPECTED: Time: HH:MM:SS
        EXPECTED: 'Today' button sets current date automatically
        EXPECTED: 'Tomorrow' button sets tomorrow's date automatically
        EXPECTED: NOTE time does not change automatically after tapping 'Today' / 'Tomorrow' button.
        """
        pass

    def test_004_verify_display_to_date_and_time(self):
        """
        DESCRIPTION: Verify 'Display to' date and time
        EXPECTED: Date: MM/DD/YYYY
        EXPECTED: Time: HH:MM:SS
        EXPECTED: 'Today' button sets current date automatically
        EXPECTED: 'Tomorrow' button sets tomorrow's date automatically
        EXPECTED: NOTE time does not change automatically after tapping 'Today' / 'Tomorrow' button
        """
        pass

    def test_005_enter_valid_display_from_and_display_to_and_save_changes(self):
        """
        DESCRIPTION: Enter valid 'Display from' and 'Display to' and save changes
        EXPECTED: The changes are saved and the data stored accordingly
        """
        pass

    def test_006_load_oxygen_and_verify_highlights_carousel(self):
        """
        DESCRIPTION: Load Oxygen and verify Highlights Carousel
        EXPECTED: Highlights Carousel is displayed in the app as current date and time belong to time box set by Display from and Display to date and time fields
        """
        pass

    def test_007_go_to_cms_set_display_from_and_display_to_date_and_time_as_time_range_from_the_past_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS, set 'Display from' and 'Display to' date and time as time range from the past and save changes
        EXPECTED: The changes are saved and the data stored accordingly
        """
        pass

    def test_008_load_oxygen_and_verify_highlights_carousel(self):
        """
        DESCRIPTION: Load Oxygen and verify Highlights Carousel
        EXPECTED: Highlights Carousel is NOT displayed in the app
        """
        pass

    def test_009_go_to_cms_and_set_display_from_and_display_to_date_and_time_as_time_range_from_the_future(self):
        """
        DESCRIPTION: Go to CMS and set 'Display from' and 'Display to' date and time as time range from the future
        EXPECTED: The changes are saved and the data stored accordingly
        """
        pass

    def test_010_load_oxygen_and_verify_highlights_carousel(self):
        """
        DESCRIPTION: Load Oxygen and verify Highlights Carousel
        EXPECTED: Highlights Carousel is NOT displayed in the app
        """
        pass

    def test_011_go_to_cms_set_display_from_from_the_past_and_display_to_in_a_few_mins_from_the_current_time_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS, set 'Display from' from the past and 'Display to' in a few mins from the current time and save changes
        EXPECTED: The changes are saved and the data stored accordingly
        """
        pass

    def test_012_load_oxygen__gt_wait_till_time_set_in_display_to_is_passed(self):
        """
        DESCRIPTION: Load Oxygen -&gt; Wait till time set in 'Display to' is passed
        EXPECTED: After time set in 'Display to' is passed verified Highlights Carousel is no more shown within the application
        """
        pass

    def test_013_go_to_cms_set_display_from_in_a_few_mins_from_current_time_and_display_to_from_the_future_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS, set 'Display from' in a few mins from current time and 'Display to' from the future and save changes
        EXPECTED: The changes are saved and the data stored accordingly
        """
        pass

    def test_014_load_oxygen__gt_wait_till_time_set_in_display_from_is_passed(self):
        """
        DESCRIPTION: Load Oxygen -&gt; Wait till time set in 'Display from' is passed
        EXPECTED: After time set in 'Display from' is passed verified Highlights Carousel appears to be shown within the application
        """
        pass

    def test_015_go_to_cms_and_try_to_set_display_from_from_the_future_and_display_to_from_the_past(self):
        """
        DESCRIPTION: Go to CMS and try to set 'Display from' from the future and 'Display to' from the past
        EXPECTED: Its NOT possible to set 'Display from' from the future and 'Display to' from the past
        """
        pass
