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
class Test_C60004654_Verify_if_there_is_no_SS_CommentaryForEvent_request_in_case_of_user_navigates_to_the_in_play_event_without_Fallback_Scoreboard_available(Common):
    """
    TR_ID: C60004654
    NAME: Verify if there is  no SS /CommentaryForEvent request in case of user navigates to the in-play event without Fallback Scoreboard available
    DESCRIPTION: This test case verifies if there is  no SS /CommentaryForEvent request in case of user navigates to the in-play event without Fallback Scoreboard available
    PRECONDITIONS: There is a pre-match Football/Badminton event available with Fallback Scoreboard (to check which scoreboard is currently displayed use https://confluence.egalacoral.com/pages/viewpage.action?pageId=145626444)
    """
    keep_browser_open = True

    def test_001_go_to_footballbadminton_landing_page(self):
        """
        DESCRIPTION: Go to Football/Badminton landing page
        EXPECTED: Events are loaded
        """
        pass

    def test_002_open_event_from_preconditions(self):
        """
        DESCRIPTION: Open event from preconditions
        EXPECTED: EDP is loaded
        EXPECTED: SS /CommentaryForEvent request is NOT loaded
        """
        pass
