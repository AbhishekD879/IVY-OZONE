import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C874383_Basketball_Scores(Common):
    """
    TR_ID: C874383
    NAME: Basketball Scores
    DESCRIPTION: This test case verifies Basketball Live Score of BIP events
    PRECONDITIONS: 1) In order to have Basketball Scores, the event should be BIP
    PRECONDITIONS: 2) To verify Basketball data use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORT_TYPE::XX::LIVE_EVENT::XXX", where XX - Category ID; XXX - Type ID
    PRECONDITIONS: Look at the attribute:
    PRECONDITIONS: *   **categoryCode** = "BASKETBALL"
    PRECONDITIONS: *   **score** : X,
    PRECONDITIONS: where X - game score for particular team;
    PRECONDITIONS: *   **role_code**='TEAM_1'/'TEAM_2' - to determine HOME and AWAY teams
    PRECONDITIONS: ![](index.php?/attachments/get/6165112)
    PRECONDITIONS: 3) To verify new received data (updated scores) use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: 'SCBRD'
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **period_code='ALL'** - scores for the full match
    PRECONDITIONS: *   **period_code='QUARTER'** - scores for the the specific Quarter
    PRECONDITIONS: *   **period_index='1/2/3/4'** - to identify the particular 'QUARTER'
    PRECONDITIONS: *   **value** - score for the particular team
    PRECONDITIONS: *   **role_code - 'TEAM_1'/'TEAM_2' or 'HOME'/'AWAY'** - to see home and away team
    PRECONDITIONS: ![](index.php?/attachments/get/6165122)
    PRECONDITIONS: 4) [How to generate Live Scores for Basketball using Amelco][1]
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/SPI/How+to+generate+Live+Score+updates+on+Tennis+and+Football+sports
    PRECONDITIONS: 5) [How to generate Live Scores for Basketball using TI][2]
    PRECONDITIONS: [2]: https://confluence.egalacoral.com/display/SPI/Testing+Fallback
    PRECONDITIONS: 6) [How to configure Fallback Scoreboard in CMS][3]
    PRECONDITIONS: [3]: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Fallback+CMS+Configs
    PRECONDITIONS: *************************
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: 1) If in the SiteServer commentary response the event has a typeFlagCode ="US" the scores should be displayed in reverse order i.e. away score on top and home score on the bottom.
    PRECONDITIONS: 2) We received all scores information, but no clock or period information. This means that the only period stored within OB is the "ALL" period, and so all 'values' are stored against this period.
    """
    keep_browser_open = True

    def test_001_load_the_application_and_navigate_to_in_play_page__basketball_tab(self):
        """
        DESCRIPTION: Load the application and navigate to 'In-Play' page > 'Basketball' tab
        EXPECTED: 'Basketball' tab on the 'In-Play' page is opened
        """
        pass

    def test_002_verify_basketball_event_with_scores_available(self):
        """
        DESCRIPTION: Verify 'Basketball' event with scores available
        EXPECTED: * Event is shown
        EXPECTED: * Live scores are displayed
        EXPECTED: * 'LIVE' label is displayed
        """
        pass

    def test_003_verify_score_displaying(self):
        """
        DESCRIPTION: Verify score displaying
        EXPECTED: Each score for particular team is shown at the same row as team's name near the Price/Odds button
        """
        pass

    def test_004_verify_event_which_doesnt_have_live_score_available(self):
        """
        DESCRIPTION: Verify event which doesn't have 'Live Score' available
        EXPECTED: * 'LIVE' label is shown below the team names
        EXPECTED: * 'Live Scores' are NOT displayed
        """
        pass

    def test_005_repeat_steps_2_4_for__homepage___featured_tabsection__homepage___in_play_tab__homepage___in_play_module_mobile__in_play_page___watch_live_tab__sports_landing_page___in_play_tab__sports_landing_page___in_play_module_mobile__in_play__live_stream_section_on_homepage_desktop(self):
        """
        DESCRIPTION: Repeat steps 2-4 for:
        DESCRIPTION: - Homepage -> 'Featured' tab/section
        DESCRIPTION: - Homepage -> 'In-Play' tab
        DESCRIPTION: - Homepage -> 'In-Play' module **Mobile**
        DESCRIPTION: - 'In-Play' page -> 'Watch Live' tab
        DESCRIPTION: - Sports Landing page -> 'In-Play' tab
        DESCRIPTION: - Sports Landing page -> 'In-Play' module **Mobile**
        DESCRIPTION: - 'In-Play & Live Stream ' section on Homepage **Desktop**
        EXPECTED: 
        """
        pass

    def test_006_desktopnavigate_to_basketball_landing_page__matches_tab_and_verify_scores_for_in_play_widget(self):
        """
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Navigate to Basketball landing page > 'Matches' tab and verify scores for 'In-play' widget
        EXPECTED: * 'LIVE' badge is displayed below the Event name
        EXPECTED: * Scores are displayed in one row for 'Home' and 'Away' player respectively
        EXPECTED: * Scores from all sets are displayed in one row but scores from previous sets have grey color and less font-size
        """
        pass

    def test_007_desktopnavigate_to_basketball_landing_page__matches_tab_and_verify_scores_for_live_stream_widget_if_available(self):
        """
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Navigate to Basketball landing page > 'Matches' tab and verify scores for 'Live Stream' widget (if available)
        EXPECTED: * 'LIVE' badge is displayed next to event class/type
        EXPECTED: * Scores are displayed in one row for 'Home' and 'Away' team respectively
        """
        pass
