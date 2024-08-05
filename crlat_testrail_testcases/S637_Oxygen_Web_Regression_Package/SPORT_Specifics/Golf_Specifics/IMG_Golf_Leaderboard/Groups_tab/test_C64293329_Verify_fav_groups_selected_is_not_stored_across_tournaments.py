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
class Test_C64293329_Verify_fav_groups_selected_is_not_stored_across_tournaments(Common):
    """
    TR_ID: C64293329
    NAME: Verify fav groups selected is not stored across tournaments
    DESCRIPTION: This tc verifies the functionality of fav icon across tournaments
    PRECONDITIONS: 1.User should have admin access to CMS
    PRECONDITIONS: 2.Navigate to CMS> System Configuration > Structure both IMGScoreboard and IMGScoreboardsports checkbox should be enabled.
    PRECONDITIONS: 3. Inplay event should be mapped with IMG feed provider event Id.
    PRECONDITIONS: 4. User is Logged in.
    PRECONDITIONS: 5. Navigate to inplay Golf EDP--> Groups tab in LB
    PRECONDITIONS: 6. Mark few groups as favorite
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

    def test_004_enable_fav_icon_in_the_header(self):
        """
        DESCRIPTION: Enable fav icon in the header.
        EXPECTED: fav icon should be enabled
        """
        pass

    def test_005_enable_fav_icon_for_few_groups(self):
        """
        DESCRIPTION: Enable fav icon for few groups.
        EXPECTED: fave icon should be enabled
        """
        pass

    def test_006_wait_fot_the_current_tournament_to_end_and_next_tournament_to_start(self):
        """
        DESCRIPTION: wait fot the current tournament to end and next tournament to start.
        EXPECTED: 
        """
        pass

    def test_007_check_the_fav_icon_status_in_the_new_tournament(self):
        """
        DESCRIPTION: Check the fav icon status in the new tournament
        EXPECTED: New tournament should not have any favs selected.
        """
        pass
