import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C28604_Verify_Favourite_Match_functionality_in_Football_events_on_the_Betslip(Common):
    """
    TR_ID: C28604
    NAME: Verify 'Favourite Match' functionality in Football events on the Betslip
    DESCRIPTION: This Test Case verifies 'Favourite Match' functionality to Football events on Betslip
    PRECONDITIONS: **JIRA Ticket** :
    PRECONDITIONS: BMA-7800 'Add 'Favourite Match' functionality to Football events on the Betslip'
    PRECONDITIONS: BMA-8264 'Favourites Journey on Betslip: Bet Receipt'
    PRECONDITIONS: **NOTE **:
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   only Football Receipt card has the ability to be added to favourites
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_football_icon_from_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap  'Football' icon from Sports Menu Ribbon
        EXPECTED: 'Football' Landing Page is opened
        """
        pass

    def test_003_tap_anywhere_within_event_section(self):
        """
        DESCRIPTION: Tap anywhere within Event section
        EXPECTED: 'Football' Event Details page is opened
        """
        pass

    def test_004_add_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add selection to the Bet Slip
        EXPECTED: *   the selection is added
        EXPECTED: *   counter of Betslip bubble is increased appropriately
        """
        pass

    def test_005_navigate_to_the_betslip_page(self):
        """
        DESCRIPTION: Navigate to the Betslip page
        EXPECTED: *   Betslip page is opened
        EXPECTED: *   added selection(s) is/are present
        """
        pass

    def test_006_enter_stake_in_stake_field_and_tap_bet_now_button(self):
        """
        DESCRIPTION: Enter stake in 'Stake' field and tap 'Bet Now' button
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   Bet Receipt is shown
        """
        pass

    def test_007_verify_match_center_functionality_on_the_displayed_bet_receipt(self):
        """
        DESCRIPTION: Verify Match Center functionality on the displayed Bet Receipt
        EXPECTED: 'Favourite all' star icon is displayed
        """
        pass

    def test_008_verify_favourite_all_star_icon_after_tapping_on_it(self):
        """
        DESCRIPTION: Verify 'Favourite all' star icon after tapping on it
        EXPECTED: *   all events displayed on the Bet Receipt are added to favourites
        EXPECTED: *   'Favourite all' star icon becomes bold
        EXPECTED: *   star icon(s) next to each event becomes bold
        """
        pass

    def test_009_verify_favourite_all_star_icon_after_tapping_on_it_one_more_time(self):
        """
        DESCRIPTION: Verify 'Favourite all' star icon after tapping on it one more time
        EXPECTED: *   all events displayed on the Bet Receipt are removed from favoruites
        EXPECTED: *   'Favourite all' star icon becomes unselected
        EXPECTED: *   star icon(s) next to each event becomes unselected
        """
        pass

    def test_010_verify_go_betting_button_on_bet_receipt(self):
        """
        DESCRIPTION: Verify 'GO BETTING' button on Bet Receipt
        EXPECTED: *Mobile*:
        EXPECTED: After tapping on 'GO BETTING' button, user is redirected to the page he/she came from
        EXPECTED: *Desktop/Tablet*:
        EXPECTED: Bet Receipt disappears from the Betslip.
        """
        pass
