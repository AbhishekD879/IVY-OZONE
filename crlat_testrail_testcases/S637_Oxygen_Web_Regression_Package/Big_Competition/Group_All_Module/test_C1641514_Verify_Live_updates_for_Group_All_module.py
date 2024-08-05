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
class Test_C1641514_Verify_Live_updates_for_Group_All_module(Common):
    """
    TR_ID: C1641514
    NAME: Verify Live updates for Group All module
    DESCRIPTION: This test case verifies Live updates for Group All module on Big Competition page
    PRECONDITIONS: * Competition should be created, set up and enabled in CMS -> Big Competition section
    PRECONDITIONS: * Module with type = 'GROUP_ALL' should be created, enabled and set up with Live Events ONLY in CMS
    PRECONDITIONS: * User is logged out
    PRECONDITIONS: * Openbet TI tool: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: * To check update from Live Serve MS open Dev Tools -> Network tab -> WS -> select '?EIO=3&transport=websocket' request
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_competition_page(self):
        """
        DESCRIPTION: Navigate to Competition page
        EXPECTED: * Competition page is opened
        EXPECTED: * Default Tab is opened (e.g. Featured)
        """
        pass

    def test_003_go_to_group_all_module(self):
        """
        DESCRIPTION: Go to Group All Module
        EXPECTED: 
        """
        pass

    def test_004_trigger_price_change_for_selections_from_one_of_outright_markets_in_group_all_module_in_openbet_ti_tool(self):
        """
        DESCRIPTION: Trigger price change for selection(s) from one of 'Outright' markets in Group All Module in Openbet TI tool
        EXPECTED: Corresponding 'Price/Odds' button immediately displays new price and for a few seconds it changes its color to:
        EXPECTED: * blue color if the price has decreased
        EXPECTED: * red color if the price has increased
        """
        pass

    def test_005_trigger_suspension_for_selections_from_one_of_outright_markets_in_group_all_module_in_openbet_ti_tool(self):
        """
        DESCRIPTION: Trigger suspension for selection(s) from one of 'Outright' markets in Group All Module in Openbet TI tool
        EXPECTED: * Corresponding 'Price/Odds' button is greyed out immediately
        EXPECTED: * Its not possible to add selection to Betslip / Quick bet
        """
        pass

    def test_006_trigger_unsuspension_for_selections_from_one_of_outright_markets_in_group_all_module_in_openbet_ti_tool(self):
        """
        DESCRIPTION: Trigger unsuspension for selection(s) from one of 'Outright' markets in Group All Module in Openbet TI tool
        EXPECTED: * Corresponding 'Price/Odds' button is active immediately
        EXPECTED: * Its possible to add selection to Betslip / Quick bet
        """
        pass

    def test_007_trigger_suspension_for_one_of_outright_markets_in_group_all_module_in_openbet_ti_tool(self):
        """
        DESCRIPTION: Trigger suspension for one of 'Outright' markets in Group All Module in Openbet TI tool
        EXPECTED: * All 'Price/Odds' buttons within Outright market are greyed out immediately
        EXPECTED: * Its not possible to add selection from 'Outright' market to Betslip / Quick bet
        """
        pass

    def test_008_trigger_unsuspension_for_one_of_outright_markets_in_group_all_module_in_openbet_ti_tool(self):
        """
        DESCRIPTION: Trigger unsuspension for one of 'Outright' markets in Group All Module in Openbet TI tool
        EXPECTED: * All 'Price/Odds' buttons within Outright market become active immediately
        EXPECTED: * Its possible to add selection from Outright market to Betslip / Quick bet
        """
        pass

    def test_009_trigger_suspension_event_that_one_of_outright_markets_belongs_to_in_group_all_module_in_openbet_ti_tool(self):
        """
        DESCRIPTION: Trigger suspension event that one of 'Outright' markets belongs to in Group All Module in Openbet TI tool
        EXPECTED: * All 'Price/Odds' buttons within Outright market are greyed out immediately
        EXPECTED: * Its not possible to add selection from 'Outright' market to Betslip / Quick bet
        """
        pass

    def test_010_trigger_unsuspension_for_event_that_one_of_outright_markets_belongs_to_in_group_all_module_in_openbet_ti_tool(self):
        """
        DESCRIPTION: Trigger unsuspension for event that one of 'Outright' markets belongs to in Group All Module in Openbet TI tool
        EXPECTED: * All 'Price/Odds' buttons within Outright market become active immediately
        EXPECTED: * Its possible to add selection from Outright market to Betslip / Quick bet
        """
        pass

    def test_011_trigger_undisplay_for_selections_from_one_of_outright_markets_in_group_all_module_in_openbet_ti_toolset_displayedn_on_selection_level(self):
        """
        DESCRIPTION: Trigger undisplay for selection(s) from one of 'Outright' markets in Group All Module in Openbet TI tool
        DESCRIPTION: (set displayed=N on selection level)
        EXPECTED: * 'displayed=N' attribute is received from Live Serve MS for selection(s)
        EXPECTED: * Corresponding Price Odds button(s) changes its value to **'N/A'**
        """
        pass

    def test_012_trigger_undisplay_for_one_of_outright_markets_in_group_all_module_in_openbet_ti_toolset_displayedn_on_market_level(self):
        """
        DESCRIPTION: Trigger undisplay for one of 'Outright' markets in Group All Module in Openbet TI tool
        DESCRIPTION: (set displayed=N on market level)
        EXPECTED: * 'displayed=N' attribute is received from Live Serve MS on market level
        EXPECTED: * All Price Odds buttons within market change its value to **'N/A'**
        """
        pass

    def test_013_trigger_undisplay_for_event_that_one_of_outright_markets_belongs_to_in_group_all_module_in_openbet_ti_toolset_displayedn_on_event_level(self):
        """
        DESCRIPTION: Trigger undisplay for event that one of 'Outright' markets belongs to in Group All Module in Openbet TI tool
        DESCRIPTION: (set displayed=N on event level)
        EXPECTED: * 'displayed=N' attribute is received from Live Serve MS on the event level
        EXPECTED: * All Price Odds buttons within market change its value to **'N/A'**
        """
        pass

    def test_014_log_in_with_valid_credentials(self):
        """
        DESCRIPTION: Log in with valid credentials
        EXPECTED: 
        """
        pass

    def test_015_go_to_settings_switch_odds_format_from_fractional_to_decimal_and_repeat_steps_4_13(self):
        """
        DESCRIPTION: Go to Settings, switch Odds format from Fractional to Decimal and repeat steps #4-13
        EXPECTED: 
        """
        pass
