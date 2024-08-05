import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C29383_Featured_Event_Becomes_Suspended(Common):
    """
    TR_ID: C29383
    NAME: Featured: Event Becomes Suspended
    DESCRIPTION: This test case verifies situation when event/events become suspended on event landing page on the 'Featured' tab(mobile/tablet)/ Featured section (desktop)
    DESCRIPTION: Autotest - [C2591580]
    PRECONDITIONS: 1. Modules are created and contain events/selections
    PRECONDITIONS: 2. Oxygen application is loaded on Mobile/Tablet or Desktop
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: 1. For creating modules use CMS (https://coral-cms-<endpoint>.symphony-solutions.eu) -> 'Featured Tab Modules' -> 'Create Featured Tab Module'
    PRECONDITIONS: 2. To get into SiteServer use this link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *   Z.ZZ  - current supported version of OpenBet SiteServer
    PRECONDITIONS: *   XXXX - event ID
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_go_to_the_featured_tab_in_module_ribbon_tabs(self):
        """
        DESCRIPTION: Go to the 'Featured' tab in Module Ribbon Tabs
        EXPECTED: **For mobile/tablet:**
        EXPECTED: 'Featured' tab is selected by default
        EXPECTED: **For desktop:**
        EXPECTED: Module Ribbon Tabs are transformed into sections, displayed in the following order:
        EXPECTED: 1) Enhanced multiples carousel
        EXPECTED: 2) In-Play & Live Stream
        EXPECTED: 3) Next Races Carousel
        EXPECTED: 4) Featured area
        """
        pass

    def test_002_expand_some_module_that_contains_an_event_with_priceodds_buttons_that_displaying_prices_or_sp_buttons_for_race_events(self):
        """
        DESCRIPTION: Expand some module that contains an event with 'Price/Odds' buttons that displaying prices (or 'SP' buttons for <Race> events)
        EXPECTED: 
        """
        pass

    def test_003_suspend_the_event_in_ti(self):
        """
        DESCRIPTION: Suspend the event in TI
        EXPECTED: Event is suspended
        """
        pass

    def test_004_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Verify outcomes for the event
        EXPECTED: *   All 'Price/Odds' buttons of this event immediately become greyed out (but prices are still displayed or 'SP' value for <Race> event)
        EXPECTED: *   All 'Price/Odds' buttons are disabled
        """
        pass

    def test_005_un_suspend_the_event_in_ti(self):
        """
        DESCRIPTION: Un-suspend the event in TI
        EXPECTED: *   All 'Price/Odds' buttons of this event immediately become active
        EXPECTED: *   All 'Price/Odds' buttons of this event are not disabled anymore
        """
        pass

    def test_006_collapse_some_module_that_contains_an_event_with_priceodds_buttons_that_displaying_prices_or_sp_buttons_for_race_events(self):
        """
        DESCRIPTION: Collapse some module that contains an event with 'Price/Odds' buttons that displaying prices (or 'SP' buttons for <Race> events)
        EXPECTED: 
        """
        pass

    def test_007_suspend_the_event_in_ti(self):
        """
        DESCRIPTION: Suspend the event in TI
        EXPECTED: Event is suspended
        """
        pass

    def test_008_expand_module_from_step_6_with_the_event_and_verify_its_outcomes(self):
        """
        DESCRIPTION: Expand module from step 6 with the event and verify its outcomes
        EXPECTED: *   All 'Price/Odds' buttons of this event immediately become greyed out (but prices are still displayed or 'SP' value for <Race> event)
        EXPECTED: *   All 'Price/Odds' buttons are disabled
        """
        pass

    def test_009_collapse_module_one_more_time(self):
        """
        DESCRIPTION: Collapse module one more time
        EXPECTED: 
        """
        pass

    def test_010_un_suspend_the_event_in_ti(self):
        """
        DESCRIPTION: Un-suspend the event in TI
        EXPECTED: Event is active again
        """
        pass

    def test_011_expand_module_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Expand module and verify outcomes for the event
        EXPECTED: *   All 'Price/Odds' buttons of this event immediately become active
        EXPECTED: *   All 'Price/Odds' buttons of this event are not disabled anymore
        """
        pass
