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
class Test_C2807911_Verify_MoneyBack_icon_for_Multiple_Bet_on_Bet_Receipt(Common):
    """
    TR_ID: C2807911
    NAME: Verify MoneyBack icon for Multiple Bet on Bet Receipt
    DESCRIPTION: This test case verifies that the MoneyBack icon is displayed for Multiple Bet on the Bet Receipt within BetSlip
    PRECONDITIONS: * Signposting toggle is Turn ON in the CMS
    PRECONDITIONS: * User is logged in and has positive balance
    PRECONDITIONS: * MoneyBack promo is available for <Sport> events on Market level
    PRECONDITIONS: * Selection should be added to the BetSlip from events **WITH** MoneyBack promo available and **WITHOUT** as well
    """
    keep_browser_open = True

    def test_001_add_a_couple_of_sport_selection_from_the_preconditions_to_the_betslip(self):
        """
        DESCRIPTION: Add a couple of <Sport> selection from the preconditions to the BetSlip
        EXPECTED: * <Sport> selections are added to the BetSlip
        EXPECTED: * Multiple bets are shown on the BetSlip
        """
        pass

    def test_002_enter_value_in_stake_field_for_one_of_multiple_bet_and_place_a_bet(self):
        """
        DESCRIPTION: Enter value in 'Stake' field for one of **Multiple** bet and place a bet
        EXPECTED: * Multiple Bet is placed successfully
        EXPECTED: * Bet Receipt for Multiple is displayed
        """
        pass

    def test_003_verify_moneyback_icon_on_the_bet_receipt(self):
        """
        DESCRIPTION: Verify 'MoneyBack' icon on the Bet Receipt
        EXPECTED: * 'MoneyBack' icon is displayed under each selection (under market name/event name section) which has 'MoneyBack' available
        """
        pass

    def test_004_repeat_steps_1_3_for_available_moneyback_promo_on_market_level(self):
        """
        DESCRIPTION: Repeat steps 1-3 for available MoneyBack promo on Market level
        EXPECTED: 
        """
        pass
