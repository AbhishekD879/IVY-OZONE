import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C64256391_Verify_betslip_by_adding_removing_the_selections_from_same_event_different_events(Common):
    """
    TR_ID: C64256391
    NAME: Verify betslip by adding & removing the selections from same event & different events.
    DESCRIPTION: Verify betslip by adding & removing the selections from same event & different events.
    PRECONDITIONS: At least 5 preplay events should be available in Front End.
    """
    keep_browser_open = True

    def test_001_load_the_application__navigate_to_any_sport_eg_football_hr(self):
        """
        DESCRIPTION: Load the application & navigate to any sport e.g., Football, HR
        EXPECTED: * Front End application is loaded.
        EXPECTED: * SLP is displayed.
        """
        pass

    def test_002_click_on_any_event_in_slp(self):
        """
        DESCRIPTION: Click on any event in SLP
        EXPECTED: * Navigated to EDP page & able to see multiple markets
        """
        pass

    def test_003_add_five_selections_to_the_betslip_from_same_event(self):
        """
        DESCRIPTION: Add five selections to the betslip from same event
        EXPECTED: * Five selections are added to betslip.
        EXPECTED: * Scroll bar shows up in the FE with the previous selections betslip size.
        """
        pass

    def test_004_remove_one_selection_from_the_betslip(self):
        """
        DESCRIPTION: Remove one selection from the betslip
        EXPECTED: * one selection is removed from betslip
        EXPECTED: * Scroll bar disappears from the betslip
        EXPECTED: * Remaining four selections are displayed without scrollbar
        """
        pass

    def test_005_repeat_step_4_until_betslip_contains_only_one_selection(self):
        """
        DESCRIPTION: Repeat step-4 until betslip contains only one selection
        EXPECTED: 
        """
        pass

    def test_006_again_add_five_selections_to_the_betslip__click_on_remove_all_option_in_betslip(self):
        """
        DESCRIPTION: Again add five selections to the betslip & click on 'Remove All' option in betslip
        EXPECTED: * Five selections are added to betslip
        EXPECTED: * Betslip becomes empty after clicking on 'Remove All'
        EXPECTED: * Betslip displays as default
        """
        pass

    def test_007_add_five_selections_to_the_betslip_from_different_events(self):
        """
        DESCRIPTION: Add five selections to the betslip from different events
        EXPECTED: * Five selections are added to betslip.
        EXPECTED: * Scroll bar is displayed with the previous selections betslip size.* Scroll bar introduces here with the previous selections betslip size.
        """
        pass

    def test_008_remove_one_selection_from_the_betslip(self):
        """
        DESCRIPTION: Remove one selection from the betslip
        EXPECTED: * one selection is removed from betslip
        EXPECTED: * Scroll bar disappears from the betslip
        EXPECTED: * Remaining four selections are displayed without scrollbar along with multiples
        """
        pass

    def test_009_repeat_step_4_until_betslip_contains_only_one_selection(self):
        """
        DESCRIPTION: Repeat step-4 until betslip contains only one selection
        EXPECTED: 
        """
        pass

    def test_010_again_add_five_selections_to_the_betslip__click_on_remove_all_option_in_betslip(self):
        """
        DESCRIPTION: Again add five selections to the betslip & click on 'Remove All' option in betslip
        EXPECTED: * Five selections are added to betslip
        EXPECTED: * Betslip becomes empty after clicking on 'Remove All'
        EXPECTED: * Betslip displays as default
        """
        pass
