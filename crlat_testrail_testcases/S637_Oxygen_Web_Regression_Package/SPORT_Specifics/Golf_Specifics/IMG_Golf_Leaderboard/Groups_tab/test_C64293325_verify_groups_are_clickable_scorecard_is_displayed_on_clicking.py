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
class Test_C64293325_verify_groups_are_clickable_scorecard_is_displayed_on_clicking(Common):
    """
    TR_ID: C64293325
    NAME: verify groups are clickable & scorecard is displayed on clicking
    DESCRIPTION: This tc verifies the functionality of click action on groups
    PRECONDITIONS: 1.User should have admin access to CMS
    PRECONDITIONS: 2.Navigate to CMS> System Configuration > Structure both IMGScoreboard and IMGScoreboardsports checkbox should be enabled.
    PRECONDITIONS: 3. Inplay event should be mapped with IMG feed provider event Id.
    PRECONDITIONS: 4. User is Logged in.
    PRECONDITIONS: 5. Navigate to inplay Golf EDP--> Groups tab in LB
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

    def test_004_clicktap_on_any_of_the_group(self):
        """
        DESCRIPTION: Click/tap on any of the group.
        EXPECTED: Scorecard of that group should be displayed
        """
        pass
