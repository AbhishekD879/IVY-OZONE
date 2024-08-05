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
class Test_C28603_Verify_Favourite_Matches_on_the_Bet_Receipt_page_if_no_Football_Event_is_present(Common):
    """
    TR_ID: C28603
    NAME: Verify 'Favourite Matches' on the Bet Receipt page if no Football Event is present
    DESCRIPTION: This Test Case verified  'Favourite Matches' on the Bet Receipt page if no Football Event is present
    PRECONDITIONS: **JIRA Ticket** :
    PRECONDITIONS: BMA-7800 'Add 'Favourite Match' functionality to Football events on the Betslip'
    PRECONDITIONS: **NOTE **:
    PRECONDITIONS: *   User is logged in
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Home Page is opened
        """
        pass

    def test_002_tap_on_any_sport_icon_not_football_from_the_sports_menu(self):
        """
        DESCRIPTION: Tap on any Sport icon (not Football) from the Sports Menu
        EXPECTED: Sport Landing Page is opened
        """
        pass

    def test_003_add_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add selection to the Bet Slip
        EXPECTED: Selection is added
        """
        pass

    def test_004_navigate_to_the_bet_slip_page(self):
        """
        DESCRIPTION: Navigate to the Bet Slip page
        EXPECTED: -Bet Slip page is open
        EXPECTED: -Selections are present
        """
        pass

    def test_005_enter_stake_in_stake_field_and_tap_bet_now_button(self):
        """
        DESCRIPTION: Enter stake in 'Stake' field and tap 'Bet Now' button
        EXPECTED: -Bet is placed successfully
        EXPECTED: -Bet Receipt is shown
        EXPECTED: -‘Favourite matches’ functionality isn't included
        EXPECTED: -'Add all to favourites' button isn't included
        """
        pass
