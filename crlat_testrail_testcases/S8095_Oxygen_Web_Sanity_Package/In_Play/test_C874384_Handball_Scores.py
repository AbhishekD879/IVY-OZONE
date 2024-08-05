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
class Test_C874384_Handball_Scores(Common):
    """
    TR_ID: C874384
    NAME: Handball Scores
    DESCRIPTION: This test case verifies Handball Live Score of BIP events
    PRECONDITIONS: 1) In order to have a Scores Handball event should be BIP
    PRECONDITIONS: 2) To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORTS::::LIVE_EVENT"
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **categoryCode** = "HANDBALL"
    PRECONDITIONS: *   **teams** - home or away
    PRECONDITIONS: *   **name** - team name
    PRECONDITIONS: *   **score** - total score for team
    PRECONDITIONS: ![](index.php?/attachments/get/6165168)
    PRECONDITIONS: 3) To verify new received data (updated scores) use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: 'SCBRD'
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **value** - to see a Game score for particular participant
    PRECONDITIONS: *   **role_code**='HOME'/'AWAY' - to determine HOME and AWAY teams
    PRECONDITIONS: ![](index.php?/attachments/get/6165169)
    PRECONDITIONS: 4) [How to generate Live Scores for Handball using Bet Genius][1]
    PRECONDITIONS: [Bet Genius credentials][2]
    PRECONDITIONS: [2]: https://confluence.egalacoral.com/display/SPI/Bet+Genius
    PRECONDITIONS: 5) [How to generate Live Scores for Badminton using TI][3]
    PRECONDITIONS: [3]: https://confluence.egalacoral.com/display/SPI/Testing+Fallback
    PRECONDITIONS: 6) [How to configure Fallback Scoreboard in CMS][4]
    PRECONDITIONS: [4]: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Fallback+CMS+Configs
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_load_handball___in_play(self):
        """
        DESCRIPTION: Load 'Handball' -> 'In-Play'
        EXPECTED: 'In-Play' tab is opened
        """
        pass

    def test_003_verify_handball_event_with_scores_available(self):
        """
        DESCRIPTION: Verify 'Handball' event with scores available
        EXPECTED: * Event is shown
        EXPECTED: * Live scores are displayed
        EXPECTED: * 'LIVE' label is displayed
        EXPECTED: * 'Watch live' icon is displayed if live stream is available
        """
        pass

    def test_004_verify_score_displaying(self):
        """
        DESCRIPTION: Verify score displaying
        EXPECTED: Match score is shown between price/odds buttons and event name
        """
        pass

    def test_005_verify_event_which_doesnt_have_live_score_available(self):
        """
        DESCRIPTION: Verify event which doesn't have 'Live Score' available
        EXPECTED: * 'LIVE' label is shown below the team names
        EXPECTED: * 'Live Scores' are NOT displayed
        """
        pass

    def test_006_repeat_steps_3_5_for__homepage___featured_tabsection__homepage___in_play_tab__homepage___in_play_module_mobile__in_play_page___watch_live_tab__sports_landing_page___in_play_tab__sports_landing_page___in_play_module_mobile__in_play__live_stream_section_on_homepage_desktop(self):
        """
        DESCRIPTION: Repeat steps №3-5 for:
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

    def test_007_for_desktop_expected_results_are_to_be_updated_due_to_redesign_for_desktoprepeat_steps_3_5_on_handball_landing_page_for_in_play_widget(self):
        """
        DESCRIPTION: **For Desktop:** (expected results are to be updated due to redesign for desktop)
        DESCRIPTION: Repeat steps №3-5 on Handball Landing page for 'In-play' widget
        EXPECTED: * 'LIVE' label is shown below the team names
        EXPECTED: * Scores are displayed on the both sides of 'LIVE' label
        """
        pass

    def test_008_for_desktoprepeat_steps_3_5_on_handball_landing_page_for_live_stream_widget_if_available(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps №3-5 on Handball Landing page for 'Live Stream' widget (if available)
        EXPECTED: * 'LIVE' label is shown in the same line as event class/type
        EXPECTED: * Scores are displayed in the same line as team names
        """
        pass
