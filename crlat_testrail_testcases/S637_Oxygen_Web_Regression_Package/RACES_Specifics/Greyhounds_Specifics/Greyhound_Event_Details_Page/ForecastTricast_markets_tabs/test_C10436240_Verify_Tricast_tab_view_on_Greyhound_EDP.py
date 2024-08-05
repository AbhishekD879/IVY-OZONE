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
class Test_C10436240_Verify_Tricast_tab_view_on_Greyhound_EDP(Common):
    """
    TR_ID: C10436240
    NAME: Verify Tricast tab view on Greyhound EDP
    DESCRIPTION: This test case verifies Tricast tab view on Greyhound EDP
    PRECONDITIONS: 1. GH event exists with Win/Each Way market exists.
    PRECONDITIONS: 2. Tricast checkbox is active on Win/Each Way market for this event
    PRECONDITIONS: 3. User is on EDP on this event in app
    """
    keep_browser_open = True

    def test_001_navigate_to_edp_of_event_from_preconditions(self):
        """
        DESCRIPTION: Navigate to EDP of event from preconditions
        EXPECTED: * Separate Tricast tab displayed after Win/Each way market tab
        """
        pass

    def test_002_select_tricast_tabverify_its_layout(self):
        """
        DESCRIPTION: Select Tricast tab
        DESCRIPTION: Verify it's layout
        EXPECTED: * List of selections with:
        EXPECTED: - runner number
        EXPECTED: - runner name
        EXPECTED: - no silks
        EXPECTED: - no race form info
        EXPECTED: * Unnamed favourites and Non Runners are NOT displayed
        EXPECTED: * Runners ordered by runner number
        EXPECTED: * 4 grey tappable buttons displayed at the right side of each runner:
        EXPECTED: - 1st
        EXPECTED: - 2nd
        EXPECTED: - 3rd
        EXPECTED: - ANY
        EXPECTED: * Green 'Add To Betslip' button displayed at the bottom of the list, disabled by default
        """
        pass

    def test_003_tap_any_1st_2nd_3rd_or_any_button(self):
        """
        DESCRIPTION: Tap any 1st, 2nd, 3rd or ANY button
        EXPECTED: Button is selected and highlighted green
        """
        pass

    def test_004_tap_same_button_again(self):
        """
        DESCRIPTION: Tap same button again
        EXPECTED: Button deselected and not highlighted
        """
        pass
