import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C146861_Verify_Tennis_Set_Scores_Displaying_in_My_Bets_section(Common):
    """
    TR_ID: C146861
    NAME: Verify Tennis Set Scores Displaying in 'My Bets' section
    DESCRIPTION: This test case verifies set scores displaying on 'Cash Out', 'Open Bets' and 'Bet History' tabs
    DESCRIPTION: **Jira Tickets:**
    DESCRIPTION: [BMA-24370 My Bets Improvement : Cashout redesign main bet details area and Remove accordions header changes] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-24370
    PRECONDITIONS: *   User is logged in;
    PRECONDITIONS: *   User has placed bets on **Tennis** matches (Singles and Multiples) where Cash Out offer is available;
    PRECONDITIONS: *   Events are started
    PRECONDITIONS: In order to get events with Scorers use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Commentary/X.XX/CommentaryForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **eventParticipantID** -  to verify player name and corresponding player score
    PRECONDITIONS: *   **periodCode**='GAME', **description**="Game in Tennis match', **state**='R/S', periodIndex="X" with the highest value  - to look at the scorers for the full match
    PRECONDITIONS: *   **periodCode**="SET", **description**="Set in Tennis match", periodIndex="X" - to look at the scorers for the specific Set (where X-set number)
    PRECONDITIONS: *   **state**='R' - set in running state
    PRECONDITIONS: *   **state**='S' - set in stopped state
    PRECONDITIONS: *   **factCode**='SCORE' &** name**='Score of the match/game' - to see Match facts
    PRECONDITIONS: *   **'fact'** - to see a score for particular participant
    PRECONDITIONS: NOTE: UAT assistance is needed for LIVE Scores changing.
    """
    keep_browser_open = True

    def test_001_navigate_to_cash_out_tab_on_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: 
        """
        pass

    def test_002_verify_single_selection_withset_score_available(self):
        """
        DESCRIPTION: Verify Single selection with set score available
        EXPECTED: Single selection with set score is shown
        """
        pass

    def test_003_verify_set_score_displaying(self):
        """
        DESCRIPTION: Verify set score displaying
        EXPECTED: *   Number of set sections corresponds to max value of **periodIndex**
        EXPECTED: *   Set score is shown horizontally (divided by line) in the same line as number of set
        """
        pass

    def test_004_verify_set_score_correctness_for_each_player(self):
        """
        DESCRIPTION: Verify set score correctness for each player
        EXPECTED: *   Score corresponds to the **fact** attribute from the SS on periodCode="SET" level
        EXPECTED: *   Scores are shown from lower set to higher based on **periodIndex **value
        """
        pass

    def test_005_verify_set_score_ordering(self):
        """
        DESCRIPTION: Verify set score ordering
        EXPECTED: *   Score for the home player is shown on the first row (roleCode="PLAYER_1")
        EXPECTED: *   Score for the away player is shown on the second row (roleCode="PLAYER_2")
        EXPECTED: Note: use **eventParticipantId** for matching Player and Score
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

    def test_006_verify_multiple_selection_withset_score_available(self):
        """
        DESCRIPTION: Verify Multiple selection with set score available
        EXPECTED: Multiple selection with set score is shown
        """
        pass

    def test_007_repeat_steps_3_5(self):
        """
        DESCRIPTION: Repeat steps №3-5
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_2_7_for_cash_out_tab_open_bets_tab_bet_history_tab_my_bets_tab_within_event_details_page(self):
        """
        DESCRIPTION: Repeat steps 2-7 for:
        DESCRIPTION: * 'Cash Out' tab
        DESCRIPTION: * 'Open Bets' tab
        DESCRIPTION: * 'Bet History' tab
        DESCRIPTION: * 'My Bets' tab within Event Details page
        EXPECTED: 
        """
        pass
