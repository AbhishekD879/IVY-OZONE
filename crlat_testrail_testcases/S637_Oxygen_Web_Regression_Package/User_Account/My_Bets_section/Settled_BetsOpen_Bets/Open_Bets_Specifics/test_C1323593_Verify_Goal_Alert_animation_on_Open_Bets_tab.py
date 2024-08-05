import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.bet_history_open_bets
@vtest
class Test_C1323593_Verify_Goal_Alert_animation_on_Open_Bets_tab(Common):
    """
    TR_ID: C1323593
    NAME: Verify Goal Alert animation on 'Open Bets' tab
    DESCRIPTION: This test case verifies the Goal Alert & Animation on 'Open Bets' tab
    PRECONDITIONS: *   User is logged in;
    PRECONDITIONS: *   User has placed a bet on **Football **match (Singles and Multiple bets);
    PRECONDITIONS: *   Event is started
    PRECONDITIONS: In order to get events with Scorers use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Commentary/X.XX/CommentaryForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **eventParticipantID** -  to verify team name and corresponding team score
    PRECONDITIONS: *   **periodCode**='ALL' & **description**="Total Duration of the game/match' - to look at the scorers for the full match
    PRECONDITIONS: *   **factCode**='SCORE' &** name**='Score of the match/game' - to see Match facts
    PRECONDITIONS: *   **fact** - to see a score for particular participant
    PRECONDITIONS: *   **roleCode** - HOME/AWAY to see home and away team
    PRECONDITIONS: Name differences could be present for Football events and environments. E.g.:
    PRECONDITIONS: TST2: 'roleCode' - TEAM_1/TEAM_2
    PRECONDITIONS: PROD: 'roleCode' - HOME/AWAY
    PRECONDITIONS: (use instruction - https://confluence.egalacoral.com/display/SPI/How+to+generate+Live+Score+updates+on+Tennis+and+Football+sports)
    """
    keep_browser_open = True

    def test_001_navigate_to_open_bets_tab_on_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Open Bets' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: 
        """
        pass

    def test_002_verify_single_bet_withlive_score_available(self):
        """
        DESCRIPTION: Verify Single bet with Live score available
        EXPECTED: Single bet with Live score is shown
        """
        pass

    def test_003_score_a_goal_in_ats(self):
        """
        DESCRIPTION: Score a Goal in ATS
        EXPECTED: * Goal Alert is displayed
        EXPECTED: * Goal Animation is played
        """
        pass

    def test_004_cancel_the_scored_goal_in_ats(self):
        """
        DESCRIPTION: Cancel the scored Goal in ATS
        EXPECTED: *Live Score is reverted to previous score
        EXPECTED: *No animation is played
        """
        pass

    def test_005_score_two_goals_in_succession(self):
        """
        DESCRIPTION: Score two goals in succession
        EXPECTED: *Live score is updated
        EXPECTED: *Goal Alert is displayed every time
        EXPECTED: *Goal Animation is played every time
        EXPECTED: *   roleCode="AWAY"
        EXPECTED: Note: use **eventParticipantId ** for matching Team and Score
        """
        pass

    def test_006_cancel_one_of_the_scored_goals_in_ats(self):
        """
        DESCRIPTION: Cancel one of the scored Goals in ATS
        EXPECTED: *Live Score is reverted to previous score
        EXPECTED: *No animation is played
        """
        pass

    def test_007_repeat_steps_3_6_for_multiples(self):
        """
        DESCRIPTION: Repeat steps №3-6 for Multiples
        EXPECTED: 
        """
        pass
