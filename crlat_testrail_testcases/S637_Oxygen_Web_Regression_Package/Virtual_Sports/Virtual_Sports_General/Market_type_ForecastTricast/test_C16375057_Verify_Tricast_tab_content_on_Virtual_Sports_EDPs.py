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
class Test_C16375057_Verify_Tricast_tab_content_on_Virtual_Sports_EDPs(Common):
    """
    TR_ID: C16375057
    NAME: Verify Tricast tab content on Virtual Sports EDPs
    DESCRIPTION: This test case verifies the content of the Tricast tab on Virtual Sports page for different sports.
    DESCRIPTION: AUTOTEST MOBILE: [C27288910]
    DESCRIPTION: DESKTOP: [C27307624]
    PRECONDITIONS: Tricast market is configured and shown for Virtual Sports such as: Horse Racing, Horse Racing Jumps, Greyhound, Motor Racing and Cycling.
    PRECONDITIONS: Note: Tricast tab should not be shown for such Virtual Sports as: VGN (Virtual Grand Nationals Races), Football, Tennis, Speedway, Boxing, Darts.
    PRECONDITIONS: The rules of displaying Virtuals Forecast and Tricast tabs:
    PRECONDITIONS: 1. Tabs are not shown at all if event does not have ncastTypeCodes attribute. Only WinOrEw Market is displayed in this case (UI looks like on current production).
    PRECONDITIONS: 2. All tabs are shown if event has ncastTypeCodes attribute with set CF and CT.
    PRECONDITIONS: 3. Two tabs: Forecast and WinOrEw are shown if event has ncastTypeCodes attribute with set only CF.
    PRECONDITIONS: 4. Two tabs: Tricast and WinOrEw are shown if event has ncastTypeCodes attribute with set only CT.
    PRECONDITIONS: Also we check if market is WinOrEw: ['To Win', 'To-Win', 'Win/EachWay', 'Win or Each Way']
    """
    keep_browser_open = True

    def test_001_navigate_to_virtual_sport_page_and_tap_on_some_sport_from_preconditions_where_tricast_tab_should_be_displayednote_this_test_cases_should_be_run_for_all_virtual_sports_where_tricast_tab_should_be_displayed(self):
        """
        DESCRIPTION: Navigate to Virtual Sport page and tap on some sport from preconditions where Tricast tab should be displayed.
        DESCRIPTION: Note: this test cases should be run for all Virtual Sports where Tricast tab should be displayed.
        EXPECTED: Separate Tricast tab is displayed after Win or Each Way (and Forecast tab if available) market tab.
        """
        pass

    def test_002_select_tricast_and_verify_its_layout(self):
        """
        DESCRIPTION: Select Tricast and verify its layout.
        EXPECTED: 1.List of selections is displayed with:
        EXPECTED: runner number
        EXPECTED: runner name
        EXPECTED: no silks
        EXPECTED: no race form info
        EXPECTED: Unnamed favourites and Non runners are NOT displayed
        EXPECTED: Runners are ordered by runner number
        EXPECTED: 2.Four grey tappable buttons displayed at the right side of each runner:
        EXPECTED: 1st
        EXPECTED: 2nd
        EXPECTED: 3rd
        EXPECTED: ANY
        EXPECTED: 3.Green 'Add To Betslip' button displayed at the bottom of the list, disabled by default.
        """
        pass

    def test_003_tap_any_1st_2nd_3rd_or_any_button(self):
        """
        DESCRIPTION: Tap any 1st, 2nd, 3rd or ANY button.
        EXPECTED: 1. Tapped button is displayed as selected and highlighted in green.
        EXPECTED: 2. All other such buttons are disabled (e.g. - after tapping on 1st button, all other 1st buttons should be disabled for all horses).
        EXPECTED: 3. All other buttons for the same horse is disabled (e.g. - after tapping on 1st button, 2nd, 3rd and ANY button should be disabled for the same horse).
        """
        pass

    def test_004_tap_the_same_button_again(self):
        """
        DESCRIPTION: Tap the same button again.
        EXPECTED: 1. Tapped button is deselected and not highlighted in green.
        EXPECTED: 2. All other buttons should be enabled again.
        """
        pass
