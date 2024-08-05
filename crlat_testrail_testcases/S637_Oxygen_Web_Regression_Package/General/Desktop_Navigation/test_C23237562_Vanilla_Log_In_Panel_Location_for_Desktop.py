import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.navigation
@vtest
class Test_C23237562_Vanilla_Log_In_Panel_Location_for_Desktop(Common):
    """
    TR_ID: C23237562
    NAME: [Vanilla] Log In Panel Location for Desktop
    DESCRIPTION: This test case verifies the location of Login Pop-up depending on screen sizes for Desktop.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: 1. Oxygen app is loaded
    PRECONDITIONS: 2. The user is logged out
    """
    keep_browser_open = True

    def test_001_for_vanilla_log_in_panel_is_always_displayed_in_the_middle_of_the_screen(self):
        """
        DESCRIPTION: For Vanilla Log in panel is always displayed in the middle of the screen.
        EXPECTED: 
        """
        pass
