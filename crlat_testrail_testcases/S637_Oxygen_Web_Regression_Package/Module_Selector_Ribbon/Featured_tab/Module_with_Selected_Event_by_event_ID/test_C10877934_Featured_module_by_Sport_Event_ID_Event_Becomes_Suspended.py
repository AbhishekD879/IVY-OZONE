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
class Test_C10877934_Featured_module_by_Sport_Event_ID_Event_Becomes_Suspended(Common):
    """
    TR_ID: C10877934
    NAME: Featured module by <Sport> Event ID: Event Becomes Suspended
    DESCRIPTION: This test case verifies situation when event becomes suspended in Featured Event Module on the 'Featured' tab(mobile/tablet)/ Featured section (desktop)
    DESCRIPTION: Update: Featured modules created by EventID and MarketID should NOT be displayed on Desktop platform for Coral and Ladbrokes brands. This has been done in scope of this bug:
    DESCRIPTION: https://jira.egalacoral.com/browse/BMA-40815
    PRECONDITIONS: 1. Module by <Sport> EventId(not Outright Event with primary market) is created in CMS and it's expanded by default.
    PRECONDITIONS: 2. User is on Homepage > Featured tab
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

    def test_001_navigate_to_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to module from Preconditions
        EXPECTED: * Configured module is displayed on Featured tab and is expanded by default
        EXPECTED: * All 'Price/Odds' buttons are active
        """
        pass

    def test_002_in_ti_find_event_from_created_module_and_suspend_it(self):
        """
        DESCRIPTION: In TI find Event from created module and suspend it
        EXPECTED: Event is suspended
        """
        pass

    def test_003_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Verify outcomes for the event
        EXPECTED: *   All 'Price/Odds' buttons of this event immediately become greyed out (but prices are still displayed)
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

    def test_005_collapse_the_module_from_the_previous_step_and_suspend_the_event_from_the_module(self):
        """
        DESCRIPTION: Collapse the module from the previous step and suspend the Event from the module
        EXPECTED: Event is suspended
        """
        pass

    def test_006_expand_module_from_step_5_with_the_event_and_verify_its_outcomes(self):
        """
        DESCRIPTION: Expand module from step 5 with the event and verify its outcomes
        EXPECTED: *   All 'Price/Odds' buttons of this event immediately become greyed out (but prices are still displayed)
        EXPECTED: *   All 'Price/Odds' buttons are disabled
        """
        pass

    def test_007_collapse_module_one_more_time(self):
        """
        DESCRIPTION: Collapse module one more time
        EXPECTED: 
        """
        pass

    def test_008_un_suspend_the_event_in_ti(self):
        """
        DESCRIPTION: Un-suspend the event in TI
        EXPECTED: Event is active again
        """
        pass

    def test_009_expand_module_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Expand module and verify outcomes for the event
        EXPECTED: *   All 'Price/Odds' buttons of this event immediately become active
        EXPECTED: *   All 'Price/Odds' buttons of this event are not disabled anymore
        """
        pass
