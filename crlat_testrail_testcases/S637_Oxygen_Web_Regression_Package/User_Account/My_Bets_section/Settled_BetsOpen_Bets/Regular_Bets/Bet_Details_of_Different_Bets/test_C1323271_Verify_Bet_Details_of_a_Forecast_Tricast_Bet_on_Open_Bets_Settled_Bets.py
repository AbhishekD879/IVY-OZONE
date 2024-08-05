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
class Test_C1323271_Verify_Bet_Details_of_a_Forecast_Tricast_Bet_on_Open_Bets_Settled_Bets(Common):
    """
    TR_ID: C1323271
    NAME: Verify Bet Details of a Forecast/Tricast Bet on Open Bets/Settled Bets
    DESCRIPTION: This test case verifies bet details of a Forecast/Tricast bet
    DESCRIPTION: AUTOTEST: [C2600794]
    PRECONDITIONS: 1. User should be logged in to view their bet.
    PRECONDITIONS: 2. 'Open Bets' and 'Settled Bets ' can be found on 'My Bets' page on mobile and on 'Bet Slip' widget for Tablet/Desktop
    PRECONDITIONS: 3. User has placed TRICAST/FORECAST bet
    PRECONDITIONS: 4. USER has a settled TRICAST/FORECAST bet
    """
    keep_browser_open = True

    def test_001_navigate_to_open_bets_tabverify_bet_details_for_placed_forecasttricast_bet(self):
        """
        DESCRIPTION: Navigate to 'Open Bets' tab
        DESCRIPTION: Verify bet details for placed Forecast/Tricast bet
        EXPECTED: The following bet details are shown:
        EXPECTED: * Bet type (e.g., "SINGLE - FORECAST") on the header
        EXPECTED: * Selection names listed in a column one under another (with silks on the left of each selection if available)
        EXPECTED: * Market name (e.g. "Win or Each Way")
        EXPECTED: * Odds placed next to market name displayed through @ symbol (eg. @1/2, @SP)
        EXPECTED: * Event name (including event time) and start time in HH:MM format (e.g. "13:00 Greyville 15:00, Today")
        EXPECTED: * 'Live' or 'Watch live' icon next to event name (if available)
        EXPECTED: * Stake (e.g., £10.00) and Est. Returns ("N/A" if not available) in the footer of event card
        EXPECTED: All the details correspond to the placed Forecast/Tricast bet
        EXPECTED: **After BMA-50453:**
        EXPECTED: * 'Bet Receipt' label and its ID (e.g. O/15242822/0000017) are shown below the stake value (on the left)
        EXPECTED: * Date of bet placement is shown to the right of Bet Receipt id
        EXPECTED: * Date of bet placement is shown in a format hh:mm AM/PM - DD/MM (14:00 - 19 June)
        """
        pass

    def test_002_navigate_to_settled_bets_tabverify_bet_details_for_settled_forecasttricast_bet(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' tab
        DESCRIPTION: Verify bet details for settled Forecast/Tricast bet
        EXPECTED: The following bet details are shown:
        EXPECTED: * Bet type (e.g., "SINGLE - FORECAST")
        EXPECTED: * Result (Won/Lost/Void/Cashed out) on the header on the right
        EXPECTED: * If bet has won the message 'You won <currency symbol><value>' is displayed on the left, under event card header with green tick icon shown before message
        EXPECTED: * Selection names listed in a column one under another (with silks on the left of each selection if available)
        EXPECTED: * Market name user has bet on (e.g. "Win or Each Way")
        EXPECTED: * Odds placed next to market name displayed through @ symbol (eg. @1/2, @SP)
        EXPECTED: * Event name (including event time) (e.g. "13:00 Greyville")
        EXPECTED: * Stake (e.g., £10.00) and Returns ("0.00" if the bet is lost)
        EXPECTED: * Date of bet placement and bet receipt ID are shown below bet details on the right
        EXPECTED: * Date of bet placement is shown in a format HH:MM-DD/MM (e.g. 15:39 - 04 July)
        EXPECTED: * 'Bet Receipt' label and its ID (e.g. O/15242822/0000017) are shown to the left of bet placement date
        EXPECTED: All the details correspond to the settled Forecast/Tricast bet
        """
        pass
