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
class Test_C1924748_Verify_data_which_is_displayed_for_Assists_Player_Market(Common):
    """
    TR_ID: C1924748
    NAME: Verify data which is displayed for 'Assists' Player Market
    DESCRIPTION: This test case verifies data displaying for  'Assists' market
    PRECONDITIONS: TO BE UPDATED
    PRECONDITIONS: 1.  'Assists' Player Market is configured in TI tool.
    PRECONDITIONS: 2.|Player_Stats_Assists| market template should be used for configuration (this template is not available for every football match - need to choose England Premier League/UEFA)
    PRECONDITIONS: 3. Example of Player name for 'Assists' market is the following: |Cristiano Ronaldo| |th1+a| (A)
    """
    keep_browser_open = True

    def test_001_open_an_event_with_configured_player_stats_assists_market(self):
        """
        DESCRIPTION: Open an event with configured 'Player_Stats_Assists' market
        EXPECTED: - #Yourcall - Player Markets section is displayed
        EXPECTED: - Tabs with team names are displayed under #Yourcall - Player Markets section
        EXPECTED: - 'Player_Stats_Assists' market is displayed in #Yourcall - Player Markets section
        EXPECTED: - 'Player_Stats_Assists' market contains 2 fields: 'Player' and 'Player_Stats_Assists Odds'
        """
        pass

    def test_002_verify_cashout_label_displaying_depending_on_cashoutavail_parameter_value(self):
        """
        DESCRIPTION: Verify 'Cashout' label displaying depending on 'cashoutAvail' parameter value
        EXPECTED: 'Cashout' label is displayed if cashoutAvail="Y" for the market
        """
        pass

    def test_003_verify_data_displaying_for_market_selectionscristiano_ronaldo_th1plusa_a_and_lionel_messi_th1plusa_h_are_examples_of_selection_name_configuration_for_player_stats_assists_market(self):
        """
        DESCRIPTION: Verify data displaying for market selections.
        DESCRIPTION: (|Cristiano Ronaldo| |th1+a| (A) and |Lionel Messi| |th1+a| (H) are examples of selection name configuration for 'Player_Stats_Assists' market)
        EXPECTED: - Player name is displayed for Home or Away team based on (H)/(A) value
        EXPECTED: - Appropriate price is displayed for each selection
        """
        pass
