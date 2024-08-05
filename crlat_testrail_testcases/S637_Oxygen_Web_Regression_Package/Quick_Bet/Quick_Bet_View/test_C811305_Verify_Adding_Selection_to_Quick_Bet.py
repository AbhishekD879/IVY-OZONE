import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.quick_bet
@vtest
class Test_C811305_Verify_Adding_Selection_to_Quick_Bet(Common):
    """
    TR_ID: C811305
    NAME: Verify Adding Selection to Quick Bet
    DESCRIPTION: This test case verifies adding Selection to Quick Bet
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * Quick Bet functionality is available for Mobile ONLY
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_one_sportrace_selection(self):
        """
        DESCRIPTION: Tap one <Sport>/<Race> selection
        EXPECTED: * Selected price/odds are highlighted in green
        EXPECTED: * Betslip counter does NOT increase by one
        """
        pass

    def test_003_verify_quick_bet(self):
        """
        DESCRIPTION: Verify Quick Bet
        EXPECTED: * Quick Bet appears at the bottom of the page
        EXPECTED: * All selection details are displayed within Quick Bet
        """
        pass

    def test_004_tap_x_button(self):
        """
        DESCRIPTION: Tap X button
        EXPECTED: * Quick Bet is not displayed anymore
        EXPECTED: After release of BMA-54870 AR will be:
        EXPECTED: * Quick Bet is closed automatically
        EXPECTED: * Selection is added to Betslip
        EXPECTED: * Betslip counter is increased by 1
        EXPECTED: * Selection is the same as was added by Quick bet
        """
        pass

    def test_005_go_to_race_landing_page_and_tap_selection_from_next_module(self):
        """
        DESCRIPTION: Go to <Race> Landing page and tap selection from Next module
        EXPECTED: * Quick Bet appears at the bottom of the page automatically
        EXPECTED: * Slide-out Betslip is NOT opened
        EXPECTED: * Betslip counter does NOT increase by one
        """
        pass

    def test_006_go_to_module_selector_ribbon_on_homepage_select_next_races_tab_and_repeat_step_7(self):
        """
        DESCRIPTION: Go to Module Selector Ribbon on Homepage, select 'Next Races' tab and repeat step #7
        EXPECTED: 
        """
        pass

    def test_007_log_in_and_repeat_steps_2_6(self):
        """
        DESCRIPTION: Log in and repeat steps #2-6
        EXPECTED: 
        """
        pass
