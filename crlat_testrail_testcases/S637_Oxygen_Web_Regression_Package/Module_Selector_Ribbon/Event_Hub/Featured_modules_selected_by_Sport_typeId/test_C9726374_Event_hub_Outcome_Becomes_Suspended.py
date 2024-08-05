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
class Test_C9726374_Event_hub_Outcome_Becomes_Suspended(Common):
    """
    TR_ID: C9726374
    NAME: Event hub: Outcome Becomes Suspended
    DESCRIPTION: This test case verifies situation when outcome/outcomes become suspended on Home page on the Event hub tab(mobile/tablet)
    PRECONDITIONS: 1. Event Hub is created on CMS. Modules are created and contain events/selections
    PRECONDITIONS: 2. Oxygen application is loaded on Mobile/Tablet
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

    def test_001_expand_some_module_that_contains_an_event_with_priceodds_buttons_that_displaying_prices_or_sp_buttons_for_ltracegt_events(self):
        """
        DESCRIPTION: Expand some module that contains an event with 'Price/Odds' buttons that displaying prices (or 'SP' buttons for &lt;Race&gt; events)
        EXPECTED: 
        """
        pass

    def test_002_trigger_the_following_situation_in_ti_for_this_eventoutcomestatuscodesfor_one_of_the_outcomes_of_ltprimary_marketgt_or_win_or_each_way_for_ltracesgtmarket_type(self):
        """
        DESCRIPTION: Trigger the following situation in TI for this event:
        DESCRIPTION: **outcomeStatusCode="S"** for one of the outcomes of '&lt;Primary market&gt;' (or 'Win Or Each Way' for &lt;Races&gt;) market type
        EXPECTED: 
        """
        pass

    def test_003_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Verify outcomes for the event
        EXPECTED: *   Only one Price/Odds button is disabled immediately (but the price is still displayed or 'SP' value for &lt;Race&gt; event)
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

    def test_005_find_another_event_with_priceodds_buttons_that_displaying_prices_or_sp_buttons_for_ltracegt_events(self):
        """
        DESCRIPTION: Find another event with 'Price/Odds' buttons that displaying prices (or 'SP' buttons for &lt;Race&gt; events)
        EXPECTED: 
        """
        pass

    def test_006_trigger_the_following_situation_for_this_eventoutcomestatuscodesfor_one_of_the_outcomes_of_ltprimary_marketgt_or_win_or_each_way_for_ltracesgtmarket_type(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: **outcomeStatusCode="S"** for one of the outcomes of '&lt;Primary market&gt;' (or 'Win Or Each Way' for &lt;Races&gt;) market type
        EXPECTED: 
        """
        pass

    def test_007_expand_module_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Expand module and verify outcomes for the event
        EXPECTED: *   Only one Price/Odds button is disabled immediately (but the price is still displayed or 'SP' value for &lt;Race&gt; event)
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
