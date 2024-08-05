import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C2552933_Banach_Player_Bets_market_functionality_for_Football_EDP(Common):
    """
    TR_ID: C2552933
    NAME: Banach. 'Player Bets' market functionality for Football EDP
    DESCRIPTION: This test case verifies 'Player Bets' market functionality for Football EDP
    DESCRIPTION: AUTOTEST [C2779801]
    PRECONDITIONS: **Config:**
    PRECONDITIONS: 1. 'Build Your Bet' tab is available on Event Details Page : In CMS -> System-configuration -> YOURCALLICONSANDTABS -> 'enableTab' is selected
    PRECONDITIONS: 2. Banach leagues are added and enabled in CMS -> Your Call -> YourCall Leagues
    PRECONDITIONS: 3. Event belonging to Banach league is mapped (on the Banach side) and created in OpenBet (T.I)
    PRECONDITIONS: 4. BYB markets are added in CMS (in particular case 'Player Bets' market)-> BYB -> BYB Markets
    PRECONDITIONS: Guide for Banach CMS configuration: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Banach
    PRECONDITIONS: **Requests:**
    PRECONDITIONS: Request for Banach leagues : https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/leagues
    PRECONDITIONS: Request for Banach event data: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/events/obEventId=xxxxx
    PRECONDITIONS: Request for Banach market groups: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v2/markets-grouped?obEventId=xxxxx
    PRECONDITIONS: Request for Banach selections: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/selections?marketIds=[ids]&obEventId=xxxxx
    PRECONDITIONS: Request for Banach players: https://coral-test2.banachtechnology.com/api/buildabet/players?obEventId=<ob_event_id>
    PRECONDITIONS: Request for Banach players statistic: https://coral-test2.banachtechnology.com/api/buildabet/playerStatistics?obEventId=<ob_event_id>&id=<player_id>
    PRECONDITIONS: Request for Banach players statistic value range: https://coral-test2.banachtechnology.com/api/buildabet/statisticValueRange?obEventId=<ob_event_id>&playerId=<player_id>&statId=<stats_id>
    PRECONDITIONS: **Note:**
    PRECONDITIONS: Be aware that
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Football Landing page
    PRECONDITIONS: 3. Navigate to the Event Details page where 'Build Your Bet'(Coral)/'Bet Builder' (Ladbrokes) tab is available
    """
    keep_browser_open = True

    def test_001_clicktap_on_build_your_betbet_builder_tab_where_player_bets_market_is_available(self):
        """
        DESCRIPTION: Click/Tap on 'Build Your Bet/Bet Builder' tab where 'Player Bets' market is available
        EXPECTED: * 'Player Bets' accordion is present and contains 'Players' dropdown
        EXPECTED: * Banach **players** response is received
        """
        pass

    def test_002_clicktap_players_dropdown_and_verifies_the_list_of_player_names_inside(self):
        """
        DESCRIPTION: Click/Tap 'Players' dropdown and verifies the list of player names inside
        EXPECTED: List of players corresponds to **name** attributes received in **players** response (excluding Goalkeepers)
        """
        pass

    def test_003_select_some_player_name(self):
        """
        DESCRIPTION: Select some player name
        EXPECTED: * Banach **player-statistics** response is received
        EXPECTED: * 'Statistic' dropdown appears in the row below
        """
        pass

    def test_004_clicktap_statistic_dropdown_and_verifies_statistics_data_inside(self):
        """
        DESCRIPTION: Click/Tap 'Statistic' dropdown and verifies statistics data inside
        EXPECTED: List of statistics corresponds to **title** attributes received in Banach **player-statistics** response
        """
        pass

    def test_005_select_some_statistic(self):
        """
        DESCRIPTION: Select some statistic
        EXPECTED: * Banach **statistic-value-range** response is received
        EXPECTED: * 'Stats Value' dropdown is prepopulated with value
        """
        pass

    def test_006_verify_prepopulated_value(self):
        """
        DESCRIPTION: Verify prepopulated value
        EXPECTED: * Integer number is displayed that corresponds to **average** attribute in **statistic-value-range** response
        EXPECTED: * In case NOT integer is received it should be rounded (i.e. 2.4 -> 2 and 2.5 -> 3)
        EXPECTED: * In case average is below minimum value, minimum value is displayed that corresponds to 'minValue'  in **statistic-value-range** response
        EXPECTED: * In case average is above maximum value, maximum value is displayed  that corresponds to 'maxValue'  in **statistic-value-range** response
        """
        pass

    def test_007_clicktap_stats_value_dropdown(self):
        """
        DESCRIPTION: Click/Tap 'Stats Value' dropdown
        EXPECTED: * List of values is displayed
        EXPECTED: * Values are between **minValue** and **maxValue** received in  **statistic-value-range** response
        EXPECTED: * Values are displayed in increments of 1, e.g.:
        EXPECTED: if **minValue:1** and **maxValue:6**, then dropdown will contain 1+,2+,3+,4+,5+,6+ values
        """
        pass

    def test_008_select_value_other_then_prepopulated(self):
        """
        DESCRIPTION: Select value other then prepopulated
        EXPECTED: Selected value is displayed within 'Stats Value' dropdown box
        """
        pass

    def test_009_click_add_to_bet_button(self):
        """
        DESCRIPTION: Click 'ADD TO BET' button
        EXPECTED: * '1. SELECT A PLAYER' label with one dropdown below is shown
        EXPECTED: * No player is selected by default
        EXPECTED: * 'Select Player' message is displayed within dropdown box
        EXPECTED: * Selection is added to Dashboard
        """
        pass
