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
class Test_C1323591_Verify_Football_Goal_Correction_Alert_animation_on_MyBets_page(Common):
    """
    TR_ID: C1323591
    NAME: Verify Football Goal/Correction Alert animation on 'MyBets' page
    DESCRIPTION: This test case verifies the Goal/Correction Alerts & Animation on 'Cash Out', 'Open Bets' and 'Bet History' tabs
    PRECONDITIONS: *   User is logged in;
    PRECONDITIONS: *   User has placed a bet on **Football **match (Singles and Multiple bets) where Cash Out offer is available;
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
    PRECONDITIONS: The designs can be found here:
    PRECONDITIONS: Ladbrokes:
    PRECONDITIONS: Goal Label: https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b/screen/5c4f20feffb735bf31092870
    PRECONDITIONS: Correction label: https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b/screen/5c4f210144fe0d63959b0004
    PRECONDITIONS: Coral:
    PRECONDITIONS: Goal Label: https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3/screen/5c63f133a981283c0b6710af
    PRECONDITIONS: Correction label : https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3/screen/5c4f18f535c1a337cde525ba
    PRECONDITIONS: Note: 'No exclamation mark for correction on both brands'
    """
    keep_browser_open = True

    def test_001_navigate_to_cash_out_tab_on_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
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
        EXPECTED: * Score is updated accordingly
        """
        pass

    def test_004_cancel_the_scored_goal_in_ats(self):
        """
        DESCRIPTION: Cancel the scored Goal in ATS
        EXPECTED: * Correction Alert is displayed (available in OX 99)
        EXPECTED: * Correction Animation is played (available in OX 99)
        EXPECTED: * Live Score is reverted to the previous score
        """
        pass

    def test_005_score_two_goals_in_succession(self):
        """
        DESCRIPTION: Score two goals in succession
        EXPECTED: * Live score is updated
        EXPECTED: * Goal Alert is displayed every time
        EXPECTED: * Goal Animation is played every time
        EXPECTED: *   roleCode="AWAY"
        EXPECTED: Note: use **eventParticipantId ** for matching Team and Score
        """
        pass

    def test_006_cancel_one_of_the_scored_goals_in_ats(self):
        """
        DESCRIPTION: Cancel one of the scored Goals in ATS
        EXPECTED: * Correction Alert is displayed (available in OX 99)
        EXPECTED: * Correction Animation is played (available in OX 99)
        EXPECTED: * Live Score is reverted to the previous score
        """
        pass

    def test_007_repeat_steps_3_6_for_multiples(self):
        """
        DESCRIPTION: Repeat steps №3-6 for Multiples
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_3_7_on_open_bets_tab(self):
        """
        DESCRIPTION: Repeat steps №3-7 on 'Open Bets' tab
        EXPECTED: 
        """
        pass

    def test_009_repeat_steps_3_7_on_my_bets_tab_within_event_details_page(self):
        """
        DESCRIPTION: Repeat steps №3-7 on 'My Bets' tab within Event Details page
        EXPECTED: 
        """
        pass
