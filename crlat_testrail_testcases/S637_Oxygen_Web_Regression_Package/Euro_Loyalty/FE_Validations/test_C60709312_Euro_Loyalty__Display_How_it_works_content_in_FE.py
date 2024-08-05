import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C60709312_Euro_Loyalty__Display_How_it_works_content_in_FE(Common):
    """
    TR_ID: C60709312
    NAME: Euro Loyalty - Display How it works content in FE
    DESCRIPTION: This test case is to validate how it works content in FE
    PRECONDITIONS: 1.  User should have oxygen CMS access
    PRECONDITIONS: 2.  Euro Loyalty Page should created,activated and should be in valid date range in CMS special pages - EuroLoyality page
    PRECONDITIONS: 3.  CMS->System Config->Structure->Euro Loyalty (Toggle-ON/OFF)
    PRECONDITIONS: 4.  How it works text configuration should done in CMS
    """
    keep_browser_open = True

    def test_001_launch_oxygen_application_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch oxygen application and login with valid credentials
        EXPECTED: User is logged into the application
        """
        pass

    def test_002_navigate_to_euro_loyality_page_from_sports_ribbon_or_from_a_z_menuin_mobilein_desktop_left_pane(self):
        """
        DESCRIPTION: Navigate to Euro Loyality page from sports ribbon or from A-Z menuin mobile
        DESCRIPTION: in Desktop left pane
        EXPECTED: Matchday rewards page should display with all the details
        EXPECTED: How it works label should should display with > icon
        """
        pass

    def test_003_click_on__icon_and_veirfy(self):
        """
        DESCRIPTION: Click on > icon and veirfy
        EXPECTED: How it works text should display as per CMS configuration
        EXPECTED: More and ok buttons should display
        """
        pass

    def test_004_cms_config_has_rich_text_editor_so_manipulate_data_in_cms_with_tables_number_list_bullets_and_font_with_different_colors_background_colors_and_verify_details_in_fe(self):
        """
        DESCRIPTION: CMS config has rich text editor so manipulate data in CMS with tables, number list, bullets and font with different colors, Background colors and verify details in FE
        EXPECTED: Data should display as per CMS configuration
        """
        pass

    def test_005_click_on_ok_button(self):
        """
        DESCRIPTION: Click on OK button
        EXPECTED: How it works popup should close and user should remain in euro loyality page
        """
        pass

    def test_006_click_on__icon_and_veirfy(self):
        """
        DESCRIPTION: Click on > icon and veirfy
        EXPECTED: How it works text should display as per CMS configuration
        EXPECTED: More and ok buttons should display
        """
        pass

    def test_007_click_on_more_button(self):
        """
        DESCRIPTION: Click on more button
        EXPECTED: Euro Loyality promotion page should display
        EXPECTED: TBD which promotion Page
        """
        pass

    def test_008_click_on_on_browser_back_button(self):
        """
        DESCRIPTION: Click on on browser back button
        EXPECTED: User should navigate back to euro loyality page
        """
        pass

    def test_009_repeat_all_the_steps_for_anonymous_user(self):
        """
        DESCRIPTION: Repeat all the steps for anonymous user
        EXPECTED: Should work as expected
        """
        pass

    def test_010_repeat_all_the_steps_for_different_user_tiers(self):
        """
        DESCRIPTION: Repeat all the steps for different user tiers
        EXPECTED: Should work as expected
        """
        pass
