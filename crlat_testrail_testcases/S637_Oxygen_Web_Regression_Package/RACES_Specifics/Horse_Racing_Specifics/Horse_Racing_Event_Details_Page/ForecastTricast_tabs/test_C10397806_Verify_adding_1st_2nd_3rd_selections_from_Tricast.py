import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C10397806_Verify_adding_1st_2nd_3rd_selections_from_Tricast(Common):
    """
    TR_ID: C10397806
    NAME: Verify adding 1st, 2nd, 3rd selections from Tricast
    DESCRIPTION: This test case verifies adding 1st, 2nd, 3rd selections from Tricast
    PRECONDITIONS: 1. HR event exists with Win/Each Way market exists.
    PRECONDITIONS: 2. Tricast checkbox is active on Win/Each Way market for this event
    PRECONDITIONS: 3. User should have a Horse Racing event detail page open ("Tricast" tab)
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

    def test_001_click_1st_selection_button_on_any_runner(self):
        """
        DESCRIPTION: Click 1st selection button on any runner
        EXPECTED: * Selected button is highlighted green
        EXPECTED: * 2nd, 3rd and ANY button for this runner become disabled
        EXPECTED: * All other 1st buttons for all other runners become disabled
        EXPECTED: * Other ANY buttons remain enabled
        EXPECTED: * Add to Betslip button still disabled
        """
        pass

    def test_002_click_2nd_selection_button_on_a_different_runner(self):
        """
        DESCRIPTION: Click 2nd selection button on a different runner
        EXPECTED: * Selected button is highlighted green. Previously selected button remains green and selected
        EXPECTED: * 1st, 3rd and ANY button for this runner become disabled
        EXPECTED: * All other 2nd buttons for all other runners become disabled
        EXPECTED: * Other ANY buttons remain enabled
        EXPECTED: * Add to Betslip button remains disabled
        """
        pass

    def test_003_click_3rd_selection_button_on_a_different_runner(self):
        """
        DESCRIPTION: Click 3rd selection button on a different runner
        EXPECTED: * Selected button is highlighted green. Previously selected button remains green and selected
        EXPECTED: * 2nd, 3rd and ANY button for this runner become disabled
        EXPECTED: * All other 3rd buttons for all other runners become disabled
        EXPECTED: * Other ANY buttons remain enabled
        EXPECTED: * Add to Betslip button becomes enabled
        """
        pass
