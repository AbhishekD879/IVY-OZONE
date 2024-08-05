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
class Test_C28544_Placing_Scorecast_bet(Common):
    """
    TR_ID: C28544
    NAME: Placing Scorecast bet
    DESCRIPTION: This scenario verifies placing a Scorecast bet for Football event
    DESCRIPTION: AUTOTEST MOBILE : [C16258403]
    DESCRIPTION: AUTOTEST DESKTOP: [C14876459]
    PRECONDITIONS: 1) In order to run this test scenario select event with market name "First Goal Scorecast" and/or "Last Goal Scorecast"
    PRECONDITIONS: 2) To get information for an event use the following url
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) User is logged in
    PRECONDITIONS: 4) User should have fractional price type as default
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tapfootballicon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon from the Sports Menu Ribbon
        EXPECTED: Football Landing page is opened
        """
        pass

    def test_003_open_event_detail_page(self):
        """
        DESCRIPTION: Open Event Detail Page
        EXPECTED: *   Football Event Details page is opened
        EXPECTED: *   FOR CORAL: 'Main Markets' collection is selected by default
        EXPECTED: *   FOR LADBROKES: 'All Markets' collection is selected by default
        """
        pass

    def test_004_go_to_scorecast_market_section(self):
        """
        DESCRIPTION: Go to Scorecast market section
        EXPECTED: Scorecast market section is present and shown after 'Correct Score' market
        """
        pass

    def test_005_select_first_scorerlast_scorer_and_home_teamaway_team_from_section_1(self):
        """
        DESCRIPTION: Select 'First Scorer'/'Last Scorer' and '<Home Team>'/'<Away Team>' from section 1
        EXPECTED: 'First Scorer'/'Last Scorer' and <Home Team>/<Away Team> options are selected
        """
        pass

    def test_006_select_firstplayer_to_scorelast_player_to_score_and_correct_score(self):
        """
        DESCRIPTION: Select '**First Player to Score**'/'**Last Player to Score**' and '**Correct Score**'
        EXPECTED: 'Odds calculation' button becomes enabled when both selections are made
        """
        pass

    def test_007_tap_odds_calculation_button(self):
        """
        DESCRIPTION: Tap 'Odds calculation' button
        EXPECTED: Bet Slip counter is changed
        """
        pass

    def test_008_open_betslip_page(self):
        """
        DESCRIPTION: Open Betslip page
        EXPECTED: *  Selection is added to the Betslip
        EXPECTED: *  All information is displayed correctly
        EXPECTED: * Odds within Betslip is the same as on selected 'Odds calculation' button
        """
        pass

    def test_009_verify_selection_name(self):
        """
        DESCRIPTION: Verify Selection Name
        EXPECTED: Selection Name contains two parts:
        EXPECTED: *   Selected Goal Scorer first (name corresponds to **player name **selected in Scorecast market section)
        EXPECTED: *   Selected Correct Score (corresponds to **correct score outcome name** selected in Scorecast market section)
        EXPECTED: in format **<goal scorer name>, <correct score>**
        """
        pass

    def test_010_verify_market_type(self):
        """
        DESCRIPTION: Verify Market Type
        EXPECTED: **'First Goal Scorecast'/'Last Goal Scorecast' **market name is displayed accordingly to market that user selects in Scorecast market section (**'First Scorer'**/**'Last Scorer' **respectively)
        """
        pass

    def test_011_verify_event_start_time_and_event_name(self):
        """
        DESCRIPTION: Verify Event Start Time and Event Name
        EXPECTED: **from OX 99**:
        EXPECTED: Event Name is shown in format:
        EXPECTED: **Team1 v/vs Team2 **
        EXPECTED: **OX 98**:
        EXPECTED: Event Start Time and Event Name are shown in format:
        EXPECTED: **Team1 v/vs Team2 **
        EXPECTED: **HH:MM AM/PM, Date**
        EXPECTED: accordingly to SS response
        """
        pass

    def test_012_enter_valid_stake_amount_and_place_a_bet_by_tapping_bet_now_button(self):
        """
        DESCRIPTION: Enter valid 'Stake' amount and place a bet by tapping 'Bet Now' button
        EXPECTED: *  Bet is placed successfully
        EXPECTED: *  User's balance is decremented by entered stake
        EXPECTED: * Bet Reciept is displayed
        """
        pass

    def test_013_change_price_type_format_from_fractional_to_decimal_and_repeat_steps_7_12(self):
        """
        DESCRIPTION: Change price type format from fractional to decimal and repeat steps #7-12
        EXPECTED: 
        """
        pass
