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
class Test_C874385_Badminton_Scores(Common):
    """
    TR_ID: C874385
    NAME: Badminton Scores
    DESCRIPTION: This test case verifies Badminton Live Score of BIP events
    PRECONDITIONS: 1) In order to have a Scores Badminton event should be BIP
    PRECONDITIONS: 2) To verify Badminton data use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORT_TYPE::XX::LIVE_EVENT::XXX", where XX - Category ID; XXX - Type ID
    PRECONDITIONS: Look at the attribute:
    PRECONDITIONS: *   **categoryCode** = "BADMINTON"
    PRECONDITIONS: *   **teams** - home or away
    PRECONDITIONS: *   **name** - team name
    PRECONDITIONS: *   **score** - total score for team
    PRECONDITIONS: ![](index.php?/attachments/get/5721848)
    PRECONDITIONS: 3) To verify new received data (updated scores) use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: 'SCBRD'
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **value** - to see a Game score for particular participant
    PRECONDITIONS: *   **role_code**='PLAYER_1'/'PLAYER_2' - to determine HOME and AWAY teams
    PRECONDITIONS: ![](index.php?/attachments/get/4211894)
    PRECONDITIONS: 4) [How to generate Live Scores for Badminton using Bet Genius][1]
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/SPI/How+to+generate+Live+Score+Updates+for+Volleyball%2C+Beach+Volleyball+and+Badminton
    PRECONDITIONS: [Bet Genius credentials][2]
    PRECONDITIONS: [2]: https://confluence.egalacoral.com/display/SPI/Bet+Genius+provider
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Bet+Genius
    PRECONDITIONS: 5) [How to generate Live Scores for Badminton using TI][3]
    PRECONDITIONS: [3]: https://confluence.egalacoral.com/display/SPI/Testing+Fallback
    PRECONDITIONS: 6) [How to configure Fallback Scoreboard in CMS][4]
    PRECONDITIONS: [4]: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Fallback+CMS+Configs
    """
    keep_browser_open = True

    def test_001_load_the_application_and_navigate_to_in_play_page__badminton_tab(self):
        """
        DESCRIPTION: Load the application and navigate to 'In-Play' page > 'Badminton' tab
        EXPECTED: 'Badminton' tab on the 'In-Play' page is opened
        """
        pass

    def test_002_verify_badminton_event_with_game_scores_available(self):
        """
        DESCRIPTION: Verify Badminton event with Game Scores available
        EXPECTED: Event is shown
        """
        pass

    def test_003_verify_game_score_displaying(self):
        """
        DESCRIPTION: Verify Game Score displaying
        EXPECTED: * Game Score for particular team is shown at the same row as team's name near the Price/Odds button
        """
        pass

    def test_004_verify_points_score_displaying(self):
        """
        DESCRIPTION: Verify Points Score displaying
        EXPECTED: * Points score for particular team is shown at the same row as team's name near the Price/Odds button
        """
        pass

    def test_005_verify_event_which_doesnt_have_live_score_available(self):
        """
        DESCRIPTION: Verify event which doesn't have LIVE Score available
        EXPECTED: * Scores are not shown
        EXPECTED: * 'LIVE' label is shown from right side of event date
        """
        pass

    def test_006_repeat_steps_2_5_for__homepage___featured_tabsection__homepage___in_play_tab__homepage___in_play_module_mobile__in_play_page___watch_live_tab__sports_landing_page___in_play_tab__sports_landing_page___in_play_module_mobile__in_play__live_stream_section_on_homepage_desktop(self):
        """
        DESCRIPTION: Repeat steps 2-5 for:
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

    def test_007_desktopnavigate_to_badminton_landing_page__matches_tab_and_verify_scoresset_number_for_in_play_widget(self):
        """
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Navigate to Badminton landing page > 'Matches' tab and verify scores/set number for 'In-play' widget
        EXPECTED: * 'LIVE' badge is displayed below the Event name
        EXPECTED: * Scores are displayed in one row for 'Home' and 'Away' player respectively
        EXPECTED: * Scores from all sets are displayed in one row but scores from previous sets have grey color and less font-size
        """
        pass

    def test_008_desktopnavigate_to_badminton_landing_page__matches_tab_and_verify_scoresset_number_for_live_stream_widget(self):
        """
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Navigate to Badminton landing page > 'Matches' tab and verify scores/set number for 'Live Stream' widget
        EXPECTED: * 'LIVE' badge is displayed next to event class/type
        EXPECTED: * Scores are displayed in one row for 'Home' and 'Away' player respectively
        """
        pass
