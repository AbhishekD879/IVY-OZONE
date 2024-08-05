import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.quick_bet
@vtest
class Test_C820359_Verify_Quick_Bet_when_screen_resolution_is_changed(Common):
    """
    TR_ID: C820359
    NAME: Verify Quick Bet when screen resolution is changed
    DESCRIPTION: This test case verifies Quick Bet when screen resolution is changed
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS
    PRECONDITIONS: * Make sure you have device that has Mobile view in portrait mode and Tablet view in landscape mode
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
        EXPECTED: Quick Bet appears at the bottom of the page
        """
        pass

    def test_003_enter_value_in_stake_field_and_check_ew_checkbox_if_available(self):
        """
        DESCRIPTION: Enter value in 'Stake' field and check 'E/W' checkbox (if available)
        EXPECTED: * 'Stake' field is pre-populated with value
        EXPECTED: * 'E/W' checkbox is selected
        """
        pass

    def test_004_change_screen_resolutioneg_rotate_device_to_landscape_mode(self):
        """
        DESCRIPTION: Change screen resolution
        DESCRIPTION: e.g rotate device to landscape mode
        EXPECTED: Page is displayed with animated mobile icon and text: "Please rotate your screen back in Portrait Mode. Please ensure you have 'screen rotate' option active."
        """
        pass

    def test_005_change_screen_resolution_one_more_time(self):
        """
        DESCRIPTION: Change screen resolution one more time
        EXPECTED: Quick Bet remains displayed with pre-populated 'Stake' field
        """
        pass
