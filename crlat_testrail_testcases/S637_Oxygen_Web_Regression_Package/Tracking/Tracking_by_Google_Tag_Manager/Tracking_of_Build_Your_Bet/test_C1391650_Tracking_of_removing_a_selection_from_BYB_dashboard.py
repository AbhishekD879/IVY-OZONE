import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C1391650_Tracking_of_removing_a_selection_from_BYB_dashboard(Common):
    """
    TR_ID: C1391650
    NAME: Tracking of removing a selection from BYB dashboard
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer of removing a selection from BYB dashboard
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Browser console should be opened
    PRECONDITIONS: 3. Navigate to Football Landing page
    PRECONDITIONS: 4. Go to the Event details page with the BYB (Leagues with available BYB are marked with BYB icon on accordion) > 'Build Your Bet' tab
    PRECONDITIONS: 5. Add a selection(s) (bet) from any market accordion to the BYB Dashboard
    """
    keep_browser_open = True

    def test_001_remove_a_selections_from_the_byb_dashboard(self):
        """
        DESCRIPTION: Remove a selection(s) from the BYB dashboard
        EXPECTED: Selection(s) is removed
        """
        pass

    def test_002_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'your call',
        EXPECTED: 'eventAction' : 'dashboard',
        EXPECTED: 'eventLabel' : 'remove selection'
        EXPECTED: 'market' : '<< MARKET >>' }
        EXPECTED: )
        """
        pass
