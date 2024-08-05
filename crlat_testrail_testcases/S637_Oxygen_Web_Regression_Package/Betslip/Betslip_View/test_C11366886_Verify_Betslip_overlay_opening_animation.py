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
class Test_C11366886_Verify_Betslip_overlay_opening_animation(Common):
    """
    TR_ID: C11366886
    NAME: Verify Betslip overlay opening animation
    DESCRIPTION: This test case verifies Betslip overlay opening/closing animation
    PRECONDITIONS: 1. Application is loaded
    PRECONDITIONS: 2. Betslip is empty
    """
    keep_browser_open = True

    def test_001_tap_betslip_counter_in_the_app_headerverify_betslip_animation_while_opening(self):
        """
        DESCRIPTION: Tap Betslip counter in the app header.
        DESCRIPTION: Verify Betslip animation while opening
        EXPECTED: - Betslip overlay is opened from the bottom to the page top
        EXPECTED: - Betslip overlay covers the full width of screen
        """
        pass

    def test_002_tap_close_button_on_the_betslip_header(self):
        """
        DESCRIPTION: Tap 'Close' button on the Betslip header
        EXPECTED: Betslip overlay is closed from the page top to the bottom
        """
        pass

    def test_003_add_selection_to_the_betslip_and_repeat_step_1(self):
        """
        DESCRIPTION: Add selection to the Betslip and repeat step 1
        EXPECTED: - Betslip overlay is opened from the bottom to the page top
        EXPECTED: - Betslip overlay covers the full width of screen
        """
        pass
