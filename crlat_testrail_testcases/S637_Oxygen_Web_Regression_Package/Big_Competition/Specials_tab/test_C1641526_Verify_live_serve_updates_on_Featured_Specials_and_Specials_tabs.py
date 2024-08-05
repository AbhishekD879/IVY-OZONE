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
class Test_C1641526_Verify_live_serve_updates_on_Featured_Specials_and_Specials_tabs(Common):
    """
    TR_ID: C1641526
    NAME: Verify live serve updates on Featured (Specials) and Specials tabs
    DESCRIPTION: This test case verifies changing price for Featured (Specials) and Special Tabs
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: Credentials:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: CMS configs:
    PRECONDITIONS: * 'Featured' tab is created, set up and enabled in CMS  (e.g. 'Big Competitions'-> 'World Cup' -> 'Featured')
    PRECONDITIONS: * 'Featured-Specials' module is created, set up and enabled in CMS -> 'Specials' tab
    PRECONDITIONS: * 'Special' module contains TypeIDs of: e.g. World Cup Specials, Yourcall Specials, Enhanced Multiples Specials
    PRECONDITIONS: To configure Special's market in Back Office TI tick 'Specials' flag on the market's level
    PRECONDITIONS: To verify valid price updates and suspended/unsuspended status see microservice - Development tool> Network> WS> /?EIO=3&transport=websocket > response with type: PRICE
    """
    keep_browser_open = True

    def test_001_load_oxygen_application_navigate_to_the_world_cup__featured_specials_module(self):
        """
        DESCRIPTION: Load Oxygen application. Navigate to the 'World Cup' > 'Featured' (Specials) module
        EXPECTED: 'World Cup' > 'Featured' tab is opened. 'Specials' module is shown
        """
        pass

    def test_002_trigger_price_change_in_back_office_ti_for_specials_market_outcome_for_an_event_with_a_market_that_has_only_one_selection_eg_enhanced_multiples_or_yourcall_specials(self):
        """
        DESCRIPTION: Trigger price change in Back Office TI for '<Special's market>' outcome (for an event with a market that has only one selection e.g. Enhanced Multiples or YourCall Specials)
        EXPECTED: Corresponding 'Price/Odds' button immediately displays new price and for a few seconds it changes its color to:
        EXPECTED: * blue color if price has decreased
        EXPECTED: * red color if price has increased
        """
        pass

    def test_003_go_to_settings_and_change_odds_format_to_decimal_and_repeat_steps_2_3(self):
        """
        DESCRIPTION: Go to Settings and change Odds format to Decimal and repeat steps 2-3
        EXPECTED: All prices are displayed in Decimal format
        """
        pass

    def test_004_suspend_eventmarketselection_an_event_with_a_market_that_has_only_one_selection_eg_enhanced_multiples_or_yourcall_specials_in_backoffice_ti(self):
        """
        DESCRIPTION: Suspend event/market/selection (an event with a market that has only one selection e.g. Enhanced Multiples or YourCall Specials) in Backoffice TI
        EXPECTED: Selection is suspended automatically. Corresponding Price/Odds selection is displayed as greyed out and become disabled
        """
        pass

    def test_005_unsuspend_eventmarketselection_an_event_with_a_market_that_has_only_one_selection_eg_enhanced_multiples_or_yourcall_specials_in_backoffice_tool(self):
        """
        DESCRIPTION: Unsuspend event/market/selection (an event with a market that has only one selection e.g. Enhanced Multiples or YourCall Specials) in Backoffice tool
        EXPECTED: Corresponding Price/Odds selection becomes active
        """
        pass

    def test_006_undisplay_eventmarketselection_an_event_with_a_market_that_has_only_one_selection_eg_enhanced_multiples_or_yourcall_specials_in_backoffice_ti(self):
        """
        DESCRIPTION: Undisplay event/market/selection (an event with a market that has only one selection e.g. Enhanced Multiples or YourCall Specials) in Backoffice TI
        EXPECTED: Selection disappears automatically
        """
        pass

    def test_007_undisplay_eventmarket_of_an_event_with_a_market_with_more_than_one_selections_eg_world_cup_specialsin_backoffice_ti(self):
        """
        DESCRIPTION: Undisplay event/market (of an event with a market with more than one selections e.g. World Cup Specials)in Backoffice TI
        EXPECTED: Event disappears automatically
        """
        pass

    def test_008_navigate_to_the_world_cup___specials_tab(self):
        """
        DESCRIPTION: Navigate to the 'World Cup' -> 'Specials' tab
        EXPECTED: 'Specials' tab is opened
        """
        pass

    def test_009_repeat_step_2_7_for_specials_tab(self):
        """
        DESCRIPTION: Repeat step 2-7 for 'Specials' tab
        EXPECTED: 
        """
        pass
