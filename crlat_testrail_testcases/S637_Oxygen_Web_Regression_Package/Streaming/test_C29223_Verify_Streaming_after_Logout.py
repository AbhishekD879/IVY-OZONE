import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.streaming
@vtest
class Test_C29223_Verify_Streaming_after_Logout(Common):
    """
    TR_ID: C29223
    NAME: Verify Streaming after Logout
    DESCRIPTION: This test scenario verifies that user is logged out by server automatically when his/her session is over on the server.
    DESCRIPTION: **Jira tickets:** BMA-5678 (Handle HTTP Error 401)
    PRECONDITIONS: User should be logged in, but session should be OVER on the server
    PRECONDITIONS: To trigger event when session is over on the server please perform the following steps:
    PRECONDITIONS: *   Login to Oxygen in one browser tab and open 'Bet History' page
    PRECONDITIONS: *   Login to Oxygen in second browser tab, logout -> session is over on the server
    PRECONDITIONS: *   Navigate back to the first browser tab where user is still logged in, however there is no active session already
    """
    keep_browser_open = True

    def test_001_open_event_details_page_of_any_sport_for_the_event_which_has_stream_available_and_tap_stream_icon(self):
        """
        DESCRIPTION: Open Event Details page of any <Sport> for the event which has stream available and tap 'Stream' icon
        EXPECTED: Popup message about logging out appears.
        EXPECTED: User is logged out from the application
        EXPECTED: User is not able to watch the stream
        EXPECTED: He/she is redirected to the Homepage
        """
        pass
