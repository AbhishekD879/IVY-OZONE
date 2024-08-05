import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.lotto
@vtest
class Test_C29593_Lucky_Dip_Buttons(Common):
    """
    TR_ID: C29593
    NAME: Lucky Dip Buttons
    DESCRIPTION: This test case verifies Lucky Dip buttons displaying and functionality
    DESCRIPTION: JIRA tickets:
    DESCRIPTION: BMA-2316 Lottery - Select a lucky dip
    PRECONDITIONS: Load Invictus app
    """
    keep_browser_open = True

    def test_001_go_to_lotto_page_and_verify_lucky_dip_elements_displaying(self):
        """
        DESCRIPTION: Go to Lotto Page and verify Lucky Dip elements displaying
        EXPECTED: *   'Choose your lucky dip' text is displayed under the grid with numbers
        EXPECTED: *   Lucky Dip buttons are displayed under the 'Choose your lucky dip' text
        """
        pass

    def test_002_verify_buttons_labels(self):
        """
        DESCRIPTION: Verify buttons labels
        EXPECTED: The buttons have following labels:
        EXPECTED: *   Lucky 3
        EXPECTED: *   Lucky 4
        EXPECTED: *   Lucky 5
        """
        pass

    def test_003_tap_lucky_3_button(self):
        """
        DESCRIPTION: Tap 'Lucky 3' button
        EXPECTED: *   3 balls are selected and marked at random
        EXPECTED: *   Selected numbers are displayed in ascending mode
        """
        pass

    def test_004_tap_lucky_4_button(self):
        """
        DESCRIPTION: Tap 'Lucky 4' button
        EXPECTED: *   4 balls are selected and marked at random
        EXPECTED: *   Selected numbers are displayed in ascending mode
        """
        pass

    def test_005_tap_lucky_5_button(self):
        """
        DESCRIPTION: Tap 'Lucky 5' button
        EXPECTED: *   5 balls are selected and marked at random
        EXPECTED: *   Selected numbers are displayed in ascending mode
        """
        pass

    def test_006_verify_animation_during_random_selection(self):
        """
        DESCRIPTION: Verify animation during random selection
        EXPECTED: Selected balls are moved a little up and down again
        """
        pass

    def test_007_verify_resitriction_for_number_of_times_to_click_the_lucky_dip_buttons(self):
        """
        DESCRIPTION: Verify resitriction for number of times to click the Lucky Dip buttons
        EXPECTED: It is possible to click the Lucky Dip buttons any number of times which will result in numbers updated respectively
        """
        pass

    def test_008_select_numbers_manually_on_the_gridtap_lucky_x_button(self):
        """
        DESCRIPTION: Select numbers manually on the grid.
        DESCRIPTION: Tap 'Lucky X' button
        EXPECTED: All currently selected balls are unselected and X balls are selected and marked at random
        """
        pass

    def test_009_after_random_numbers_selection_tap_on_the_number_from_the_grid_manually(self):
        """
        DESCRIPTION: After random numbers selection tap on the number from the grid manually
        EXPECTED: All currently selected  random balls are unselected and selected ball is marked on the grid
        """
        pass

    def test_010_tap_lucky_x_buttontap_done_button(self):
        """
        DESCRIPTION: Tap 'Lucky X' button.
        DESCRIPTION: Tap 'Done' button
        EXPECTED: *   Pop-up with numbers grid is closed.
        EXPECTED: *   Selected randomly balls are displayed in the carousel
        """
        pass
