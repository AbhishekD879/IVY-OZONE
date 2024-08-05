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
class Test_C723658_Verify_Handball_Live_Scores_Displaying_and_Updating(Common):
    """
    TR_ID: C723658
    NAME: Verify Handball Live Scores Displaying and Updating
    DESCRIPTION: This test case verifies live scores displaying when score was changed for HOME player.
    PRECONDITIONS: 1) In order to have a Scores Handball event should be BIP event
    PRECONDITIONS: 2) To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: SCBRD
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **categoryCode** = "HANDBALL"
    PRECONDITIONS: *   **value** - to see update with score
    PRECONDITIONS: *   **role_code=HOME**  - to determine HOME team
    PRECONDITIONS: 3) Live Scores are received in event name from BetGenius or can be created manually in Openbet TI in next format:
    PRECONDITIONS: "|Team A Name|" ScoreA-ScoreB "|Team B Name|"
    """
    keep_browser_open = True

    def test_001_open__handball___in_play_tab(self):
        """
        DESCRIPTION: Open  'Handball' -> 'In-Play' tab
        EXPECTED: 'In Play' tab is opened
        """
        pass

    def test_002_verify_handball_event_with_score_available(self):
        """
        DESCRIPTION: Verify Handball event with score available
        EXPECTED: *  'LIVE' label is displayed
        EXPECTED: **For mobile/tablet:**
        EXPECTED: *   Set score is shown between price/odds buttons and event name
        EXPECTED: *   Set score is shown vertically
        EXPECTED: **For desktop:**
        EXPECTED: *   Set score is shown below event name
        EXPECTED: *   Set score is shown horizontally next to 'LIVE' label
        """
        pass

    def test_003_verify_score_correctness_for_home_team(self):
        """
        DESCRIPTION: Verify score correctness for Home team
        EXPECTED: Score corresponds to the **events.[i].comments.teams.home.score'** attribute from the WS,
        EXPECTED: where [i] - number of event that contains particular class
        """
        pass

    def test_004_verify_score_correctness_for_away_team(self):
        """
        DESCRIPTION: Verify score correctness for Away team
        EXPECTED: Score corresponds to the **events.[i].comments.teams.home.score'** attribute from the WS,
        EXPECTED: where [i] - number of event that contains particular class
        """
        pass

    def test_005_trigger_the_following_situationthe_score_is_changed_for_home_team(self):
        """
        DESCRIPTION: Trigger the following situation:
        DESCRIPTION: the score is changed for HOME team
        EXPECTED: * Score immediately starts displaying new value for Home player
        EXPECTED: * Update is received in WS and corresponds to **event.scoreboard.ALL.value** where **role_code=HOME**
        """
        pass

    def test_006_verify_score_change_for_home_player_for_sections_in_a_collapsed_state(self):
        """
        DESCRIPTION: Verify Score change for HOME player for sections in a collapsed state
        EXPECTED: If section is collapsed and Score was changed, after expanding the section - updated Score will be shown there
        """
        pass

    def test_007_trigger_the_following_situationthe_score_is_changed_for_away_team(self):
        """
        DESCRIPTION: Trigger the following situation:
        DESCRIPTION: the score is changed for AWAY team
        EXPECTED: * Score immediately starts displaying new value for Away player
        EXPECTED: * Update is received in WS and corresponds to event.scoreboard.ALL.value where role_code=AWAY
        """
        pass

    def test_008_verify_score_change_for_away_player_for_sections_in_a_collapsed_state(self):
        """
        DESCRIPTION: Verify Score change for AWAY player for sections in a collapsed state
        EXPECTED: If section is collapsed and Score was changed, after expanding the section - updated Score will be shown there
        """
        pass

    def test_009_go_to_in_play_page_handball_sorting_type_and_repeat_steps_2_4(self):
        """
        DESCRIPTION: Go to 'In Play' page, 'Handball' sorting type and repeat steps #2-4
        EXPECTED: 
        """
        pass

    def test_010_go_to_in_play_tab_on_module_selector_ribbon_and_repeat_steps_2_4(self):
        """
        DESCRIPTION: Go to 'In Play' tab on Module Selector Ribbon and repeat steps #2-4
        EXPECTED: 
        """
        pass

    def test_011_go_to_in_play_widget_and_repeat_steps_2_4(self):
        """
        DESCRIPTION: Go to 'In Play' widget and repeat steps #2-4
        EXPECTED: 
        """
        pass

    def test_012_go_to_featured_tab_and_repeat_steps_2_4(self):
        """
        DESCRIPTION: Go to Featured tab and repeat steps #2-4
        EXPECTED: 
        """
        pass
