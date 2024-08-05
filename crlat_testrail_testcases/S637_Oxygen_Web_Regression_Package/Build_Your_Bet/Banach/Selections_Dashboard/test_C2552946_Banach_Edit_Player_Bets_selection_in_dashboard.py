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
class Test_C2552946_Banach_Edit_Player_Bets_selection_in_dashboard(Common):
    """
    TR_ID: C2552946
    NAME: Banach. Edit Player Bets selection in dashboard
    DESCRIPTION: This test case verifies possibility of editing added Player Bets selection(s) in dashboard
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: **Requests:**
    PRECONDITIONS: Request for Banach leagues : https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/leagues
    PRECONDITIONS: Request for Banach event data: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/events/obEventId=xxxxx
    PRECONDITIONS: Request for Banach market groups: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v2/markets-grouped?obEventId=xxxxx
    PRECONDITIONS: Request for Banach selections: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/selections?marketIds=[ids]&obEventId=xxxxx
    PRECONDITIONS: Request for Banach players: https://coral-test2.banachtechnology.com/api/buildabet/players?obEventId=<ob_event_id>
    PRECONDITIONS: Request for Banach players statistic: https://coral-test2.banachtechnology.com/api/buildabet/playerStatistics?obEventId=<ob_event_id>&id=<player_id>
    PRECONDITIONS: Request for Banach players statistic value range: https://coral-test2.banachtechnology.com/api/buildabet/statisticValueRange?obEventId=<ob_event_id>&playerId=<player_id>&statId=<stats_id>
    PRECONDITIONS: * BYB **Coral**/Bet Builder **Ladbrokes** tab on event details page is loaded
    PRECONDITIONS: * Player Bet selections are added to the dashboard, e.g. Player 1 to have 2+Shots on Goals and Player 2 to have 5+ Passes
    """
    keep_browser_open = True

    def test_001_tapclick_on_edit_icon_next_to_one_of_player_bet_selections_in_dashboard(self):
        """
        DESCRIPTION: Tap/click on 'Edit' icon next to one of Player Bet selections in dashboard
        EXPECTED: 'Edit selection' section is shown, consisting of:
        EXPECTED: - 'Edit selection' section title
        EXPECTED: - 'Done' label
        EXPECTED: - 'Change player' title and drop-down with previously selected player
        EXPECTED: - 'Change statistic' title and 2 drop-downs with previously selected statistics
        """
        pass

    def test_002_tapclick_on_change_player_dropdown_and_verify_list_of_player_names(self):
        """
        DESCRIPTION: Tap/click on 'Change player' dropdown and verify list of player names
        EXPECTED: List of players corresponds to **name** attribute received in **players** response
        """
        pass

    def test_003_select_any_player_from_drop_down(self):
        """
        DESCRIPTION: Select any player from drop-down
        EXPECTED: - Selected player is displayed
        EXPECTED: - 2 'Change statistic' drop-downs are cleared
        EXPECTED: - Odds area becomes disabled
        """
        pass

    def test_004_tapclick_on_statistic_dropdown_and_verify_statistics_values(self):
        """
        DESCRIPTION: Tap/click on 'Statistic' dropdown and verify statistics values
        EXPECTED: List of statistics corresponds to **title** attribute received in **player-statistics** response
        """
        pass

    def test_005_select_any_statistic_value(self):
        """
        DESCRIPTION: Select any statistic value
        EXPECTED: - Selected statistic is displayed
        EXPECTED: - 'Stats Value' dropdown is prepopulated with **average** value from **statistic-value-range** response with **+** sign
        EXPECTED: - Odds area becomes enabled, containing recalculated price from **price** request/response
        """
        pass

    def test_006_verify_average_value(self):
        """
        DESCRIPTION: Verify **average** value
        EXPECTED: * Integer number is displayed that corresponds to **average** attribute in **statistic-value-range** response
        EXPECTED: * In case NOT integer is received it should be rounded (i.e. 2.4 -> 2 and 2.5 -> 3)
        EXPECTED: * In case average is below minimum value, minimum value is displayed that corresponds to 'minValue'  in **statistic-value-range** response
        EXPECTED: * In case average is above maximum value, maximum value is displayed  that corresponds to 'maxValue'  in **statistic-value-range** response
        """
        pass

    def test_007_tapclick_on_stats_value_dropdown_and_verify_values(self):
        """
        DESCRIPTION: Tap/click on 'Stats Value' dropdown and verify values
        EXPECTED: * List of values is displayed
        EXPECTED: * Values are between **minValue** and **maxValue** received in **statistic-value-range** response
        EXPECTED: * Values are displayed in increments of 5 for PASSES statistic, e.g.: if 'minValue:5' and 'maxValue:30', then dropdown will contain 5+,10+,15+,20+,25+,30+ values
        EXPECTED: * Values are displayed in increments of 1 for all other statistics, e.g.: if 'minValue:1' and 'maxValue:6', then dropdown will contain 1+,2+,3+,4+,5+,6+ values
        """
        pass

    def test_008_tapclick_on_done_label(self):
        """
        DESCRIPTION: Tap/click on 'Done' label
        EXPECTED: - 'Edit selection' section is closed
        EXPECTED: - Newly selected values are displayed in dashboard
        EXPECTED: - 'Edit' and 'delete' icons are displayed next to selection
        """
        pass
