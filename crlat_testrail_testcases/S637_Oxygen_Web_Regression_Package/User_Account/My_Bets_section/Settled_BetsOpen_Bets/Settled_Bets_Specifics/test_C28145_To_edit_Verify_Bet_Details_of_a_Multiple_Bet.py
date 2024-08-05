import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.bet_history_open_bets
@vtest
class Test_C28145_To_edit_Verify_Bet_Details_of_a_Multiple_Bet(Common):
    """
    TR_ID: C28145
    NAME: [To edit] Verify Bet Details of a Multiple Bet
    DESCRIPTION: Steps 6,7,8,9 looks like invalid, need to be clarified
    DESCRIPTION: This test case verifies Bet Details of a Multiple Bet
    PRECONDITIONS: 1. User should be logged in to view their settled bets.
    PRECONDITIONS: 2. User should have few open/won/settled/void/cashed out Multiples bets
    PRECONDITIONS: 3. User should have Multiples bets that were reviewed by Overask functionality (rejected, offered and so on)
    """
    keep_browser_open = True

    def test_001_navigate_to_settled_bets_tab_on_my_bets_page(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' tab on 'My Bets' page
        EXPECTED: * 'Settled' page is opened with 'Settled Bets' header and Back button
        EXPECTED: *  Open/won/settled/void/cashed out bet sections are present
        """
        pass

    def test_002_verify_bet_details_of_a_won_multiple_bet(self):
        """
        DESCRIPTION: Verify bet details of a **WON** Multiple bet
        EXPECTED: **For** **98** **Release**:
        EXPECTED: * "WON" status is shown in the top right corner of the section
        EXPECTED: * All selections have "WON" indicators next to them
        EXPECTED: Bet details are correct:
        EXPECTED: * Bet type (Multiple)
        EXPECTED: * Selection name user has bet on
        EXPECTED: * Odds of selection
        EXPECTED: * Market name user has bet on - e.g., "Match Result & Both Teams to Score"
        EXPECTED: * Event name
        EXPECTED: * Event match clock/"Live" label, live scores, "Watch live" icon (if available)
        EXPECTED: * Date when bet was placed
        EXPECTED: * Bet Receipt number
        EXPECTED: * Stake <currency symbol> <value> (e.g., £10.00)
        EXPECTED: * Est. Returns <currency symbol> <value> (e.g., £30.00)
        EXPECTED: **For** **99** **Release**:
        EXPECTED: * "WON" status is shown in the top right corner of the section
        EXPECTED: * 'You won <currency sign and value>' label right under header, on top of event card is shown
        EXPECTED: * All selections have "green tick" icons on the left to them
        EXPECTED: Bet details are correct:
        EXPECTED: * Bet type (Multiple)
        EXPECTED: * Selection name user has bet on
        EXPECTED: * Odds of selection displayed through @ symbol next to selection name (eg. Home@1/4)
        EXPECTED: * Market name user has bet on - e.g., "Match Result & Both Teams to Score"
        EXPECTED: * Event name
        EXPECTED: * Event match time next to event name
        EXPECTED: * Stake <currency symbol> <value> (e.g., £10.00) in the card footer
        EXPECTED: * Est. Returns <currency symbol> <value> (e.g., £30.00) next to stake value
        EXPECTED: * Bet Receipt number and date of placing the bet
        """
        pass

    def test_003_verify_bet_details_of_a_lost_multiple_bet(self):
        """
        DESCRIPTION: Verify bet details of a **LOST** Multiple bet
        EXPECTED: **For** **98** **Release**:
        EXPECTED: * "LOST" status is shown in the top right corner of the section
        EXPECTED: * Won selections have "WON" indicators under the odds
        EXPECTED: * Lost selections have "LOST" indicators under the odds
        EXPECTED: * In case selection does not resulted  - No label is shown
        EXPECTED: Bet details are correct: same as in Step#2
        EXPECTED: **For** **99** **Release**:
        EXPECTED: * "LOST" status is shown in the top right corner of the section
        EXPECTED: * Won selections have "green tick" icons on the left of the selection
        EXPECTED: * Lost selections have "red cross" icons on the left of the selection
        EXPECTED: * In case selection is not resulted  - No label is shown
        EXPECTED: Bet details are correct: same as in Step#2
        """
        pass

    def test_004_verify_bet_details_of_a_void_multiple_betnote_all_selection_in_the_bet_should_be_resulted(self):
        """
        DESCRIPTION: Verify bet details of a **VOID** Multiple bet
        DESCRIPTION: NOTE: ALL Selection in the bet should be resulted
        EXPECTED: **For** **98** **Release**:
        EXPECTED: * "VOID" status is shown in the top right corner of the section
        EXPECTED: * Won selections have "WON" indicators under the odds
        EXPECTED: * Lost selections have "LOST" indicators under the odds
        EXPECTED: Bet details are correct: same as in Step#2
        EXPECTED: **For** **99** **Release**:
        EXPECTED: * "VOID" status is shown in the top right corner of the section
        EXPECTED: * Won selections have "green tick" icons on the left of the selection
        EXPECTED: * Lost selections have "red cross" icons on the left of the selection
        EXPECTED: Bet details are correct: same as in Step#2
        """
        pass

    def test_005_verify_bet_details_of_a_cashed_out_multiple_bet(self):
        """
        DESCRIPTION: Verify bet details of a **CASHED OUT** Multiple bet
        EXPECTED: * "CASHED OUT" status is shown in the top right corner of the section
        EXPECTED: Bet details are correct: same as in Step#2
        """
        pass

    def test_006_trigger_overask_during_bet_placement_and_reject_a_bet_in_openbet_ti_systemverify_the_bet_on_settled_bets_tab(self):
        """
        DESCRIPTION: Trigger Overask during bet placement and reject a bet in Openbet TI system
        DESCRIPTION: Verify the bet on 'Settled Bets' tab
        EXPECTED: *   Bet with status 'Void' is present in Bet Overview, details are correct
        EXPECTED: *   Rejected bet has 'Status=X' attribute in response
        EXPECTED: *   Bets with  'Status=P' attribute in response are NOT present
        """
        pass

    def test_007_trigger_overask_during_bet_placement_and_offer_max_bet_bet_in_openbet_ti_systemverify_the_bet_on_settled_bets_tab(self):
        """
        DESCRIPTION: Trigger Overask during bet placement and offer max bet bet in Openbet TI system
        DESCRIPTION: Verify the bet on 'Settled Bets' tab
        EXPECTED: *   Bet with status 'Void' is present in Bet Overview, details are correct
        EXPECTED: *   Rejected bet has 'Status=X' attribute in response
        EXPECTED: *   Bets with  'Status=P' attribute in response are NOT present
        """
        pass

    def test_008_trigger_overask_during_bet_placement_and_split_the_bet_in_two_in_openbet_ti_systemverify_the_bet_on_settled_bets_tab(self):
        """
        DESCRIPTION: Trigger Overask during bet placement and split the bet in two in Openbet TI system
        DESCRIPTION: Verify the bet on 'Settled Bets' tab
        EXPECTED: *   Bet with status 'Void' should be present in Bet Overview, details are correct
        EXPECTED: *   Offered the max bet has 'Status=X' attribute in response
        EXPECTED: *   Bets with  'Status=P' attribute in response are NOT present
        EXPECTED: NOTE: If user decides not to select Offered max bet and clicks 'Confirm' button, it means that bet is not placed and not canceled. It is omitted. So in this case bet will not have 'Status=X' attribute in response and it won`t be listed on 'Bet History' tab
        """
        pass

    def test_009_repeat_steps_2_15_for_settled_bets_tab_account_history_page_for_mobile_bet_slip_widget_for_tabletdesktop(self):
        """
        DESCRIPTION: Repeat steps 2-15 for:
        DESCRIPTION: * 'Settled Bets' tab 'Account History' page (for mobile)
        DESCRIPTION: * 'Bet Slip' widget (for Tablet/Desktop)
        EXPECTED: *   Two splited out bets with status 'Void' should be present in Bet Overview, details are correct
        EXPECTED: *   Splited out bets have 'Status=X' attribute in response
        EXPECTED: *   Bets with  'Status=P' attribute in response are NOT present
        EXPECTED: NOTE: If user decides not to select Splited bets and clicks 'Confirm' button, it means that bet is not placed and not canceled. It is omitted. So in this case bet will not have 'Status=X' attribute in response and it won't be listed on 'Bet History' tab
        """
        pass
