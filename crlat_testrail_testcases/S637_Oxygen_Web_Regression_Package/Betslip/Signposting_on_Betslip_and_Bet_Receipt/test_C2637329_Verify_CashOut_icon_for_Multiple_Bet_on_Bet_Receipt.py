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
class Test_C2637329_Verify_CashOut_icon_for_Multiple_Bet_on_Bet_Receipt(Common):
    """
    TR_ID: C2637329
    NAME: Verify CashOut icon for Multiple Bet on Bet Receipt
    DESCRIPTION: This test case verifies that the CashOut icon is displayed on the Bet Receipt for Multiple Bet
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: [BMA-33418 Promo / Signposting : Cashout Bet Receipt] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-33418
    DESCRIPTION: [BMA-33416 / Promo / Signposting : Cashout : Bet Slip] [2]
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-33416
    PRECONDITIONS: * User is logged in and has positive balance
    PRECONDITIONS: * CashOut should be available for all selections on all levels (category/type/event/market)
    """
    keep_browser_open = True

    def test_001_add_multiple_selection_with_available_cashout_to_the_betslip(self):
        """
        DESCRIPTION: Add multiple selection with available CashOut to the BetSlip
        EXPECTED: * Selection is added to the BetSlip
        EXPECTED: * Multiple bets are shown on the BetSlip
        EXPECTED: * CashOut icon is displayed between event name and Stake section for each selection in the Singles section
        EXPECTED: * CashOut icon stays displayed at all times even when selection details are minimized/maximized
        EXPECTED: * CashOut icon is displayed under the Bet Type for each Bet type in the Multiples section
        """
        pass

    def test_002_enter_value_in_stake_field_for_one_of_multiple_bet_and_place_a_bet(self):
        """
        DESCRIPTION: Enter value in 'Stake' field for one of **Multiple** bet and place a bet
        EXPECTED: * Multiple Bet is placed successfully
        EXPECTED: * Bet Receipt for Multiple bet is displayed
        """
        pass

    def test_003_verify_cashout_icon_on_the_bet_receipt(self):
        """
        DESCRIPTION: Verify CashOut icon on the Bet Receipt
        EXPECTED: * CashOut icon is displayed below Market name/Event name section (or below each/way odds if available)
        EXPECTED: * CashOut icon is displayed ONLY ONCE, below the last selection
        """
        pass

    def test_004_repeat_steps_1_3_with_multiple_selections_with_cashout_disabled_at_eventselection_level(self):
        """
        DESCRIPTION: Repeat steps 1-3 with multiple selections with CashOut disabled at event/selection level
        EXPECTED: * Cashout icon is not displayed on Betslip
        EXPECTED: * Cashout icon is not displayed on Bet Receipt
        """
        pass
