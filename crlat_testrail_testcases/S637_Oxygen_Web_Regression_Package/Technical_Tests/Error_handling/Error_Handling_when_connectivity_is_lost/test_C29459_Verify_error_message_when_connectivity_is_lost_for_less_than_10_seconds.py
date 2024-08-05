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
class Test_C29459_Verify_error_message_when_connectivity_is_lost_for_less_than_10_seconds(Common):
    """
    TR_ID: C29459
    NAME: Verify error message when connectivity is lost for less than 10 seconds
    DESCRIPTION: This test case verifies error message when connectivity is lost for less than 10 seconds
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

    def test_002_go_to_any_pagetab_within_the_application(self):
        """
        DESCRIPTION: Go to any page/tab within the application
        EXPECTED: User is redirected to the selected area
        """
        pass

    def test_003_turn_off_the_internet_connection__navigate_to_other_pagetab___turn_on_the_internet_connection_in_less_than_10_seconds(self):
        """
        DESCRIPTION: Turn off the Internet connection -> navigate to other page/tab -> turn on the Internet connection **in less than 10 seconds**
        EXPECTED: *   User is navigated to selected page/tab
        EXPECTED: *   Message about lost connection is NOT shown
        EXPECTED: *   Reload of the application is performed when connection is active again (after connection request failed there is 2 seconds delay before **retry **-> if second request is successful - app is reloaded)
        """
        pass

    def test_004_verify_application_after_reload(self):
        """
        DESCRIPTION: Verify application after reload
        EXPECTED: *   Homepage is opened
        EXPECTED: *   User is able to browse the application and see the peges' content
        """
        pass
