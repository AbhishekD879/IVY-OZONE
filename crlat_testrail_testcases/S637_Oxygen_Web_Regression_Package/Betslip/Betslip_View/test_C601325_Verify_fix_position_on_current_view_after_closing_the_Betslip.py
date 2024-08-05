import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C601325_Verify_fix_position_on_current_view_after_closing_the_Betslip(Common):
    """
    TR_ID: C601325
    NAME: Verify fix position on current view after closing the Betslip
    DESCRIPTION: This test case verifies fix position on current view after closing the Betslip
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_scroll_page_down_and_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Scroll page down and add selection to the Betslip
        EXPECTED: Selection is displayed as selected
        """
        pass

    def test_003_open_the_betslip(self):
        """
        DESCRIPTION: Open the Betslip
        EXPECTED: * Betslip is opened
        EXPECTED: * Added selection is displayed within the Betslip
        """
        pass

    def test_004_tap_on_the_background_behind_the_opened_betslip(self):
        """
        DESCRIPTION: Tap on the background behind the opened Betslip
        EXPECTED: * Betslip is closed
        EXPECTED: * User is back to the current position of page that was chosen in step 2
        EXPECTED: * User is not redirected to the top of the page
        """
        pass

    def test_005_open_the_betslip(self):
        """
        DESCRIPTION: Open the Betslip
        EXPECTED: * Betslip is opened
        EXPECTED: * Added selection is displayed within the Betslip
        """
        pass

    def test_006_tap_on_close_x_button_for_closing_the_betslip(self):
        """
        DESCRIPTION: Tap on 'Close [X]' button for closing the Betslip
        EXPECTED: * Betslip is closed
        EXPECTED: * User is back to the current position of page that was chosen in step 2
        EXPECTED: * User is not redirected to the top of the pagee
        """
        pass

    def test_007_open_the_betslip(self):
        """
        DESCRIPTION: Open the Betslip
        EXPECTED: * Betslip is opened
        EXPECTED: * Added selection is displayed within the Betslip
        """
        pass

    def test_008_tap_on_confirm_clear_betslip_button_for_clearing_the_betslip_content(self):
        """
        DESCRIPTION: Tap on 'Confirm Clear Betslip' button for clearing the Betslip content
        EXPECTED: * All selections are removed from the Betslip
        EXPECTED: * Betslip is closed automatically
        EXPECTED: * User is back to the current position of page that was chosen in step 2
        EXPECTED: * User is not redirected to the top of the page
        """
        pass

    def test_009_repeat_step_2_3(self):
        """
        DESCRIPTION: Repeat step 2-3
        EXPECTED: * Betslip is opened
        EXPECTED: * Added selection is displayed within the Betslip
        """
        pass

    def test_010_trigger_bet_placement(self):
        """
        DESCRIPTION: Trigger bet placement
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet receipt is displayed
        """
        pass

    def test_011_tap_on_done_button_on_bet_receipt(self):
        """
        DESCRIPTION: Tap on 'Done' button on Bet Receipt
        EXPECTED: * Betslip is closed automatically
        EXPECTED: * User is back to the current position of page that was chosen in step 2
        EXPECTED: * User is not redirected to the top of the page
        """
        pass

    def test_012_repeat_steps_2_11_but_add_several_selections_to_the_betslip(self):
        """
        DESCRIPTION: Repeat steps 2-11 but add several selections to the Betslip
        EXPECTED: * User is back to the current position of page that was chosen in step 2
        EXPECTED: * User is not redirected to the top of the page
        """
        pass

    def test_013_repeat_steps_2_12_on_different_pages_of_the_application(self):
        """
        DESCRIPTION: Repeat steps 2-12 on different pages of the application
        EXPECTED: * User is back to the current position of page that was chosen in step 2
        EXPECTED: * User is not redirected to the top of the page
        """
        pass
