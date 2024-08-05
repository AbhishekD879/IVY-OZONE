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
class Test_C808186_Verify_Featured_In_Play_error_handling(Common):
    """
    TR_ID: C808186
    NAME: Verify Featured/In-Play error handling
    DESCRIPTION: This test case verifies error handling for Featured and In-Play pages when connection to  Featured/In-Play MS Middleware is lost
    PRECONDITIONS: Load Oxygen application
    """
    keep_browser_open = True

    def test_001_turn_network_connection_off_to_lose_connection_to_featured_middleware(self):
        """
        DESCRIPTION: Turn Network connection off to lose connection to Featured middleware
        EXPECTED: 
        """
        pass

    def test_002_go__to_featured_tab(self):
        """
        DESCRIPTION: Go  to Featured tab
        EXPECTED: - Loading cursor is displayed till 5 requests to connect to middleware with no response are done
        EXPECTED: - Error message 'Server is unavailable at the moment, please try again later. If this problem persists, contact our Customer Service Department'  with 'Reload' button
        EXPECTED: **From OX98.2.9**:
        EXPECTED: Loading cursor is displayed till **15 requests** to connect to middleware with no response are done
        EXPECTED: **From OX100.3 Ladbrokes (Coral from OX 101.1):**
        EXPECTED: Error message 'Oops! We are having trouble loading this page. Please check your connection' with 'Try Again' button
        """
        pass

    def test_003_restore_the_connection_to_featured_middleware_and_tap_try_again_button(self):
        """
        DESCRIPTION: Restore the connection to Featured middleware and tap 'Try Again' button
        EXPECTED: Featured tab content is displayed
        """
        pass

    def test_004_turn_network_connection_off_to_lose_connection_to_in_play_middleware(self):
        """
        DESCRIPTION: Turn Network connection off to lose connection to In-Play middleware
        EXPECTED: 
        """
        pass

    def test_005_go__to_in_play_tab(self):
        """
        DESCRIPTION: Go  to In-Play tab
        EXPECTED: - Loading cursor is displayed till 15 requests to connect to middleware with no response are done
        EXPECTED: - Error message 'Server is unavailable at the moment, please try again later. If this problem persists, contact our Customer Service Department' with 'Reload' button
        EXPECTED: **From OX100.3 Ladbrokes (Coral from OX 101.1):**
        EXPECTED: Error message 'Oops! We are having trouble loading this page. Please check your connection' with 'Try Again' button
        """
        pass

    def test_006_restore_the_connection_to_in_play_middleware_and_tap_try_again_button(self):
        """
        DESCRIPTION: Restore the connection to In-Play middleware and tap 'Try Again' button
        EXPECTED: In-Play tab content is displayed
        """
        pass
