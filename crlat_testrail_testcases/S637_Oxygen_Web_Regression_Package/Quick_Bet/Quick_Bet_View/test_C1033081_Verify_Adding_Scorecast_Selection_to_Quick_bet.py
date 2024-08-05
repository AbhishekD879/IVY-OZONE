import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.quick_bet
@vtest
class Test_C1033081_Verify_Adding_Scorecast_Selection_to_Quick_bet(Common):
    """
    TR_ID: C1033081
    NAME: Verify Adding Scorecast Selection to Quick bet
    DESCRIPTION: This test case verifies adding Scorecast selection to Quick bet
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user's settings
    PRECONDITIONS: * Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: * Application is loaded
    PRECONDITIONS: * User is logged in and has positive balance
    """
    keep_browser_open = True

    def test_001_tap_football_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon from the Sports Menu Ribbon
        EXPECTED: Football Landing page is opened
        """
        pass

    def test_002_open_event_detail_page(self):
        """
        DESCRIPTION: Open Event Detail Page
        EXPECTED: * Football Event Details page is opened
        EXPECTED: * 'Main Markets' collection is selected by default
        """
        pass

    def test_003_go_to_scorecast_market(self):
        """
        DESCRIPTION: Go to Scorecast market
        EXPECTED: 
        """
        pass

    def test_004_select_first_scorerlast_scorer_and_home_teamaway_team_from_section_1(self):
        """
        DESCRIPTION: Select 'First Scorer'/'Last Scorer' and '<Home Team>'/'<Away Team>' from section 1
        EXPECTED: 'First Scorer'/'Last Scorer' and <Home Team>/<Away Team> options are selected
        """
        pass

    def test_005_select_first_player_to_score__last_player_to_score_and_correct_score(self):
        """
        DESCRIPTION: Select **First Player to Score** / **Last Player to Score** and **Correct Score**
        EXPECTED: 'Odds calculation' button becomes enabled when both selections are made
        """
        pass

    def test_006_tap_odds_calculation_button(self):
        """
        DESCRIPTION: Tap 'Odds calculation' button
        EXPECTED: * 50001(30001) request is sent to Remote Betslip microservice with 2 outcomes and **selectionType="scorecast"**
        EXPECTED: * Quick Bet is displayed at the bottom of the page
        """
        pass

    def test_007_verify_selection_name(self):
        """
        DESCRIPTION: Verify Selection Name
        EXPECTED: Selection Name consists of two part:
        EXPECTED: Name 1,  Name 2,
        EXPECTED: where
        EXPECTED: Name 1 corresponds to **event.markets.[i].outcome.name**
        EXPECTED: and Name 2 corresponds to **event.market.[i+1].outcome.name** from 51001(31001) response in WS
        EXPECTED: **NOTE** that selection part from Correct Score market should be always displayed in the second place
        """
        pass

    def test_008_verify_market_name(self):
        """
        DESCRIPTION: Verify Market Name
        EXPECTED: **'First Goal Scorecast'/'Last Goal Scorecast' **market name is displayed accordingly to market that user selects in Scorecast market section (**'First Scorer'**/**'Last Scorer' **respectively)
        """
        pass

    def test_009_tap_add_to_betslip_button(self):
        """
        DESCRIPTION: Tap 'ADD TO BETSLIP' button
        EXPECTED: * Quick Bet is closed
        EXPECTED: * Betslip counter is increased by one
        EXPECTED: * Scorecast selection is added to Betslip after tapping button
        EXPECTED: * Only one outcome is displayed within Betslip
        """
        pass
