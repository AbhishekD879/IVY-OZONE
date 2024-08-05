import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C883673_Verify_Quick_Bet_Receipt_Details(Common):
    """
    TR_ID: C883673
    NAME: Verify Quick Bet Receipt Details
    DESCRIPTION: This test case verifies Bet Receipt Details
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. User is logged in and has a positive balance
    PRECONDITIONS: 3. Tap one <Sport>/<Race> selection
    PRECONDITIONS: 4. Make sure that Quick Bet is displayed at the bottom of the page
    PRECONDITIONS: 5. Enter value in 'Stake' field and select 'E/W' option if available
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: * To get bet receipt details open Dev Tools -> Networks -> WS -> '?EIO=3&transport=websocket' request -> Frames section
    """
    keep_browser_open = True

    def test_001_tap_bet_now_button(self):
        """
        DESCRIPTION: Tap 'BET NOW' button
        EXPECTED: * Bet is placed successfully with correct date and time
        EXPECTED: * Bet Receipt is displayed
        """
        pass

    def test_002_verify_selection_name(self):
        """
        DESCRIPTION: Verify selection name
        EXPECTED: Selection name orresponds to **data.receipt.ResponseDto.[i].outcome.name** attribute from 30012 response in WS
        EXPECTED: where [i] - number of bet returned
        """
        pass

    def test_003_verify_handicap_value_check_using_football_event_where_handicap_market_is_available(self):
        """
        DESCRIPTION: Verify handicap value (check using football event where 'handicap' market is available)
        EXPECTED: Selection name orresponds to **data.receipt.ResponseDto.[i].outcome.name** attribute from 30012 response in WS
        EXPECTED: where [i] - number of bet returned
        """
        pass

    def test_004_verify_market_name(self):
        """
        DESCRIPTION: Verify market name
        EXPECTED: Market name corresponds to **data.receipt.ResponseDto.[i].market.name** attribute from 30012 response in WS
        EXPECTED: where [i] - number of bet returned
        """
        pass

    def test_005_verify_event_name(self):
        """
        DESCRIPTION: Verify event name
        EXPECTED: Event name corresponds to **data.receipt.ResponseDto.[i].event.name** attribute from 30012 response in WS
        EXPECTED: where [i] - number of bet returned
        """
        pass

    def test_006_verify_odds_price(self):
        """
        DESCRIPTION: Verify Odds (Price)
        EXPECTED: Odds value corresponds to **data.receipt.ResponseDto.[i].price** attribute from 30012 response in WS
        EXPECTED: where [i] - number of bet returned
        """
        pass

    def test_007_verify_bet_receipt_number_correctness(self):
        """
        DESCRIPTION: Verify Bet Receipt number correctness
        EXPECTED: Bet Receipt number corresponds to **data.receipt.ResponseDto.[i].receipt.id** attribute from 30012 response in WS
        EXPECTED: where [i] - number of bet returned
        """
        pass

    def test_008_verify_stakecoralstake_for_this_betladbrokes_correctness(self):
        """
        DESCRIPTION: Verify Stake(Coral)/Stake for this bet(Ladbrokes) correctness
        EXPECTED: Stake value corresponds to **data.receipt.ResponseDto.[i].stakePerLive** attribute from 30012 response in WS
        EXPECTED: where [i] - number of bet returned
        """
        pass

    def test_009_verify_stakecoralstake_for_this_betladbrokes_correctness_check_using_horse_racing_when_ew_option_is_enabled(self):
        """
        DESCRIPTION: Verify Stake(Coral)/Stake for this bet(Ladbrokes) correctness (Check using Horse Racing when 'E/W' option is enabled)
        EXPECTED: Stake value corresponds to **data.receipt.ResponseDto.[i].amount** attribute from 30012 response in WS
        EXPECTED: where [i] - number of bet returned
        """
        pass

    def test_010_verify_est_returnscoralpotential_returnsladbrokes_correctness(self):
        """
        DESCRIPTION: Verify Est Returns(Coral)/Potential Returns(Ladbrokes) correctness
        EXPECTED: Total Est. Returns value corresponds to **data.receipt.ResponseDto.[i].payout.potential** attribute from 30012 response in WS
        EXPECTED: where [i] - number of bet returned
        """
        pass
