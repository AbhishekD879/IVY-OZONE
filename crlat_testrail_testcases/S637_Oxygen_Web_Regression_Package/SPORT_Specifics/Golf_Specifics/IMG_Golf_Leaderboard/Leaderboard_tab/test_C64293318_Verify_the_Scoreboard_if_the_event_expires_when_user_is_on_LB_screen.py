import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C64293318_Verify_the_Scoreboard_if_the_event_expires_when_user_is_on_LB_screen(Common):
    """
    TR_ID: C64293318
    NAME: Verify the Scoreboard if the event expires when user is on LB screen
    DESCRIPTION: This tc verifies the SB if the event expires when user is on LB screen
    PRECONDITIONS: 1.User should have admin access to CMS
    PRECONDITIONS: 2.Navigate to CMS> System Configuration > Structure both IMGScoreboard and IMGScoreboardsports checkbox should be enabled.
    PRECONDITIONS: 3. Inplay event should be mapped with IMG feed provider event Id.
    """
    keep_browser_open = True

    def test_001_login_into_application(self):
        """
        DESCRIPTION: Login into application.
        EXPECTED: User is logged in
        """
        pass

    def test_002_open_any_inplay_golf_event_which_is_about_to_end_and_has_active_leaderboard(self):
        """
        DESCRIPTION: Open any inplay Golf event which is about to end and has active leaderboard.
        EXPECTED: LB should load on EDP
        """
        pass

    def test_003_stay_on_lb_screen__till_the_event_expires(self):
        """
        DESCRIPTION: Stay on LB screen  till the event expires.
        EXPECTED: Scoreboard still appears with winner tags beside player who won
        """
        pass
