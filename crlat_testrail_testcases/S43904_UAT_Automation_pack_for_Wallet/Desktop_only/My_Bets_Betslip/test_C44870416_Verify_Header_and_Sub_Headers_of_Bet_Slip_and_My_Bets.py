import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870416_Verify_Header_and_Sub_Headers_of_Bet_Slip_and_My_Bets(Common):
    """
    TR_ID: C44870416
    NAME: Verify Header and Sub -Headers of Bet Slip and My Bets.
    DESCRIPTION: This TC is to verify contents of Bet Slip and My Bets in desktop.
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_check_user_sees_following_headers_and_sub_headers__betslip__my_bets_cash_out_open_bets_settled_bets(self):
        """
        DESCRIPTION: "Check user sees following headers and sub-headers
        DESCRIPTION: - Betslip
        DESCRIPTION: - My Bets
        DESCRIPTION: . Cash Out
        DESCRIPTION: . Open bets
        DESCRIPTION: . Settled Bets
        EXPECTED: User is able to see
        EXPECTED: - BETSLIP
        EXPECTED: - MY BETS
        EXPECTED: . CASH OUT
        EXPECTED: . OPEN BETS
        EXPECTED: . SETTLED BETS
        """
        pass

    def test_002_betslip__no_selections_message___check_user_sees_your_betslip_is_empty_message_when_no_selections_in_their_betsliplogged_in_or_out(self):
        """
        DESCRIPTION: BETSLIP- NO SELECTIONS MESSAGE - Check user sees ''Your Betslip is empty'' message when no selections in their betslip((logged in or out))
        EXPECTED: User sees ''Your betslip is empty'  message when no selections in their betslip (logged in or out).
        """
        pass

    def test_003_betslip__with_selections____check__user_sees_their_betsadded_selections_when_they_view_their_betslip_logged_in_or_logged_out_and_betslip_count_with_number_of_selection(self):
        """
        DESCRIPTION: BETSLIP- WITH SELECTIONS  - Check  user sees their bets(added selections) when they view their betslip (logged in or logged out) and Betslip count with number of selection
        EXPECTED: User is able to see their bets(added selections) when they view their betslip (logged in or logged out) and Betslip count with number of selections.
        """
        pass

    def test_004_betslip__suspended_selections___check_user_is_seeing__signposting_and_messages_for_suspended_selections_as_belowheader_some_of_your_selections_have_been_suspendedgreyed_out_bet_with_suspended_labelfooter_some_of_your_selections_have_been_suspended(self):
        """
        DESCRIPTION: BETSLIP- SUSPENDED SELECTIONS - Check user is seeing  signposting and messages for suspended selections as below
        DESCRIPTION: Header: Some of your selections have been suspended
        DESCRIPTION: Greyed out bet with suspended label
        DESCRIPTION: Footer: Some of your selections have been suspended"
        EXPECTED: User should see
        EXPECTED: Header: Some of your selections have been suspended
        EXPECTED: Greyed out bet with suspended label
        EXPECTED: Footer: Some of your selections have been suspended"
        """
        pass
