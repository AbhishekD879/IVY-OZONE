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
class Test_C64293322_verify_the_groups_list_is_displayed_properly_after_the_header(Common):
    """
    TR_ID: C64293322
    NAME: verify the groups list is displayed properly after the header
    DESCRIPTION: This tc verifies the groups list below the header
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

    def test_004_verify_the_groups_list_is_displayed_according_to_the_design(self):
        """
        DESCRIPTION: Verify the groups list is displayed according to the design
        EXPECTED: Groups list displayed below header should appear without any graphical glitches or misalignments
        """
        pass
