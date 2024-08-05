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
class Test_C10397805_Verify_Tricast_tab_view_on_Horse_Racing_EDP_Build_Your_Racecard_page(Common):
    """
    TR_ID: C10397805
    NAME: Verify Tricast tab view on Horse Racing EDP/Build Your Racecard page
    DESCRIPTION: This test case verifies Tricast tab view on Horse Racing EDP
    PRECONDITIONS: 1. HR event exists with Win/Each Way market.
    PRECONDITIONS: 2. Tricast checkbox is active on Win/Each Way market for this event
    PRECONDITIONS: 3. User should have a Horse Racing event detail page open
    PRECONDITIONS: * Navigate to HR landing page
    PRECONDITIONS: * Choose the particular event from the 'Race Grid'
    PRECONDITIONS: * Select 'Tricast' tab
    PRECONDITIONS: **AND REPEAT FOR**
    PRECONDITIONS: Build Your Racecard page for specific Event ("Tricast" tab) **Desktop**:
    PRECONDITIONS: * Navigate to HR landing page
    PRECONDITIONS: * Click 'Build a Racecard' button
    PRECONDITIONS: * Select at least one Event with Tricast are available
    PRECONDITIONS: * Click 'Build Your Racecard' button
    PRECONDITIONS: * Select 'Tricast' tab
    """
    keep_browser_open = True

    def test_001_select_tricast_tabverify_its_layout(self):
        """
        DESCRIPTION: Select Tricast tab
        DESCRIPTION: Verify it's layout
        EXPECTED: * List of selections with:
        EXPECTED: - runner number
        EXPECTED: - runner name
        EXPECTED: - no silks
        EXPECTED: - no race form info
        EXPECTED: * Unnamed favourites are not displayed (BMA-45935)
        EXPECTED: * Runners ordered by runner number
        EXPECTED: * 4 grey tappable buttons displayed at the right side of each runner:
        EXPECTED: - 1st
        EXPECTED: - 2nd
        EXPECTED: - 3rd
        EXPECTED: - ANY
        EXPECTED: * Green 'Add To Betslip' button displayed at the bottom of the list, disabled by default
        """
        pass

    def test_002__tapclick_on_any_of_1st_2nd_and_3rd_selections_for_different_runnersor_tapclick_on_3plus_any_selections_for_different_runners(self):
        """
        DESCRIPTION: * Tap/Click on any of 1st, 2nd and 3rd selections for different runners
        DESCRIPTION: or
        DESCRIPTION: * Tap/Click on 3+ ANY selections for different runners
        EXPECTED: Button is enabled and highlighted green
        """
        pass

    def test_003_tapclick_on_one_of_the_picked_selections(self):
        """
        DESCRIPTION: Tap/Click on one of the picked selections
        EXPECTED: Button is not enabled and not highlighted
        """
        pass
