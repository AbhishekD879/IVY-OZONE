import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.5_a_side
@vtest
class Test_C57119755_Verify_Bet_Placement_on_5_A_Side_bets(Common):
    """
    TR_ID: C57119755
    NAME: Verify Bet Placement on  '5-A-Side' bets
    DESCRIPTION: This test case verifies bet placement on  '5-A-Side' bets
    DESCRIPTION: AUTOTESTS:
    DESCRIPTION: Mobile [C58428330]
    DESCRIPTION: Desktop [C58616846]
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Football event details page that has all 5-A-Side configs
    PRECONDITIONS: 3. Choose the '5-A-Side' tab
    PRECONDITIONS: 4. Click/Tap on the 'Build Team' button on '5-A-Side' launcher
    PRECONDITIONS: 5. Make sure that '5-A-Side' overlay is opened
    PRECONDITIONS: **5-A-Side config:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - '5-A-Side' tab is created in CMS > EDP Markets
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Formations are added in CMS -> BYB -> 5 A Side
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: - Statistic is mapped for the particular event. Use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=91089483#OPTA/BWINScoreboardmappingtoanOBevent-Appendix_A
    PRECONDITIONS: - Player's statisctic takes from local storage 'scoreBoards_dev_prematch_eventId':
    PRECONDITIONS: ![](index.php?/attachments/get/73440082)
    PRECONDITIONS: - Players are taken from Banach provider and received in the following response:
    PRECONDITIONS: https://buildyourbet-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/api/v1/players?obEventId=XXXXX
    PRECONDITIONS: where
    PRECONDITIONS: XXXXX - Event ID
    PRECONDITIONS: ![](index.php?/attachments/get/62325587)
    """
    keep_browser_open = True

    def test_001_select_at_least_2_players_on_the_pitch_view(self):
        """
        DESCRIPTION: Select at least 2 players on the 'Pitch View'
        EXPECTED: * The players are added and displayed on the corresponding position on the 'Pitch View'
        EXPECTED: * 'Odds/Place Bet' button is active
        EXPECTED: * Corresponding Odds value is displayed on 'Odds/Place Bet' button taken from <price> response
        """
        pass

    def test_002_clicktap_the_place_bet_buttonverify_5_a_side_betslip_content(self):
        """
        DESCRIPTION: Click/Tap the' Place Bet' button.
        DESCRIPTION: Verify '5-A-Side Betslip' content.
        EXPECTED: * '5-A-Side Betslip' appears over the 'Pitch View'
        EXPECTED: * '50001' request is triggered in 'remotebetslip' connection in the WS
        EXPECTED: * '5-A-Side Betslip' contains the following elements:
        EXPECTED: * Header with 'Betslip' title and 'Close' button
        EXPECTED: * The list of added selections in the following format:
        EXPECTED: * 'Player Bets' title
        EXPECTED: * 'Player Name' + 'Market Name'
        EXPECTED: * 'Odds' and 'Stake' box
        EXPECTED: * 'Quick Stakes' buttons (e.g. "+£5", "+£10" "+£50", "+£100")
        EXPECTED: * 'Total Stake' value
        EXPECTED: * 'Estimated returns'/'Potential returns' value
        EXPECTED: * 'Back' button is active
        EXPECTED: * 'Place bet' is disabled
        """
        pass

    def test_003__enter_any_value_into_the_stake_field_clicktap_place_bet_button(self):
        """
        DESCRIPTION: * Enter any value into the 'Stake' field.
        DESCRIPTION: * Click/Tap 'Place bet' button.
        EXPECTED: * Spinner is displayed on "Place bet" for a few seconds
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet receipt is displayed
        EXPECTED: * User Balance is updated
        """
        pass

    def test_004_verify_data_in_remotebetslip_connection_in_ws_client(self):
        """
        DESCRIPTION: Verify data in 'remotebetslip' connection in WS client
        EXPECTED: * '50011' request contains price, stake, currency, token and channel: "f" (for '5-A-Side' bets) info
        EXPECTED: * '51101' response contains "response code":1, date, betPotentialWin, numLines, betNo, betID, receipt, totalStake info
        EXPECTED: **Note:** if we receive 'Connection timeout' in websocket: (51102) from Banach, bet is not placed at 1st time, thus try several times to place a bet. It's related to tst2 env, could be reproduced only for this env.
        EXPECTED: ![](index.php?/attachments/get/74408400)
        """
        pass

    def test_005_verify_the_bet_receipt_content(self):
        """
        DESCRIPTION: Verify the 'Bet Receipt' content
        EXPECTED: Bet Receipt consists of:
        EXPECTED: * Header with 'Bet Receipt' title and 'Close' button
        EXPECTED: * Subheader with '✓Bet Placed Successfully' title and time of the placed bet (format DD/MM/YYYY, HH:MM)
        EXPECTED: * 'Single @' title with 'Odds'
        EXPECTED: * 'Receipt No' value
        EXPECTED: * The list of added selections in the following format:
        EXPECTED: * 'Player Bets' title
        EXPECTED: * 'Player Name' + 'Market Name'
        EXPECTED: * 'Stake for this bet' value
        EXPECTED: * 'Estimated returns'/'Potential returns' value
        """
        pass

    def test_006_clicktap_on_the_close_button(self):
        """
        DESCRIPTION: Click/Tap on the 'Close' button
        EXPECTED: * '5-A-Side Betslip' is closed
        EXPECTED: * '5-A-Side Overlay' is closed as well
        """
        pass

    def test_007_navigate_to_the_my_bets_pagetabverify_the_bet_details_displaying(self):
        """
        DESCRIPTION: Navigate to the 'My Bets' page/tab.
        DESCRIPTION: Verify the Bet Details displaying.
        EXPECTED: The following data is displayed for the bet:
        EXPECTED: * Type of bet (e.g. SINGLE-5-A-SIDE)
        EXPECTED: * 'Market name' + 'Player Name'
        EXPECTED: * 'Odds' value
        EXPECTED: * '5-A-Side' label
        EXPECTED: * Event name (e.g. Team 1 v Team 2)
        EXPECTED: * Time of the event in format HH:MM, DD Month(for example, 10:30, 17 Jan)
        EXPECTED: * The currency is as user set during registration
        EXPECTED: * 'Stake' value
        EXPECTED: * 'Est. Returns'/'Potential returns' value
        EXPECTED: * 'Cashout' button (if available)
        """
        pass
