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
class Test_C29204375_Single_bet_on_Open_Bets_with_Handicap_value_changed(Common):
    """
    TR_ID: C29204375
    NAME: Single bet on Open Bets with Handicap value changed
    DESCRIPTION: This test case verifies single in-play bet on Open Bets tab when handicap value has changed.
    DESCRIPTION: Prod Incident: https://jira.egalacoral.com/browse/BMA-47150
    PRECONDITIONS: - user is logged in
    PRECONDITIONS: - user has navigated to Football In-Play page
    PRECONDITIONS: - event with handicap market should be available
    PRECONDITIONS: NOTE: For new cashout (CMS -> Cashout'isV4Enabled') use 'bet-details' response to check the bet error.
    """
    keep_browser_open = True

    def test_001_place_single_in_play_bet_which_contains_handicap_value(self):
        """
        DESCRIPTION: Place single in-play bet which contains HANDICAP value
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_002_navigate_to_open_bets_tab(self):
        """
        DESCRIPTION: Navigate to Open Bets tab
        EXPECTED: - tab is opened
        EXPECTED: - Placed bet is displayed
        """
        pass

    def test_003_trigger_cashout_unavailable_for_the_bet_eg_change_handicap_value_from_22___122(self):
        """
        DESCRIPTION: Trigger cashout unavailable for the bet (eg. change handicap value from: 2.2 -> 12.2)
        EXPECTED: - Bet is still displayed on Open Bets tab and does not disappear even when cashout for bet is unavailable (cashout button is disabled)
        EXPECTED: - Error is received in Network: 'getBetDetail' response:
        EXPECTED: cashoutStatus: "Cashout unavailable: Selections are not available for cashout"
        EXPECTED: cashoutValue: "CASHOUT_SELN_NO_CASHOUT"
        EXPECTED: - Bet does not disappear after few seconds
        """
        pass
