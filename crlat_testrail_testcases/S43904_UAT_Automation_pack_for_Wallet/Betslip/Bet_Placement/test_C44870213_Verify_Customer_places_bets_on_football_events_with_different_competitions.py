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
class Test_C44870213_Verify_Customer_places_bets_on_football_events_with_different_competitions(Common):
    """
    TR_ID: C44870213
    NAME: "Verify Customer places bets on football events with different competitions
    DESCRIPTION: ".Customer places bets on football events with different competitions
    DESCRIPTION: a)Premier league
    DESCRIPTION: b)Champion ship
    DESCRIPTION: c)League One
    DESCRIPTION: d)League Two"
    PRECONDITIONS: UserName: goldenbuild1   Password: password1
    """
    keep_browser_open = True

    def test_001_launch_oxygen_application(self):
        """
        DESCRIPTION: Launch oxygen application
        EXPECTED: HomePage opened
        """
        pass

    def test_002_go_to_football__competition__english__premier_league(self):
        """
        DESCRIPTION: Go to Football > competition > English > premier league
        EXPECTED: Premier league EDP displayed
        """
        pass

    def test_003_verify_match_result_market_is_selected_by_defaultverify_user_can_change_the_market_from_drop_down(self):
        """
        DESCRIPTION: verify Match result market is selected by default
        DESCRIPTION: verify user can change the market from drop down
        EXPECTED: user can change the market displayed in drop down
        EXPECTED: - Match Result
        EXPECTED: - Next Team to Score - design updated. Small tweak needed to show Xth goal
        EXPECTED: - Extra Time Result (need designs) Updated design below:
        EXPECTED: - Total Goals Over/Under 2.5
        EXPECTED: - Both Teams to Score
        EXPECTED: - To Win & Both Teams to Score
        EXPECTED: - Draw No Bet
        EXPECTED: - 1st Half Result
        EXPECTED: - To Qualify
        """
        pass

    def test_004_make_a_selection_and_add_to_betslip(self):
        """
        DESCRIPTION: Make a selection and add to betslip
        EXPECTED: Selection added
        """
        pass

    def test_005_verify_bet_is_placed(self):
        """
        DESCRIPTION: Verify bet is placed
        EXPECTED: Bet placed successfully
        """
        pass

    def test_006_verify_user_can_change_the_competition_to_national_league_league_1_league_2_etc_and_repeat_step_2_to_57_for_all_competition(self):
        """
        DESCRIPTION: Verify user can change the competition to National league, league 1 League 2 etc and repeat step #2 to 57 for all competition
        EXPECTED: 
        """
        pass
