import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.bet_history_open_bets
@vtest
class Test_C238150_Verify_Int_Tote_Bet_Details_on_Open_Bets(Common):
    """
    TR_ID: C238150
    NAME: Verify Int Tote Bet Details on Open Bets
    DESCRIPTION: This test case verifies 'Open Bets' tab when user Logged In for 'Pools' for International Tote events
    PRECONDITIONS: 1. User should be logged in
    PRECONDITIONS: 2. User should have 'Pending' bets on Pools  i.e. user placed bets on International Tote events
    PRECONDITIONS: 1) In order to view details for bets search for Request to Proxy:
    PRECONDITIONS: accountHistory?poolBetId={PoolID}
    PRECONDITIONS: 2) In order to view collapsed pools info search for Request to Proxy:
    PRECONDITIONS: accountHistory?fromDate={XXXX-XX-X1+00:00:00}&group=POOLBET&pagingBlockSize=20&toDate={XXXX-XX-X2+00:00:00}
    """
    keep_browser_open = True

    def test_001_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My Bets' item on Top Menu
        EXPECTED: *  'My Bets' page/'Bet Slip' widget is shown
        EXPECTED: *  'Open Bets' tab is shown next to 'Cash Out' tab
        """
        pass

    def test_002_tap_open_bets_tab(self):
        """
        DESCRIPTION: Tap 'Open Bets' tab
        EXPECTED: *  'Regular', 'Player Bets', 'Lotto' and 'Pools' sort filters are shown
        EXPECTED: *  'Regular' sort filter is selected by default
        """
        pass

    def test_003_navigate_to_pools_and_check_content_within(self):
        """
        DESCRIPTION: Navigate to 'Pools' and check content within
        EXPECTED: 1. All '**Pending bets**' sections are displayed chronologically (**'settled=N'** attribute is set for all displayed bets (from response select 'Network' tab-> 'All' filter -> choose the request described in 2 point in preconditions->'Preview' tab))
        EXPECTED: 2. All sections are collapsed by default
        EXPECTED: 3. If there are more than 20 events, they should be loaded after scrolling by portions (20 events by portion)
        """
        pass

    def test_004_search_for_international_tote_bet_and_collapseexpand_this_bet(self):
        """
        DESCRIPTION: Search for International Tote bet and Collapse/expand this bet
        EXPECTED: It is possible to collapse/expand bet section
        """
        pass

    def test_005_verify_collapsed_view(self):
        """
        DESCRIPTION: Verify collapsed view
        EXPECTED: Must Display:
        EXPECTED: - date and time the bet was placed
        EXPECTED: - Selection name
        EXPECTED: - Event name
        EXPECTED: - Meeting Name
        EXPECTED: - Pool Type
        EXPECTED: - Unit and Total Stake
        EXPECTED: - Status icon
        """
        pass

    def test_006_verify_expanded_view(self):
        """
        DESCRIPTION: Verify expanded view
        EXPECTED: Must display:
        EXPECTED: - Bet Receipt #
        EXPECTED: - Selection name
        EXPECTED: - Event name
        EXPECTED: - Meeting Name
        EXPECTED: - Pool Type
        EXPECTED: - Event Start time
        EXPECTED: - Result
        """
        pass

    def test_007_check_the_correctness_of_result_field_point_1_in_preconditions(self):
        """
        DESCRIPTION: Check the correctness of <Result> field (point 1 in preconditions)
        EXPECTED: PoolLeg-> poolPart->outcome
        EXPECTED: verify the outcomeResult value
        """
        pass

    def test_008_trigger_the_situation_of_winning_a_bet_and_verify_if_bet_is_disappeared_from_open_bets_after_refresh(self):
        """
        DESCRIPTION: Trigger the situation of Winning a bet and verify if bet is disappeared from 'Open Bets' after refresh
        EXPECTED: Bet  with status 'Won' is NOT displayed in 'Open Bets' tab
        """
        pass

    def test_009_trigger_the_situation_of_losing_a_bet_and_verify_if_bet_is_disappeared_from_open_bets_after_refresh(self):
        """
        DESCRIPTION: Trigger the situation of Losing a bet and verify if bet is disappeared from 'Open Bets' after refresh
        EXPECTED: Bet with status 'Lost' is NOT displayed in 'Open Bets' tab
        """
        pass

    def test_010_trigger_the_situation_of_cancelling_a_bet_and_verify_if_bet_is_disappeared_from_open_bets_after_refresh(self):
        """
        DESCRIPTION: Trigger the situation of Cancelling a bet and verify if bet is disappeared from 'Open Bets' after refresh
        EXPECTED: Bet with status 'Cancelled' is NOT displayed in 'Open Bets' tab
        """
        pass
