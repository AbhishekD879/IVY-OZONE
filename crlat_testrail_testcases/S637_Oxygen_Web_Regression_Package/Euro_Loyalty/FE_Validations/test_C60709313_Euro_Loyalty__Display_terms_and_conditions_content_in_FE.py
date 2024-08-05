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
class Test_C60709313_Euro_Loyalty__Display_terms_and_conditions_content_in_FE(Common):
    """
    TR_ID: C60709313
    NAME: Euro Loyalty - Display terms and conditions content in FE
    DESCRIPTION: This test case is to validate terms and conditions content in FE
    PRECONDITIONS: 1.  User should have oxygen CMS access
    PRECONDITIONS: 2.  Euro Loyalty Page should created,activated and should be in valid date range in CMS special pages - EuroLoyality page
    PRECONDITIONS: 3.  CMS->System Config->Structure->Euro Loyalty (Toggle-ON/OFF)
    PRECONDITIONS: 4.  Terms and conditions text configuration should done in CMS
    """
    keep_browser_open = True

    def test_001_launch_oxygen_application_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch oxygen application and login with valid credentials
        EXPECTED: User is logged into the application
        """
        pass

    def test_002_navigate_to_euro_loyality_page(self):
        """
        DESCRIPTION: Navigate to Euro Loyality page
        EXPECTED: Matchday rewards page should display with all the details
        """
        pass

    def test_003_scroll_down_to_the_page(self):
        """
        DESCRIPTION: Scroll down to the page
        EXPECTED: Label "Terms and conditions should display"
        EXPECTED: terms and conditions content created in CMS should display in Terms and Conditions Text area with the full terms and conditions active URL
        """
        pass

    def test_004_cms_config_has_rich_text_editor_so_manipulate_data_in_cms_with_tables_number_list_bullets_and_font_with_different_colors_background_colors_and_verify_details_in_fe(self):
        """
        DESCRIPTION: CMS config has rich text editor so manipulate data in CMS with tables, number list, bullets and font with different colors, Background colors and verify details in FE
        EXPECTED: Data should display as per CMS configuration
        """
        pass

    def test_005_click_on_full_terms_and_conditions_link(self):
        """
        DESCRIPTION: Click on Full terms and conditions link
        EXPECTED: Full terms and conditions page should open as per CMS config(Full terms and conditions URL)
        EXPECTED: Page should auto navigate and adjust
        """
        pass

    def test_006_repeat_all_the_steps_for_anonymous_user(self):
        """
        DESCRIPTION: Repeat all the steps for anonymous user
        EXPECTED: Should work as expected
        """
        pass

    def test_007_repeat_all_the_steps_for_different_user_tiers(self):
        """
        DESCRIPTION: Repeat all the steps for different user tiers
        EXPECTED: Should work as expected
        """
        pass
