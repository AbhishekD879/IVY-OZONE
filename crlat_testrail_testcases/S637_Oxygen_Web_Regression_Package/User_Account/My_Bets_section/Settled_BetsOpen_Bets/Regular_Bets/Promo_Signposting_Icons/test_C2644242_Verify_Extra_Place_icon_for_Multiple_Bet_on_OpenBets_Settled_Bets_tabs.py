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
class Test_C2644242_Verify_Extra_Place_icon_for_Multiple_Bet_on_OpenBets_Settled_Bets_tabs(Common):
    """
    TR_ID: C2644242
    NAME: Verify Extra Place icon for Multiple Bet on OpenBets/Settled Bets tabs
    DESCRIPTION: This test case verifies that the Extra Place icon for Multiple Bet is displayed on the OpenBets/Settled Bets tabs
    PRECONDITIONS: * Signposting toggle is Turn ON in the CMS
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User has placed the following bets:
    PRECONDITIONS: OPEN BETS:
    PRECONDITIONS: (1) Multiple bet for events with Extra Place promo available on **Market level**
    PRECONDITIONS: (2) Multiple bet which consists of the following selections:
    PRECONDITIONS: - event with Extra Place promo available on any level
    PRECONDITIONS: - event without Extra Place promo
    PRECONDITIONS: ALREADY SETTLED BET:
    PRECONDITIONS: (1) Multiple bet for events with Extra Place promo available on **Market level**
    PRECONDITIONS: (2) Multiple bet which consists of the following selections:
    PRECONDITIONS: - event with Extra Place promo available on any level
    PRECONDITIONS: - event without Extra Place promo
    """
    keep_browser_open = True

    def test_001_navigate_to_the_open_bets_tabverify_extra_place_icon_on_the_multiple_bet_1_from_preconditions(self):
        """
        DESCRIPTION: Navigate to the Open Bets tab
        DESCRIPTION: Verify 'Extra Place' icon on the **Multiple bet (1)** from Preconditions
        EXPECTED: * 'Extra Place' icon and label are displayed below each selection
        EXPECTED: * 'Extra Place' icon and label are aligned to the left
        """
        pass

    def test_002_verify_extra_place_icon_on_the_multiple_bet_2_from_preconditions(self):
        """
        DESCRIPTION: Verify 'Extra Place' icon on the **Multiple bet (2)** from Preconditions
        EXPECTED: * 'Extra Place' and label are displayed only below selection from event with Extra Place promo available
        EXPECTED: * There is no 'Extra Place' icon or and label under the another selection
        """
        pass

    def test_003_navigate_to_settled_bets_tabverify_extra_place_icon_on_the_multiple_bet_1_from_preconditions(self):
        """
        DESCRIPTION: Navigate to Settled Bets tab
        DESCRIPTION: Verify 'Extra Place' icon on the **Multiple bet (1)** from Preconditions
        EXPECTED: * 'Extra Place' icon and label are displayed below each selection
        EXPECTED: * 'Extra Place' icon and label are aligned to the left
        """
        pass

    def test_004_verify_extra_place_icon_on_the_multiple_bet_2_from_preconditions(self):
        """
        DESCRIPTION: Verify 'Extra Place' icon on the **Multiple bet (2)** from Preconditions
        EXPECTED: * 'Extra Place' and label are displayed only under selection from event with Extra Place promo available
        EXPECTED: * There is no 'Extra Place' icon or and label under the another selection
        """
        pass
