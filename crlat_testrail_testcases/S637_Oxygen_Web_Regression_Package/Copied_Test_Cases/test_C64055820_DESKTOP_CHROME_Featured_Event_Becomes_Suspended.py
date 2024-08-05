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
class Test_C64055820_DESKTOP_CHROME_Featured_Event_Becomes_Suspended(Common):
    """
    TR_ID: C64055820
    NAME: [DESKTOP CHROME] Featured Event Becomes Suspended
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001___________in_ti_create_football_event_and_featured_module(self):
        """
        DESCRIPTION: *          In TI, create football event and featured module
        EXPECTED: *          Football event and featured module were created
        """
        pass

    def test_002___________go_to_the_featured_tab_in_module_ribbon_tabs(self):
        """
        DESCRIPTION: *          Go to the 'Featured' tab in Module Ribbon Tabs
        EXPECTED: *          **For mobile/tablet:**
        EXPECTED: *          'Featured' tab is selected by default
        EXPECTED: *          **For desktop:**
        EXPECTED: *          'Featured' section is displayed
        """
        pass

    def test_003___________expand_some_module_that_contains_an_event_with_priceodds_buttons_that_displaying_prices__________or_sp_buttons_for_race_events(self):
        """
        DESCRIPTION: *          Expand some module that contains an event with 'Price/Odds' buttons that displaying prices
        DESCRIPTION: *          (or 'SP' buttons for <Race> events)
        EXPECTED: *          Module is expanded
        """
        pass

    def test_004___________suspend_the_event_in_ti(self):
        """
        DESCRIPTION: *          Suspend the event in TI
        EXPECTED: *          Event is suspended
        """
        pass

    def test_005___________verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: *          Verify outcomes for the event
        EXPECTED: *          * All 'Price/Odds' buttons of this event immediately become greyed out (prices are still displayed)
        EXPECTED: *          * All 'Price/Odds' buttons are disabled
        """
        pass

    def test_006___________un_suspend_the_event_in_ti(self):
        """
        DESCRIPTION: *          Un-suspend the event in TI
        EXPECTED: *          * All 'Price/Odds' buttons of this event immediately become active
        EXPECTED: *          * All 'Price/Odds' buttons of this event are not disabled anymore
        """
        pass

    def test_007___________collapse_some_module_that_contains_an_event_with_priceodds_buttons_that_displaying_prices__________or_sp_buttons_for_race_events(self):
        """
        DESCRIPTION: *          Collapse some module that contains an event with 'Price/Odds' buttons that displaying prices
        DESCRIPTION: *          (or 'SP' buttons for <Race> events)
        EXPECTED: *          Module is collapsed
        """
        pass

    def test_008___________suspend_the_event_in_ti(self):
        """
        DESCRIPTION: *          Suspend the event in TI
        EXPECTED: *          Event is suspended
        """
        pass

    def test_009___________expand_module_from_step_6_with_the_event_and_verify_its_outcomes(self):
        """
        DESCRIPTION: *          Expand module from step 6 with the event and verify its outcomes
        EXPECTED: *          * All 'Price/Odds' buttons of this event immediately become greyed out (prices are still displayed)
        EXPECTED: *          * All 'Price/Odds' buttons are disabled
        """
        pass

    def test_010___________collapse_module_one_more_time(self):
        """
        DESCRIPTION: *          Collapse module one more time
        EXPECTED: *          Module is collapsed
        """
        pass

    def test_011___________un_suspend_the_event_in_ti(self):
        """
        DESCRIPTION: *          Un-suspend the event in TI
        EXPECTED: *          Event is active again
        """
        pass

    def test_012___________expand_module_and_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: *          Expand module and verify outcomes for the event
        EXPECTED: *          * All 'Price/Odds' buttons of this event immediately become active
        EXPECTED: *          * All 'Price/Odds' buttons of this event are not disabled anymore
        """
        pass
