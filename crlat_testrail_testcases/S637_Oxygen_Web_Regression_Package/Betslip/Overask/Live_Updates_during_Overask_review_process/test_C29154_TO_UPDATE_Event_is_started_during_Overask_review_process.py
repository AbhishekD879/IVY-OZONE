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
class Test_C29154_TO_UPDATE_Event_is_started_during_Overask_review_process(Common):
    """
    TR_ID: C29154
    NAME: TO UPDATE Event is started during Overask review process
    DESCRIPTION: This test case verifies start of event during Overask review process
    DESCRIPTION: JIRA Tickets:
    DESCRIPTION: BMA-9501 Overask: Price change/ Suspension  when bet is with the trader
    DESCRIPTION: BMA-20390 New Betslip - Overask design improvements
    PRECONDITIONS: 1. User is logged in to application
    PRECONDITIONS: 2. Overask functionality is enabled for the user
    PRECONDITIONS: TO UPDATE according to new design and suspension flow
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

    def test_003_tap_bet_now_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' button
        EXPECTED: *   'Please wait, your bet is being reviewed by one of our Traders. This normally takes less than a minute.' message is displayed on yellow background anchored to the footer
        EXPECTED: *   Loading spinner is shown on the green button, replacing 'Bet Now' label
        EXPECTED: *   'Clear Betslip' and 'Bet Now' buttons become disabled
        EXPECTED: *   'Stake' field becomes disabled
        EXPECTED: **From OX 99**
        EXPECTED: *   CMS configurable Title and Message for OverAsk are displayed on an overlay on white background anchored to the footer
        EXPECTED: * Mobile: Background is disabled and not clickable, Desktop/Tablet: Widget is disabled and not clickable
        EXPECTED: *   Green (Coral) and black (Ladbrokes) loading spinner is centred and shown between title and text
        EXPECTED: *   'maxAllowed' value is displayed in the text in '£X,XXX' format and comes from OB in 'buildBet' response while adding selection to the bet slip
        """
        pass

    def test_004_while_review_is_pending_trigger_event_start_for_selection_under_review(self):
        """
        DESCRIPTION: While review is pending trigger event start for selection under review
        EXPECTED: *   Message about event start is NOT displayed on Betslip
        EXPECTED: *   Selection is NOT suspended
        """
        pass

    def test_005_trigger_offer_for_the_selection(self):
        """
        DESCRIPTION: Trigger Offer for the selection
        EXPECTED: *   Offer is displayed for the user with 'Accept & Bet ([number of accepted bets])' and 'Cancel' buttons
        EXPECTED: *   Selection is NOT suspended
        """
        pass

    def test_006_confirm_offer_from_the_trader(self):
        """
        DESCRIPTION: Confirm Offer from the Trader
        EXPECTED: Bet for the selection is placed successfully
        """
        pass

    def test_007_repeat_steps_1_5(self):
        """
        DESCRIPTION: Repeat steps 1-5
        EXPECTED: 
        """
        pass

    def test_008_cancel_the_offer_from_the_trader(self):
        """
        DESCRIPTION: Cancel the Offer from the Trader
        EXPECTED: *   Bet is not placed
        EXPECTED: *   Selection is still displayed in Betslip
        EXPECTED: *   Message about event start is displayed
        EXPECTED: *   Selection and all buttons are disabled
        """
        pass

    def test_009_repeat_steps_1_5(self):
        """
        DESCRIPTION: repeat steps 1-5
        EXPECTED: 
        """
        pass

    def test_010_trigger_bet_decline_by_trader(self):
        """
        DESCRIPTION: Trigger Bet decline by Trader
        EXPECTED: *   Message about bet decline is displayed in Betslip with 'Continue' button
        EXPECTED: *   Selection is NOT suspended
        """
        pass

    def test_011_tapclick_on_continue_button(self):
        """
        DESCRIPTION: Tap/click on 'Continue' button
        EXPECTED: Selection is removed from Betslip
        """
        pass
