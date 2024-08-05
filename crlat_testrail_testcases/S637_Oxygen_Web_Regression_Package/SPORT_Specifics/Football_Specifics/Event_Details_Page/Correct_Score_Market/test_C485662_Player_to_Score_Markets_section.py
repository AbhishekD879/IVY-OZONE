import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C485662_Player_to_Score_Markets_section(Common):
    """
    TR_ID: C485662
    NAME: Player to Score Markets section
    DESCRIPTION: This test case verifies Player to Score Markets section on Football Event Details pages
    PRECONDITIONS: 1) To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) In order to create different kinds of Player to Score Markets use the following Markets templates:
    PRECONDITIONS: |||:Market Name|:Market Template
    PRECONDITIONS: || Player to Score and Team Win|ScoreAndTeamWin
    PRECONDITIONS: || Player to Score Exactly 1|ToScoreExactly1
    PRECONDITIONS: || Player to Score and Team Draw|ScoreAndTeamDraw
    PRECONDITIONS: || Player to Score Exactly 2|ToScoreExactly2
    PRECONDITIONS: || Player to Score and Team Lose|ScoreAndTeamLose
    PRECONDITIONS: || Player to Score Exactly 3|ToScoreExactly3
    PRECONDITIONS: || Player to Score First and Team Win|ScoreFirstAndTeamWin
    PRECONDITIONS: || Player to Score First and Team Draw|ScoreFirstAndTeamDraw
    PRECONDITIONS: || Player to Score First and Team Lose|ScoreFirstAndTeamLose
    PRECONDITIONS: || Player to Score in Both Halves|ScoreInBothHalves
    PRECONDITIONS: **NOTE** In order to map each player (which actually corresponds to the selection of each market above) create e.g. |First Goalscorer| market and create selections for it with the same names as you use for the markets above. Select desired team for each selection (player) in the 'Selection Type' field (home/away)
    PRECONDITIONS: 3) Make sure that all of these markets are created
    PRECONDITIONS: 4) Set up prices for some players for each of the markets above.
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Go to Event Details page of Football event
        EXPECTED: Event Details page is opened successfully representing available markets
        """
        pass

    def test_003_go_to_player_to_score__result_section(self):
        """
        DESCRIPTION: Go to 'Player to Score & Result' section
        EXPECTED: * Section is present on Event Details Page and titled 'Player to Score & Result'
        EXPECTED: * The following markets are aggregated into this one section
        EXPECTED: 1. Player to Score and Team Win| **ScoreAndTeamWin**
        EXPECTED: 2. Player to Score and Team Draw| **ScoreAndTeamDraw**
        EXPECTED: 3. Player to Score and Team Lose| **ScoreAndTeamLose**
        EXPECTED: * It is possible to collapse/expand the section
        """
        pass

    def test_004_verify_cash_out_label_next_to_goalscorer_market_section_name(self):
        """
        DESCRIPTION: Verify Cash out label next to Goalscorer Market section name
        EXPECTED: If market has cashoutAvail="Y" then label Cash out should be displayed next to market section name
        """
        pass

    def test_005_expand_player_to_score__result_section(self):
        """
        DESCRIPTION: Expand 'Player to Score & Result' section
        EXPECTED: Section consists of:
        EXPECTED: * Grid with Players names in cell of corresponding team (three columns)
        EXPECTED: * Grid with price/odds buttons in cell of corresponding player  (three columns)
        """
        pass

    def test_006_repeat_steps_3_5_for_the_rest_next_markets_player_to_score_exactly_1_player_to_score_exactly_2_player_to_score_exactly_3_player_to_score_first_and_team_win_player_to_score_first_and_team_draw_player_to_score_first_and_team_lose_player_to_score_in_both_halves(self):
        """
        DESCRIPTION: Repeat steps 3-5 for the rest next markets:
        DESCRIPTION: * Player to Score Exactly 1
        DESCRIPTION: * Player to Score Exactly 2
        DESCRIPTION: * Player to Score Exactly 3
        DESCRIPTION: * Player to Score First and Team Win
        DESCRIPTION: * Player to Score First and Team Draw
        DESCRIPTION: * Player to Score First and Team Lose
        DESCRIPTION: * Player to Score in Both Halves
        EXPECTED: * The following markets are aggregated into "Player to Score Exact Goals" section
        EXPECTED: 1. Player to Score Exactly 1| **ToScoreExactly1**
        EXPECTED: 2. Player to Score Exactly 2| **ToScoreExactly2**
        EXPECTED: 3. Player to Score Exactly 3| **ToScoreExactly3**
        EXPECTED: * The following markets are aggregated into "Player to Score First & Result" section
        EXPECTED: 1. Player to Score First and Team Win| **ScoreFirstAndTeamWin**
        EXPECTED: 2. Player to Score First and Team Draw| **ScoreFirstAndTeamDraw**
        EXPECTED: 3. Player to Score First and Team Lose| **ScoreFirstAndTeamLose**
        EXPECTED: * "Player to Score in Both Halves" market is shown with sections per each team with corresponding team players
        EXPECTED: * It is possible to collapse/expand each section
        EXPECTED: * The rest of expected result from steps above are met
        """
        pass
