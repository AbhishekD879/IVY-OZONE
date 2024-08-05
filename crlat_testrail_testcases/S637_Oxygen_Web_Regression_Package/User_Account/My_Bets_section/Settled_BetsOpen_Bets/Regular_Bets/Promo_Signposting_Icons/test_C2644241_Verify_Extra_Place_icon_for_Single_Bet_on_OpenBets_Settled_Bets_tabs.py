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
class Test_C2644241_Verify_Extra_Place_icon_for_Single_Bet_on_OpenBets_Settled_Bets_tabs(Common):
    """
    TR_ID: C2644241
    NAME: Verify Extra Place icon for Single Bet on OpenBets/Settled Bets tabs
    DESCRIPTION: This test case verifies that the Extra Place icon for Single Bet displayed on the OpenBets/Settled Bets tabs
    DESCRIPTION: Extra Place icon is configurable in TI on Market level only
    PRECONDITIONS: Signposting toggle is Turn ON in the CMS
    PRECONDITIONS: USER is logged in
    PRECONDITIONS: - Extra Place promo is available for <Race> event on Market level, User has placed Single bet on this market
    PRECONDITIONS: - Extra Place promo is available for <Race> event on Market level, User has placed Single bet on this market and this **MARKET IS SETTLED**
    """
    keep_browser_open = True

    def test_001_navigate_to_the_open_bets_tab(self):
        """
        DESCRIPTION: Navigate to the **Open Bets tab**
        EXPECTED: * Open Bets tab is opened
        EXPECTED: * **NOT SETTLED**Single bets from precondition are presents on OpenBet tab
        """
        pass

    def test_002_verify_extra_place_icon_on_the_single_bet_for_event_with_extra_place_promo_available_on_market_level(self):
        """
        DESCRIPTION: Verify 'Extra Place' icon on the Single bet for event with Extra Place promo available on **Market level**
        EXPECTED: * 'Extra Place' icon and label are displayed between event name and Stake info
        EXPECTED: * 'Extra Place' icon and label are aligned to the left
        EXPECTED: ![](index.php?/attachments/get/53285771)
        EXPECTED: ![](index.php?/attachments/get/53285772)
        """
        pass

    def test_003_navigate_to_the_settled_bets_tab(self):
        """
        DESCRIPTION: Navigate to the **Settled Bets tab**
        EXPECTED: * Settled Bets tab is opened
        EXPECTED: * **SETTLED** Single bets from precondition are presents on Settled Bets tab
        """
        pass

    def test_004_verify_extra_place_icon_on_the_single_bet_for_event_with_extra_place_promo_available_on_market_level(self):
        """
        DESCRIPTION: Verify 'Extra Place' icon on the Single bet for event with Extra Place promo available on **Market level**
        EXPECTED: * 'Extra Place' icon and label are displayed between event name and Stake info
        EXPECTED: * 'Extra Place' icon and label are aligned to the left
        EXPECTED: ![](index.php?/attachments/get/53285773)
        EXPECTED: ![](index.php?/attachments/get/53285774)
        """
        pass
