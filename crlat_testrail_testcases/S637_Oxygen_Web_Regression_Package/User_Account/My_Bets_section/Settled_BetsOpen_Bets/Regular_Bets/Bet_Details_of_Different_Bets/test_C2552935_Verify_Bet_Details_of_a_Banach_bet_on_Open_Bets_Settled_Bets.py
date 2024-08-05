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
class Test_C2552935_Verify_Bet_Details_of_a_Banach_bet_on_Open_Bets_Settled_Bets(Common):
    """
    TR_ID: C2552935
    NAME: Verify Bet Details of a Banach bet on Open Bets/Settled Bets
    DESCRIPTION: Test case verifies Banach bet display on Settled Bets and Open Bets
    DESCRIPTION: AUTOTEST [C2604453]
    PRECONDITIONS: Build Your Bet CMS configuration
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: To check Open Bet data for event on Bet History tabs:
    PRECONDITIONS: in Dev tools > Network find **accountHistory** request
    PRECONDITIONS: **User has placed Banach bet(s)**
    PRECONDITIONS: **User has a settled Banach bet(s)**
    PRECONDITIONS: 'Open Bets' and 'Settled Bets' can be found on 'My Bets' page on mobile and on 'Bet Slip' widget for Tablet/Desktop
    PRECONDITIONS: Make sure that Bet Tracking feature is disabled in CMS: System-configuration -> Structure -> BetTracking config -> enabled = false
    """
    keep_browser_open = True

    def test_001__navigate_to_open_bets_tab_verify_display_of_banach_bet(self):
        """
        DESCRIPTION: * Navigate to 'Open Bets' tab.
        DESCRIPTION: * Verify display of Banach bet.
        EXPECTED: - Bet type **BUILD YOUR BET** (for Coral) **/ BET BUILDER** (for Ladbrokes)
        EXPECTED: - Selection names user has bet on, displayed in a list view (Player Bets selections have the following format: X.X To Make X+ Passes)
        EXPECTED: - **Build Your Bet** (for Coral) **/ BET BUILDER** (for Ladbrokes) text
        EXPECTED: - Corresponding Event name which is redirecting users to corresponding Event Details Page
        EXPECTED: - Event start date in hh:mm AM/PM (time only displayed for Today's events) - DD/MM
        EXPECTED: - Date of event is shown next to Teams name (eg. A vs B)
        EXPECTED: - Date of event is shown in a format hh:mm AM/PM - DD/MM
        EXPECTED: - Stake <currency symbol> <value> (e.g., £10.00) shown in the footer of event card on the left
        EXPECTED: - Est. Returns <currency symbol> <value> (e.g., £30.00) shown next to stake value on the right
        EXPECTED: - Odds (displayed through '@' symbol next to selection name) eg.@1/5
        EXPECTED: All the details correspond to the placed Banach bet
        EXPECTED: If the bet is Suspended, event name will be greyed out and SUSP label shown:
        EXPECTED: **After BMA-50453:**
        EXPECTED: * 'Bet Receipt' label and its ID (e.g. O/15242822/0000017) are shown below the stake value (on the left)
        EXPECTED: * Date of bet placement is shown to the right of Bet Receipt id
        EXPECTED: * Date of bet placement is shown in a format hh:mm AM/PM - DD/MM (14:00 - 19 June)
        """
        pass

    def test_002__navigate_to_settled_bets_tab_verify_display_of_banach_bet(self):
        """
        DESCRIPTION: * Navigate to 'Settled Bets tab.
        DESCRIPTION: * Verify display of Banach bet.
        EXPECTED: - Bet type **BUILD YOUR BET** (for Coral) **/ BET BUILDER** (for Ladbrokes)
        EXPECTED: - Selection names user has bet on, displayed in a list view (Player Bets selections have the following format: X.X To Make X+ Passes)
        EXPECTED: - **Build Your Bet** (for Coral) **/ BET BUILDER** (for Ladbrokes) text
        EXPECTED: - Won/Lost/Void label on the right in the header
        EXPECTED: - In case Bet won: 'You won <currency sign and value>' label right under header on event card is shown
        EXPECTED: - Corresponding Event name
        EXPECTED: - Stake <currency symbol> <value> (e.g., £10.00) displayed in the footer of event card
        EXPECTED: - Est. Returns <currency symbol> <value> (e.g., £30.00) next to the Stake value
        EXPECTED: - 'Bet Receipt' label and its ID (e.g. O/15242822/0000017) are shown below the stake value (on the left)
        EXPECTED: - Date of bet placement is shown to the right of Bet Receipt id
        EXPECTED: - Date of bet placement is shown in a format hh:mm AM/PM - DD/MM (14:00 - 19 June)
        EXPECTED: - Odds (displayed through '@' symbol next to selection name) eg.@1/5
        EXPECTED: All the details correspond to the settled Banach bet
        """
        pass
