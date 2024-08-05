import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C59997792_Verify_there_is_SS_CommentaryForEvent_request_on_EDP_in_case_of_pre_match_event_with_Fallback_Scoreboard_available(Common):
    """
    TR_ID: C59997792
    NAME: Verify there is SS /CommentaryForEvent request on EDP in case of pre match event with Fallback Scoreboard available
    DESCRIPTION: This test case verifies there is SS /CommentaryForEvent request in case of pre match event with Fallback Scoreboard available
    PRECONDITIONS: 1. There is a pre-match Football/Badminton event available with Fallback Scoreboard (to check which scoreboard is currently displayed use Inspect Element)
    PRECONDITIONS: 2. User is on corresponding landing page
    """
    keep_browser_open = True

    def test_001_navigate_to_edp_of_event_from_preconditions(self):
        """
        DESCRIPTION: Navigate to EDP of event from preconditions
        EXPECTED: * EDP is loaded
        EXPECTED: * /CommentaryForEvent is sent and response received
        EXPECTED: * event is subscribed to "sSCBRD" push live serve updates
        """
        pass

    def test_002_make_event_live_and_trigger_some_score_update(self):
        """
        DESCRIPTION: Make event Live and trigger some score update
        EXPECTED: * push score update received
        EXPECTED: * new score is displayed on UI
        """
        pass
