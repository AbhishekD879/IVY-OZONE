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
class Test_C1491080_Verify_Winning_Losing_Indicator_for_Football_bets_in_My_Bets_section(Common):
    """
    TR_ID: C1491080
    NAME: Verify Winning/Losing Indicator for Football bets in 'My Bets' section
    DESCRIPTION: This test case verifies Winning/Losing Indicator for Football bets on 'Cash Out', 'Open Bets' and 'Bet History' tabs
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: [BMA-28053 My BetsImprovement : Cashout / OpenBets - Winning /Losing Indicator for Football bets] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-28053
    PRECONDITIONS: *   User is logged in;
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

    def test_001_place_a_single_bet_on_football_in_play_match_with_scores_match_resultbetting_market_where_cash_out_offer_is_available(self):
        """
        DESCRIPTION: Place a Single bet on **Football** In-Play match with scores (Match Result/Betting market) where Cash Out offer is available
        EXPECTED: Single bet is placed successfully
        """
        pass

    def test_002_navigate_to_cash_out_tab_on_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: Single bet with Live scores is shown
        """
        pass

    def test_003_verify_live_score_displaying_for_selection(self):
        """
        DESCRIPTION: Verify Live score displaying for selection
        EXPECTED: * Live scores are displayed on the same line with relevant team names
        EXPECTED: * Live scores are displayed after Event name and Match Time
        EXPECTED: * Live scores are shown in format **x-y** (e.g., “2-1")
        """
        pass

    def test_004_verify_winning_indicator(self):
        """
        DESCRIPTION: Verify **Winning** Indicator
        EXPECTED: **FOR** **99** **Release** :
        EXPECTED: "Winning Indicator" should look like "green arrow' icon on the left of the selection.
        EXPECTED: * Winning Indicator is shown in case:
        EXPECTED: * When user placed a bet on Team A (Home) and current team **wins** / Score is (for example) 2:0
        EXPECTED: * When user placed a bet on Team B (Away) and current team **wins** / and Score is 0:2
        EXPECTED: * When user placed a bet on Draw (Draw) and Score is 2:2
        EXPECTED: **FOR** **98** **Release** :
        EXPECTED: * Winning Indicator is shown in case:
        EXPECTED: * When user placed a bet on Team A (Home) and current team **wins** / Score is (for example) 2:0
        EXPECTED: * When user placed a bet on Team B (Away) and current team **wins** / and Score is 0:2
        EXPECTED: * When user placed a bet on Draw (Draw) and Score is 2:2
        """
        pass

    def test_005_verify_losing_indicator(self):
        """
        DESCRIPTION: Verify **Losing** Indicator
        EXPECTED: **FOR** **99** **Release**:
        EXPECTED: "Losing Indicator" should look like "red arrow' icon on the left of the selection.
        EXPECTED: * Losing Indicator is shown in case:
        EXPECTED: * When user placed a bet on Team A (Home) and current team **loses** / Score is (for example) 0:2
        EXPECTED: * When user placed a bet on Team B (Away) and current team **loses** / and Score is 2:0
        EXPECTED: * When user placed a bet on Draw (Draw) and Team A is **loses** / Score is 0:2
        EXPECTED: * When user placed a bet on Draw (Draw) and Team B is **loses** / Score is 2:0
        EXPECTED: **FOR** **98** **Release**
        EXPECTED: * Losing Indicator is shown in case:
        EXPECTED: * When user placed a bet on Team A (Home) and current team **loses** / Score is (for example) 0:2
        EXPECTED: * When user placed a bet on Team B (Away) and current team **loses** / and Score is 2:0
        EXPECTED: * When user placed a bet on Draw (Draw) and Team A is **loses** / Score is 0:2
        EXPECTED: * When user placed a bet on Draw (Draw) and Team B is **loses** / Score is 2:0
        """
        pass

    def test_006_place_an_single_bet_on_football_in_play_match_on_not_match_resultbetting_markets_where_cash_out_offer_is_available(self):
        """
        DESCRIPTION: Place an Single bet on **Football** In-Play match on **NOT** Match Result/Betting markets where Cash Out offer is available
        EXPECTED: Single bet is placed successfully
        """
        pass

    def test_007_navigate_to_cash_out_tab_on_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: Single bet with Live scores is shown
        """
        pass

    def test_008_verify_winning__losing_indicators(self):
        """
        DESCRIPTION: Verify **Winning** / **Losing** Indicators
        EXPECTED: Winning/Losing Indicators aren't shown for bets from **NOT** Match Result/Betting markets
        """
        pass

    def test_009_repeat_steps_3_8_for_multiples_football_bets(self):
        """
        DESCRIPTION: Repeat steps 3-8 for Multiples Football bets
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps_3_9_for_cash_out_tab_open_bets_tab_bet_history_tab_my_bets_tab_within_event_details_page(self):
        """
        DESCRIPTION: Repeat steps 3-9 for:
        DESCRIPTION: * 'Cash Out' tab
        DESCRIPTION: * 'Open Bets' tab
        DESCRIPTION: * 'Bet History' tab
        DESCRIPTION: * 'My Bets' tab within Event Details page
        EXPECTED: 
        """
        pass
