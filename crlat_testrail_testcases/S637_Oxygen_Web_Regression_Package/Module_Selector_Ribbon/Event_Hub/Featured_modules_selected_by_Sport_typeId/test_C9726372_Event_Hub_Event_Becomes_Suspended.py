import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C9726372_Event_Hub_Event_Becomes_Suspended(Common):
    """
    TR_ID: C9726372
    NAME: Event Hub: Event Becomes Suspended
    DESCRIPTION: This test case verifies situation when event/events become suspended on event landing page on the 'Event Hub' tab(mobile/tablet)
    PRECONDITIONS: 1. Event Hub is created in CMS. Modules are created and contain events/selections
    PRECONDITIONS: 2. Oxygen application is loaded on Mobile/Tablet
    PRECONDITIONS: 3. user is on Event Hub tab on Homepage
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: 1. For creating modules use CMS (https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed) ->Sport pages > Event Hub -> Add Sport Module
    PRECONDITIONS: 2. To get into SiteServer use this link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *   Z.ZZ  - current supported version of OpenBet SiteServer
    PRECONDITIONS: *   XXXX - event ID
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3. After suspending <Race> events they disappear from the FE which is by design.
    """
    keep_browser_open = True

    def test_001_expand_some_module_that_contains_an_event_with_priceodds_buttons_that_displaying_prices_or_sp_buttons_for_race_events(self):
        """
        DESCRIPTION: Expand some module that contains an event with 'Price/Odds' buttons that displaying prices (or 'SP' buttons for <Race> events)
        EXPECTED: 
        """
        pass

    def test_002_suspend_the_event_in_ti(self):
        """
        DESCRIPTION: Suspend the event in TI
        EXPECTED: Event is suspended
        """
        pass

    def test_003_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Verify outcomes for the event
        EXPECTED: *   All 'Price/Odds' buttons of this event immediately become greyed out (but prices are still displayed or 'SP' value for <Race> event)
        EXPECTED: *   All 'Price/Odds' buttons are disabled
        """
        pass

    def test_004_un_suspend_the_event_in_ti(self):
        """
        DESCRIPTION: Un-suspend the event in TI
        EXPECTED: *   All 'Price/Odds' buttons of this event immediately become active
        EXPECTED: *   All 'Price/Odds' buttons of this event are not disabled anymore
        """
        pass

    def test_005_collapse_some_module_that_contains_an_event_with_priceodds_buttons_that_displaying_prices_or_sp_buttons_for_race_events(self):
        """
        DESCRIPTION: Collapse some module that contains an event with 'Price/Odds' buttons that displaying prices (or 'SP' buttons for <Race> events)
        EXPECTED: 
        """
        pass

    def test_006_suspend_the_event_in_ti(self):
        """
        DESCRIPTION: Suspend the event in TI
        EXPECTED: Event is suspended
        """
        pass

    def test_007_expand_module_from_step_6_with_the_event_and_verify_its_outcomes(self):
        """
        DESCRIPTION: Expand module from step 6 with the event and verify its outcomes
        EXPECTED: *   All 'Price/Odds' buttons of this event immediately become greyed out (but prices are still displayed or 'SP' value for <Race> event)
        EXPECTED: *   All 'Price/Odds' buttons are disabled
        """
        pass

    def test_008_collapse_module_one_more_time(self):
        """
        DESCRIPTION: Collapse module one more time
        EXPECTED: 
        """
        pass

    def test_009_un_suspend_the_event_in_ti(self):
        """
        DESCRIPTION: Un-suspend the event in TI
        EXPECTED: Event is active again
        """
        pass

    def test_010_expand_module_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Expand module and verify outcomes for the event
        EXPECTED: *   All 'Price/Odds' buttons of this event immediately become active
        EXPECTED: *   All 'Price/Odds' buttons of this event are not disabled anymore
        """
        pass
