import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C1033082_Verify_Bet_Placement_on_Scorecast_Selection(Common):
    """
    TR_ID: C1033082
    NAME: Verify Bet Placement on Scorecast Selection
    DESCRIPTION: This test case verifies Bet Placement on Scorecast Selection
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: * User is logged in and has positive balance
    PRECONDITIONS: * Dev Tools should be opened
    PRECONDITIONS: How to create Scorecast market: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=How+to+create+Scorecast+market+and+calculate+odds+prices+for+them
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_football_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon from the Sports Menu Ribbon
        EXPECTED: Football Landing page is opened
        """
        pass

    def test_003_open_event_detail_page(self):
        """
        DESCRIPTION: Open Event Detail Page
        EXPECTED: * Football Event Details page is opened
        EXPECTED: * 'Main Markets' collection is selected by default
        """
        pass

    def test_004_go_to_scorecast_market(self):
        """
        DESCRIPTION: Go to Scorecast market
        EXPECTED: 
        """
        pass

    def test_005_select_first_scorerlast_scorer_and_home_teamaway_team_from_section_1(self):
        """
        DESCRIPTION: Select 'First Scorer'/'Last Scorer' and '<Home Team>'/'<Away Team>' from section 1
        EXPECTED: 'First Scorer'/'Last Scorer' and <Home Team>/<Away Team> options are selected
        """
        pass

    def test_006_select_first_player_to_score__last_player_to_score_and_correct_score(self):
        """
        DESCRIPTION: Select **First Player to Score** / **Last Player to Score** and **Correct Score**
        EXPECTED: 'Odds calculation' button becomes enabled when both selections are made
        """
        pass

    def test_007_tap_odds_calculation_button(self):
        """
        DESCRIPTION: Tap 'Odds calculation' button
        EXPECTED: * 'Odds calculation' button is selected and highlighted in green
        EXPECTED: * Quick Bet is displayed at the bottom of the page
        """
        pass

    def test_008_enter_value_in_stake_field(self):
        """
        DESCRIPTION: Enter value in 'Stake' field
        EXPECTED: 'Stake' field is populated with value
        """
        pass

    def test_009_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'PLACE BET' button
        EXPECTED: * Bet is placed successfully
        EXPECTED: * User balance is decreased by stake entered on step #8
        EXPECTED: * Bet Receipt is displayed with bet ID number
        """
        pass

    def test_010_verify_selection_name_correctness(self):
        """
        DESCRIPTION: Verify Selection name correctness
        EXPECTED: Selection name consists of two parts:
        EXPECTED: Name 1, Name 2,
        EXPECTED: where
        EXPECTED: Name 1 corresponds to **receipt.legParts.[i].outcomeDesc** when **marketDesc = First/Last Goal Scorer from 30012 response from WS
        EXPECTED: Name 2 corresponds to **receipt.legParts.[i].outcomeDesc** when **marketDesc = Correct Score** from 30012 response from WS
        """
        pass

    def test_011_check_placed_bet_correctness_on_openbet_ti_tool_find_bet_by_using_bet_id_displayed_on_bet_receipt(self):
        """
        DESCRIPTION: Check placed bet correctness on Openbet Ti tool (find bet by using bet ID displayed on Bet Receipt)
        EXPECTED: All information about bet is correct and stored in Openbet Ti tool
        """
        pass
