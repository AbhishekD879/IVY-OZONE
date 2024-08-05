import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C10940587_Tennis_BIP_events_Live_Score_displaying_and_updating(Common):
    """
    TR_ID: C10940587
    NAME: Tennis BIP events: Live Score displaying and updating
    DESCRIPTION: This test case verifies Live Score displaying and updating on Tennis BIP events on the Featured tab in Featured module by Tennis EventID.
    PRECONDITIONS: 1. Modules by Tennis BIP EventId with an available score and not BIP EventId are created in CMS.
    PRECONDITIONS: 3. User is on Homepage > Featured tab
    PRECONDITIONS: - In order to get events with Scorers use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Commentary/X.XX/CommentaryForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **eventParticipantID** -  to verify player name and corresponding player score
    PRECONDITIONS: *   **periodCode**='GAME', **description**="Game in Tennis match', **state**='R/S', periodIndex="X" with the highest value  - to look at the scorers for the full match
    PRECONDITIONS: *   **periodCode**="SET", **description**="Set in Tennis match", periodIndex="X" - to look at the scorers for the specific Set (where X-set number)
    PRECONDITIONS: *   **state**='R' - set in running state
    PRECONDITIONS: *   **state**='S' - set in stopped state
    PRECONDITIONS: *   **factCode**='SCORE' &** name**='Score of the match/game' - to see Match facts
    PRECONDITIONS: *   **'fact'** - to see a score for particular participant
    """
    keep_browser_open = True

    def test_001_navigate_to_module_with_bip_event_and_verify_tennis_event_with_scores_available(self):
        """
        DESCRIPTION: Navigate to module with BIP Event and verify Tennis event with Scores available
        EXPECTED: Event is shown
        """
        pass

    def test_002_verify_game_score_displaying(self):
        """
        DESCRIPTION: Verify Game Score displaying
        EXPECTED: Total Game Score is shown between player names
        EXPECTED: Each Score for particular player is shown near player name
        """
        pass

    def test_003_verify_game_score_correctness_for_each_player(self):
        """
        DESCRIPTION: Verify Game Score correctness for each player
        EXPECTED: Game Score corresponds to the** 'fact'** attribute from the SS on:
        EXPECTED: periodCode="SET" level with the highest value of **periodIndex**
        EXPECTED: **-->**
        EXPECTED: periodCode="GAME" level with the highest value of **periodIndex**
        """
        pass

    def test_004_verify_game_score_ordering(self):
        """
        DESCRIPTION: Verify Game Score ordering
        EXPECTED: *   Score for the home player is shown near home player name (roleCode="PLAYER_1")
        EXPECTED: *   Score for the away player is shown near away player name (roleCode="PLAYER_2")
        EXPECTED: Note: use **eventParticipantId **for matching Player and Score
        """
        pass

    def test_005_verify_set_score_displaying(self):
        """
        DESCRIPTION: Verify set score displaying
        EXPECTED: *   Number of columns corresponds to max value of **periodIndex**
        EXPECTED: *   Set score is shown between price/odds buttons
        EXPECTED: *   Set score is shown vertically
        """
        pass

    def test_006_verify_set_score_correctness_for_each_player(self):
        """
        DESCRIPTION: Verify set score correctness for each player
        EXPECTED: *   Score corresponds to the** 'fact'** attribute from the SS on periodCode="SET" level
        EXPECTED: *   Scores are shown from lower set to higher based on **periodIndex **value
        """
        pass

    def test_007_verify_set_score_ordering(self):
        """
        DESCRIPTION: Verify set score ordering
        EXPECTED: *   Score for the home player is shown on the first row (roleCode="PLAYER_1")
        EXPECTED: *   Score for the away player is shown on the second row (roleCode="PLAYER_2")
        EXPECTED: Note: use **eventParticipantId **for matching Player and Score
        EXPECTED: e.g.
        EXPECTED: Player1 vs Player2
        EXPECTED: Set 1 (periodIndex="1")
        EXPECTED: Set 2 (periodIndex="2")
        EXPECTED: 'fact' value of Player1 (roleCode="PLAYER_1")
        EXPECTED: 'fact' value of Player1 (roleCode="PLAYER_1")
        EXPECTED: 'fact' value of Player2 (roleCode="PLAYER_2")
        EXPECTED: 'fact' value of Player2 (roleCode="PLAYER_2")
        """
        pass

    def test_008_verify_value_below_the_tennis_icon(self):
        """
        DESCRIPTION: Verify value below the Tennis icon
        EXPECTED: Number of Set is shown in format:** '<set>st/nd/th Set'**
        EXPECTED: <set> corresponds to the highest **periodIndex** attribute on the periodCode="SET"
        """
        pass

    def test_009_trigger_the_following_situationfactis_changed_for_home_player_rolecodeplayer_1_on_the_higestperiodindexlevelandfactis_changed_for_home_player_on_periodcodegame_level_of_the_highestperiodindex(self):
        """
        DESCRIPTION: Trigger the following situation:
        DESCRIPTION: **'fact'** is changed for HOME player (roleCode="PLAYER_1")  on the higest **periodIndex **level
        DESCRIPTION: AND
        DESCRIPTION: **'fact'** is changed for HOME player on periodCode="GAME" level of the highest **periodIndex**
        EXPECTED: Score is immediately start displaying new value for Home player on Game Score and on highest Set Score
        """
        pass

    def test_010_trigger_the_following_situationfactis_changed_for_away_player_rolecodeplayer_2_on_higherperiodindexlevelandfactis_changed_for_away_player_on_periodcodegame_level_of_the_highestperiodindex(self):
        """
        DESCRIPTION: Trigger the following situation:
        DESCRIPTION: **'fact'** is changed for AWAY player (roleCode="PLAYER_2")  on higher **periodIndex **level
        DESCRIPTION: AND
        DESCRIPTION: **'fact'** is changed for AWAY player on periodCode="GAME" level of the highest **periodIndex**
        EXPECTED: Score is immediately start displaying new value for Away player on Game Score and highest Set Score
        """
        pass

    def test_011_trigger_the_following_situationnew_set_appears(self):
        """
        DESCRIPTION: Trigger the following situation:
        DESCRIPTION: **New set appears**
        EXPECTED: *   Score for new set immediately appears
        EXPECTED: *   Number of set below the sport icon is increased by one set
        """
        pass

    def test_012_navigate_to_module_with_not_bip_event_and_verify_event_which_doesnt_have_live_score_available(self):
        """
        DESCRIPTION: Navigate to module with not BIP Event and verify event which doesn't have LIVE Score available
        EXPECTED: Only 'LIVE' label is shown between player names instead of Game Score
        """
        pass
