import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C2555607_Verify_that_CMS_configuration_for_Odds_Boost_is_shown_in_application(Common):
    """
    TR_ID: C2555607
    NAME: Verify that CMS configuration for Odds Boost is shown in application
    DESCRIPTION: This test case verifies that configurations for "Odds boost" in CMS are shown on application
    DESCRIPTION: AUTOTEST C10581662
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office for User1
    PRECONDITIONS: Token is NOT expired
    PRECONDITIONS: CMS configuration for Odds Boost are added:
    PRECONDITIONS: Odds Boost is Active
    PRECONDITIONS: *Image1* is added in Custom field for Image (svg)
    PRECONDITIONS: *'Header_Text_1'* text is added in Custom rich text field for Logged Out Header Text
    PRECONDITIONS: *'Header_Text_2' text is added in Custom rich text field for Logged In Header Text
    PRECONDITIONS: *'T&C_Text_1'* text is added in Custom Field for Terms&Conditions text
    """
    keep_browser_open = True

    def test_001_load_applicationdo_not_loginnavigate_to_odds_boost_page_httpsbeta_sportscoralcoukoddsboostverify_that_appropriate_odds_boost_elements_are_shown_on_odds_boost_header(self):
        """
        DESCRIPTION: Load application
        DESCRIPTION: Do NOT login
        DESCRIPTION: Navigate to Odds Boost page (https://beta-sports.coral.co.uk/oddsboost)
        DESCRIPTION: Verify that appropriate odds boost elements are shown on Odds Boost Header
        EXPECTED: The following elements are shown on Odds Boost page:
        EXPECTED: - Image_1
        EXPECTED: - 'Header_Text_1'
        EXPECTED: - 'T&C_Text_1'
        """
        pass

    def test_002_tap_log_in_button_login_with_user1_from_preconditionverify_that__appropriate_odds_boost_elements_are_shown_on_odds_boost_header_after_login(self):
        """
        DESCRIPTION: Tap Log In button (login with User1 from precondition)
        DESCRIPTION: Verify that  appropriate odds boost elements are shown on Odds Boost Header after login
        EXPECTED: The following elements are shown on Odds Boost page:
        EXPECTED: - Image_1
        EXPECTED: - 'Header_Text_2'
        EXPECTED: - 'T&C_Text_1'
        """
        pass

    def test_003_load_cmsnavigate_to_odds_boost_menu_item_in_the_navigation_menuremove_image_1change_logged_out_header_text_to_header_text_3change_logged_in_header_text_to_header_text_4change_termsconditions_text_to_tc_text_2save_changes(self):
        """
        DESCRIPTION: Load CMS
        DESCRIPTION: Navigate to "Odds Boost" Menu item in the navigation menu
        DESCRIPTION: Remove Image_1
        DESCRIPTION: Change Logged Out Header Text to 'Header_Text_3'
        DESCRIPTION: Change Logged In Header Text to 'Header_Text_4'
        DESCRIPTION: Change Terms&Conditions Text to 'T&C_Text_2'
        DESCRIPTION: Save changes
        EXPECTED: Changes are saved in CMS
        """
        pass

    def test_004_navigate_back_to_the_applicationrefresh_odds_boost_pageverify_that_appropriate_updated_on_odds_boost_header_according_to_cms_changes(self):
        """
        DESCRIPTION: Navigate back to the application
        DESCRIPTION: Refresh Odds Boost page
        DESCRIPTION: Verify that appropriate updated on Odds Boost Header according to CMS changes
        EXPECTED: The following elements are shown on Odds Boost page:
        EXPECTED: - Default odds boost image
        EXPECTED: - 'Header_Text_4'
        EXPECTED: - 'T&C_Text_1'
        """
        pass

    def test_005_log_out_from_applicationnavigate_to_odds_boost_pageverify_that_appropriate_updated_on_odds_boost_header_according_to_cms_changes(self):
        """
        DESCRIPTION: Log out from application
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that appropriate updated on Odds Boost Header according to CMS changes
        EXPECTED: The following elements are shown on Odds Boost page:
        EXPECTED: - Default odds boost image
        EXPECTED: - 'Header_Text_3'
        EXPECTED: - 'T&C_Text_1'
        """
        pass

    def test_006_load_cmsnavigate_to_odds_boost_menu_item_in_the_navigation_menuturn_off_odds_boost_toggle___save_changes(self):
        """
        DESCRIPTION: Load CMS
        DESCRIPTION: Navigate to "Odds Boost" Menu item in the navigation menu
        DESCRIPTION: Turn OFF "Odds Boost" Toggle -> Save changes
        EXPECTED: Changes are saved in CMS
        """
        pass

    def test_007_reload_application_and_login_with_user1verify_that_odds_boost_functionality_is_not_shown_in_the_application(self):
        """
        DESCRIPTION: Reload application and Login with User1
        DESCRIPTION: Verify that Odds Boost functionality is not shown in the application
        EXPECTED: - Odds Boost token summary popup is not shown
        EXPECTED: - Odds Boost is not shown in (Menu)?
        EXPECTED: - Odds boost page is anavailable
        EXPECTED: - Odds Boost button is not shown in Betslip
        EXPECTED: - Odds Boost button is not shown in Quick Bet
        """
        pass
