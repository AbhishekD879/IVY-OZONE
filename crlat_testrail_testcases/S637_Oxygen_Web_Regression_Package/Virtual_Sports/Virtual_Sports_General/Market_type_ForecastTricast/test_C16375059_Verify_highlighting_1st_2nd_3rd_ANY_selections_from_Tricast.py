import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.virtual_sports
@vtest
class Test_C16375059_Verify_highlighting_1st_2nd_3rd_ANY_selections_from_Tricast(Common):
    """
    TR_ID: C16375059
    NAME: Verify highlighting 1st, 2nd, 3rd, ANY selections from Tricast
    DESCRIPTION: This test case verifies functionality of adding and removing 1st, 2nd, 3rd and ANY selections from Tricast tab.
    PRECONDITIONS: 1. Tricast market is configured and shown for Virtual Sports such as: Horse Racing, Horse Racing Jumps, Greyhound, Motor Racing and Cycling. Note: Forecast tab should not be shown for such Virtual Sports as: VGN (Virtual Grand Nationals Races), Football, Tennis, Speedway, Boxing, Darts.
    PRECONDITIONS: 2. User is on Virtual Sports page/Tricast tab (this test case should be run for all sports displayed in the previous step where Tricast tab should be displayed).
    PRECONDITIONS: The rules of displaying Virtuals Forecast and Tricast tabs:
    PRECONDITIONS: 1. Tabs are not shown at all if event does not have ncastTypeCodes attribute. Only WinOrEw Market is displayed in this case (UI looks like on current production).
    PRECONDITIONS: 2. All tabs are shown if event has ncastTypeCodes attribute with set CF and CT.
    PRECONDITIONS: 3. Two tabs: Forecast and WinOrEw are shown if event has ncastTypeCodes attribute with set only CF.
    PRECONDITIONS: 4. Two tabs: Tricast and WinOrEw are shown if event has ncastTypeCodes attribute with set only CT.
    PRECONDITIONS: Also we check if market is WinOrEw: ['To Win', 'To-Win', 'Win/EachWay', 'Win or Each Way']
    """
    keep_browser_open = True

    def test_001_tap_1st_button_for_any_runner(self):
        """
        DESCRIPTION: Tap 1st button for any runner.
        EXPECTED: - Selected button is highlighted in green;
        EXPECTED: - 2nd, 3rd and ANY buttons for this runner become disabled;
        EXPECTED: - All other 1st buttons for all other runners become disabled;
        EXPECTED: - Add to Betslip button is still disabled.
        """
        pass

    def test_002_tap_2nd_button_for_any_other_runner(self):
        """
        DESCRIPTION: Tap 2nd button for any other runner.
        EXPECTED: - Selected button is highlighted in green. Previously selected button remains green and selected;
        EXPECTED: - 1st, 3rd and ANY button for this runner become disabled;
        EXPECTED: - All other 2nd buttons for all other runners become disabled;
        EXPECTED: - Other 3rd and ANY buttons remain enabled;
        EXPECTED: - Add to Betslip button is still disabled.
        """
        pass

    def test_003_tap_3rd_button_for_any_runner(self):
        """
        DESCRIPTION: Tap 3rd button for any runner.
        EXPECTED: - Selected button is highlighted in green. Previously selected button remains green and selected;
        EXPECTED: - 1st, 2nd and ANY button for this runner become disabled;
        EXPECTED: - All other 3rd buttons for all other runners become disabled;
        EXPECTED: - All ANY buttons remain enabled;
        EXPECTED: - Add to Betslip button becomes enabled.
        """
        pass

    def test_004_tap_any_button_for_any_runner(self):
        """
        DESCRIPTION: Tap ANY button for any runner.
        EXPECTED: - Selected button is highlighted in green;
        EXPECTED: - All 1st 2nd and 3rd buttons became disabled and unhighlighted;
        EXPECTED: - Other ANY buttons remain enabled;
        EXPECTED: - 'Add to Betslip' button becomes disabled.
        """
        pass

    def test_005_tap_any_button_for_one_more_runner(self):
        """
        DESCRIPTION: Tap ANY button for one more runner.
        EXPECTED: - Selected button is highlighted in green;
        EXPECTED: - All 1st 2nd and 3rd buttons became disabled and unhighlighted;
        EXPECTED: - Other ANY buttons remain enabled;
        EXPECTED: - 'Add to Betslip' button remains disabled.
        """
        pass

    def test_006_tap_any_button_for_one_more_runner(self):
        """
        DESCRIPTION: Tap ANY button for one more runner.
        EXPECTED: - Selected button and previously tapped button are highlighted in green;
        EXPECTED: - All 1st 2nd and 3rd buttons are still disabled and unhighlighted;
        EXPECTED: - Other ANY buttons remain enabled;
        EXPECTED: - 'Add to Betslip' button becomes enabled.
        """
        pass
