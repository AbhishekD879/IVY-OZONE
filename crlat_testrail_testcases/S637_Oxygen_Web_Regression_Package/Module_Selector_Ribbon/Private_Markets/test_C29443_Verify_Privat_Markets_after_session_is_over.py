import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.promotions_banners_offers
@vtest
class Test_C29443_Verify_Privat_Markets_after_session_is_over(Common):
    """
    TR_ID: C29443
    NAME: Verify Privat Markets after session is over
    DESCRIPTION: This test scenario verifies that user is logged out by the server automatically when his/her session is over on the server.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: 1. User should have account with Private Markets available
    PRECONDITIONS: 2. **accountFreebets?freebetTokenType=ACCESS** request is used in order to get a private market for particular user after a page refresh or navigating to Homepage from any other page and **user** request is used to get private market after login(open Dev tools -> Network ->XHR tab)
    PRECONDITIONS: 3. User should be logged in, but session should be OVER on the server
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: To trigger event when session is over on the server please perform the following steps:
    PRECONDITIONS: *   Login to Oxygen in one browser tab
    PRECONDITIONS: *   Login to Oxygen in second browser tab, logout -> session is over on the server
    PRECONDITIONS: *   Navigate back to the first browser tab where user is still logged in, however, there is no active session already
    """
    keep_browser_open = True

    def test_001_load_oxygen_app_and_log_in_using_an_account_with_private_markets_available(self):
        """
        DESCRIPTION: Load Oxygen app and log in using an account with Private Markets available
        EXPECTED: *   Homepage is opened
        EXPECTED: *   'Your Enhanced Markets' tab is present and selected by default **for mobile/tablet**
        EXPECTED: *   'Your Enhanced Markets' section is present at the top of the page (below Hero Header) **for mobile/tablet**
        """
        pass

    def test_002_make_steps_from_preconditions_regarding_session_over_on_the_server(self):
        """
        DESCRIPTION: Make steps from Preconditions regarding session OVER on the server
        EXPECTED: 
        """
        pass

    def test_003_navigation_back_to_the_first_browser_tab_when_no_active_session_already(self):
        """
        DESCRIPTION: Navigation back to the first browser tab when no active session already
        EXPECTED: * Popup message about logging out appears
        EXPECTED: * User is logged out from the application
        """
        pass

    def test_004_verify_your_enhancedmarkets_tabsection(self):
        """
        DESCRIPTION: Verify 'Your Enhanced Markets' tab/section
        EXPECTED: * User is not able to see the content of 'Your Enhanced Markets' tab/section
        EXPECTED: * 'Your Enhanced Markets' tab/section is no more shown on the Homepage
        """
        pass
