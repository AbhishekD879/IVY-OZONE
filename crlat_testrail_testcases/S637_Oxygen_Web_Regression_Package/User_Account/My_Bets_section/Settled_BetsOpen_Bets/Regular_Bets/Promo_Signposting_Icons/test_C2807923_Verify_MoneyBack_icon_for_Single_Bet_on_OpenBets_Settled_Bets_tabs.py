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
class Test_C2807923_Verify_MoneyBack_icon_for_Single_Bet_on_OpenBets_Settled_Bets_tabs(Common):
    """
    TR_ID: C2807923
    NAME: Verify MoneyBack icon for Single Bet on OpenBets/Settled Bets tabs
    DESCRIPTION: This test case verifies that the MoneyBack icon for Single Bet is displayed on the OpenBets/Settled Bets tabs
    PRECONDITIONS: * Signposting toggle is Turn ON in the CMS
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * MoneyBack promo is available for <Sports> event on Event level, User has placed Single bet on this event
    PRECONDITIONS: * MoneyBack promo is available for <Sports> event on Market level, User has placed Single bet on this market
    PRECONDITIONS: * MoneyBack promo is available for <Sports> event on Event level, User has placed Single bet on this event and this **EVENT IS SETTLED**
    PRECONDITIONS: * MoneyBack promo is available for <Sports> event on Market level, User has placed Single bet on this market and this **MARKET IS SETTLED**
    """
    keep_browser_open = True

    def test_001_navigate_to_the_open_bets_tab(self):
        """
        DESCRIPTION: Navigate to the **Open Bets tab**
        EXPECTED: * Open Bets tab is opened
        EXPECTED: * **NOT SETTLED** Single bets from precondition are presents on OpenBet tab
        """
        pass

    def test_002_verify_moneyback_icon_on_the_single_bet_for_event_with_moneyback_promo_available_on_event_level(self):
        """
        DESCRIPTION: Verify 'MoneyBack' icon on the Single bet for event with MoneyBack promo available on **Event level**
        EXPECTED: * 'MoneyBack' icon and label are NOT displayed between event name and Stake info
        """
        pass

    def test_003_verify_moneyback_icon_on_the_single_bet_for_event_with_moneyback_promo_available_on_market_level(self):
        """
        DESCRIPTION: Verify 'MoneyBack' icon on the Single bet for event with MoneyBack promo available on **Market level**
        EXPECTED: * 'MoneyBack' icon and label are displayed between event name and Stake info
        EXPECTED: * 'MoneyBack' icon and label are aligned to the left
        """
        pass

    def test_004_navigate_to_the_settled_bets_tab(self):
        """
        DESCRIPTION: Navigate to the **Settled Bets tab**
        EXPECTED: * Bet History tab is opened
        EXPECTED: * **SETTLED** Single bets from precondition are presents on Bet History tab
        """
        pass

    def test_005_verify_moneyback_icon_on_the_single_bet_for_event_with_moneyback_promo_available_on_event_level(self):
        """
        DESCRIPTION: Verify 'MoneyBack' icon on the Single bet for event with MoneyBack promo available on **Event level**
        EXPECTED: * 'MoneyBack' icon and label are NOT displayed between event name and Stake info
        """
        pass

    def test_006_verify_moneyback_icon_on_the_single_bet_for_event_with_moneyback_promo_available_on_market_level(self):
        """
        DESCRIPTION: Verify 'MoneyBack' icon on the Single bet for event with MoneyBack promo available on **Market level**
        EXPECTED: * 'MoneyBack' icon and label are displayed between event name and Stake info
        EXPECTED: * 'MoneyBack' icon and label are aligned to the left
        """
        pass
