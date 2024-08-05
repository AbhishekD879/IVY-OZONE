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
class Test_C2807910_Verify_MoneyBack_icon_for_Single_Bet_on_Bet_Receipt(Common):
    """
    TR_ID: C2807910
    NAME: Verify MoneyBack icon for Single Bet on Bet Receipt
    DESCRIPTION: This test case verifies that the MoneyBack icon is displayed on the Bet Receipt within BetSlip/Quickbet (for mobile)
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: [https://jira.egalacoral.com/browse/BMA-36252]
    PRECONDITIONS: * Signposting toggle is Turn ON in the CMS
    PRECONDITIONS: * User is logged in and has positive balance
    PRECONDITIONS: * MoneyBack promo is available for event on Market level
    """
    keep_browser_open = True

    def test_001_add_selection_with_available_moneyback_promo_on_market_level_to_betslipquickbet_for_mobile(self):
        """
        DESCRIPTION: Add selection with available MoneyBack promo on Market level to betslip/Quickbet (for mobile)
        EXPECTED: Selection is added to the BetSlip
        """
        pass

    def test_002_enter_value_in_stake_field_and_place_a_bet(self):
        """
        DESCRIPTION: Enter value in 'Stake' field and place a bet
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is displayed
        """
        pass

    def test_003_verify_moneyback_icon_on_the_bet_receipt(self):
        """
        DESCRIPTION: Verify 'MoneyBack' icon on the Bet Receipt
        EXPECTED: * 'MoneyBack' icon is located below market name/event name section
        EXPECTED: * If any other signposting are available for the bet they are placed one by one in line with 'Cashout' icon coming first
        """
        pass

    def test_004_add_selection_without_moneyback_promo_available_to_betslipquickbet_for_mobile_and_place_bet(self):
        """
        DESCRIPTION: Add selection without MoneyBack promo available to betslip/Quickbet (for mobile) and place bet
        EXPECTED: There is no 'MoneyBack' icon displayed on bet slip/Quickbet (for mobile).
        """
        pass
