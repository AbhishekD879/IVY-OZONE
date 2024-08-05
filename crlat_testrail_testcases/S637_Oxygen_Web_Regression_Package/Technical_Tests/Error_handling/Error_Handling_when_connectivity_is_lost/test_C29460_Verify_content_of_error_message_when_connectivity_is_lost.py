import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C29460_Verify_content_of_error_message_when_connectivity_is_lost(Common):
    """
    TR_ID: C29460
    NAME: Verify content of error message when connectivity is lost
    DESCRIPTION: This test case verifies content of error message when connectivity is lost while user surf the application
    DESCRIPTION: **Jira tickets:**
    DESCRIPTION: *   BMA-7647 Display Message To Users When Connectivity Is Lost
    DESCRIPTION: *   BMA-7698 As a PO I want the app to retry to connect to a failed HTTP or Websocket request once before displaying an information message.
    DESCRIPTION: *   BMA-7891 Connection issue during under maintenance
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_turn_off_the_internet_connection(self):
        """
        DESCRIPTION: Turn off the Internet connection
        EXPECTED: *   Connection to the internet is lost
        EXPECTED: *   Application is opened
        """
        pass

    def test_003_navigate_to_other_pagetab_within_the_application_eg_module_selector_ribbon_tabs_in_play_page_etc(self):
        """
        DESCRIPTION: Navigate to other page/tab within the application (e.g. Module Selector Ribbon tabs, In-Play page etc)
        EXPECTED: *   Selected page/tab is opened
        EXPECTED: *   Error message about lost connection is shown to the user as pop-up window in approx 10 seconds
        """
        pass

    def test_004_verify_pop_up_content(self):
        """
        DESCRIPTION: Verify pop-up content
        EXPECTED: *   Pop-up header is: **'No internet connection'**
        EXPECTED: *   Pop-up content is the following: *'You are currently experiencing issues connecting to the internet. Please check your internet connection and try again'*
        EXPECTED: [FOR CORAL ONLY]:
        EXPECTED: *   It is possible to close pop-up via 'x' button or tap out of pop-up
        EXPECTED: *   **'Retry'** button is shown within pop-up
        EXPECTED: [FOR LADBROKES ONLY]:
        EXPECTED: *   It is possible to close pop-up via 'OK' button or tap out of pop-up
        """
        pass
