import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C59115908_Verify_Bet_Placement_and_Receipt_after_Market_change(Common):
    """
    TR_ID: C59115908
    NAME: Verify Bet Placement and Receipt after Market change
    DESCRIPTION: Test case verifies successful Banach bet placement and Bet receipt after change of player's market
    PRECONDITIONS: Feature epic: https://jira.egalacoral.com/browse/BMA-49261
    PRECONDITIONS: Story: https://jira.egalacoral.com/browse/BMA-49310
    PRECONDITIONS: Designs: https://app.zeplin.io/project/5e0a3b413cbeb61b6eb8f5c9/dashboard
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: - Formations are added in CMS -> BYB -> 5 A Side
    PRECONDITIONS: User is logged in and on Football event details page:
    PRECONDITIONS: - '5 A Side' sub tab (event type specified above):
    PRECONDITIONS: - 'Build a team' button (pitch view)
    """
    keep_browser_open = True

    def test_001_select_at_least_2_valid_players_on_pitch_view(self):
        """
        DESCRIPTION: Select at least 2 valid players on Pitch view
        EXPECTED: - Players are selected on Pitch view
        EXPECTED: - 'Place Bet' button becomes active
        """
        pass

    def test_002_clicktap_on_one_of_previously_selected_player(self):
        """
        DESCRIPTION: Click/Tap on one of previously selected player
        EXPECTED: - 'Player Card' view of previously selected player is displayed
        EXPECTED: - Drop-down with the list of the markets applicable for the player is displayed
        EXPECTED: - 'Update player' button
        """
        pass

    def test_003_change_market_for_player___clicktab_update_player_button(self):
        """
        DESCRIPTION: Change Market for player -> Click/Tab 'Update player' button
        EXPECTED: - 'Pitch View' section is displayed
        EXPECTED: - Player stands on the same position on the pitch
        """
        pass

    def test_004_clicktap_place_bet_button(self):
        """
        DESCRIPTION: Click/Tap 'Place Bet' button
        EXPECTED: - Banach Betslip appears at the bottom of the page on top of pitch view
        EXPECTED: - 'remotebetslip' request is triggered in WS
        EXPECTED: ![](index.php?/attachments/get/113167517)
        """
        pass

    def test_005_enter_any_value_into_the_stake_field_and_clicktap_place_bet_button(self):
        """
        DESCRIPTION: Enter any value into the 'Stake' field and click/tap 'Place bet' button
        EXPECTED: - Bet is placed successfully
        EXPECTED: - Bet receipt is displayed
        EXPECTED: - User Balance is updated
        EXPECTED: - Bet Placement details: WS code "51101"
        EXPECTED: *Note*: if we receive 'Connection timeout' in websocket: (51102) from Banach, bet is not placed at 1st time, thus try several times to place a bet.
        """
        pass

    def test_006_verify_channel_used_for_5_a_side_bets(self):
        """
        DESCRIPTION: Verify channel used for 5-A-Side bets
        EXPECTED: Channel: "f" is present in '50011' request in 'remotebetslip' websocket
        """
        pass

    def test_007_verify_bet_receipt_on_ui(self):
        """
        DESCRIPTION: Verify Bet receipt on UI
        EXPECTED: - Main Header: '5-A-Side Bet Receipt' title with 'X' button
        EXPECTED: - Sub header : Tick icon, 'Bet Placed Successfully' text, date & time stamp (in the next format: i.e. 19/09/2019, 14:57)
        EXPECTED: - Block of Bet Type Summary:
        EXPECTED: - Win Alerts Toggle (if enabled in CMS)
        EXPECTED: - bet type name: i.e. 5-A-Side
        EXPECTED: - price of bet : e.g @90/1
        EXPECTED: - Bet ID:( Coral )/Receipt No:( Ladbrokes ) e.g Bet ID: 0/17781521/0000041
        EXPECTED: For each selection:
        EXPECTED: - selection name and market in the format of X.X To Make X+ Passes
        EXPECTED: - event name
        EXPECTED: Footer:
        EXPECTED: - 'Total stake'( Coral ) / 'Stake for this bet' ( Ladbrokes )
        EXPECTED: - 'Est. returns'( Coral ) / 'Potential returns' ( Ladbrokes )
        EXPECTED: ![](index.php?/attachments/get/113167518)
        """
        pass

    def test_008_close_bet_receipt(self):
        """
        DESCRIPTION: Close bet Receipt
        EXPECTED: - Bet Receipt is closed together with pitch view
        EXPECTED: - User is on '5 A Side' tab on EDP
        """
        pass
