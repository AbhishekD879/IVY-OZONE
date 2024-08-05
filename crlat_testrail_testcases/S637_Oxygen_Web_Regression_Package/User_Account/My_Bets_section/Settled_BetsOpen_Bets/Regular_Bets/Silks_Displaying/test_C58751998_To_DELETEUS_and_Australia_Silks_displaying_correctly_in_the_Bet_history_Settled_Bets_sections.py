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
class Test_C58751998_To_DELETEUS_and_Australia_Silks_displaying_correctly_in_the_Bet_history_Settled_Bets_sections(Common):
    """
    TR_ID: C58751998
    NAME: [To DELETE]US and Australia Silks displaying correctly in the Bet history/Settled Bets sections.
    DESCRIPTION: This test case Verifies US and Australia Silks displaying correctly in the Bet history/Settled bet section.
    PRECONDITIONS: User is logged in;
    PRECONDITIONS: User has placed Single bet(7,8,9) on Greyhounds races with silks(US or Australia)
    PRECONDITIONS: User has placed Single bet(7,8,9) on Greyhounds races with silks and the bet is already settled(US or Australia)
    PRECONDITIONS: Design - https://app.zeplin.io/project/5ba3a1f77d3b30391d93e665/dashboard?seid=5c1bb70753c672af289b1d3b
    PRECONDITIONS: NOTE: According to the PO, this will be done in scope of the another story
    """
    keep_browser_open = True

    def test_001_navigate_to_bet_history_tab_on_my_bets_pagebet_slip_widgetverify_that_silk_is_displaying_for_single_greyhound_bet(self):
        """
        DESCRIPTION: Navigate to 'Bet History' tab on 'My Bets' page/'Bet Slip' widget
        DESCRIPTION: Verify that Silk is displaying for Single Greyhound bet
        EXPECTED: Correct silk is displayed for placed bet at the left of a Greyhound name
        """
        pass

    def test_002_navigate_to_settled_bets_tab_on_my_bets_pagebet_slip_widgetverify_that_silk_is_displaying_for_single_greyhound_settled_bet(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' tab on 'My Bets' page/'Bet Slip' widget
        DESCRIPTION: Verify that Silk is displaying for Single Greyhound settled bet
        EXPECTED: Correct silk is displayed for settled bet at the left of a Greyhounds name
        """
        pass
