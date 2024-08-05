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
class Test_C52190439_Verify_Bet_Details_of_a_5_A_Side_bets_on_Open_Bets_Settled_Bets_page_tab(Common):
    """
    TR_ID: C52190439
    NAME: Verify Bet Details of a '5-A-Side' bet(s) on 'Open Bets/Settled Bets' page/tab
    DESCRIPTION: Test case verifies '5-A-Side' bet on 'Open Bets/Settled Bets' page/tab
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Log in the app
    PRECONDITIONS: 3. User has placed '5-A-Side' bet(s)
    PRECONDITIONS: 4. User has a settled '5-A-Side' bet(s)
    PRECONDITIONS: 5. Navigate to 'Open Bets' and 'Settled Bets' tabs via 'My Bets' page **Mobile** and via 'Bet Slip' widget **Tablet/Desktop**
    PRECONDITIONS: **5-A-Side config:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Formations are added in CMS -> BYB -> 5-A-Side
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * To check 'Open Bets' data for the event on 'My Bets' open the Dev tools > Network find **bet-details** request
    PRECONDITIONS: * To check 'Settled Bets' data for the event on 'My Bets' open the Dev tools > Network find **accountHistory** request
    PRECONDITIONS: * To identify that it's the '5-A-Side' bet(s) verify the 'source' ('channel') parameter in the response - it should be 'f'
    PRECONDITIONS: * Make sure that Bet Tracking feature is disabled in CMS: System-configuration -> Structure -> BetTracking config -> enabled = false
    """
    keep_browser_open = True

    def test_001__navigate_to_open_bets_tab_verify_displaying_of_5_a_side_bets(self):
        """
        DESCRIPTION: * Navigate to 'Open Bets' tab.
        DESCRIPTION: * Verify displaying of '5-A-Side' bet(s).
        EXPECTED: The following bet details are shown for '5-A-Side' bet(s):
        EXPECTED: - Bet type **5-A-SIDE**
        EXPECTED: - Selections names have the following format: X.X To Make X+ Passes and displayed in a list view
        EXPECTED: - **5-A-Side** text
        EXPECTED: - Event name which redirects users to corresponding Event Details Page
        EXPECTED: - Event start date in HH:MM, DD MMM (e.g. 20:00, 21 Feb) and is shown next to Event name (eg. A vs B)
        EXPECTED: - 'Watch' label if stream is available for the event
        EXPECTED: - Stake: <currency symbol> <value> (e.g., £10.00) shown in the footer of event card on the left
        EXPECTED: - Est. Returns/Potential Returns: <currency symbol> <value> (e.g., £30.00) shown next to stake value on the right
        EXPECTED: - Odds (displayed through '@' symbol next to selection name) eg.@1/5
        EXPECTED: All the details correspond to the placed '5-A-Side' bet(s)
        EXPECTED: If the bet is Suspended, event name will be greyed out and SUSP label shown
        EXPECTED: **After BMA-50453:**
        EXPECTED: * 'Bet Receipt' label and its ID (e.g. O/15242822/0000017) are shown below the stake value (on the left)
        EXPECTED: * Date of bet placement is shown to the right of Bet Receipt id
        EXPECTED: * Date of bet placement is shown in a format hh:mm AM/PM - DD/MM (14:00 - 19 June)
        """
        pass

    def test_002__navigate_to_settled_bets_tab_verify_displaying_of_5_a_side_bets(self):
        """
        DESCRIPTION: * Navigate to 'Settled Bets' tab.
        DESCRIPTION: * Verify displaying of '5-A-Side' bet(s).
        EXPECTED: The following bet details are shown for '5-A-Side' bet(s):
        EXPECTED: - Bet type **5-A-SIDE**
        EXPECTED: - Selections names have the following format: X.X To Make X+ Passes and displayed in a list view
        EXPECTED: - **5-A-Side** text
        EXPECTED: - 'Won'/'Lost'/'Void' label on the right in the header
        EXPECTED: - In case Bet won: 'You won <currency sign and value>' label right under the header on event card is shown and 'green tick' icon on the left side of the card
        EXPECTED: - In case Bet void: 'Void' label on the left side of the event card is shown and the card is greyed out
        EXPECTED: - In case Bet lost: 'red cross' icon on the left side of the event card is shown
        EXPECTED: - Corresponding Event name which is redirecting users to corresponding Event Details Page
        EXPECTED: - Stake: <currency symbol> <value> (e.g., £10.00) displayed in the footer of event card
        EXPECTED: - Est. Returns/Returns: <currency symbol> <value> (e.g., £30.00) next to the Stake value
        EXPECTED: - 'Bet Receipt:' label and its ID (e.g. O/15242822/0000017) are shown below the stake value (on the left)
        EXPECTED: - Date of bet placement is shown in a format HH:MM AM/PM - DD MMM (14:00 - 19 June) to the right of Bet Receipt ID
        EXPECTED: - Odds (displayed through '@' symbol next to selection name) eg.@1/5
        EXPECTED: All the details correspond to the settled Banach bet
        """
        pass
