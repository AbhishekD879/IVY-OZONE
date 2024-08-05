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
class Test_C28965790_ACCA_9_bet_on_Open_Bets_containing_selection_with_Handicap_value_changed(Common):
    """
    TR_ID: C28965790
    NAME: ACCA 9 bet on Open Bets containing selection with Handicap value changed
    DESCRIPTION: This test case verifies ACCA 9 bet on Open Bets tab when one of selections has handicap value changed.
    DESCRIPTION: Prod Incident: https://jira.egalacoral.com/browse/BMA-47150
    DESCRIPTION: Related test case: https://ladbrokescoral.testrail.com/index.php?/cases/edit/28965790
    PRECONDITIONS: - user is logged in
    PRECONDITIONS: - user has navigated to Football In-Play page
    PRECONDITIONS: - event with handicap market should be available
    PRECONDITIONS: NOTE: For new cashout (CMS -> Cashout'isV4Enabled') use 'bet-details' response to check the bet error.
    """
    keep_browser_open = True

    def test_001_place_acca_9_bet_on_football_in_play_events_one_of_which_contains_handicap_value(self):
        """
        DESCRIPTION: Place ACCA 9 bet on Football In-play events one of which contains HANDICAP value
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_002_navigate_to_open_bets_tab(self):
        """
        DESCRIPTION: Navigate to Open Bets tab
        EXPECTED: - tab is opened
        EXPECTED: - Placed ACCA 9 bet is displayed
        """
        pass

    def test_003_trigger_any_live_update_for_the_bet_and_observe_the_bet__price_change(self):
        """
        DESCRIPTION: Trigger any live update for the bet and observe the bet:
        DESCRIPTION: - price change
        EXPECTED: Bet is still displayed on Open Bets tab and does not disappear (even when update is received)
        """
        pass

    def test_004_trigger_cashout_unavailable_for_the_bet_eg_handicap_value_change_22___122(self):
        """
        DESCRIPTION: Trigger cashout unavailable for the bet (eg. handicap value change: 2.2 -> 12.2)
        EXPECTED: - Bet is still displayed on Open Bets tab and does not disappear even when cashout for bet is unavailable (cashout button is disabled)
        EXPECTED: - Error is received in Network: 'getBetDetail' response:
        EXPECTED: cashoutStatus: "Cashout unavailable: Selections are not available for cashout"
        EXPECTED: cashoutValue: "CASHOUT_SELN_NO_CASHOUT"
        EXPECTED: ![](index.php?/attachments/get/3169181)
        """
        pass
