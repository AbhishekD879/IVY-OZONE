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
class Test_C29384_Featured_Primary_Market_Becomes_Suspended(Common):
    """
    TR_ID: C29384
    NAME: Featured: Primary Market Becomes Suspended
    DESCRIPTION: This test case verifies situation when market/markets become suspended on event landing page on the 'Featured' tab(mobile/tablet)/ Featured section (desktop)
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

    def test_002_expand_some_module_that_contains_an_event_with_priceodds_buttons_that_displaying_prices_or_sp_buttons_for_ltracegt_events(self):
        """
        DESCRIPTION: Expand some module that contains an event with 'Price/Odds' buttons that displaying prices (or 'SP' buttons for &lt;Race&gt; events)
        EXPECTED: 
        """
        pass

    def test_003_trigger_the_following_situation_in_ti_for_this_eventmarketstatuscodesfor_ltprimary_marketgt_or_win_or_each_way_for_ltracesgt_market_type(self):
        """
        DESCRIPTION: Trigger the following situation in TI for this event:
        DESCRIPTION: **marketStatusCode="S"** for '&lt;Primary market&gt;' (or 'Win Or Each Way' for &lt;Races&gt;) market type
        EXPECTED: Event is suspended
        """
        pass

    def test_004_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Verify outcomes for the event
        EXPECTED: * All 'Price/Odds' buttons of this event immediately become greyed out (but prices are still displayed or 'SP' value for &lt;Race&gt; event)
        EXPECTED: * All 'Price/Odds' buttons are disabled
        """
        pass

    def test_005_change_attribute_for_this_event_in_timarketstatuscodeafor_ltprimary_marketgt_or_win_or_each_way_for_ltracesgtmarket_type(self):
        """
        DESCRIPTION: Change attribute for this event in TI:
        DESCRIPTION: **marketStatusCode="A"** for '&lt;Primary market&gt;'  (or 'Win Or Each Way' for &lt;Races&gt;) market type
        EXPECTED: Event is active
        """
        pass

    def test_006_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Verify outcomes for the event
        EXPECTED: * All 'Price/Odds' buttons of this event immediately become active
        EXPECTED: * All 'Price/Odds' buttons of this event are not disabled anymore
        """
        pass

    def test_007_collapse_some_module_that_contains_an_event_with_priceodds_buttons_that_displaying_prices_or_sp_buttons_for_ltracegt_events(self):
        """
        DESCRIPTION: Collapse some module that contains an event with 'Price/Odds' buttons that displaying prices (or 'SP' buttons for &lt;Race&gt; events)
        EXPECTED: 
        """
        pass

    def test_008_change_attribute_in_ti_for_this_eventmarketstatuscodesfor_ltprimary_marketgt_or_win_or_each_way_for_ltracesgtmarket_type(self):
        """
        DESCRIPTION: Change attribute in TI for this event:
        DESCRIPTION: **marketStatusCode="S"** for '&lt;Primary market&gt;'  (or 'Win Or Each Way' for &lt;Races&gt;) market type
        EXPECTED: 
        """
        pass

    def test_009_expand_module_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Expand module and verify outcomes for the event
        EXPECTED: * All 'Price/Odds' buttons of this event immediately become greyed out (but prices are still displayed or 'SP' value for &lt;Race&gt; event)
        EXPECTED: * All 'Price/Odds' buttons are disabled
        """
        pass

    def test_010_collapse_module_one_more_time(self):
        """
        DESCRIPTION: Collapse module one more time
        EXPECTED: 
        """
        pass

    def test_011_change_attribute_in_ti_for_this_eventmarketstatuscodeafor_ltprimary_marketgt_or_win_or_each_way_for_ltracesgtmarket_type(self):
        """
        DESCRIPTION: Change attribute in TI for this event:
        DESCRIPTION: **marketStatusCode="A"** for '&lt;Primary market&gt;'  (or 'Win Or Each Way' for &lt;Races&gt;) market type
        EXPECTED: 
        """
        pass

    def test_012_expand_module_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Expand module and verify outcomes for the event
        EXPECTED: * All 'Price/Odds' buttons of this event immediately become active
        EXPECTED: * All 'Price/Odds' buttons of this event are not disabled anymore
        """
        pass
