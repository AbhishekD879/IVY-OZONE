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
class Test_C10397579_Verify_Forecast_tab_view_on_Horse_Racing_EDP_Build_Your_Racecard_page(Common):
    """
    TR_ID: C10397579
    NAME: Verify Forecast tab view on Horse Racing EDP/Build Your Racecard page
    DESCRIPTION: This test case verifies the view of the Forecast tab on Horse Racing EDP
    PRECONDITIONS: 1. HR event exists with Win/Each Way market exists.
    PRECONDITIONS: 2. Forecast checkbox is active on Win/Each Way market for this event
    PRECONDITIONS: 3. User should have a Horse Racing event detail page open ("Forecast" tab)
    PRECONDITIONS: * Navigate to HR landing page
    PRECONDITIONS: * Choose the particular event from the 'Race Grid'
    PRECONDITIONS: * Select 'Forecast' tab
    PRECONDITIONS: **AND REPEAT FOR**
    PRECONDITIONS: Build Your Racecard page for specific Event ("Forecast" tab) **Desktop**:
    PRECONDITIONS: * Navigate to HR landing page
    PRECONDITIONS: * Click 'Build a Racecard' button
    PRECONDITIONS: * Select at least one Event with Forecast are available
    PRECONDITIONS: * Click 'Build Your Racecard' button
    PRECONDITIONS: * Select 'Forecast' tab
    """
    keep_browser_open = True

    def test_001_verify_its_layout(self):
        """
        DESCRIPTION: Verify it's layout
        EXPECTED: * List of selections with:
        EXPECTED: - runner number
        EXPECTED: - runner name
        EXPECTED: - no silks
        EXPECTED: - no race form info
        EXPECTED: * Unnamed favourites and Non runners are NOT displayed
        EXPECTED: * Runners ordered by runner number
        EXPECTED: * 3 grey tappable buttons displayed at the right side of each runner:
        EXPECTED: - 1st
        EXPECTED: - 2nd
        EXPECTED: - ANY
        EXPECTED: * Green 'Add To Betslip' button displayed at the bottom of the list, disabled by default
        """
        pass

    def test_002__tapclick_any_of_1st_and_2nd_selections_for_different_runnersor_tapclick_2plus_any_selections_for_different_runners(self):
        """
        DESCRIPTION: * Tap/Click any of '1st' and '2nd' selections for different runners
        DESCRIPTION: or
        DESCRIPTION: * Tap/Click 2+ ANY selections for different runners
        EXPECTED: 'Add To Betslip' button is enabled and highlighted green
        """
        pass

    def test_003_tapclick_on_one_of_highlighted_selections(self):
        """
        DESCRIPTION: Tap/Click on one of highlighted selections
        EXPECTED: 'Add To Betslip' button is not enabled and not highlighted
        """
        pass
