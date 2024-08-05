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
class Test_C10397804_Verify_functionality_of_adding_1st_or_2nd_and_then_ANY_selection(Common):
    """
    TR_ID: C10397804
    NAME: Verify functionality of adding 1st or 2nd and then ANY selection
    DESCRIPTION: This test case verifies functionality of adding 1st or 2nd and then ANY selection
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

    def test_001_click_1st_or_2nd_selection_button_on_any_runner(self):
        """
        DESCRIPTION: Click 1st (or 2nd) selection button on any runner
        EXPECTED: * Selected button is highlighted green
        EXPECTED: * 2nd (or 1st) and ANY button for this runner become disabled
        EXPECTED: * All other 1st buttons for all other runners become disabled
        EXPECTED: * Other ANY buttons remain enabled
        EXPECTED: * Add to Betslip button still disabled
        """
        pass

    def test_002_click_any_selection_button_for_any_other_racer(self):
        """
        DESCRIPTION: Click ANY selection button for any other racer
        EXPECTED: * Selected button is highlighted green
        EXPECTED: * Previously selected button becomes deselected and disabled
        EXPECTED: * ALL 1st and 2nd buttons become disabled
        EXPECTED: * ALL ANY buttons become enabled
        EXPECTED: * Add to Betslip button still disabled
        """
        pass

    def test_003_click_another_any_selection_button_for_any_other_racer(self):
        """
        DESCRIPTION: Click another ANY selection button for any other racer
        EXPECTED: * Selected button is highlighted green
        EXPECTED: * All other ANY buttons remain enabled
        EXPECTED: * ALL 1st and 2nd buttons remain disabled
        EXPECTED: * Add to Betslip button becomes enabled
        """
        pass
