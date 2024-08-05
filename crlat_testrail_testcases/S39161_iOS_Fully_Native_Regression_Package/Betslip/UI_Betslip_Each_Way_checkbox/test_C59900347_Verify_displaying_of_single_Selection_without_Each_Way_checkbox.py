import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.native
@vtest
class Test_C59900347_Verify_displaying_of_single_Selection_without_Each_Way_checkbox(Common):
    """
    TR_ID: C59900347
    NAME: Verify displaying of  single  Selection  without  "Each Way" checkbox
    DESCRIPTION: Test case verifies displaying of single selection for which  "Each Way" checkbox unavailable
    DESCRIPTION: ble
    PRECONDITIONS: Light Theme is enabled on tested device (Setting -> Display & Brightness -> Select "Light" theme)
    PRECONDITIONS: Install native app
    PRECONDITIONS: Open the app
    PRECONDITIONS: User is on Home page
    PRECONDITIONS: Betslip is empty
    PRECONDITIONS: Coral design: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/dashboard?sid=5eaa983ae1344bbac8b9f021
    PRECONDITIONS: Ladbrokes design: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/dashboard?sid=5ea97d244f68f62598af7515
    """
    keep_browser_open = True

    def test_001_tap_on_any_selection_of_the_event_where_for_selection_each_way_option_is_not_available_eg_events_from_horse_racinggreyhounds_etc(self):
        """
        DESCRIPTION: Tap on any selection of the event where for selection "Each Way" option is not available (e.g. Events from Horse Racing,Greyhounds etc.)
        EXPECTED: Selected single selection added to Betslip
        EXPECTED: Betslip in collapsed mode displays the selection in the bottom of the screen
        EXPECTED: "Each Way" checkbox is not displayed for current selection below stake field
        """
        pass

    def test_002_tap_on_selection_in_betslip(self):
        """
        DESCRIPTION: Tap on selection in Betslip
        EXPECTED: Betslip expands with current selection
        """
        pass

    def test_003_make_sure_that_each_way_checkbox_is_not_displayed_for_current_selection(self):
        """
        DESCRIPTION: Make sure that "Each Way" checkbox is not displayed for current selection
        EXPECTED: * "Each Way" checkbox is not displayed below "Stake" field
        """
        pass

    def test_004__enable_dark_theme_on_device(self):
        """
        DESCRIPTION: * Enable "Dark" theme on device
        EXPECTED: * "Dark" theme on device is enabled
        EXPECTED: * Betslip remains expanded with current selection
        EXPECTED: * "Each Way" checkbox is not displayed below "Stake" field
        """
        pass

    def test_005__collapse_betslip(self):
        """
        DESCRIPTION: * Collapse Betslip
        EXPECTED: * Betslip collapsed
        EXPECTED: * Betslip displays current selection
        EXPECTED: * "Each Way" checkbox is not displayed below "Stake" field
        """
        pass
