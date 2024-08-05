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
class Test_C2635878_Need_to_be_updatedVerify_CashOut_icon_for_Single_Bet_on_BetSlip_and_Bet_Receipt(Common):
    """
    TR_ID: C2635878
    NAME: [Need to be updated]Verify CashOut icon for Single Bet on BetSlip and Bet Receipt
    DESCRIPTION: [Need to be updated step 1]
    DESCRIPTION: [10:17 AM] Amit Bhardwaj
    DESCRIPTION: Hi mate, I think we took out Cashout icons
    DESCRIPTION: ​[10:17 AM] Amit Bhardwaj
    DESCRIPTION: As we offer Cashout on everything and all customers are aware about it
    DESCRIPTION: This test case verifies that the CashOut icon is displayed on the Betslip and Bet Receipt within BetSlip for Single Bet
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: [BMA-33418 Promo / Signposting : Cashout Bet Receipt] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-33418
    DESCRIPTION: [BMA-33416 / Promo / Signposting : Cashout : Bet Slip] [2]
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-33416
    PRECONDITIONS: * User is logged in and has positive balance
    PRECONDITIONS: * CashOut should be available for bet on all levels (category/type/event/market)
    """
    keep_browser_open = True

    def test_001_add_selection_with_available_cashout_to_the_betslipquickbet_for_mobile(self):
        """
        DESCRIPTION: Add selection with available CashOut to the BetSlip/Quickbet (for mobile)
        EXPECTED: * Selection is added to the BetSlip/Quickbet (for mobile)
        EXPECTED: * CashOut icon is displayed between event name and Stake section
        EXPECTED: * CashOut icon stays displayed at all times even when selection details are minimized/maximized
        """
        pass

    def test_002_enter_value_in_stake_field_and_place_a_bet(self):
        """
        DESCRIPTION: Enter value in 'Stake' field and place a bet
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is displayed
        """
        pass

    def test_003_verify_cashout_icon_on_the_bet_receipt(self):
        """
        DESCRIPTION: Verify CashOut icon on the Bet Receipt
        EXPECTED: * CashOut icon is displayed below Market name/Event name section
        """
        pass

    def test_004__place_bet_on_horse_racing_selection_that_has_both_cash_out_and_eachway_odds_available_verify_cashout_icon_on_the_bet_receipt(self):
        """
        DESCRIPTION: * Place bet on Horse Racing selection that has both cash out and Each/Way Odds available
        DESCRIPTION: * Verify CashOut icon on the Bet Receipt
        EXPECTED: * CashOut icon is displayed below Each/Way Odds
        """
        pass

    def test_005_repeat_steps_1_4_with_multiple_selections_with_cashout_disabled_at_eventselection_level(self):
        """
        DESCRIPTION: Repeat steps 1-4 with multiple selections with CashOut disabled at event/selection level
        EXPECTED: * Cashout icon is not displayed on Betslip/Quickbet (for mobile)
        EXPECTED: * Cashout icon is not displayed on Bet Receipt
        """
        pass
