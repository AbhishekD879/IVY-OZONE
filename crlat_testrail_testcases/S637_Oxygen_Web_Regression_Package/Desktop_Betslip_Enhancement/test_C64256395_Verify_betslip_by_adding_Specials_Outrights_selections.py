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
class Test_C64256395_Verify_betslip_by_adding_Specials_Outrights_selections(Common):
    """
    TR_ID: C64256395
    NAME: Verify betslip by adding Specials & Outrights selections.
    DESCRIPTION: Verify betslip by adding Specials & Outrights selections.
    PRECONDITIONS: * Specials & Outright events should be available in front end
    """
    keep_browser_open = True

    def test_001_navigate_to_any_sport_eg_football__gt_specials_tab(self):
        """
        DESCRIPTION: Navigate to any sport e.g., Football -&gt; Specials tab
        EXPECTED: * Specials tab is opened
        """
        pass

    def test_002_add_any_4_selections_from_specials_events(self):
        """
        DESCRIPTION: Add any 4 selections from specials events
        EXPECTED: * 4 Selections are added to betslip but won't see multiples here
        EXPECTED: * Betslip size is going to increase dynamically without scrollbar irrespective of lengthy selection names.
        """
        pass

    def test_003_add_fifth_selection_from_specials_events(self):
        """
        DESCRIPTION: Add fifth selection from specials events
        EXPECTED: * Fifth selection is added to betslip  but won't see multiples here.
        EXPECTED: * Scroll bar shows up in the FE with the previous selections betslip size.
        """
        pass

    def test_004_remove_all_selections_from_betslip__navigate_to_any_sport_eg_football__gt__outrights_tab(self):
        """
        DESCRIPTION: Remove all selections from betslip & Navigate to any sport e.g., Football -&gt;  Outrights tab
        EXPECTED: * Betslip becomes empty
        EXPECTED: * Outrights tab is opened
        """
        pass

    def test_005_repeat_step_2_step_3_for_outright_events(self):
        """
        DESCRIPTION: Repeat step-2, step-3 for outright events
        EXPECTED: 
        """
        pass

    def test_006_again_clear_betslip(self):
        """
        DESCRIPTION: Again clear betslip
        EXPECTED: * Betslip becomes empty
        """
        pass

    def test_007_repeat_step_2__step_3_for_combination_of_specials__outrights_events(self):
        """
        DESCRIPTION: Repeat step-2 & step-3 for combination of specials & outrights events
        EXPECTED: 
        """
        pass
