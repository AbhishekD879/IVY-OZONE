import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C44870212_In_play_sports_bet_placement(Common):
    """
    TR_ID: C44870212
    NAME: In-play sports bet placement
    DESCRIPTION: this test case verify - Customer places single, double and complex bets on football, Cricket, Basketball sports verify Accumulator bets,YAN,PAT,TRX,CAN etc complex bet types
    PRECONDITIONS: UserName: goldenbuild1 Password: Password1
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: HomePage opened
        """
        pass

    def test_002_make_sure_the_user_is_logged_into_their_account(self):
        """
        DESCRIPTION: Make sure the user is logged into their account
        EXPECTED: User logged in
        """
        pass

    def test_003_the_users_account_balance_is_sufficient_to_cover_a_bet_stake(self):
        """
        DESCRIPTION: The User's account balance is sufficient to cover a bet stake
        EXPECTED: Header balance displayed sufficient balance
        """
        pass

    def test_004_go_to_football_in_play_event_make_a_selection_and_add_to_betslip(self):
        """
        DESCRIPTION: Go to football In-play event, make a selection and add to betslip
        EXPECTED: Selection added to betslip
        """
        pass

    def test_005_verify_selection_details_in_betslip(self):
        """
        DESCRIPTION: Verify Selection details in betslip
        EXPECTED: Event Name
        EXPECTED: Market Name
        EXPECTED: Event time
        EXPECTED: Odds
        EXPECTED: Sake box
        EXPECTED: Potential retus etc are displayed in betslip
        """
        pass

    def test_006_verify_bet_receipt_displaying_after_clickingtapping_the_place_bet_button_and_verify_bet_is_placed_successfully(self):
        """
        DESCRIPTION: Verify Bet Receipt displaying after clicking/tapping the 'Place Bet' button and verify Bet is placed successfully
        EXPECTED: Bet is placed successfully
        EXPECTED: User 'Balance' is decreased by the value entered in 'Stake' field
        EXPECTED: Bet Slip is replaced with a Bet Receipt view
        """
        pass

    def test_007_verify_bet_receipt_layout(self):
        """
        DESCRIPTION: Verify Bet Receipt layout
        EXPECTED: Bet Receipt header and subheader
        EXPECTED: Card with selections information
        EXPECTED: 'Reuse Selections' and 'Go Betting' buttons
        """
        pass

    def test_008_verify_bet_receipt_header(self):
        """
        DESCRIPTION: Verify Bet Receipt header
        EXPECTED: Bet Receipt header contains the following elements:
        EXPECTED: * 'X' button
        EXPECTED: * 'Bet Receipt' title
        EXPECTED: * 'User Balance' button
        """
        pass

    def test_009_repeat_steps_4_to_8_for_different_in_play_sports_and_multiple__complex_bet(self):
        """
        DESCRIPTION: Repeat steps #4 to #8 for different in-play sports and Multiple & complex bet
        EXPECTED: 
        """
        pass
