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
class Test_C64293326_Verify_user_is_able_to_switch_between_Hole_scorecard_shots_views_by_clicking_on_respective_buttons_at_the_bottom_of_groups_Scorecard_screen(Common):
    """
    TR_ID: C64293326
    NAME: Verify user is able to switch between Hole, scorecard & shots views by clicking on respective buttons at the bottom of groups Scorecard screen
    DESCRIPTION: This tc verifies the functionality of user is able to switch between Hole, scorecard & shots views by clicking on respective buttons at the bottom of groups Scorecard screen
    PRECONDITIONS: 1.User should have admin access to CMS
    PRECONDITIONS: 2.Navigate to CMS> System Configuration > Structure both IMGScoreboard and IMGScoreboardsports checkbox should be enabled.
    PRECONDITIONS: 3. Inplay event should be mapped with IMG feed provider event Id.
    PRECONDITIONS: 4. User is Logged in.
    PRECONDITIONS: 5. Navigate to inplay Golf EDP--> Groups tab in LB
    """
    keep_browser_open = True

    def test_001_navigate_to_leaderboard_when_the_event_is_inplay(self):
        """
        DESCRIPTION: Navigate to Leaderboard when the event is inplay.
        EXPECTED: LB should load
        """
        pass

    def test_002_navigate_to_groups_tab(self):
        """
        DESCRIPTION: Navigate to Groups tab.
        EXPECTED: Groups tab is opened
        """
        pass

    def test_003_verify_the_switching_between_hole_scorecard__shots_views_by_clicking_on_respective_buttons_at_the_bottom_of_groups_scorecard_screen(self):
        """
        DESCRIPTION: Verify the switching between Hole, scorecard & shots views by clicking on respective buttons at the bottom of groups Scorecard screen
        EXPECTED: User should be able to switch as per design.
        """
        pass
