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
class Test_C10877936_Featured_module_by_Sport_Event_ID_Outcome_Becomes_Suspended(Common):
    """
    TR_ID: C10877936
    NAME: Featured module by <Sport> Event ID: Outcome Becomes Suspended
    DESCRIPTION: This test case verifies situation when outcome/outcomes become suspended on Home page on the 'Featured' tab(mobile/tablet)/ Featured section (desktop)
    PRECONDITIONS: 1. Module by <Sport> EventId(not Outright Event with primary market) is created in CMS and is expanded by default.
    PRECONDITIONS: 2. User is on Homepage > Featured tab
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: 1) For creating modules use CMS (https://coral-cms-<endpoint>.symphony-solutions.eu) -> 'Featured Tab Modules' -> 'Create Featured Tab Module'
    PRECONDITIONS: 2) To get into SiteServer use this link:
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

    def test_002_trigger_the_following_situation_in_ti_for_this_eventoutcomestatuscodesfor_one_of_the_outcomes_of_the_market(self):
        """
        DESCRIPTION: Trigger the following situation in TI for this event:
        DESCRIPTION: **outcomeStatusCode="S"** for one of the outcomes of the market
        EXPECTED: 
        """
        pass

    def test_003_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Verify outcomes for the event
        EXPECTED: *   Only one Price/Odds button is disabled immediately
        EXPECTED: *   The rest Price/Odds buttons of the same market are not changed
        """
        pass

    def test_004_change_attribute_for_this_eventoutcomestatuscodeafor_the_same_outcome(self):
        """
        DESCRIPTION: Change attribute for this event:
        DESCRIPTION: **outcomeStatusCode="A"** for the same outcome
        EXPECTED: *   Price/Odds button of this outcome is not disabled anymore
        EXPECTED: *   Price/Odds button becomes active
        """
        pass

    def test_005_collapse_module(self):
        """
        DESCRIPTION: Collapse module
        EXPECTED: 
        """
        pass

    def test_006_trigger_the_following_situation_in_ti_for_this_eventoutcomestatuscodesfor_one_of_the_outcomes_of_the_market(self):
        """
        DESCRIPTION: Trigger the following situation in TI for this event:
        DESCRIPTION: **outcomeStatusCode="S"** for one of the outcomes of the market
        EXPECTED: 
        """
        pass

    def test_007_expand_module_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Expand module and verify outcomes for the event
        EXPECTED: *   Only one Price/Odds button is disabled immediately
        EXPECTED: *   The rest Price/Odds buttons of the same market are not changed
        """
        pass

    def test_008_collapse_module(self):
        """
        DESCRIPTION: Collapse module
        EXPECTED: 
        """
        pass

    def test_009_change_attribute_for_this_eventoutcomestatuscodeafor_the_same_outcome(self):
        """
        DESCRIPTION: Change attribute for this event:
        DESCRIPTION: **outcomeStatusCode="A"** for the same outcome
        EXPECTED: 
        """
        pass

    def test_010_expand_module_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Expand module and verify outcomes for the event
        EXPECTED: *   Price/Odds button of this outcome is not disabled anymore
        EXPECTED: *   Price/Odds button becomes active
        """
        pass
