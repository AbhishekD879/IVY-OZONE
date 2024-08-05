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
class Test_C1924269_Verify_In_Play_Player_Stats_Markets_displaying_in_Event_Details_page(Common):
    """
    TR_ID: C1924269
    NAME: Verify In-Play Player Stats Markets displaying in Event Details page
    DESCRIPTION: This test case verifies Player Markets displaying for Football EDP
    PRECONDITIONS: Event with Player Markets is configured in TI tool (|Player_Stats_Assist|, |Player_Stats_Shots templates| - these markets are a kind of Yourcall markets)
    PRECONDITIONS: Example of Player name is the following: |Cristiano Ronaldo| |th1+a| (A) - away team player or |Cristiano Ronaldo| |th1+a| (H) - home team player
    PRECONDITIONS: Displaying of In-Play Player Stats Markets for events is configurable in CMS - System Configuration - Structure - 'your Call Player Stats Name' option
    """
    keep_browser_open = True

    def test_001_open_event_in_application_and_verify_player_markets_section_displaying_in_event_details_page_edp(self):
        """
        DESCRIPTION: Open event in application and verify Player Markets section displaying in Event Details Page (EDP)
        EXPECTED: Player Markets section with following elements:
        EXPECTED: - main Player Markets accordion with section name - #YOURCALL - PLAYER MARKETS
        EXPECTED: - Teams switcher with teams names ( e.g. BRAZIL - GERMANY)
        EXPECTED: - Home (left) team is selected by default
        EXPECTED: - Configured Player Markets
        """
        pass

    def test_002_verify_number_of_player_markets_which_are_expanded_by_default(self):
        """
        DESCRIPTION: Verify number of Player Markets which are expanded by default
        EXPECTED: Only 1st Player Market is expanded by default
        """
        pass

    def test_003_verify_player_markets_displaying_according_to_configured_in_ti_tool_ordering(self):
        """
        DESCRIPTION: Verify Player markets displaying according to configured in TI tool ordering
        EXPECTED: All markets are displayed:
        EXPECTED: - by displayOrder in ascending
        EXPECTED: - if displayOrder is the same then alphanumerically
        """
        pass

    def test_004_verify_cash_out_label_displaying_next_to_market_section_name_in_the_main_accordion(self):
        """
        DESCRIPTION: Verify Cash out label displaying next to Market section name in the main accordion
        EXPECTED: If one of markets has cashoutAvail="Y" then label Cash out should be displayed next to market section name
        """
        pass

    def test_005_verify_possibility_to_switch_between_teams(self):
        """
        DESCRIPTION: Verify possibility to switch between teams
        EXPECTED: - It is possible to switch between Home/Away teams
        EXPECTED: - Markets content is updated appropriately to the selected team ((H)/(A) parameter in player name in TI tool is used for defining of Home/Away players)
        """
        pass

    def test_006_verify_main_player_markets_accordion_displaying_when_all_player_markets_are_undisplayed(self):
        """
        DESCRIPTION: Verify main Player Markets accordion displaying when all Player Markets are undisplayed
        EXPECTED: Main accordion is not displayed on the page
        """
        pass
