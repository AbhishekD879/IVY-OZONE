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
class Test_C64293323_Verify_the_latest_round_being_played_is_selected_by_default_in_the_round_selection_dropdown(Common):
    """
    TR_ID: C64293323
    NAME: Verify the latest round being played is selected by default in the round selection dropdown
    DESCRIPTION: This tc verifies the round selection dropdown in Groups tab
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

    def test_003_navigate_to_groups_tab(self):
        """
        DESCRIPTION: Navigate to Groups tab.
        EXPECTED: Groups tab is opened
        """
        pass

    def test_004_verify_that_the_latest_round_being_played_is_selected_as_default(self):
        """
        DESCRIPTION: Verify that the latest round being played is selected as default
        EXPECTED: Latest round being played should be selected as default when we open Groups tab.
        """
        pass
