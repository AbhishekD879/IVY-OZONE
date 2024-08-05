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
class Test_C62167378_Verify_Cricket_100_opta_scoreboard(Common):
    """
    TR_ID: C62167378
    NAME: Verify Cricket 100 opta scoreboard
    DESCRIPTION: This test case verifies In-Play Cricket 100 event that is subscribed to Opta and has available Scoreboard & Visualization.
    PRECONDITIONS: 1.In-Play Cricket 100 event subscribed to Opta Scoreboards(to be sure if Opta Scoreboard mapped to event please
    PRECONDITIONS: checkRequestURL:https://com[ENV].api.datafabric.dev.aws.ladbrokescoral.com/sdm/stats/inplay/CORAL/[EVENT_ID]/?api-key=[API_KEY] >>Status Code:200
    PRECONDITIONS: 2.In Network tab ->XHR->filter ->api-key 232210976?api-key=...(provider:"OPTA").
    """
    keep_browser_open = True

    def test_001_navigate_to_cricket_100__from_a_z_sportsribbon_tabhomepage(self):
        """
        DESCRIPTION: Navigate to Cricket 100  from A-Z sports/ribbon tab/Homepage
        EXPECTED: User should be navigated to cricket 100.
        EXPECTED: -Matches tab should be displayed by default.
        """
        pass

    def test_002_go_to_in_play_tab(self):
        """
        DESCRIPTION: Go to in-play tab.
        EXPECTED: In-play page should be loaded.
        """
        pass

    def test_003_click_on_any_cricket_100_event_and_verify_whether_the_user_is_able_to_navigate_to__event_details_page_edp_(self):
        """
        DESCRIPTION: Click on any Cricket 100 event and verify whether the user is able to navigate to  event details page (edp ).
        EXPECTED: User should be navigated to event details page (edp).
        """
        pass

    def test_004_verify_displaying_of_cricket_100_opta_scoreboardnote_refer_pre_conditions(self):
        """
        DESCRIPTION: Verify displaying of Cricket 100 opta scoreboard.
        DESCRIPTION: Note: Refer pre-conditions
        EXPECTED: Opta scoreboard should be displayed.
        """
        pass

    def test_005_verify_opta_scoreboard(self):
        """
        DESCRIPTION: Verify opta scoreboard.
        EXPECTED: 5.User should be able to see team names with innings.
        EXPECTED: -A dot should be displayed beside the team name indicating the team's batting/bowling
        EXPECTED: - Strategic time out indicator and power play indicator should be displayed when it is in active state.
        EXPECTED: -User should be able to see Batter stats.
        EXPECTED: -User should be able to see Bowler's stats.
        EXPECTED: -User should be able to see ball by ball indicator.
        EXPECTED: Note:
        EXPECTED: In Network tab ->XHR->filter ->api-key 232210976?api-key=...(provider:"OPTA").
        """
        pass
