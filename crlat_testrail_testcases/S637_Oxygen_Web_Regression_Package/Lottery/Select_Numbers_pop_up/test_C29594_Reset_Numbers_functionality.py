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
class Test_C29594_Reset_Numbers_functionality(Common):
    """
    TR_ID: C29594
    NAME: Reset Numbers functionality
    DESCRIPTION: JIRA Tickets:
    DESCRIPTION: BMA 7579 Lottery - Select numbers (as popup)
    PRECONDITIONS: Launch Invictus application and go to the Lotto section
    """
    keep_browser_open = True

    def test_001_on_the_main_lotto_page_tap_number_line_for_selected_lottery(self):
        """
        DESCRIPTION: On the main lotto page tap number line for selected lottery
        EXPECTED: Select Numbers pop-up is displayed
        """
        pass

    def test_002_do_not_select_any_ball_on_select_numbers_pop_upverify_reset_numbers_button_state(self):
        """
        DESCRIPTION: Do not select any ball on Select Numbers pop-up.
        DESCRIPTION: Verify 'Reset Numbers' button state
        EXPECTED: 'Reset Numbers' button is disabled and inactive
        """
        pass

    def test_003_select_at_least_one_ballverify_reset_numbers_button_state(self):
        """
        DESCRIPTION: Select at least one ball.
        DESCRIPTION: Verify 'Reset Numbers' button state
        EXPECTED: 'Reset Numbers' button becomes enabled if at least one ball is selected
        """
        pass

    def test_004_select_more_balls_which_became_marked_appropriately_on_select_numbers_pop_uptap_reset_numbers_button(self):
        """
        DESCRIPTION: Select more balls which became marked appropriately on Select Numbers pop-up.
        DESCRIPTION: Tap 'Reset Numbers' button
        EXPECTED: All previously selected balls are unselected and unmarked
        """
        pass

    def test_005_there_are_already_selected_numbers_in_the_number_linetap_any_number_in_the_line(self):
        """
        DESCRIPTION: There are already selected numbers in the number line.
        DESCRIPTION: Tap any number in the line.
        EXPECTED: *   Select Numbers pop-up is displayed
        EXPECTED: *   Already selected numbers are appropriately marked
        EXPECTED: *   'Reset Numbers' button is enabled and active
        """
        pass
