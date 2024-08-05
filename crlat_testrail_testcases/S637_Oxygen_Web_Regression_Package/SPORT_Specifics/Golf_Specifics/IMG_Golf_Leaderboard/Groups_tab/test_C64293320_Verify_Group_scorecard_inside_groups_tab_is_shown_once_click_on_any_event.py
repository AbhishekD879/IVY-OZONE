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
class Test_C64293320_Verify_Group_scorecard_inside_groups_tab_is_shown_once_click_on_any_event(Common):
    """
    TR_ID: C64293320
    NAME: Verify Group scorecard inside groups tab is shown once click on any event
    DESCRIPTION: This tc Verifies the Group scorecard inside groups tab is
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

    def test_002_navigate_to_leaderboard_when_the_event_is_inplay(self):
        """
        DESCRIPTION: Navigate to Leaderboard when the event is inplay.
        EXPECTED: LB should load
        """
        pass

    def test_003_go_to_the_event_for_which_groups_is_available(self):
        """
        DESCRIPTION: Go to the event for which Groups is available.
        EXPECTED: Group tab should load.
        """
        pass
