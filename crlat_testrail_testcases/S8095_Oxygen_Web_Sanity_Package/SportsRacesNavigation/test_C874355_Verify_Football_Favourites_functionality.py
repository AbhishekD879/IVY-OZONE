import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C874355_Verify_Football_Favourites_functionality(Common):
    """
    TR_ID: C874355
    NAME: Verify Football Favourites functionality
    DESCRIPTION: AUTOTEST [C58199579]
    DESCRIPTION: This Test Case verifies Football 'Favourites’ functionality
    DESCRIPTION: *NOTE:*
    DESCRIPTION: Steps 7-12 should be ran only on Mobile/Tablet
    PRECONDITIONS: * Football Events are present on FE (not older than 12 hours from the start time of the event)
    PRECONDITIONS: * User is Logged Out
    """
    keep_browser_open = True

    def test_001_navigate_to_the_football_landing_page(self):
        """
        DESCRIPTION: Navigate to the Football Landing page
        EXPECTED: * Football Landing page is opened
        EXPECTED: * 'Favourite' icon (star icon) is displayed next to 'Event (Team A v Team B)'
        EXPECTED: * 'Favourite' icon (star icon) is NOT displayed near Enhanced Multiples
        EXPECTED: * 'Favourites' widget is empty **(Desktop)**
        EXPECTED: * 'Favourites' counter on 'Football' top header = 0 **(Mobile/Tablet)**
        """
        pass

    def test_002_tap_on_the_favourite_icon_star_icon_next_to__event_team_a_v_team_b(self):
        """
        DESCRIPTION: Tap on the 'Favourite' icon (star icon) next to  'Event (Team A v Team B)'
        EXPECTED: 'Log In' pop-up appears
        """
        pass

    def test_003_enter_valid_user_name_and_password_and_press_log_in(self):
        """
        DESCRIPTION: Enter valid user name and password and press 'Log In'
        EXPECTED: * User is Logged In
        EXPECTED: * 'Favourite' icon becomes bold (yellow)
        EXPECTED: * The event is added to the 'Favourite Matches'
        EXPECTED: * 'Favourites' widget has one Favourite event **(Desktop)**
        EXPECTED: * 'Favourites' counter on 'Football' top header = exact amount of added to Favourites events **(Mobile/Tablet)**
        """
        pass

    def test_004_tap_on_selected_favourite_icon_star_icon_next_to_the_same_event(self):
        """
        DESCRIPTION: Tap on selected 'Favourite' icon (star icon) next to the same Event
        EXPECTED: * 'Favourite' icon is not filled (not selected)
        EXPECTED: * The event is removed from the 'Favourite Matches'
        EXPECTED: * 'Favourites' widget is empty **(Desktop)**
        EXPECTED: * 'Favourites' counter on 'Football' top header = 0 **(Mobile/Tablet)**
        """
        pass

    def test_005_navigate_to_the_football_event_details_page(self):
        """
        DESCRIPTION: Navigate to the Football Event Details page
        EXPECTED: * Football Event Details page is opened
        EXPECTED: * **For Desktop:** 'Favourite' icon (star icon) is displayed at the left side of the Event Bar
        EXPECTED: * **For Mobile/Tablet:** 'Favourite' icon (star icon) is displayed at the right side icon block (under 'Statistics' section)
        """
        pass

    def test_006_tap_on_favourite_icon_star_icon(self):
        """
        DESCRIPTION: Tap on 'Favourite' icon (star icon)
        EXPECTED: * 'Favourite' icon becomes bold (yellow)
        EXPECTED: * The event is added to the 'Favourite Matches'
        EXPECTED: * 'Favourites' widget has one Favourite event **(Desktop)**
        EXPECTED: * 'Favourites' counter on 'Football' top header = exact amount of added to Favourites events **(Mobile/Tablet)**
        """
        pass

    def test_007_tap_on_favourite_icon_star_icon_on_football_page_header_mobiletablet(self):
        """
        DESCRIPTION: Tap on 'Favourite' icon (star icon) on Football page header **(Mobile/Tablet)**
        EXPECTED: 'Favourite Matches' page is opened **(Mobile/Tablet)**
        """
        pass

    def test_008_verify_favourite_matches_elements_mobiletablet(self):
        """
        DESCRIPTION: Verify 'Favourite Matches' elements **(Mobile/Tablet)**
        EXPECTED: * 'Clear All Favourites' button is displayed at the top of the page
        EXPECTED: * Football matches which user has previously selected as favourites are displayed
        EXPECTED: * Information text is displayed as follows:
        EXPECTED: "Browse through the matches currently available and add them to your favourite list."
        EXPECTED: * 'Go to Matches' button
        EXPECTED: * 'Go to In-Play Matches' button
        """
        pass

    def test_009_tap_on_clear_all_favourites_button_mobiletablet(self):
        """
        DESCRIPTION: Tap on 'Clear All Favourites' button **(Mobile/Tablet)**
        EXPECTED: Football matches which user has previously selected as favourites disappear
        """
        pass

    def test_010_tap_on_go_to_matches_button_mobiletablet(self):
        """
        DESCRIPTION: Tap on 'Go to Matches' button **(Mobile/Tablet)**
        EXPECTED: * Football Landing page is opened
        EXPECTED: * 'Matches' tab is opened
        """
        pass

    def test_011_navigate_to_the_favourite_matches_page_by_tapping_on_favourite_icon_star_icon_on_football_page_header_mobiletablet(self):
        """
        DESCRIPTION: Navigate to the 'Favourite Matches' page by tapping on 'Favourite' icon (star icon) on Football page header **(Mobile/Tablet)**
        EXPECTED: 'Favourite Matches' page is opened
        """
        pass

    def test_012_tap_on_go_to_in_play_matches_button_mobiletablet(self):
        """
        DESCRIPTION: Tap on 'Go to In-Play Matches' button **(Mobile/Tablet)**
        EXPECTED: * Football Landing page is opened
        EXPECTED: * 'In-Play' tab is opened
        """
        pass

    def test_013_add_in_play_football_event_to_favourite(self):
        """
        DESCRIPTION: Add In-Play Football Event to 'Favourite'
        EXPECTED: The event is added to the 'Favourite Matches'
        EXPECTED: * 'Favourites' widget has one Favourite event **(Desktop)**
        EXPECTED: * 'Favourites' counter on 'Football' top header = exact amount of added to Favourites events **(Mobile/Tablet)**
        """
        pass

    def test_014_place_a_bet_on_football_event_that_is_not_added_to_favourites_not_enhanced_multiples_or_outrights(self):
        """
        DESCRIPTION: Place a bet on Football Event that is not added to Favourites (not Enhanced Multiples or Outrights)
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is shown on the Bet Slip
        EXPECTED: * 'Favourite all' with 'Favourite' icon is displayed at the top of Bet Receipt
        EXPECTED: * 'Favourite' icon (star icon) is displayed at the Bet Receipt
        """
        pass

    def test_015_tap_on_favourite_icon_star_icon_on_bet_receipt(self):
        """
        DESCRIPTION: Tap on 'Favourite' icon (star icon) on Bet Receipt
        EXPECTED: * 'Favourite' icon becomes bold
        EXPECTED: * The event is added to the 'Favourite Matches'
        EXPECTED: * 'Favourites' widget has one Favourite event **(Desktop)**
        EXPECTED: * 'Favourites' counter on 'Football' top header = exact amount of added to Favourites events **(Mobile/Tablet)**
        """
        pass

    def test_016_navigate_to_the_football_outrights_page(self):
        """
        DESCRIPTION: Navigate to the Football Outrights page
        EXPECTED: * Outrights page is opened
        EXPECTED: * Favourites Matches functionality is not included on the Outrights page
        """
        pass

    def test_017_navigate_to_the_other_sport_or_race_pages(self):
        """
        DESCRIPTION: Navigate to the other <Sport> or Race pages
        EXPECTED: * Favourites Matches functionality is not included on the other <Sport> pages
        EXPECTED: * Favourites Matches functionality is not included on the Race pages
        """
        pass

    def test_018_verify_favourite_icon_presence_on_the_homepage(self):
        """
        DESCRIPTION: Verify Favourite icon presence on the Homepage
        EXPECTED: Favourite icon is present near Football Match events on the Featured modules on the Homepage
        """
        pass
