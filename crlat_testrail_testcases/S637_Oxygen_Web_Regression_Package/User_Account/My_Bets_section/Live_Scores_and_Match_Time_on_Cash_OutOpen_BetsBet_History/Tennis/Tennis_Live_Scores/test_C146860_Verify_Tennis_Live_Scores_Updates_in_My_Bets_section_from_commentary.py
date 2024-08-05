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
class Test_C146860_Verify_Tennis_Live_Scores_Updates_in_My_Bets_section_from_commentary(Common):
    """
    TR_ID: C146860
    NAME: Verify Tennis Live Scores Updates in 'My Bets' section (from commentary)
    DESCRIPTION: This test case verifies live scores displaying when score was changed on 'Cash Out', 'Open Bets' and 'Bet History' tabs
    DESCRIPTION: **Jira Tickets:**
    DESCRIPTION: [BMA-24370 My Bets Improvement : Cashout redesign main bet details area and Remove accordions header changes] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-24370
    PRECONDITIONS: *   User is logged in;
    PRECONDITIONS: *   User has placed bets on **Tennis** matches (Singles and Multiples) where Cash Out offer is available;
    PRECONDITIONS: *   Events are started
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

    def test_002_verify_single_upcoming_selection(self):
        """
        DESCRIPTION: Verify Single Upcoming selection
        EXPECTED: Live scores are not displayed
        """
        pass

    def test_003_trigger_the_following_situationevent_becomes_started_isstartedtrue(self):
        """
        DESCRIPTION: Trigger the following situation:
        DESCRIPTION: Event becomes started (isStarted=true)
        EXPECTED: Badge with **LIVE** label is displayed below sport icon
        """
        pass

    def test_004_verify_multiple_upcoming_selection(self):
        """
        DESCRIPTION: Verify Multiple Upcoming selection
        EXPECTED: Live scores are not displayed
        """
        pass

    def test_005_repeat_step_3(self):
        """
        DESCRIPTION: Repeat step №3
        EXPECTED: 
        """
        pass

    def test_006_verify_single_selection_with_live_scores_available(self):
        """
        DESCRIPTION: Verify Single selection with Live Scores available
        EXPECTED: 
        """
        pass

    def test_007_trigger_the_following_situationfactis_changed_for_home_player_rolecodeplayer_1_on_the_higestperiodindex_levelandfactis_changed_for_home_player_on_periodcodegame_level_of_the_highestperiodindex(self):
        """
        DESCRIPTION: Trigger the following situation:
        DESCRIPTION: **fact** is changed for HOME player (roleCode="PLAYER_1")  on the higest **periodIndex** level
        DESCRIPTION: AND
        DESCRIPTION: **'fact'** is changed for HOME player on periodCode="GAME" level of the highest **periodIndex**
        EXPECTED: Scores immediately start displaying new value for Home player on Game Score and on highest Set Score
        """
        pass

    def test_008_trigger_the_following_situationfactis_changed_for_away_player_rolecodeplayer_2_on_higherperiodindex_levelandfactis_changed_for_away_player_on_periodcodegame_level_of_the_highestperiodindex(self):
        """
        DESCRIPTION: Trigger the following situation:
        DESCRIPTION: **fact** is changed for AWAY player (roleCode="PLAYER_2")  on higher **periodIndex** level
        DESCRIPTION: AND
        DESCRIPTION: **fact** is changed for AWAY player on periodCode="GAME" level of the highest **periodIndex**
        EXPECTED: Score is immediately start displaying new value for Away player on Game Score and highest Set Score
        """
        pass

    def test_009_verify_multiple_selection_with_live_score_available(self):
        """
        DESCRIPTION: Verify Multiple selection with Live score available
        EXPECTED: Multiple selection with Live Scores is shown
        """
        pass

    def test_010_repeat_steps_7_8(self):
        """
        DESCRIPTION: Repeat steps №7-8
        EXPECTED: 
        """
        pass

    def test_011_verify_score_change_before_application_is_opened(self):
        """
        DESCRIPTION: Verify Score change before application is opened
        EXPECTED: If application was not started/opened and Score was changed for HOME/AWAY team, after opening application and verified event - updated Score will be shown there
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
