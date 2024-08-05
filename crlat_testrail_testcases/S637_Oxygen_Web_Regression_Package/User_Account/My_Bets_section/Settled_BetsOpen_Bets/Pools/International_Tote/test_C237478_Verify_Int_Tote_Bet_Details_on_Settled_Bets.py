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
class Test_C237478_Verify_Int_Tote_Bet_Details_on_Settled_Bets(Common):
    """
    TR_ID: C237478
    NAME: Verify Int Tote Bet Details on Settled Bets
    DESCRIPTION: This test case verifies 'Pools' sort filter and bet details for International Tote pools
    DESCRIPTION: [Need to update according to BMA-24547] Verify Bet Details of 'Pools' bets (International Tote Pools)
    PRECONDITIONS: User should be logged in
    PRECONDITIONS: User should make bets on International Tote Pools with **'Status'**:
    PRECONDITIONS: - Open
    PRECONDITIONS: - Lose
    PRECONDITIONS: - Won
    PRECONDITIONS: - Cancelled
    PRECONDITIONS: 1) In order to view details for bets search for Request to Proxy:
    PRECONDITIONS: **accountHistory?poolBetId={PoolID}**
    PRECONDITIONS: 2) In order to view collapsed pools info search for Request to Proxy:
    PRECONDITIONS: accountHistory?fromDate={XXXX-XX-X1+00:00:00}&group=POOLBET&pagingBlockSize=20&toDate={XXXX-XX-X2+00:00:00}
    PRECONDITIONS: **JIRA tickets:**
    PRECONDITIONS: * BMA-17166 International Tote: Bets to appear in Bet History
    PRECONDITIONS: * BMA-19886 International Tote - Add meetings/tracks to bet history & openbets
    PRECONDITIONS: * [BMA-24547 RTS: Account history tabs > General view (Bet History / Transactions / Gaming History)] [1]
    PRECONDITIONS: [1]: https://jira.egalacoral.com/browse/BMA-24547
    """
    keep_browser_open = True

    def test_001_navigate_to_settled_bets_tab_on_my_bets_page_for_mobile(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' tab on 'My Bets' page (for mobile)
        EXPECTED: 'Bet History' page/tab is opened
        """
        pass

    def test_002_go_to_pools_sort_filter(self):
        """
        DESCRIPTION: Go to 'Pools' sort filter
        EXPECTED: * Open/Won/Lose/Cancelled bet sections are present
        EXPECTED: * All sections are collapsed by default
        """
        pass

    def test_003_search_for_international_pools(self):
        """
        DESCRIPTION: Search for International Pools
        EXPECTED: International pool is found in bets
        """
        pass

    def test_004_verify_collapsed_view_of_tote_pools_bets(self):
        """
        DESCRIPTION: Verify collapsed view of tote Pools bets
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

    def test_005_verify_expanded_view_of_tote_pools_bets(self):
        """
        DESCRIPTION: Verify expanded view of Tote pools bets
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

    def test_006_check_the_correctness_of_result_field_point_1_in_preconditions(self):
        """
        DESCRIPTION: Check the correctness of <Result> field (point 1 in preconditions)
        EXPECTED: PoolLeg-> poolPart->outcome
        EXPECTED: verify the outcomeResult value
        """
        pass

    def test_007_place_a_bet_and_verify_bet_with_status_open_is_not_shown_in_settled_bets(self):
        """
        DESCRIPTION: Place a bet and verify bet with status 'Open' is not shown in Settled Bets
        EXPECTED: Bet with status 'Open' is NOT present in Settled Bets (point 2 in preconditions)
        EXPECTED: settled:N
        """
        pass

    def test_008_trigger_the_situation_of_winning_a_bet_and_verify_bet_with_status_won_in_settled_bets(self):
        """
        DESCRIPTION: Trigger the situation of Winning a bet and verify bet with status 'Won' in Settled Bets
        EXPECTED: Bet with status 'Won' should be present in Settled Bets
        EXPECTED: 'You won <currency sign and value>' label right under header, on top of event card is shown
        EXPECTED: settled:Y
        EXPECTED: Winning !=0
        """
        pass

    def test_009_trigger_the_situation_of_losing_a_bet_and_verify_bet_with__lost_in_settled_bets(self):
        """
        DESCRIPTION: Trigger the situation of Losing a bet and verify bet with  'Lost' in Settled Bets
        EXPECTED: Bet with status 'Lost' should be present in Settled Bets
        EXPECTED: settled:Y
        EXPECTED: Refunds!=0
        """
        pass

    def test_010_trigger_the_situation_of_cancelling_a_bet_and_verify_bet_with__void_in_settled_bets(self):
        """
        DESCRIPTION: Trigger the situation of Cancelling a bet and verify bet with  'Void' in Settled Bets
        EXPECTED: Bet with status 'Void' should be present in Settled Bets
        EXPECTED: settled:Y
        EXPECTED: winning =0 and Refund =0
        """
        pass

    def test_011_repeat_steps_2_11_for_settled_bets_tab_account_history_page_for_mobile_bet_slip_widget_for_tabletdesktop(self):
        """
        DESCRIPTION: Repeat steps 2-11 for:
        DESCRIPTION: * 'Settled Bets' tab 'Account History' page (for mobile)
        DESCRIPTION: * 'Bet Slip' widget (for Tablet/Desktop)
        EXPECTED: 
        """
        pass
