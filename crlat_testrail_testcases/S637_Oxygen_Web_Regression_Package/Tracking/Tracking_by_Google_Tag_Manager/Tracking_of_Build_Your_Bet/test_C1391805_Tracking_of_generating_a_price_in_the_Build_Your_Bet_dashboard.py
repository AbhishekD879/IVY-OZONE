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
class Test_C1391805_Tracking_of_generating_a_price_in_the_Build_Your_Bet_dashboard(Common):
    """
    TR_ID: C1391805
    NAME: Tracking of generating a price in the Build Your Bet dashboard
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer of generating a price in the Build Your Bet dashboard
    PRECONDITIONS: 1. Test case should be run on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: 2. Browser console should be opened
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football Landing page
        EXPECTED: Football Landing page is opened
        """
        pass

    def test_003_go_to_the_event_details_page_with_the_yourcall_leagues_with_available_yourcall_are_marked_with_yourcall_icon_on_accordion__build_your_bet_tab(self):
        """
        DESCRIPTION: Go to the Event details page with the #YourCall (Leagues with available YourCall are marked with YourCall icon on accordion) > Build Your Bet tab
        EXPECTED: - Event details page is opened
        EXPECTED: - Build Your Bet tab is opened
        """
        pass

    def test_004_add_a_selection_or_combination_of_selections_which_generate_the_price(self):
        """
        DESCRIPTION: Add a selection or combination of selections which generate the price
        EXPECTED: The new price is generated
        """
        pass

    def test_005_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: {  'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'your call',
        EXPECTED: 'eventAction' : 'display odds',
        EXPECTED: 'eventLabel' : '(display the actual odds i.e 3.00)'
        EXPECTED: >> All odds are converted to decimal for tracking
        """
        pass
