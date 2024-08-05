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
class Test_C29132_Request_expires_without_Traders_Offer(Common):
    """
    TR_ID: C29132
    NAME: Request expires without Trader's Offer
    DESCRIPTION: JIRA Tickets:
    DESCRIPTION: BMA-6573 Overask - Pending requests
    DESCRIPTION: BMA-20390 New Betslip - Overask design improvements
    DESCRIPTION: Note: Cannot automate as we cannot wait 10 min in test (time for request to expire without trader's action)
    PRECONDITIONS: 1. User is logged in to application
    PRECONDITIONS: 2. Overask functionality is enabled for the user
    PRECONDITIONS: NOTE: System always automatically declined bet during testing
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
        EXPECTED: *   'Please wait, your bet is being reviewed by one of our Traders. This normally takes less than a minute.' message is displayed above 'Bet now' button with yellow background
        EXPECTED: *   'Stake' field becomes disabled
        EXPECTED: *   'Clear Betslip' and 'Bet Now' buttons become disabled
        EXPECTED: *   Loading spinner is shown on green button, replacing 'Bet Now' label
        """
        pass

    def test_004_wait_till_the_request_expires_without_traders_offer_for_max_bet(self):
        """
        DESCRIPTION: Wait till the Request expires without Trader's Offer for Max Bet
        EXPECTED: 
        """
        pass

    def test_005_verify_state_of_selection_which_triggered_the_overask_after_request_expires(self):
        """
        DESCRIPTION: Verify state of selection which triggered the Overask after Request expires.
        EXPECTED: *   The System sends an automatic Max Bet offer to the User
        EXPECTED: *   Unchecked checkboxes are displayed in order to allow the User to accept the offer
        EXPECTED: *   Confirm button is present, but inactive (e.g. greyed out)
        EXPECTED: *   The Stake field is displaying the new value in green, to bring user's attention
        """
        pass

    def test_006_verify_state_of_other_selections_which_did_not_trigger_the_overask_after_requets_expires_without_traders_offer_for_max_bet(self):
        """
        DESCRIPTION: Verify state of other selections which did not trigger the Overask after requets expires without  Trader's Offer for Max Bet
        EXPECTED: *   The Checkboxes for the Selections that did not trigger the Overask automatically enabled
        EXPECTED: *   'Confirm' button is active, in order to allow the user to place these bets normally
        """
        pass
