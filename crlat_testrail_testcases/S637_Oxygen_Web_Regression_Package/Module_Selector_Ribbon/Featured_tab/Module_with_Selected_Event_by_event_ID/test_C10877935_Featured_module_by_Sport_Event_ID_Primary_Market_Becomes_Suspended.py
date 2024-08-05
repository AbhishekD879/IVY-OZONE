import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C10877935_Featured_module_by_Sport_Event_ID_Primary_Market_Becomes_Suspended(Common):
    """
    TR_ID: C10877935
    NAME: Featured module by <Sport> Event ID: Primary Market Becomes Suspended
    DESCRIPTION: This test case verifies situation when the market becomes suspended in Featured module by <Sport> Event ID
    PRECONDITIONS: 1. Module by <Sport> EventId(not Outright Event with primary market) is created in CMS and is expanded by default.
    PRECONDITIONS: 2. User is on Homepage > Featured tab
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: 1. List of primary markets can be found here: https://jira.egalacoral.com/browse/BMA-39433
    PRECONDITIONS: 1. For creating modules use CMS (https://coral-cms-<endpoint>.symphony-solutions.eu) -> 'Featured Tab Modules' -> 'Create Featured Tab Module'
    PRECONDITIONS: 2. To get into SiteServer use this link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *   Z.ZZ  - current supported version of OpenBet SiteServer
    PRECONDITIONS: *   XXXX - event ID
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_navigate_to_the_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to the module from Preconditions
        EXPECTED: 
        """
        pass

    def test_002_trigger_the_following_situation_in_ti_for_this_eventmarketstatuscodesfor_primary_market_market_type(self):
        """
        DESCRIPTION: Trigger the following situation in TI for this event:
        DESCRIPTION: **marketStatusCode="S"** for '<Primary market>' market type
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

    def test_004_change_attribute_for_this_event_in_timarketstatuscodeafor_primary_marketmarket_type(self):
        """
        DESCRIPTION: Change attribute for this event in TI:
        DESCRIPTION: **marketStatusCode="A"** for '<Primary market>' market type
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

    def test_006_collapse_the_module_from_the_previous_step(self):
        """
        DESCRIPTION: Collapse the module from the previous step
        EXPECTED: 
        """
        pass

    def test_007_change_attribute_in_ti_for_this_eventmarketstatuscodesfor_primary_marketmarket_type(self):
        """
        DESCRIPTION: Change attribute in TI for this event:
        DESCRIPTION: **marketStatusCode="S"** for '<Primary market>' market type
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

    def test_010_change_attribute_in_ti_for_this_eventmarketstatuscodeafor_primary_market_market_type(self):
        """
        DESCRIPTION: Change attribute in TI for this event:
        DESCRIPTION: **marketStatusCode="A"** for '<Primary market>' market type
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
