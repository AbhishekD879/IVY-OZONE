import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C2911497_Banach_Trigger_selections_dashboard_and_price_for_Player_Bets_market(Common):
    """
    TR_ID: C2911497
    NAME: Banach. Trigger selections dashboard and price for 'Player Bets' market
    DESCRIPTION: This test case verifies triggering of selections dashboard and price for 'Player Bets' market
    PRECONDITIONS: **Config:**
    PRECONDITIONS: 1. BYB **Coral**/Bet Builder **Ladbrokes** tab is available on Event Details Page : In CMS -> System-configuration -> YOURCALLICONSANDTABS -> 'enableTab' is selected
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
    PRECONDITIONS: Check price value: Open Dev tools > Network > 'price' request
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Football Landing page
    PRECONDITIONS: 3. Navigate to the Event Details page where 'Build Your Bet' tab is available
    PRECONDITIONS: 4. Banach markets are loaded (especially 'Player Bets' market)
    """
    keep_browser_open = True

    def test_001_add_only_one_selection_to_the_dashboard_from_player_bets_market(self):
        """
        DESCRIPTION: Add only one selection to the dashboard from 'Player Bets' market
        EXPECTED: * Dashboard appears with slide animation and is expanded (when selection is added for the first time)
        EXPECTED: * Odds area appears next to dashboard header
        """
        pass

    def test_002_verify_odds_area_for_fractional_odds_format(self):
        """
        DESCRIPTION: Verify Odds area for fractional odds format
        EXPECTED: * Odds value taken from 'price' response is displayed
        EXPECTED: * Odds are displayed in the fractional format defined in Settings/Header Menu
        EXPECTED: * 'PLACE BET' text below odds
        """
        pass

    def test_003_change_odds_format_in_settings_for_mobiletablet_or_header_menu_for_desktop(self):
        """
        DESCRIPTION: Change odds format in Settings for Mobile/Tablet or Header Menu for Desktop
        EXPECTED: Odds are changed to decimal
        """
        pass

    def test_004_navigate_back_to_edp_of_event_that_has_banach_markets_and_select_build_your_bet_for_coral__bet_builder_for_ladbrokes_tab(self):
        """
        DESCRIPTION: Navigate back to EDP of event that has Banach markets and select 'Build Your Bet' (for Coral) / 'Bet Builder' (for Ladbrokes) tab
        EXPECTED: BYB **Coral**/Bet Builder **Ladbrokes** tab on event details page with Banach markets is loaded
        """
        pass

    def test_005_verify_odds_area_for_decimal_odds_format(self):
        """
        DESCRIPTION: Verify Odds area for decimal odds format
        EXPECTED: * Odds value taken from 'price' response is displayed
        EXPECTED: * Odds are displayed in the decimal format defined in Settings/Header Menu
        EXPECTED: * 'PLACE BET' text below odds
        """
        pass

    def test_006_add_one_more_selection_from_player_bets_market(self):
        """
        DESCRIPTION: Add one more selection from 'Player bets' market
        EXPECTED: * Dashboard is still displayed
        EXPECTED: * Odds area is present next to dashboard header
        """
        pass

    def test_007_verify_odds_area(self):
        """
        DESCRIPTION: Verify Odds area
        EXPECTED: * Odds value taken from 'price' response is displayed
        EXPECTED: * Odds are displayed in the format defined in Settings/Header Menu
        EXPECTED: * 'PLACE BET' text below odds
        """
        pass

    def test_008_remove_all_selections_from_dashboard(self):
        """
        DESCRIPTION: Remove all selections from Dashboard
        EXPECTED: Dashboard is not displayed anymore on EDP
        """
        pass
