import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.bet_history_open_bets
@vtest
class Test_C28147_Verify_Bet_Details_of_Lotto_bets_on_Settle_Bets(Common):
    """
    TR_ID: C28147
    NAME: Verify Bet Details of 'Lotto' bets on Settle Bets
    DESCRIPTION: This test case verifies 'Lotto' sort filter and bet details for bet lines within
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: *   [BMA- 5880 'Lottery - View history for lottery bets'][1]
    DESCRIPTION: *   [BMA-9153 Add extra filters to Bet History][2]
    DESCRIPTION: *   [BMA-13748 Add Digital Sports Bet History in Oxygen platform][3]
    DESCRIPTION: *   [BMA-12422: Digital Sports - Change name Pick & Mix to Player Bets][4]
    DESCRIPTION: * [BMA-15524: Removing Bet History Download Links from Bet History Pages] [5]
    DESCRIPTION: *   [BMA-24547 RTS: Account history tabs > General view (Bet History / Transactions / Gaming History)] [6]
    DESCRIPTION: * [BMA-24479 Bet History: Lotto Redesign] [7]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-5880
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-9153
    DESCRIPTION: [3]: https://jira.egalacoral.com/browse/BMA-13748
    DESCRIPTION: [4]: https://jira.egalacoral.com/browse/BMA-12422
    DESCRIPTION: [5]: https://jira.egalacoral.com/browse/BMA-15524
    DESCRIPTION: [6]: https://jira.egalacoral.com/browse/BMA-24547
    DESCRIPTION: [7]: https://jira.egalacoral.com/browse/BMA-24479
    PRECONDITIONS: 1. User is logged in.
    PRECONDITIONS: 2. User should have few win/lose/cancelled bets on Lotto i.e. user should place bets on Lotto, which should be settled after that
    PRECONDITIONS: To trigger win/lose/cancelled bets on TST2: http://backoffice-tst2.coral.co.uk/office > Admin> Queries > Lottery bet
    PRECONDITIONS: NOTE: For all configurations on STG2 environment contact UAT team
    """
    keep_browser_open = True

    def test_001_navigate_to_settled_bets_tab_on_my_bets_page_for_mobile(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' tab on 'My Bets' page (for mobile)
        EXPECTED: * 'Settled Bets' page/tab is opened
        EXPECTED: * Win/lose/cancelled/cashed out bet sections are present
        """
        pass

    def test_002_go_to_lotto_sort_filter___verify_bet_details_and_check_if_bet_details_are_same_as_inob_backofficesystem(self):
        """
        DESCRIPTION: Go to 'Lotto' sort filter -> verify bet details and check if bet details are same as in **OB Backoffice** system
        EXPECTED: Bet details are shown:
        EXPECTED: * Lottery Type in the header of the Individual Lotto Bets
        EXPECTED: * Result : pending/won/lost/cancelled/cashed out
        EXPECTED: * In case Bet won: 'You won <currency sign and value>' label right under header, on event card is shown
        EXPECTED: * User's picks : X, x, x, x, x (this section must be repeated as many separate draws the user selected for the bet)
        EXPECTED: * Draw Type : e.g. Monday Draw
        EXPECTED: * Draw Date : date of draw
        EXPECTED: * Stake : stake value
        EXPECTED: * Bet placed at : date of lotto bet placement
        EXPECTED: * Bet Receipt #
        EXPECTED: * Stake: stake value
        EXPECTED: * Returns Details : returns value
        """
        pass

    def test_003_trigger_the_situation_of_winning_a_bet_and_verify_bet_with_status_won_in_settled_betsselect_bet_from_the_list_or_go_directly_to_httpbackoffice_tst2coralcoukadminactionadminbetgoxgamereceiptbetidbet_identer_winning_value(self):
        """
        DESCRIPTION: Trigger the situation of Winning a bet and verify bet with status 'Won' in Settled Bets
        DESCRIPTION: (Select bet from the list or go directly to http://backoffice-tst2.coral.co.uk/admin?action=ADMIN::BET::GoXGameReceipt&BetId=<bet_id>
        DESCRIPTION: Enter winning value)
        EXPECTED: Bet with status 'Won' should be present in Bet History, bet details are correct
        """
        pass

    def test_004_trigger_the_situation_of_losing_a_bet_and_verify_bet_with_lost_in_settled_betsclick_settle_bet_without_entering_any_value(self):
        """
        DESCRIPTION: Trigger the situation of  Losing a bet and verify bet with  'Lost' in Settled Bets
        DESCRIPTION: (Click 'Settle bet' without entering any value)
        EXPECTED: Bet with status 'Lost' should be present in Bet History, bet details are correct
        """
        pass

    def test_005_trigger_the_situation_of_cancelling_a_bet_and_verify_bet_withcancelled_in_settled_betsfill_refund_field_with_a_value__bet_amount(self):
        """
        DESCRIPTION: Trigger the situation of  Cancelling a bet and verify bet with 'Cancelled' in Settled Bets
        DESCRIPTION: (Fill Refund field with a value <= bet amount)
        EXPECTED: Bet with status 'Void' should be present in Bet History, bet details are correct
        """
        pass

    def test_006_trigger_the_situation_of_making_a_bet_void_and_verify_bet_with_void_in_settled_betsclick_void(self):
        """
        DESCRIPTION: Trigger the situation of  making a bet Void and verify bet with  'Void' in Settled Bets
        DESCRIPTION: (Click Void)
        EXPECTED: Bet with status 'Void' should be present in Bet History, bet details are correct
        """
        pass
