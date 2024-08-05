import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C2807922_Verify_MoneyBack_icon_for_Multiple_Bet_on_CashOut_tab(Common):
    """
    TR_ID: C2807922
    NAME: Verify MoneyBack icon for Multiple Bet on CashOut tab
    DESCRIPTION: This test case verifies that the MoneyBack icon for Multiple Bet is displayed on the CashOut tab
    PRECONDITIONS: * Signposting toggle is Turn ON in the CMS
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User has placed the following bets:
    PRECONDITIONS: (1) Multiple bet for events with MoneyBack promo available on **Market level**
    PRECONDITIONS: (2) Multiple bet which consists of the following selections:
    PRECONDITIONS: - event with MoneyBack promo available on Market level
    PRECONDITIONS: - event without MoneyBack promo
    """
    keep_browser_open = True

    def test_001_navigate_to_the_cashout_tab(self):
        """
        DESCRIPTION: Navigate to the CashOut tab
        EXPECTED: * CashOut tab is opened
        EXPECTED: * Multiple bet from precondition is present on CashOut tab
        """
        pass

    def test_002_verify_moneyback_icon_on_the_multiple_bet_1_from_preconditions(self):
        """
        DESCRIPTION: Verify 'MoneyBack' icon on the Multiple bet (1) from Preconditions
        EXPECTED: * 'MoneyBack' icon and text are displayed under each selection
        EXPECTED: * 'MoneyBack' icon and text are aligned to the left
        """
        pass

    def test_003_verify_moneyback_icon_on_the_multiple_bet_2_from_preconditions(self):
        """
        DESCRIPTION: Verify 'MoneyBack' icon on the Multiple bet (2) from Preconditions
        EXPECTED: * 'MoneyBack' and label are displayed only under selection from event with MoneyBack promo available
        EXPECTED: * There is no 'MoneyBack' icon or and label under the another selection
        """
        pass
