import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C1500086_Log_In_Panel_Location_for_Desktop(Common):
    """
    TR_ID: C1500086
    NAME: Log In Panel Location for Desktop
    DESCRIPTION: This test case verifies the location of Login Pop-up depending on screen sizes for Desktop.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: 1. Oxygen app is loaded
    PRECONDITIONS: 2. The user is logged out
    """
    keep_browser_open = True

    def test_001_resize_page_from_1600px_to_1280px_width(self):
        """
        DESCRIPTION: Resize page from 1600px to 1280px width
        EXPECTED: Screen size is reduced
        """
        pass

    def test_002_click_log_in_button(self):
        """
        DESCRIPTION: Click 'Log in' button
        EXPECTED: * 'Log in' pop-up is displayed
        EXPECTED: * Login Pop up appears on the right side and fully visible
        """
        pass

    def test_003_resize_page_from_1280px_to_1025px_width__repeat_step_3(self):
        """
        DESCRIPTION: Resize page from 1280px to 1025px width & repeat step 3
        EXPECTED: Screen size is reduced
        EXPECTED: * 'Log in' pop-up is displayed
        EXPECTED: * Login Pop up appears on the right side and fully visible
        """
        pass

    def test_004_reduce_screen_size_to_1024px__repeat_step_3(self):
        """
        DESCRIPTION: Reduce screen size to 1024px & repeat step 3
        EXPECTED: Screen size is reduced
        EXPECTED: * 'Log in' pop-up is displayed
        EXPECTED: * Login Pop up centered and fully visible
        """
        pass

    def test_005_reduce_screen_size_to_970px__repeat_step_3(self):
        """
        DESCRIPTION: Reduce screen size to 970px & repeat step 3
        EXPECTED: Screen size is reduced
        EXPECTED: * 'Log in' pop-up is displayed
        EXPECTED: * Login Pop up centered and fully visible
        """
        pass
