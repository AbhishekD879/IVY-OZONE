import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.build_your_bet
@vtest
class Test_C2022256_Build_Your_Bet_Banach_bet_placement(Common):
    """
    TR_ID: C2022256
    NAME: Build Your Bet Banach bet placement
    DESCRIPTION: Test case verifies success flow of adding Banach(Match Market) selections to BYB betslip and placing a bet
    DESCRIPTION: AUTOTESTS [C48975899]
    PRECONDITIONS: **TEST2 event: 8424205**
    PRECONDITIONS: CMS config:
    PRECONDITIONS: **Guide on CMS configuration for Banach and Digital Sport:**
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Banach
    PRECONDITIONS: 1) Build Your Bet tab is available on Event Details Page :
    PRECONDITIONS: a) Build Your Bet tab is available on Event Details Page : In CMS -> System-configuration -> YOURCALLICONSANDTABS -> 'enableTab' is selected
    PRECONDITIONS: b) Banach leagues are mapped in CMS: Your Call > YourCall leagues
    PRECONDITIONS: c) Event belonging to Banach league is mapped (on Banach side)
    PRECONDITIONS: 2) Match Markets switcher is turned on : BYB > BYB switchers > enable Match Markets
    PRECONDITIONS: HL requests:
    PRECONDITIONS: Request for Banach leagues: https://buildyourbet-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/api/v1/leagues
    PRECONDITIONS: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/leagues
    PRECONDITIONS: Request for Banach market groups: https://buildyourbet-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/api/v2/markets-grouped?obEventId=xxxxx
    PRECONDITIONS: Request for Banach selections: https://buildyourbet-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/api/v1/selections?marketIds=[ids]&obEventId=xxxxx
    PRECONDITIONS: Check the following WS for Adding selection to Quick bet and placing bet:
    PRECONDITIONS: wss://remotebetslip-dev1.coralsports.dev.cloud.ladbrokescoral.com/quickbet/?EIO=3&transport=websocket
    PRECONDITIONS: Build Your Bet tab on event details page is loaded and no selection added to dashboard
    """
    keep_browser_open = True

    def test_001_add_a_few_selections_from_different_markets_to_dashboard(self):
        """
        DESCRIPTION: Add a few selections from different markets to dashboard
        EXPECTED: Selections are added to the dashboard:
        EXPECTED: * The BYB overlay with the name of selections and teams
        EXPECTED: * Active "Place bet" button with odds
        EXPECTED: * The selections with delete buttons
        EXPECTED: * "Open"/"Close" buttons to expand and collapse the BYB overlay
        EXPECTED: ![](index.php?/attachments/get/56623626)
        """
        pass

    def test_002_tap_on_the_place_bet_button_with_odds(self):
        """
        DESCRIPTION: Tap on the "Place bet" button with odds
        EXPECTED: - BYB betslip appears:
        EXPECTED: * Betslip header and "X" button
        EXPECTED: * Selection and market names
        EXPECTED: * Price odds and Stake box
        EXPECTED: * Quick Stakes (For example, "+£5", "+£10" "+£50", "+£100")
        EXPECTED: * Total Stake & Estimated returns
        EXPECTED: * The button "Back" is active and "Place bet" is disabled
        EXPECTED: - In WS client sends message with code 50001 containing selections ids and receives message from quick bet with code 51001 with price
        EXPECTED: ![](index.php?/attachments/get/56623627)
        """
        pass

    def test_003_tap_on_the_stake_field_and_enter_any_value(self):
        """
        DESCRIPTION: Tap on the "Stake" field and enter any value
        EXPECTED: * The keyboard appears
        EXPECTED: * "Stake" field is populated with entered value
        EXPECTED: * The buttons "Back" and "Place bet" are active
        EXPECTED: Please note The keyboard doesn't appear when using "Quick Stake" buttons
        """
        pass

    def test_004_tap_on_place_bet_button(self):
        """
        DESCRIPTION: Tap on "Place bet" button
        EXPECTED: * Spinner is displayed on "Place bet" for a few seconds
        EXPECTED: * Bet is placed successfully
        EXPECTED: * User balance is decreased by stake entered on step #3
        EXPECTED: - In WS client sends message with code 50011 containing price, stake, currency info and receives message with from quick bet with code 51101 containing "response code":1, bet id, receipt, stake.
        """
        pass

    def test_005_verify_the_bet_receipt(self):
        """
        DESCRIPTION: Verify the Bet Receipt
        EXPECTED: Bet Receipt consists of:
        EXPECTED: * "Bet Receipt" header and "X" button
        EXPECTED: * The message "✓Bet Placed Successfully"
        EXPECTED: * Date and time of the placed bet (format DD/MM/YYYY, HH:MM)
        EXPECTED: * Selection & Market names
        EXPECTED: * Odds
        EXPECTED: * Bet receipt ID
        EXPECTED: * Stake & Est. Returns
        EXPECTED: ![](index.php?/attachments/get/56623629)
        """
        pass

    def test_006_click_on_the_x_button(self):
        """
        DESCRIPTION: Click on the "X" button
        EXPECTED: The Quick Bet is closed
        """
        pass

    def test_007_click_on_my_bets_button_from_the_header(self):
        """
        DESCRIPTION: Click on My Bets button from the header
        EXPECTED: Check the following data correctness:
        EXPECTED: * Type of bet (for example, SINGLE-BUILD YOUR BET)
        EXPECTED: * Selection & Market name @odds (for example, Match Betting ASTON VILLA, Both Teams to Score YES @4/1)
        EXPECTED: * Build Your Bet
        EXPECTED: * Event name
        EXPECTED: * Time of the event in format HH:MM, DD Month(for example, 10:30, 17 Jan)
        EXPECTED: * The currency is as user set during registration
        EXPECTED: * Stake & Est. Returns
        EXPECTED: * Cashout button (if available)
        EXPECTED: ![](index.php?/attachments/get/56623621)
        """
        pass
