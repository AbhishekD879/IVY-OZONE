import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C60088146_Verify_user_redirection_from_Featured_Highlights_tab_to_the_next_available_tab_in_case_Featured_MS_is_down(Common):
    """
    TR_ID: C60088146
    NAME: Verify user redirection from Featured/Highlights tab to the next available tab in case Featured MS is down.
    DESCRIPTION: This test case verifies the behaviour of user redirection from Featured/Highlights tab to the next available tab on the Homepage in case Featured MS is down.
    PRECONDITIONS: 1. Featured modules data can be found in Dev Console/Network/WS/wss://featured-sports-prd0.ladbrokesoxygen.prod.cloud.ladbrokescoral.com/socket.io/?EIO=3&transport=websocket/'FEATURED_STRUCTURE_CHANGED' message;
    PRECONDITIONS: 2. The behaviour of redirection should be triggered in two cases:
    PRECONDITIONS: - 'invalid namespace' error is received from Featured MS so modules are not shown;
    PRECONDITIONS: - empty data/invalid structure is received in 'FEATURED_STRUCTURE_CHANGED' WS message.
    PRECONDITIONS: 3. The behaviour of redirection should be trigger only one time - when user loads home page for the first time (cache and local storage should be cleared);
    PRECONDITIONS: 4. Homepage/'Featured' (Coral)/'Highlights' (Ladbrokes) tab should be loaded by default after launching the application.
    """
    keep_browser_open = True

    def test_001_simulate_the_featured_ms_errors_described_in_precondition_2_each_case_should_be_checked_separately(self):
        """
        DESCRIPTION: Simulate the Featured MS errors described in Precondition #2 (each case should be checked separately).
        EXPECTED: 
        """
        pass

    def test_002_launch_the_application_for_the_first_time(self):
        """
        DESCRIPTION: Launch the application for the first time.
        EXPECTED: User is automatically redirected to the next available tab (In-Play, Next Races etc).
        """
        pass

    def test_003_switch_back_to_the_featuredhighlights_tab(self):
        """
        DESCRIPTION: Switch back to the 'Featured'/'Highlights' tab.
        EXPECTED: 'Featured'/'Highlights' tab is open and the appropriate error is shown on the page/modules are not shown on the page.
        """
        pass

    def test_004_navigate_to_some_sportrace_page_and_go_back_to_the_homepage(self):
        """
        DESCRIPTION: Navigate to some Sport/Race page and go back to the Homepage.
        EXPECTED: - 'Featured'/'Highlights' tab is open and the appropriate error is shown on the page/modules are not shown on the page.
        EXPECTED: - User is NOT redirected automatically to the next available tab on the Homepage.
        """
        pass
