import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.cash_out
@vtest
class Test_C52190570_Verify_Bet_Details_of_the_5_A_Side_bets_on_Cash_Out_tab(Common):
    """
    TR_ID: C52190570
    NAME: Verify  Bet Details of the '5-A-Side'  bet(s) on 'Cash Out' tab
    DESCRIPTION: Test case verifies Bet Details of the '5-A-Side'  bet(s) on 'Cash Out' tab
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Log in the app
    PRECONDITIONS: 3. User has placed '5-A-Side' bet(s)
    PRECONDITIONS: 4. Navigate to 'Cash Out' tab via 'My Bets' page **Mobile** and via 'Bet Slip' widget **Tablet/Desktop**
    PRECONDITIONS: **5-A-Side config:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Formations are added in CMS -> BYB -> 5-A-Side
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * To check data for the event on 'Cash Out' tab on 'My Bets' open the Dev tools > Network find **bet-details** request
    PRECONDITIONS: * To identify that it's the '5-A-Side' bet(s) verify the 'source' ('channel') parameter in the response - it should be 'f'
    """
    keep_browser_open = True

    def test_001__navigate_to_the_cash_out_tab_verify_displaying_of_5_a_side_bets(self):
        """
        DESCRIPTION: * Navigate to the 'Cash Out' tab.
        DESCRIPTION: * Verify displaying of '5-A-Side' bet(s).
        EXPECTED: The following bet details are shown for '5-A-Side' bet(s):
        EXPECTED: - Bet type **Single - 5-A-SIDE**
        EXPECTED: - Selections names have the following format:[Market name SELECTION NAME] and separated by a comma, truncated into a few lines
        EXPECTED: - **5-A-Side** text
        EXPECTED: - Corresponding Event name which redirects users to corresponding Event Details Page
        EXPECTED: - Event start date in HH:MM, DD MMM (e.g. 20:00, 21 Feb) and is shown next to Teams name (eg. A vs B)
        EXPECTED: - 'Watch' label if stream is available for the event
        EXPECTED: - Stake: <currency symbol> <value> (e.g., £10.00) shown in the footer of event card on the left
        EXPECTED: - Est. Returns/Potential Returns: <currency symbol> <value> (e.g., £30.00) shown next to stake value on the right
        EXPECTED: - Odds (displayed through '@' symbol next to selection name) eg.@1/5
        EXPECTED: - 'Cash Out <currency symbol> <value>' and 'Partial Cashout' buttons
        EXPECTED: All the details correspond to the placed '5-A-Side' bet(s)
        EXPECTED: **After BMA-50453:**
        EXPECTED: * 'Bet Receipt' label and its ID (e.g. O/15242822/0000017) are shown below the stake value (on the left)
        EXPECTED: * Date of bet placement is shown to the right of Bet Receipt id
        EXPECTED: * Date of bet placement is shown in a format hh:mm AM/PM - DD/MM (14:00 - 19 June)
        """
        pass
