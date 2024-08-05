import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.races
@vtest
class Test_C10436236_Verify_Forecast_tab_view_on_Greyhound_EDP(Common):
    """
    TR_ID: C10436236
    NAME: Verify Forecast tab view on Greyhound EDP
    DESCRIPTION: This test case verifies the view of the Forecast tab on Greyhound EDP
    PRECONDITIONS: 1. GH event exists with Win/Each Way market exists.
    PRECONDITIONS: 2. Forecast checkbox is active on Win/Each Way market for this event
    """
    keep_browser_open = True

    def test_001_navigate_to_edp_of_event_from_preconditions(self):
        """
        DESCRIPTION: Navigate to EDP of event from preconditions
        EXPECTED: * Separate Forecast tab displayed after Win/Each way market tab
        """
        pass

    def test_002_select_forecast_tabverify_its_layout(self):
        """
        DESCRIPTION: Select Forecast tab
        DESCRIPTION: Verify it's layout
        EXPECTED: * List of selections with:
        EXPECTED: - runner number
        EXPECTED: - runner name
        EXPECTED: - no silks
        EXPECTED: - no race form info
        EXPECTED: * Unnamed favorites and Non Runners are NOT displayed
        EXPECTED: * Runners ordered by runner number
        EXPECTED: * 3 grey tappable buttons displayed at the right side of each runner:
        EXPECTED: - 1st
        EXPECTED: - 2nd
        EXPECTED: - ANY
        EXPECTED: * Green 'Add To Betslip' button displayed at the bottom of the list, disabled by default
        """
        pass

    def test_003_tap_any_1st_2nd_or_any_button(self):
        """
        DESCRIPTION: Tap any 1st, 2nd or ANY button
        EXPECTED: * Button is selected and highlighted green
        """
        pass

    def test_004_tap_same_button_again(self):
        """
        DESCRIPTION: Tap same button again
        EXPECTED: * Button deselected and not highlighted
        """
        pass
