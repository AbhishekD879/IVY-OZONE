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
class Test_C2009420_Tracking_of_editing_a_bet(Common):
    """
    TR_ID: C2009420
    NAME: Tracking of editing a bet
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer of editing a bet
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
        EXPECTED: - Player Markets tab opened by default
        """
        pass

    def test_004_add_a_selections_bet_from_player_bets_accordion_to_the_yc_dashboard_and_click_edit_bet(self):
        """
        DESCRIPTION: Add a selection(s) (bet) from Player Bets accordion to the #YC Dashboard and click Edit bet
        EXPECTED: 
        """
        pass

    def test_005_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'your call',
        EXPECTED: 'eventAction' : 'dashboard',
        EXPECTED: 'eventLabel' : 'edit bet'
        EXPECTED: })
        """
        pass

    def test_006_make_any_corrections___click_on_done_same_selection_as_on_step_4(self):
        """
        DESCRIPTION: Make any corrections -> click on Done (same selection as on step 4)
        EXPECTED: 
        """
        pass

    def test_007_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is NOT tracked twice in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'your call',
        EXPECTED: 'eventAction' : 'dashboard',
        EXPECTED: 'eventLabel' : 'edit bet'
        EXPECTED: })
        """
        pass
