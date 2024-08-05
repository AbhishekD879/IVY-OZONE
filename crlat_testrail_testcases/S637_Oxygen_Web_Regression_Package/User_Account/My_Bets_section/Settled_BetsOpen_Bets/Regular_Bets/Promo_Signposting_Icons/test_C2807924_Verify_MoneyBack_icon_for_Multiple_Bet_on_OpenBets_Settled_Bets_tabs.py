import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C2807924_Verify_MoneyBack_icon_for_Multiple_Bet_on_OpenBets_Settled_Bets_tabs(Common):
    """
    TR_ID: C2807924
    NAME: Verify MoneyBack icon for Multiple Bet on OpenBets/Settled Bets tabs
    DESCRIPTION: This test case verifies that the MoneyBack icon for Multiple Bet is displayed on the OpenBets/Settled Bets tabs
    DESCRIPTION: MoneyBack icon is configurable in TI on Market level only
    PRECONDITIONS: * Signposting toggle is Turn ON in the CMS
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User has placed the following bets:
    PRECONDITIONS: OPEN BETS:
    PRECONDITIONS: (1) Multiple bet for events with MoneyBack promo available on **Market level**
    PRECONDITIONS: (2) Multiple bet which consists of the following selections:
    PRECONDITIONS: - event with MoneyBack promo
    PRECONDITIONS: - event without MoneyBack promo
    PRECONDITIONS: ALREADY SETTLED BET:
    PRECONDITIONS: (1) Multiple bet for events with MoneyBack promo available on **Market level**
    PRECONDITIONS: (2) Multiple bet which consists of the following selections:
    PRECONDITIONS: - event with MoneyBack promo available
    PRECONDITIONS: - event without MoneyBack promo
    """
    keep_browser_open = True

    def test_001_navigate_to_the_open_bets_tabverify_moneyback_icon_on_the_multiple_bet_1_from_preconditions(self):
        """
        DESCRIPTION: Navigate to the **Open Bets tab**
        DESCRIPTION: Verify 'MoneyBack' icon on the Multiple bet (1) from Preconditions
        EXPECTED: * 'MoneyBack' icon and label are displayed under each selection
        EXPECTED: * 'MoneyBack' icon and label are aligned to the left
        EXPECTED: ![](index.php?/attachments/get/53285775)
        EXPECTED: ![](index.php?/attachments/get/53285781)
        """
        pass

    def test_002_verify_moneyback_icon_on_the_multiple_bet_2_from_preconditions(self):
        """
        DESCRIPTION: Verify 'MoneyBack' icon on the Multiple bet (2) from Preconditions
        EXPECTED: * 'MoneyBack' and label are displayed only under selection from event with MoneyBack promo available
        EXPECTED: * There is no 'MoneyBack' icon or and label under the another selection
        EXPECTED: ![](index.php?/attachments/get/53285776)
        EXPECTED: ![](index.php?/attachments/get/53285782)
        """
        pass

    def test_003_navigate_to_settled_betsy_tabverify_moneyback_icon_on_the_multiple_bet_1_from_preconditions(self):
        """
        DESCRIPTION: Navigate to Settled Betsy tab
        DESCRIPTION: Verify 'MoneyBack' icon on the Multiple bet (1) from Preconditions
        EXPECTED: * 'MoneyBack' icon and label are displayed under each selection
        EXPECTED: * 'MoneyBack' icon and label are aligned to the left
        EXPECTED: ![](index.php?/attachments/get/53285778)
        EXPECTED: ![](index.php?/attachments/get/53285784)
        """
        pass

    def test_004_verify_moneyback_icon_on_the_multiple_bet_2_from_preconditions(self):
        """
        DESCRIPTION: Verify 'MoneyBack' icon on the Multiple bet (2) from Preconditions
        EXPECTED: * 'MoneyBack' and label are displayed only under selection from event with MoneyBack promo available
        EXPECTED: * There is no 'MoneyBack' icon or and label under the another selection
        EXPECTED: ![](index.php?/attachments/get/53285779)
        EXPECTED: ![](index.php?/attachments/get/53285783)
        """
        pass
