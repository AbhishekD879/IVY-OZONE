import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C9726373_Event_Hub_Primary_Market_Becomes_Suspended(Common):
    """
    TR_ID: C9726373
    NAME: Event Hub: Primary Market Becomes Suspended
    DESCRIPTION: This test case verifies situation when market/markets become suspended on event landing page on the 'Event Hub' tab(mobile/tablet)
    PRECONDITIONS: 1. Modules are created and contain events/selections
    PRECONDITIONS: 2. Oxygen application is loaded on Mobile/Tablet or Desktop
    PRECONDITIONS: 3. User is on Event hub tab
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: 1. For creating modules use CMS (https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed) -> Sport Pages > Event Hub -> Event Hub Edit page > Add sport module
    PRECONDITIONS: 2. To get into SiteServer use this link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *   Z.ZZ  - current supported version of OpenBet SiteServer
    PRECONDITIONS: *   XXXX - event ID
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_expand_some_module_that_contains_an_event_with_priceodds_buttons_that_displaying_prices_or_sp_buttons_for_race_events(self):
        """
        DESCRIPTION: Expand some module that contains an event with 'Price/Odds' buttons that displaying prices (or 'SP' buttons for <Race> events)
        EXPECTED: 
        """
        pass

    def test_002_trigger_the_following_situation_in_ti_for_this_eventmarketstatuscodesfor_primary_market_or_win_or_each_way_for_races_market_type(self):
        """
        DESCRIPTION: Trigger the following situation in TI for this event:
        DESCRIPTION: **marketStatusCode="S"** for '<Primary market>' (or 'Win Or Each Way' for <Races>) market type
        EXPECTED: Event is suspended
        """
        pass

    def test_003_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Verify outcomes for the event
        EXPECTED: * All 'Price/Odds' buttons of this event immediately become greyed out (but prices are still displayed or 'SP' value for <Race> event)
        EXPECTED: * All 'Price/Odds' buttons are disabled
        """
        pass

    def test_004_change_attribute_for_this_event_in_timarketstatuscodeafor_primary_market_or_win_or_each_way_for_racesmarket_type(self):
        """
        DESCRIPTION: Change attribute for this event in TI:
        DESCRIPTION: **marketStatusCode="A"** for '<Primary market>'  (or 'Win Or Each Way' for <Races>) market type
        EXPECTED: Event is active
        """
        pass

    def test_005_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Verify outcomes for the event
        EXPECTED: * All 'Price/Odds' buttons of this event immediately become active
        EXPECTED: * All 'Price/Odds' buttons of this event are not disabled anymore
        """
        pass

    def test_006_collapse_some_module_that_contains_an_event_with_priceodds_buttons_that_displaying_prices_or_sp_buttons_for_race_events(self):
        """
        DESCRIPTION: Collapse some module that contains an event with 'Price/Odds' buttons that displaying prices (or 'SP' buttons for <Race> events)
        EXPECTED: 
        """
        pass

    def test_007_change_attribute_in_ti_for_this_eventmarketstatuscodesfor_primary_market_or_win_or_each_way_for_racesmarket_type(self):
        """
        DESCRIPTION: Change attribute in TI for this event:
        DESCRIPTION: **marketStatusCode="S"** for '<Primary market>'  (or 'Win Or Each Way' for <Races>) market type
        EXPECTED: 
        """
        pass

    def test_008_expand_module_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Expand module and verify outcomes for the event
        EXPECTED: * All 'Price/Odds' buttons of this event immediately become greyed out (but prices are still displayed or 'SP' value for <Race> event)
        EXPECTED: * All 'Price/Odds' buttons are disabled
        """
        pass

    def test_009_collapse_module_one_more_time(self):
        """
        DESCRIPTION: Collapse module one more time
        EXPECTED: 
        """
        pass

    def test_010_change_attribute_in_ti_for_this_eventmarketstatuscodeafor_primary_market_or_win_or_each_way_for_racesmarket_type(self):
        """
        DESCRIPTION: Change attribute in TI for this event:
        DESCRIPTION: **marketStatusCode="A"** for '<Primary market>'  (or 'Win Or Each Way' for <Races>) market type
        EXPECTED: 
        """
        pass

    def test_011_expand_module_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Expand module and verify outcomes for the event
        EXPECTED: * All 'Price/Odds' buttons of this event immediately become active
        EXPECTED: * All 'Price/Odds' buttons of this event are not disabled anymore
        """
        pass
