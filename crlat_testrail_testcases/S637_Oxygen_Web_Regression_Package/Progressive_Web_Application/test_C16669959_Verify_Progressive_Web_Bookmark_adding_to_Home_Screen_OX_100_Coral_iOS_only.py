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
class Test_C16669959_Verify_Progressive_Web_Bookmark_adding_to_Home_Screen_OX_100_Coral_iOS_only(Common):
    """
    TR_ID: C16669959
    NAME: Verify Progressive Web Bookmark adding to Home Screen [OX 100: Coral iOS only]
    DESCRIPTION: This test case verifies the possibility to add Coral website as Web Progressive App to Home Screen.
    DESCRIPTION: NOTE:
    DESCRIPTION: Currently, functionality is applicable only for Coral brand, iOS devices and Safari browser.
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_open_coral_website(self):
        """
        DESCRIPTION: Open Coral website
        EXPECTED: 
        """
        pass

    def test_002_press_share_button_on_footer_browser_menu_and_select_add_to_home_screen_option(self):
        """
        DESCRIPTION: Press Share button on Footer browser Menu and select "Add to Home Screen" option
        EXPECTED: Add to Home Screen page/popup is open
        """
        pass

    def test_003_verify_data_correctness_icon_bookmark_name_and_link(self):
        """
        DESCRIPTION: Verify data correctness: icon, Bookmark name and link
        EXPECTED: All data are correct
        """
        pass

    def test_004_press_add(self):
        """
        DESCRIPTION: Press Add
        EXPECTED: Bookmark is added on Home Screen
        """
        pass

    def test_005_verify_pwa_icon_on_homescreen(self):
        """
        DESCRIPTION: Verify PWA icon on Homescreen
        EXPECTED: Icon format is correct
        EXPECTED: Link to Zeplin: https://app.zeplin.io/project/5d15f6536a586eafd5eae119/dashboard
        """
        pass

    def test_006_open_bookmark_from_home_screen(self):
        """
        DESCRIPTION: Open Bookmark from Home Screen
        EXPECTED: Coral website is open in the format of Progressive Web App
        """
        pass
