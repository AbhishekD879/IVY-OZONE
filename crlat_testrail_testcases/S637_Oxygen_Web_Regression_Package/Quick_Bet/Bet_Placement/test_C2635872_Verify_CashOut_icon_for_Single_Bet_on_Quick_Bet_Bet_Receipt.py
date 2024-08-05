import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C2635872_Verify_CashOut_icon_for_Single_Bet_on_Quick_Bet_Bet_Receipt(Common):
    """
    TR_ID: C2635872
    NAME: Verify CashOut icon for Single Bet on Quick Bet Bet Receipt
    DESCRIPTION: This test case verifies that the CashOut icon is displayed on the Bet Receipt within Quick Bet
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: [BMA-35709 CLONE FOR QUICKBET - Promo / Signposting : Cashout Bet Receipt] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-35709
    DESCRIPTION: [BMA-36231 Promo / Signposting: Quick Ber for CashOut] [2]
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-36231
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * User is logged in and has positive balance
    PRECONDITIONS: * CashOut should be available for bet on all levels (category/type/event/market)
    """
    keep_browser_open = True

    def test_001_add_selection_with_available_cashout_to_the_quick_bet(self):
        """
        DESCRIPTION: Add selection with available CashOut to the Quick Bet
        EXPECTED: * Selection is added to the Quick Bet
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
        EXPECTED: * CashOut icon is displayed below market name/event name section
        EXPECTED: ![](index.php?/attachments/get/53285820)
        EXPECTED: ![](index.php?/attachments/get/53285822)
        """
        pass
