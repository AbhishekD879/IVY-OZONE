import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.bet_history_open_bets
@vtest
class Test_C146855_Verify_Football_Live_Scores_Updates_in_My_Bets_section_from_commentary(Common):
    """
    TR_ID: C146855
    NAME: Verify Football Live Scores Updates in 'My Bets' section (from commentary)
    DESCRIPTION: This test case verifies live scores displaying when score was changed on 'Cash out', 'Open Bets' and 'Bet History' tabs (coming from commentary data)
    DESCRIPTION: **Jira Tickets:**
    DESCRIPTION: [BMA-24370 My Bets Improvement : Cashout redesign main bet details area and Remove accordions header changes] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-24370
    PRECONDITIONS: *   User is logged in;
    PRECONDITIONS: *   User has placed bets on **Football** matches (Singles and Multiple bets) where Cash Out offer is available;
    PRECONDITIONS: *   Event is started
    PRECONDITIONS: NOTE: In order to have live scores, the event has to be configured in Amelco. Scores can be changed in the same tool.
    PRECONDITIONS: Instruction: https://confluence.egalacoral.com/display/SPI/How+to+generate+Live+Score+updates+on+Tennis+and+Football+sports
    PRECONDITIONS: In order to get event with Score use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Commentary/X.XX/CommentaryForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **eventParticipantID** -  to verify team name and corresponding team score
    PRECONDITIONS: *   **periodCode**='ALL' & **description**="Total Duration of the game/match' - to look at the scorers for the full match
    PRECONDITIONS: *   **factCode**='SCORE' &** name**='Score of the match/game' - to see Match facts
    PRECONDITIONS: *   **'fact'** - to see a score for particular participant
    PRECONDITIONS: *   **'roleCode' - **HOME/AWAY to see home and away team.
    PRECONDITIONS: Name differences could be present for Football events and environments. E.g.:
    PRECONDITIONS: TST2: 'roleCode' - TEAM_1/TEAM_2
    PRECONDITIONS: PROD: 'roleCode' - HOME/AWAY
    """
    keep_browser_open = True

    def test_001_navigate_to_cash_out_tab_on_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: 
        """
        pass

    def test_002_verify_single_selection_with_live_scores_available(self):
        """
        DESCRIPTION: Verify **Single** selection with Live Scores available
        EXPECTED: Live scores are shown for the selection
        """
        pass

    def test_003_change_score_for_home_team_in_the_amelco_toolfact_is_changed_for_home_team_rolecodehome(self):
        """
        DESCRIPTION: Change score for home team in the Amelco tool:
        DESCRIPTION: **fact** is changed for HOME team (roleCode="HOME")
        EXPECTED: Score immediately starts displaying new value for Home team
        """
        pass

    def test_004_change_score_for_away_team_in_the_amelco_toolfactis_changed_for_away_team_rolecodeaway(self):
        """
        DESCRIPTION: Change score for away team in the Amelco tool:
        DESCRIPTION: **fact** is changed for AWAY team (roleCode="AWAY")
        EXPECTED: Scores immediately start displaying new value for Away team
        """
        pass

    def test_005_verify_multiple_selections_with_live_score_available(self):
        """
        DESCRIPTION: Verify **Multiple** selections with Live score available
        EXPECTED: 
        """
        pass

    def test_006_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps №3-4
        EXPECTED: 
        """
        pass

    def test_007_verify_case_when_score_is_changed_before_application_is_opened(self):
        """
        DESCRIPTION: Verify case when score is changed before application is opened
        EXPECTED: If application was not started/opened and Score was changed for HOME/AWAY team, after opening application and verified event - updated Score will be shown there
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
