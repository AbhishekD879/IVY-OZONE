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
class Test_C146783_Verify_Football_Live_Scores_Displaying_in_My_Bets_section_from_commentary(Common):
    """
    TR_ID: C146783
    NAME: Verify Football Live Scores Displaying in 'My Bets' section (from commentary)
    DESCRIPTION: This test case verifies Live Scores Displaying on 'Cash Out', 'Open Bets' and 'Bet History' tabs (coming from commentary data)
    DESCRIPTION: **Jira Tickets:**
    DESCRIPTION: [BMA-24370 My Bets Improvement : Cashout redesign main bet details area and Remove accordions header changes] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-24370
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
    PRECONDITIONS: Example of rolecode - screenshot attached
    PRECONDITIONS: ![](index.php?/attachments/get/34440)
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

    def test_003_verify_live_score_displaying(self):
        """
        DESCRIPTION: Verify Live score displaying
        EXPECTED: * Live scores are displayed on the same line with relevant team names
        EXPECTED: * Live scores are displayed after Event name and Match Time
        EXPECTED: * Live scores are shown in format **x-y** (e.g., “2-1")
        """
        pass

    def test_004_verify_live_score_correctness_for_each_team(self):
        """
        DESCRIPTION: Verify Live score correctness for each team
        EXPECTED: Score corresponds to the **fact** attribute from the SS
        EXPECTED: on periodCode="**ALL**" level
        """
        pass

    def test_005_verify_live_score_ordering(self):
        """
        DESCRIPTION: Verify Live score ordering
        EXPECTED: Score for the **Home** team is shown first
        EXPECTED: *   roleCode="HOME"
        EXPECTED: Score for the **Away** team is shown second
        EXPECTED: *   roleCode="AWAY"
        EXPECTED: Note: use **eventParticipantId ** for matching Team and Score
        """
        pass

    def test_006_verify_multiple_selection_with_live_score_available(self):
        """
        DESCRIPTION: Verify Multiple selection with Live score available
        EXPECTED: Live scores are shown for the corresponding selection in the above described format
        """
        pass

    def test_007_repeat_steps_2_5_for_the_multiple(self):
        """
        DESCRIPTION: Repeat steps 2-5 for the multiple
        EXPECTED: 
        """
        pass

    def test_008_verify_live_scores_and_match_clock_for_a_pre_play_event_single_and_multiple(self):
        """
        DESCRIPTION: Verify live scores and match clock for a **Pre-play event** (single and multiple)
        EXPECTED: Live scores and match clock are NOT shown for pre-play events
        """
        pass

    def test_009_verify_live_scores_and_match_clock_for_an_in_play_event_which_does_not_have_live_scores_and_match_clock_available_single_and_multiple(self):
        """
        DESCRIPTION: Verify live scores and match clock for an **In-play event** which does not have live scores and match clock available (single and multiple)
        EXPECTED: * Live scores and match clock are NOT shown for such event
        EXPECTED: * "LIVE" label is shown instead
        """
        pass

    def test_010_verify_live_scores_and_match_clock_for_outrights_single_and_multiple(self):
        """
        DESCRIPTION: Verify live scores and match clock for **Outrights** (single and multiple)
        EXPECTED: Live scores and match clock are NOT shown for outrights
        """
        pass

    def test_011_repeat_steps_2_10_for_cash_out_tab_open_bets_tab_bet_history_tab_my_bets_tab_within_event_details_page(self):
        """
        DESCRIPTION: Repeat steps 2-10 for:
        DESCRIPTION: * 'Cash Out' tab
        DESCRIPTION: * 'Open Bets' tab
        DESCRIPTION: * 'Bet History' tab
        DESCRIPTION: * 'My Bets' tab within Event Details page
        EXPECTED: 
        """
        pass
