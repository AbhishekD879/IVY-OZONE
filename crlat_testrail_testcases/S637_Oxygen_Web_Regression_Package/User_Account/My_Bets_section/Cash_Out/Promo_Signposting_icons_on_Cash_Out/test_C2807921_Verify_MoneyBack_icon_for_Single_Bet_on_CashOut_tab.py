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
class Test_C2807921_Verify_MoneyBack_icon_for_Single_Bet_on_CashOut_tab(Common):
    """
    TR_ID: C2807921
    NAME: Verify MoneyBack icon for Single Bet on CashOut tab
    DESCRIPTION: This test case verifies that the MoneyBack icon for Single Bet is displayed on the CashOut tab
    PRECONDITIONS: * Signposting toggle is Turn ON in the CMS
    PRECONDITIONS: * User is logged in and has positive balance
    PRECONDITIONS: * MoneyBack promo is available for <Sports> event on Market lvl.
    PRECONDITIONS: * User has placed a Single bet on event with MoneyBack promo and CashOut available
    """
    keep_browser_open = True

    def test_001_navigate_to_the_cashout_tab(self):
        """
        DESCRIPTION: Navigate to the CashOut tab
        EXPECTED: * CashOut tab is opened
        EXPECTED: * Single bet from precondition is present on CashOut tab
        """
        pass

    def test_002_verify_moneyback_icon_on_the_single_bet_for_event_with_moneyback_promo_available_on_market_level(self):
        """
        DESCRIPTION: Verify 'MoneyBack' icon on the Single bet for event with MoneyBack promo available on **Market level**
        EXPECTED: * 'MoneyBack' icon and label are displayed between bet type (e.g. Single) and event name
        EXPECTED: * 'MoneyBack' icon and label are aligned to the left
        """
        pass
