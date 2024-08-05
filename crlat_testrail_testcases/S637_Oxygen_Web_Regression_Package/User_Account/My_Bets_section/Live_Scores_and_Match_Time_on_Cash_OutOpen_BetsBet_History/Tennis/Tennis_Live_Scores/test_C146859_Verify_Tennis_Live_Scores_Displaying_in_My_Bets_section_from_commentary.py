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
class Test_C146859_Verify_Tennis_Live_Scores_Displaying_in_My_Bets_section_from_commentary(Common):
    """
    TR_ID: C146859
    NAME: Verify Tennis Live Scores Displaying in 'My Bets' section (from commentary)
    DESCRIPTION: This test case verifies Live Scores Displaying on 'Cash Out', 'Open Bets' and 'Bet History' tabs
    DESCRIPTION: **Jira Tickets:**
    DESCRIPTION: [BMA-24370 My Bets Improvement : Cashout redesign main bet details area and Remove accordions header changes] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-24370
    PRECONDITIONS: *   User is logged in;
    PRECONDITIONS: *   User has placed bets on **Tennis** matches (Singles and Multiples) where Cash Out offer is available;
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
    PRECONDITIONS: NOTE: UAT assistance is needed for LIVE Scores changing. ([or use instruction][1])
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/MOB/How+to+generate+Live+Score+updates+on+Tennis+and+Football+sports
    """
    keep_browser_open = True

    def test_001_navigate_to_cash_out_tab_on_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: 
        """
        pass

    def test_002_verify_single_bet_section_withlive_score_available(self):
        """
        DESCRIPTION: Verify Single bet section with Live score available
        EXPECTED: Single section with Live score is shown
        """
        pass

    def test_003_verify_live_score_displaying(self):
        """
        DESCRIPTION: Verify Live score displaying
        EXPECTED: * Live scores are displayed on the same line with Team Names
        EXPECTED: * Live scores are displayed after Match Time (or FT label)
        """
        pass

    def test_004_verify_live_score_correctness_for_each_player(self):
        """
        DESCRIPTION: Verify Live score correctness for each player
        EXPECTED: Score corresponds to the **fact** attribute from the SS
        EXPECTED: on periodCode="**SET**" level with the highest value of periodIndex ​--> periodCode="**GAME**" level with the highest value of periodIndex
        """
        pass

    def test_005_verify_live_score_ordering(self):
        """
        DESCRIPTION: Verify Live score ordering
        EXPECTED: Score for the Player 1 is shown first
        EXPECTED: *   roleCode="PLAYER_1"
        EXPECTED: Score for the Player 2 is shown second
        EXPECTED: *   roleCode="PLAYER_2"
        EXPECTED: Note: use **eventParticipantId** for matching Player and Score
        """
        pass

    def test_006_verify_multiple_selection_with_live_score_available(self):
        """
        DESCRIPTION: Verify Multiple selection with Live score available
        EXPECTED: Multiple selection with Live score is shown
        """
        pass

    def test_007_repeat_steps_3_5_for_multiples(self):
        """
        DESCRIPTION: Repeat steps №3-5 for Multiples
        EXPECTED: 
        """
        pass

    def test_008_verify_single_selection_which_doesnt_have_live_score_available(self):
        """
        DESCRIPTION: Verify Single selection which doesn't have Live Score available
        EXPECTED: Live scores are not displayed
        """
        pass

    def test_009_verify_multiple_selection_which_doesnt_have_live_score_available(self):
        """
        DESCRIPTION: Verify Multiple selection which doesn't have Live Score available
        EXPECTED: Live scores are not displayed
        """
        pass

    def test_010_verify_live_score_for_upcoming_single_selection(self):
        """
        DESCRIPTION: Verify Live Score for Upcoming Single selection
        EXPECTED: Live Scores are not displayed
        """
        pass

    def test_011_verify_live_score_for_upcoming_multiple_selection(self):
        """
        DESCRIPTION: Verify Live Score for Upcoming Multiple selection
        EXPECTED: Live Scores are not displayed
        """
        pass

    def test_012_repeat_steps_2_11_for_cash_out_tab_open_bets_tab_bet_history_tab_my_bets_tab_within_event_details_page(self):
        """
        DESCRIPTION: Repeat steps 2-11 for:
        DESCRIPTION: * 'Cash Out' tab
        DESCRIPTION: * 'Open Bets' tab
        DESCRIPTION: * 'Bet History' tab
        DESCRIPTION: * 'My Bets' tab within Event Details page
        EXPECTED: 
        """
        pass
