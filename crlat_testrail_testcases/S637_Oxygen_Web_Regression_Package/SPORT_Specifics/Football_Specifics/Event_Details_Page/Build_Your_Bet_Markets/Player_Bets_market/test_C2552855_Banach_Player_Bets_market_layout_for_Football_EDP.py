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
class Test_C2552855_Banach_Player_Bets_market_layout_for_Football_EDP(Common):
    """
    TR_ID: C2552855
    NAME: Banach. 'Player Bets' market layout for Football EDP
    DESCRIPTION: This test case verifies 'Player Bets' market layout for Football EDP
    DESCRIPTION: AUTOTEST [C2779912]
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
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Football Landing page
    PRECONDITIONS: 3. Navigate to the Event Details page where 'Build Your Bet'(Coral)/'Bet Builder'(Ladbrokes) tab is available
    PRECONDITIONS: 4. Click/Tap on 'Build Your Bet/Bet Builder' tab
    """
    keep_browser_open = True

    def test_001_verify_player_bets_accordion_content(self):
        """
        DESCRIPTION: Verify 'Player Bets' accordion content
        EXPECTED: * '1. SELECT A PLAYER' label with dropdown below is shown
        EXPECTED: * No player is selected by default
        EXPECTED: * 'Select Player' message is displayed within dropdown box
        """
        pass

    def test_002_clicktap_players_dropdown(self):
        """
        DESCRIPTION: Click/Tap 'Players' dropdown
        EXPECTED: List of all available player names is shown
        """
        pass

    def test_003_select_some_player_name(self):
        """
        DESCRIPTION: Select some player name
        EXPECTED: * Selected player name is displayed within dropdown box
        EXPECTED: Label
        EXPECTED: * '2. SELECT A STATISTIC' label in one line appears together with two dropdown boxes in another line
        EXPECTED: * 'Select Stat' message is displayed within first dropdown on the left
        EXPECTED: * Empty second dropdown is displayed on the right
        """
        pass

    def test_004_clicktap_statistic_dropdown(self):
        """
        DESCRIPTION: Click/Tap 'Statistic' dropdown
        EXPECTED: List of all available statistics is shown (except Cards statistic)
        """
        pass

    def test_005_select_some_statistic(self):
        """
        DESCRIPTION: Select some statistic
        EXPECTED: * Selected statistic name is displayed within Statistic dropdown box
        EXPECTED: * Next dropdown box is prepopulated with statistic value with **+** sign (e.g. 2+, 50+ etc)
        EXPECTED: * 'ADD TO BET' green button appears under dropdown boxes
        """
        pass

    def test_006_clicktap_stats_value_dropdown(self):
        """
        DESCRIPTION: Click/Tap 'Stats Value' dropdown
        EXPECTED: List of all available values for selected Statistic is shown
        """
        pass

    def test_007_select_value_other_than_prepopulated(self):
        """
        DESCRIPTION: Select value other than prepopulated
        EXPECTED: Selected value is displayed within 'Stats Value' dropdown box
        """
        pass
