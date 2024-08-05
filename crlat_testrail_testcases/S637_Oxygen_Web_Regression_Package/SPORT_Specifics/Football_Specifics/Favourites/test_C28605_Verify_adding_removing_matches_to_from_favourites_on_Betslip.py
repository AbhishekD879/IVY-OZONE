import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28605_Verify_adding_removing_matches_to_from_favourites_on_Betslip(Common):
    """
    TR_ID: C28605
    NAME: Verify adding/removing matches to /from favourites on 'Betslip'
    DESCRIPTION: This Test Case verified adding/removing matches to/from favourites on Betslip
    PRECONDITIONS: **JIRA Ticket** :
    PRECONDITIONS: BMA-7800 'Add 'Favourite Match' functionality to Football events on the Betslip'
    PRECONDITIONS: BMA-8264 'Favourites Journey on Betslip: Bet Receipt'
    PRECONDITIONS: **NOTE **:
    PRECONDITIONS: *   User is logged in, has positive balance
    PRECONDITIONS: *   User is on Football landing page
    PRECONDITIONS: *   only Football Receipt card has the ability to be added to favourites
    PRECONDITIONS: *   Test case should be validated for Events with primary market title "Match Results" and "Match Betting"
    """
    keep_browser_open = True

    def test_001_add_a_football_selections_to_the_betslip_and_open_betslip(self):
        """
        DESCRIPTION: Add a Football selection(s) to the Betslip and open Betslip
        EXPECTED: *   Betslip page is opened
        EXPECTED: *   added selection(s) is/are present
        """
        pass

    def test_002_enter_stake_in_stake_field_and_tap_bet_now_button(self):
        """
        DESCRIPTION: Enter stake in 'Stake' field and tap 'Bet Now' button
        EXPECTED: Bet Receipt is shown
        """
        pass

    def test_003_tap_on_the_favourite_maches_star_icon(self):
        """
        DESCRIPTION: Tap on the 'Favourite Maches' star icon
        EXPECTED: *   the star icon becomes bold
        EXPECTED: *   the event is added to the 'Favourite Matches' page/widget
        """
        pass

    def test_004_close_betslip_and_navigate_to_favourites_pagewidget_desktop(self):
        """
        DESCRIPTION: Close betslip and navigate to Favourites page/widget (desktop)
        EXPECTED: * Event is displayed on Favourites page/widget
        """
        pass

    def test_005_navigate_back_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate back to Football Landing page
        EXPECTED: 
        """
        pass

    def test_006_tap_on_the_favourite_maches_icon_star_icon(self):
        """
        DESCRIPTION: Tap on the 'Favourite Maches' icon (star icon)
        EXPECTED: *   the star icon appeared in bold
        EXPECTED: *   the event is added to the 'Favourites Matches' page/widget
        """
        pass

    def test_007_add_selection_to_the_bet_slip_of_the_same_event_and_open_betslip(self):
        """
        DESCRIPTION: Add selection to the Bet Slip (of the same Event) and open Betslip
        EXPECTED: *   Betslip page is open
        EXPECTED: *   the added selection(s) is/are present
        """
        pass

    def test_008_place_bet_on_selection(self):
        """
        DESCRIPTION: Place Bet on selection
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   Bet Receipt is shown
        EXPECTED: *   'Favourites matches' star icon is displayed as bold
        """
        pass

    def test_009_tap_on_the_favourite_maches_icon_star_icon(self):
        """
        DESCRIPTION: Tap on the 'Favourite Maches' icon (star icon)
        EXPECTED: * Fafourites star icon becomes unselected
        """
        pass

    def test_010_close_betslip_go_to_favourite_matches_pagewidget_and_verify_presence_of_the_event(self):
        """
        DESCRIPTION: Close Betslip, Go to 'Favourite Matches' page/widget and verify presence of the Event
        EXPECTED: The Event is not displayed on 'Favourite Matches' page/widget
        """
        pass
