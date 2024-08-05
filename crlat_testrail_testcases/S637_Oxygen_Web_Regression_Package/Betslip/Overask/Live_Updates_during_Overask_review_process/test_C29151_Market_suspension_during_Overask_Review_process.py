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
class Test_C29151_Market_suspension_during_Overask_Review_process(Common):
    """
    TR_ID: C29151
    NAME: Market suspension during Overask Review process
    DESCRIPTION: This test case verifies Market suspension during Overask Review process
    DESCRIPTION: Edited based on LCRCORE-13090: AS A Trader I NEED a way to prevent any overasked bets on suspended selections from getting accepted through TI
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. User is logged in to the app
    PRECONDITIONS: 3. Overask functionality is enabled for the user
    """
    keep_browser_open = True

    def test_001_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip
        EXPECTED: Selection is successfully added
        """
        pass

    def test_002_enter_stake_value_which_is_higher_then_maximum_limit_for_added_selection(self):
        """
        DESCRIPTION: Enter stake value which is higher then maximum limit for added selection
        EXPECTED: 
        """
        pass

    def test_003_clicktap_bet_now_button(self):
        """
        DESCRIPTION: Click/Tap 'Bet Now' button
        EXPECTED: *   CMS configurable Title and Message for OverAsk are displayed on an overlay on white background anchored to the footer
        EXPECTED: * Mobile: Background is disabled and not clickable, Desktop/Tablet: Widget is disabled and not clickable
        EXPECTED: *   Green (Coral) and black (Ladbrokes) loading spinner is centred and shown between title and text
        EXPECTED: *   'maxAllowed' value is displayed in the text in '£X,XXX' format and comes from OB in 'buildBet' response while adding selection to the bet slip
        """
        pass

    def test_004_while_review_is_pending_trigger_market_suspension_for_selection_under_the_review(self):
        """
        DESCRIPTION: While review is pending trigger market suspension for selection under the review
        EXPECTED: Selection is suspended in the Betslip
        """
        pass

    def test_005_trigger_offer_for_the_selection(self):
        """
        DESCRIPTION: Trigger Offer for the selection
        EXPECTED: * Result is FAIL in the backoffice.
        EXPECTED: * Bet is not placed and a 'This bet has not been accepted by traders!' message is shown on **Bet receipt**.
        EXPECTED: * Selection, Market and Even names are still displayed
        EXPECTED: * 'Stake' field disappears
        EXPECTED: * 'Continue'/'Go betting' button is present ('Reuse Selections' button is absent)
        EXPECTED: * Balance is not reduced
        """
        pass

    def test_006_clicktap_on_continuego_betting_button(self):
        """
        DESCRIPTION: Click/Tap on 'Continue'/'Go Betting' button
        EXPECTED: *   Betslip is cleared automatically
        EXPECTED: *   'You have no selections in the slip' message is shown (tablet, desktop)
        EXPECTED: *   Betslip is closed automatically (mobile)
        """
        pass

    def test_007_repeat_steps_1_4(self):
        """
        DESCRIPTION: Repeat steps 1-4
        EXPECTED: 
        """
        pass

    def test_008_trigger_bet_decline_by_trader(self):
        """
        DESCRIPTION: Trigger bet decline by Trader
        EXPECTED: * Result is FAIL in the backoffice.
        EXPECTED: * Bet is not placed and a 'This bet has not been accepted by traders!' message is shown on **Bet receipt**.
        EXPECTED: * Selection, Market and Even names are still displayed
        EXPECTED: * 'Stake' field disappears
        EXPECTED: * 'Continue'/'Go betting' button is present ('Reuse Selections' button is absent)
        EXPECTED: * Balance is not reduced
        """
        pass

    def test_009_clicktap_on_continuego_betting_button(self):
        """
        DESCRIPTION: Click/Tap on 'Continue'/'Go Betting' button
        EXPECTED: *   Betslip is cleared automatically
        EXPECTED: *   'You have no selections in the slip' message is shown (tablet, desktop)
        EXPECTED: *   Betslip is closed automatically (mobile)
        """
        pass
