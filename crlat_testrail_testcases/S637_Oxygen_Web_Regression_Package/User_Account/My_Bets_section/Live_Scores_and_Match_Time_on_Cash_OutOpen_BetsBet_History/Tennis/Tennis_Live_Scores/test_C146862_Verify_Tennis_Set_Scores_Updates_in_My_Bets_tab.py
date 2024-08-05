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
class Test_C146862_Verify_Tennis_Set_Scores_Updates_in_My_Bets_tab(Common):
    """
    TR_ID: C146862
    NAME: Verify Tennis Set Scores Updates in 'My Bets' tab
    DESCRIPTION: This test case verifies set scores displaying when new set appears on 'Cash Out', 'Open Bets' and 'Bet History' tabs
    DESCRIPTION: **Jira Tickets:**
    DESCRIPTION: [BMA-24370 My Bets Improvement : Cashout redesign main bet details area and Remove accordions header changes] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-24370
    PRECONDITIONS: *   User is logged in;
    PRECONDITIONS: *   User has placed bets on **Tennis** matches (Singles and Multiples) where Cash Out offer is available;
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

    def test_003_trigger_the_following_situationnew_set_appears(self):
        """
        DESCRIPTION: Trigger the following situation:
        DESCRIPTION: **New set appears**
        EXPECTED: *   Score for new set immediately appears
        EXPECTED: *   Number of set near Event Name is increased by one set  (e.g.'1st Set' is changed to '2nd Set', '2nd Set' is changed to '3rd Set')
        """
        pass

    def test_004_verify_new_set_appearing_before_application_is_opened(self):
        """
        DESCRIPTION: Verify new set appearing before application is opened
        EXPECTED: If application was not started/opened and new set appears, after opening application and verified event - score of new set and updated set number will be shown there
        """
        pass

    def test_005_verify_multiple_selection_withset_score_available(self):
        """
        DESCRIPTION: Verify Multiple selection with set score available
        EXPECTED: Multiple selection with set score is shown
        """
        pass

    def test_006_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps №3-4
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_2_6_for_cash_out_tab_open_bets_tab_bet_history_tab_my_bets_tab_within_event_details_page(self):
        """
        DESCRIPTION: Repeat steps 2-6 for:
        DESCRIPTION: * 'Cash Out' tab
        DESCRIPTION: * 'Open Bets' tab
        DESCRIPTION: * 'Bet History' tab
        DESCRIPTION: * 'My Bets' tab within Event Details page
        EXPECTED: 
        """
        pass
