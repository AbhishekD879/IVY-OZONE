import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.retail
@vtest
class Test_C2461983_Verify_the_work_of_Dont_show_me_this_again_link(Common):
    """
    TR_ID: C2461983
    NAME: Verify the work of 'Don’t show me this again' link
    DESCRIPTION: This test case verifies the work of 'Don’t show me this again' link
    DESCRIPTION: To update: Need to login? Where does the overlay supposed to appear?
    PRECONDITIONS: Make sure Connect Overlay tutorial feature is turned on in CMS: System configuration -> Connect -> overlay
    PRECONDITIONS: * If no overlay appears, ensure that in dev tool -> Application tab -> cookies: field Name 'CONNECT_TRACKER' = 'false' and in Locale storage: OX.retailOverlayRemain = 4.
    PRECONDITIONS: * Reload the SB app
    """
    keep_browser_open = True

    def test_001_tap_dont_show_me_this_again_link(self):
        """
        DESCRIPTION: Tap 'Don’t show me this again' link
        EXPECTED: * The Connect overlay is closed
        EXPECTED: * dev tool -> Application tab ->Locale storage: OX.connectOverlayRemain is 0
        """
        pass

    def test_002_reload_the_page(self):
        """
        DESCRIPTION: Reload the page
        EXPECTED: * A user is on the same page
        EXPECTED: * Connect overlay is not displayed
        """
        pass
