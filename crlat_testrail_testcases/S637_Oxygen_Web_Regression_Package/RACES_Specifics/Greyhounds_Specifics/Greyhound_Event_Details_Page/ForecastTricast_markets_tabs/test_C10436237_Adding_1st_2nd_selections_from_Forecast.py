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
class Test_C10436237_Adding_1st_2nd_selections_from_Forecast(Common):
    """
    TR_ID: C10436237
    NAME: Adding 1st, 2nd selections from Forecast
    DESCRIPTION: This test case verifies functionality of adding and removing 1st, 2nd selections from Forecast
    PRECONDITIONS: 1. GH event exists with Win/Each Way market exists.
    PRECONDITIONS: 2. Forecast checkbox is active on Win/Each Way market for this event
    PRECONDITIONS: 3. User is on EDP on this event in app
    """
    keep_browser_open = True

    def test_001_select_forecast_tab(self):
        """
        DESCRIPTION: Select Forecast tab
        EXPECTED: 
        """
        pass

    def test_002_click_1st_selection_button_on_any_runner(self):
        """
        DESCRIPTION: Click 1st selection button on any runner
        EXPECTED: * Selected button is highlighted green
        EXPECTED: * 2nd and ANY button for this runner become disabled
        EXPECTED: * All other 1st buttons for all other runners become disabled
        EXPECTED: * Add to Betslip button still disabled
        """
        pass

    def test_003_click_2nd_selection_button_on_a_different_runner(self):
        """
        DESCRIPTION: Click 2nd selection button on a different runner
        EXPECTED: * Selected button is highlighted green. Previously selected button remains green and selected
        EXPECTED: * 1st and ANY button for this runner become disabled
        EXPECTED: * All other 2nd buttons for all other runners become disabled
        EXPECTED: * Other ANY buttons remain enabled
        EXPECTED: * Add to Betslip button becomes enabled
        """
        pass
