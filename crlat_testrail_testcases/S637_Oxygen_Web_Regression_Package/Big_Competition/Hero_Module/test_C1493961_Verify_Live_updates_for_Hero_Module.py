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
class Test_C1493961_Verify_Live_updates_for_Hero_Module(Common):
    """
    TR_ID: C1493961
    NAME: Verify Live updates for Hero Module
    DESCRIPTION: This test case verifies Live updates for Hero Module
    PRECONDITIONS: * Competition should be created, set up and enabled in CMS -> Big Competition section
    PRECONDITIONS: * Module with type = 'NEXT_EVENTS' should be created, enabled and set up with Live Events ONLY in CMS
    PRECONDITIONS: * User is logged out
    PRECONDITIONS: * To run steps #11-13 event should have only one marked added in Openbet TI tool
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

    def test_003_go_to_hero_module_next_events_module_for_live_events(self):
        """
        DESCRIPTION: Go to Hero Module (Next Events Module for Live Events)
        EXPECTED: 
        """
        pass

    def test_004_trigger_price_change_for_selections_from_primary_market_for_one_of_event_in_hero_module_in_openbet_ti_tool(self):
        """
        DESCRIPTION: Trigger price change for selection(s) from 'Primary market' for one of event in Hero Module in Openbet TI tool
        EXPECTED: Corresponding 'Price/Odds' button immediately displays new price and for a few seconds it changes its color to:
        EXPECTED: * blue color if the price has decreased
        EXPECTED: * red color if the price has increased
        """
        pass

    def test_005_trigger_suspension_for_selections_for_one_of_the_event_in_hero_module_in_openbet_ti_tool(self):
        """
        DESCRIPTION: Trigger suspension for selection(s) for one of the event in Hero Module in Openbet TI tool
        EXPECTED: * Corresponding 'Price/Odds' button is greyed out immediately
        EXPECTED: * Its not possible to add selection to Betslip / Quick bet
        """
        pass

    def test_006_trigger_unsuspension_for_selections_for_one_of_the_event_in_hero_module_in_openbet_ti_tool(self):
        """
        DESCRIPTION: Trigger unsuspension for selection(s) for one of the event in Hero Module in Openbet TI tool
        EXPECTED: * Corresponding 'Price/Odds' button is active immediately
        EXPECTED: * Its possible to add selection to Betslip / Quick bet
        """
        pass

    def test_007_trigger_suspension_for_primary_market_one_of_the_event_in_hero_module_in_openbet_ti_tool(self):
        """
        DESCRIPTION: Trigger suspension for 'Primary market' one of the event in Hero Module in Openbet TI tool
        EXPECTED: * All 'Price/Odds' buttons within Primary Market are greyed out immediately
        EXPECTED: * Its not possible to add selection from 'Primary Market' to Betslip / Quick bet
        """
        pass

    def test_008_trigger_unsuspension_for_primary_market_one_of_the_event_in_hero_module_in_openbet_ti_tool(self):
        """
        DESCRIPTION: Trigger unsuspension for 'Primary market' one of the event in Hero Module in Openbet TI tool
        EXPECTED: * All 'Price/Odds' buttons within Primary Market become active immediately
        EXPECTED: * Its possible to add selection from 'Primary Market' to Betslip / Quick bet
        """
        pass

    def test_009_trigger_suspension_for_event_in_hero_module_in_openbet_ti_tool(self):
        """
        DESCRIPTION: Trigger suspension for event in Hero Module in Openbet TI tool
        EXPECTED: * All 'Price/Odds' buttons within event are greyed out immediately
        EXPECTED: * Its not possible to add selection from event to Betslip / Quick bet
        """
        pass

    def test_010_trigger_unsuspension_for_event_in_hero_module_in_openbet_ti_tool(self):
        """
        DESCRIPTION: Trigger unsuspension for event in Hero Module in Openbet TI tool
        EXPECTED: * All 'Price/Odds' buttons within event become active immediately
        EXPECTED: * Its possible to add selection from event to Betslip / Quick bet
        """
        pass

    def test_011_trigger_undisplay_all_selection_for_one_of_the_event_in_hero_module_in_openbet_ti_toolset_displayedn_on_selection_level(self):
        """
        DESCRIPTION: Trigger undisplay all selection for one of the event in Hero Module in Openbet TI tool
        DESCRIPTION: (set displayed=N on selection level)
        EXPECTED: * 'displayed=N' attribute is received from Live Serve MS for all selections
        EXPECTED: * Event is disappeared immediately from Hero Module
        """
        pass

    def test_012_trigger_undisplay_for_primary_market_in_hero_module_in_openbet_ti_toolset_displayedn_on_market_level(self):
        """
        DESCRIPTION: Trigger undisplay for Primary Market in Hero Module in Openbet TI tool
        DESCRIPTION: (set displayed=N on market level)
        EXPECTED: * 'displayed=N' attribute is received from Live Serve MS for market level
        EXPECTED: * Event is disappeared immediately from Hero Module
        """
        pass

    def test_013_trigger_undisplay_for_event_in_hero_module_in_openbet_ti_toolset_displayedn_on_event_level(self):
        """
        DESCRIPTION: Trigger undisplay for event in Hero Module in Openbet TI tool
        DESCRIPTION: (set displayed=N on event level)
        EXPECTED: * 'displayed=N' attribute is received from Live Serve MS on the event level
        EXPECTED: * Event is disappeared immediately from Hero Module
        """
        pass

    def test_014_log_in_with_valid_credentials(self):
        """
        DESCRIPTION: Log in with valid credentials
        EXPECTED: User is logged in
        """
        pass

    def test_015_go_to_settings_switch_odds_format_from_fractional_to_decimal_and_repeat_steps_4_13(self):
        """
        DESCRIPTION: Go to Settings, switch Odds format from Fractional to Decimal and repeat steps #4-13
        EXPECTED: 
        """
        pass
