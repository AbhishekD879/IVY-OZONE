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
class Test_C1489741_Verify_Basketball_Live_Scores_Update_for_Home_Away_Team(Common):
    """
    TR_ID: C1489741
    NAME: Verify Basketball Live Scores Update for Home/Away Team
    DESCRIPTION: This test case verifies Basketball Live Scores Displaying when Score was Changed for HOME/AWAY Team on 'CASH OUT', 'Open Bets', 'Bet History' tabs
    PRECONDITIONS: * User should be logged in to see their cash out/open bets/bet history
    PRECONDITIONS: * User should have placed bets on a Bsketball live event with scores available
    PRECONDITIONS: 1) In order to have a Scores Basketball event should be in-play
    PRECONDITIONS: 2) To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: SCBRD
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: **participant_id** -  to verify team name and corresponding team score
    PRECONDITIONS: **period_code='ALL'** - to look at the scorers for the full match
    PRECONDITIONS: **period_code='QUARTER'** - to look at the scorers for the the specific time
    PRECONDITIONS: **period_index='1/2/3/4'** - to identify the particular 'QUARTER'
    PRECONDITIONS: **code='SCORE'**
    PRECONDITIONS: **value** - to see a score for the particular participant
    PRECONDITIONS: **role_code - 'TEAM_1'/'TEAM_2' or 'HOME'/'AWAY'** - to see home and away team
    PRECONDITIONS: Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: TST2: roleCode - 'TEAM_1'/'TEAM_2'
    PRECONDITIONS: PROD: roleCode - 'HOME/'AWAY'
    PRECONDITIONS: 3) Use the following link for verification SS commentary response http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Commentary/X.XX/CommentaryForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: *NOTE:*
    PRECONDITIONS: 1) Use https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Amelco+Systems in order to generate live scores for BIP event.
    PRECONDITIONS: 2) If in the SiteServer commentary response the event has a typeFlagCode ="US" the scores should be displayed in reverse order i.e. away score first and home score last.
    PRECONDITIONS: 3) We received all score information, but no clock or period information. This means that the only period stored within OB is the "ALL" period, and so all 'values' are stored against this period.
    """
    keep_browser_open = True

    def test_001_go_to_cash_out_tab_on_my_bets_page_bet_slip_widget(self):
        """
        DESCRIPTION: Go to 'Cash out' tab on 'My Bets' page/ 'Bet Slip' widget
        EXPECTED: * Cash out page is opened
        EXPECTED: * User's cash out bets are shown
        """
        pass

    def test_002_verify_basketball_bet_with_scores_available(self):
        """
        DESCRIPTION: Verify 'Basketball' bet with scores available
        EXPECTED: * The bet is shown in the cash out section
        EXPECTED: * Live scores are displayed
        EXPECTED: * 'LIVE' label is displayed
        """
        pass

    def test_003_change_the_score_for_home_team_in_amelco_tool(self):
        """
        DESCRIPTION: Change the score for HOME team in Amelco tool
        EXPECTED: * Score immediately starts displaying new value for HOME team
        EXPECTED: * Score corresponds to the 'value' attribute from WS
        """
        pass

    def test_004_verify_ws_response_with_scbrd_type___all(self):
        """
        DESCRIPTION: Verify WS response with 'SCBRD' type -> ALL
        EXPECTED: The particular score is displayed in 'value' attribute for HOME team
        """
        pass

    def test_005_change_the_score_for_away_team_in_amelco_tool(self):
        """
        DESCRIPTION: Change the score for AWAY team in Amelco tool
        EXPECTED: * Score immediately starts displaying new value for AWAY team
        EXPECTED: * Score corresponds to the 'value' attribute from WS
        """
        pass

    def test_006_verify_ws_response_with_scbrd_type___all(self):
        """
        DESCRIPTION: Verify WS response with 'SCBRD' type -> ALL
        EXPECTED: The particular score is displayed in 'value' attribute for AWAY team
        """
        pass

    def test_007_verify_score_change_before_application_is_opened_for_homeaway_team(self):
        """
        DESCRIPTION: Verify 'Score' change before application is opened for HOME/AWAY team
        EXPECTED: If application was not started/opened and Score was changed for HOME/AWAY team, after opening application and cash out page with verified bet - updated Score will be shown there
        """
        pass

    def test_008_for_multiples_repeat_steps_2_7(self):
        """
        DESCRIPTION: For multiples repeat steps 2-7
        EXPECTED: 
        """
        pass

    def test_009_repeat_steps_2_8_for_cash_out_tab_my_bets_tab_bet_history_tab(self):
        """
        DESCRIPTION: Repeat steps 2-8 for:
        DESCRIPTION: * 'Cash Out' tab
        DESCRIPTION: * 'My Bets' tab
        DESCRIPTION: * 'Bet History' tab
        EXPECTED: 
        """
        pass
