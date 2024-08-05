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
class Test_C3233910_Betslip_counter_and_animation(Common):
    """
    TR_ID: C3233910
    NAME: Betslip counter and animation
    DESCRIPTION: This test case verifies bestilp counter and animation during adding and removing selections from betslip.
    PRECONDITIONS: - You should be logged in
    PRECONDITIONS: - You should have no selections added to betslip
    """
    keep_browser_open = True

    def test_001___tap_on_any_selection_and_add_to_betslip_via_quick_bet_window__verify_counter_updating_and_betslip_animation(self):
        """
        DESCRIPTION: - Tap on any selection and add to betslip via quick bet window
        DESCRIPTION: - Verify counter updating and betslip animation
        EXPECTED: Counter is updated to '1' in live and betslip animation is performed during adding
        """
        pass

    def test_002___tap_on_any_another_selection__verify_counter_updating_and_betslip_animation(self):
        """
        DESCRIPTION: - Tap on any another selection
        DESCRIPTION: - Verify counter updating and betslip animation
        EXPECTED: Counter is updated to '2' in live and betslip animation is performed during adding
        """
        pass

    def test_003___open_betslip_and_remove_one_of_the_selections__close_betslip_mobile_only__verify_counter_updating(self):
        """
        DESCRIPTION: - Open betslip and remove one of the selections
        DESCRIPTION: - Close betslip (Mobile only)
        DESCRIPTION: - Verify counter updating
        EXPECTED: Mobile:
        EXPECTED: Counter is updated to '1'
        EXPECTED: Tablet:
        EXPECTED: Counter is updated to '1' in live and betslip animation is performed during removing
        """
        pass

    def test_004___tap_on_the_last_selection_added_to_betslip_to_deselect_it_to_remove_it_from_betslip__verify_counter_updating_and_betslip_animation(self):
        """
        DESCRIPTION: - Tap on the last selection added to betslip to deselect it (to remove it from betslip)
        DESCRIPTION: - Verify counter updating and betslip animation
        EXPECTED: Counter is updated to '0' in live and betslip animation is performed during removing
        """
        pass
