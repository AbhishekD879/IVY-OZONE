import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C12600660_Verify_Reuse_Selections_and_Start_Betting_Go_Betting_buttons_on_Bet_Receipt(Common):
    """
    TR_ID: C12600660
    NAME: Verify 'Reuse Selections' and 'Start Betting'/'Go Betting' buttons on Bet Receipt
    DESCRIPTION: This test case verifies 'Reuse Selections' and 'Start Betting'/'Go Betting' buttons on Bet Receipt
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Make sure the user is logged into their account
    PRECONDITIONS: 3. The User's account balance is sufficient to cover a bet stake
    PRECONDITIONS: 4. Make bet placement for several single selections (at least 4)
    PRECONDITIONS: 5. Make sure Bet is placed successfully
    PRECONDITIONS: For <Sport>  it is possible to place a bet from:
    PRECONDITIONS: - event landing page
    PRECONDITIONS: - event details page
    PRECONDITIONS: For <Races> it is possible to place a bet from:
    PRECONDITIONS: - 'Next 4' module
    PRECONDITIONS: - event details page
    """
    keep_browser_open = True

    def test_001_verify_bet_receipt_displaying_after_clickingtapping_the_bet_now_button(self):
        """
        DESCRIPTION: Verify Bet Receipt displaying after clicking/tapping the 'Bet Now' button
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Slip is replaced with a Bet Receipt view
        EXPECTED: * 'Reuse Selections' and 'Go Betting' buttons are present in the bottom area of Bet Receipt
        """
        pass

    def test_002_scroll_the_page_down_and_up(self):
        """
        DESCRIPTION: Scroll the page down and up
        EXPECTED: * Bottom area with 'Reuse Selections' and 'Go Betting' buttons is sticky (for Coral only)
        EXPECTED: * Bottom area with 'Reuse Selections' and 'Go Betting' buttons is NOT sticky (for Ladbrokes only)
        """
        pass

    def test_003_clicktap_reuse_selection_button_on_bet_receipt_page(self):
        """
        DESCRIPTION: Click/Tap 'Reuse Selection' button on Bet Receipt page
        EXPECTED: User is returned to the Betslip to initiate bet placement again on the same selection or selections
        """
        pass

    def test_004_clicktap_go_betting_button_on_bet_receipt_page(self):
        """
        DESCRIPTION: Click/Tap 'Go Betting' button on Bet Receipt page
        EXPECTED: * BetSlip page closes
        EXPECTED: * 'Go Betting' button navigates to the last visited page
        """
        pass
