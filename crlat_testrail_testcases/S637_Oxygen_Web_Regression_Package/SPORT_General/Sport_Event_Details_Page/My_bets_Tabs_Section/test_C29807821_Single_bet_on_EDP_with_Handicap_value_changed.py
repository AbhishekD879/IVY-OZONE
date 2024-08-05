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
class Test_C29807821_Single_bet_on_EDP_with_Handicap_value_changed(Common):
    """
    TR_ID: C29807821
    NAME: Single bet on EDP with Handicap value changed
    DESCRIPTION: This test case verifies single in-play bet view on sport EDP after handicap value has changed
    DESCRIPTION: Prod Incident: https://jira.egalacoral.com/browse/BMA-47150
    DESCRIPTION: Related test case: https://ladbrokescoral.testrail.com/index.php?/cases/edit/28965790
    PRECONDITIONS: - user is logged in
    PRECONDITIONS: - user has navigated to Football In-Play page
    PRECONDITIONS: - event with handicap market should be available
    PRECONDITIONS: - user has placed football single in-play bet with handicap value
    PRECONDITIONS: NOTE: For new cashout (CMS -> Cashout'isV4Enabled') use 'bet-details' response to check the bet error.
    PRECONDITIONS: **From release XXX.XX (according to BMA-50940/BMA-50937/BMA-50936):**
    PRECONDITIONS: - WebSocket connection to Cashout MS is created when user lands on EPD of event, user has placed bets
    """
    keep_browser_open = True

    def test_001_navigate_to_football_edp_of_bet_placed_from_preconditions_to_my_bets_tab(self):
        """
        DESCRIPTION: Navigate to Football EDP of bet placed (from preconditions), to 'My Bets' tab
        EXPECTED: Bet placed is shown within the tab content
        EXPECTED: **From release XXX.XX:**
        EXPECTED: WebSocket connection to Cashout MS is created
        """
        pass

    def test_002_trigger_cashout_unavailable_for_the_bet_eg_handicap_value_change_22___122(self):
        """
        DESCRIPTION: Trigger cashout unavailable for the bet (eg. handicap value change: 2.2 -> 12.2)
        EXPECTED: - Bet is still displayed on My Bets tab and does not disappear even when cashout for bet is unavailable (cashout button is disabled)
        EXPECTED: - Error is received in Network: 'getBetDetail' response: cashoutStatus: "Cashout unavailable: Selections are not available for cashout" cashoutValue: "CASHOUT_SELN_NO_CASHOUT"
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * Bet is still displayed on My Bets tab and does not disappear even when cashout for bet is unavailable (cashout button is removed)
        EXPECTED: * cashoutStatus: "Cashout unavailable: Selections are not available for cashout" and cashoutValue: "CASHOUT_HCAP_CHANGED" are received in betUpdate
        EXPECTED: ![](index.php?/attachments/get/118215542)
        """
        pass
