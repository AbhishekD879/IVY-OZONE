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
class Test_C2552934_Banach_Ordering_in_Player_Bets_market_for_Football_EDP(Common):
    """
    TR_ID: C2552934
    NAME: Banach. Ordering in 'Player Bets' market for Football EDP
    DESCRIPTION: This test case verifies ordering in 'Player Bets' market for Football EDP
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

    def test_001_clicktap_players_dropdown_and_verify_ordering_of_player_names(self):
        """
        DESCRIPTION: Click/Tap 'Players' dropdown and verify ordering of player names
        EXPECTED: Player names are ordered in the following way: **Home Team first (list shown alphabetically by surname A-Z) - Away Team last (list shown alphabetically by surname A-Z)** Goalkeepers are not shown
        """
        pass

    def test_002_select_some_player_name(self):
        """
        DESCRIPTION: Select some player name
        EXPECTED: * Selected player name is displayed within 'Players' dropdown
        EXPECTED: * 'Statistic' dropdown appears below with 'Stats Value' dropdown in the same row
        """
        pass

    def test_003_clicktap_statistic_dropdown_and_verify_ordering_of_stats(self):
        """
        DESCRIPTION: Click/Tap 'Statistic' dropdown and verify ordering of stats
        EXPECTED: Statistics are sorted by alphabetical order
        """
        pass

    def test_004_select_some_statistic(self):
        """
        DESCRIPTION: Select some statistic
        EXPECTED: * Selected statistic name is displayed within 'Statistic' dropdown
        EXPECTED: * 'Stats Value' dropdown is prepopulated with corresponding statistic average value
        """
        pass

    def test_005_clicktap_stats_value_dropdown_and_verify_ordering_of_values(self):
        """
        DESCRIPTION: Click/Tap 'Stats Value' dropdown and verify ordering of values
        EXPECTED: * Stats values are sorted from lowest to highest numerical order
        EXPECTED: * Stats values have **+** sign near each value
        """
        pass
