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
class Test_C16375058_Verify_highlighting_1st_2nd_ANY_selections_from_Forecast(Common):
    """
    TR_ID: C16375058
    NAME: Verify highlighting 1st, 2nd, ANY selections from Forecast
    DESCRIPTION: This test case verifies functionality of adding and removing 1st, 2nd and ANY selections from Forecast tab.
    PRECONDITIONS: 1. Forecast market is configured and shown for Virtual Sports such as: Horse Racing, Horse Racing Jumps, Greyhound, Motor Racing and Cycling.
    PRECONDITIONS: Note: Forecast tab should not be shown for such Virtual Sports as: VGN (Virtual Grand Nationals Races), Football, Tennis, Speedway, Boxing, Darts.
    PRECONDITIONS: 2. User is on Virtual Sports page/Forecast tab (this test case should be run for all sports displayed in the previous step where Forecast tab should be displayed).
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
        EXPECTED: - 2nd and ANY buttons for this runner become disabled;
        EXPECTED: - All other 1st buttons for all other runners become disabled;
        EXPECTED: - Add to Betslip button is still disabled.
        """
        pass

    def test_002_tap_2nd_button_for_some_other_runner(self):
        """
        DESCRIPTION: Tap 2nd button for some other runner.
        EXPECTED: - Selected button is highlighted in green. Previously selected button remains green and selected;
        EXPECTED: - 1st and ANY button for this runner become disabled;
        EXPECTED: - All other 2nd buttons for all other runners become disabled;
        EXPECTED: - Other ANY buttons remain enabled;
        EXPECTED: - Add to Betslip button becomes enabled.
        """
        pass

    def test_003_tap_any_selection_button_for_any_runner(self):
        """
        DESCRIPTION: Tap ANY selection button for any runner.
        EXPECTED: - Selected button is highlighted in green;
        EXPECTED: - All 1st and 2nd buttons become disabled and unhighlighted;
        EXPECTED: - Other ANY buttons remain enabled;
        EXPECTED: - 'Add to Betslip' button becomes disabled.
        """
        pass

    def test_004_tap_any_selection_button_for_some_other_runner(self):
        """
        DESCRIPTION: Tap ANY selection button for some other runner.
        EXPECTED: - Selected button is highlighted in green;
        EXPECTED: - All 1st and 2nd buttons remain disabled;
        EXPECTED: - Other ANY buttons remain enabled;
        EXPECTED: - 'Add to Betslip' button becomes enabled.
        """
        pass
