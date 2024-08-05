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
class Test_C51794970_Verify_5_A_Side_layout_on_Football_EDP(Common):
    """
    TR_ID: C51794970
    NAME: Verify '5-A-Side' layout on Football EDP
    DESCRIPTION: This test case verifies '5-A-Side' layout on Football EDP
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Football event details page that has all 5-A-Side configs
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
    PRECONDITIONS: - The Outfield player's stats label mapping according to stats name from CMS and stats value from OPTA:
    PRECONDITIONS: ![](index.php?/attachments/get/90015196)
    """
    keep_browser_open = True

    def test_001_verify_5_a_side_tab_displaying(self):
        """
        DESCRIPTION: Verify '5-A-Side' tab displaying
        EXPECTED: * '5-A-Side' tab is present on EDP
        EXPECTED: * 'New' label is displayed on the tab if it's enabled in CMS
        EXPECTED: * '5-A-Side' tab is displayed in the order set in CMS
        """
        pass

    def test_002_clicktap_on_the_5_a_side_tab(self):
        """
        DESCRIPTION: Click/Tap on the '5-A-Side' tab
        EXPECTED: * '5-A-Side' tab is selected and highlighted
        EXPECTED: * URL ends with event_id/5-a-side
        """
        pass

    def test_003_verify_5_a_side_launcher_content(self):
        """
        DESCRIPTION: Verify '5-A-Side' launcher content
        EXPECTED: * '5-A-Side' launcher is present when '5-A-Side' tab is selected
        EXPECTED: * Content of '5-A-Side' tab corresponds to 'five-a-side-launcher' static block in CMS > Static Blocks
        EXPECTED: * Title
        EXPECTED: * Text
        EXPECTED: * Button
        EXPECTED: * 'five-a-side-launcher' response is received from CMS with data set in CMS
        """
        pass

    def test_004_clicktap_on_the_build_team_button(self):
        """
        DESCRIPTION: Click/Tap on the 'Build Team' button
        EXPECTED: * '5-A-Side' overlay is loaded
        EXPECTED: * URL ends with event_id/5-a-side/pitch
        """
        pass

    def test_005_verify_5_a_side_overlay_content(self):
        """
        DESCRIPTION: Verify '5-A-Side' overlay content
        EXPECTED: * '5-A-Side' header with the following elements:
        EXPECTED: * 'Ladbrokes 5-A-Side' title
        EXPECTED: *'Select a formation and build your team' instruction text
        EXPECTED: * Formation toggles carousel with created formations in CMS
        EXPECTED: * Close 'x' button
        EXPECTED: * '5-A-Side' subheader with the following elements:
        EXPECTED: * Event name
        EXPECTED: * Selected formation (corresponds to value in 'Actual formation' dropdown in CMS  e.g. 1-1-2-1)
        EXPECTED: * '5-A-Side' pitch view with the following elements:
        EXPECTED: * ('+') 'Add Player' buttons
        EXPECTED: * Player Information:
        EXPECTED: * Positions (corresponds to entered in CMS 'Position' input field)
        EXPECTED: * Statistics (corresponds to selected in CMS 'Stat' dropdown)
        EXPECTED: * 'Odds/Place Bet' button is disabled by default
        EXPECTED: * Background Pitch Image
        """
        pass

    def test_006_clicktap_on_the_plus_add_player_buttonverify_the_player_list_view_content(self):
        """
        DESCRIPTION: Click/Tap on the ('+') 'Add Player' button.
        DESCRIPTION: Verify the 'Player List' view content.
        EXPECTED: * 'Player List' view is opened
        EXPECTED: * 'Player List' view contains the following elements:
        EXPECTED: * '< Back' button
        EXPECTED: * Title "Add a 'Position name'" below the 'Back' button (e.g 'Add a Cruncher'. Position name sets in the CMS)
        EXPECTED: * Subtitle is the name of the Statistic (e.g. To Win X Tackles, To Make X Passes etc. sets in the CMS)
        EXPECTED: * 'All Players'(selected by default), 'Home', 'Away' buttons. (For all positions except Goalkeeper).
        EXPECTED: * Event name
        EXPECTED: * The list of players that contains:
        EXPECTED: * Crest of the team made up of primary and secondary color set in CMS
        EXPECTED: * Team name
        EXPECTED: * Position playing (If available from Datahub feed) [Goalkeeper -(GK), Defender - (DF), Midfielder - (MF), Forward -(FW)]
        EXPECTED: * Player name
        EXPECTED: * Stats label and value of the player (e.g. 0, 1, N/A, etc.)
        EXPECTED: * Chevron indicating the user can tap on the player - when tapped launch the player card
        """
        pass

    def test_007_select_the_player_by_clickingtapping_on_the_cardverify_the_player_card_view_content(self):
        """
        DESCRIPTION: Select the player by clicking/tapping on the card.
        DESCRIPTION: Verify the 'Player Card' view content.
        EXPECTED: * 'Player Card' view is opened
        EXPECTED: * 'Player Card' view contains the following elements:
        EXPECTED: * '< Back' button
        EXPECTED: * 'Player name' below the 'Back' button
        EXPECTED: * 'Team name'|'Player position' (if received from Data Hub provider)
        EXPECTED: * Selected market (e.g. 'Goals Inside The Box')
        EXPECTED: * 'Player name' + to have + 'Stats value' + 'Stats name'
        EXPECTED: * 'Stats value' (eg. 1+) where default step value is displayed as average stat value with clickable +/- buttons on the sides
        EXPECTED: * List of Player statistics (eg. Goals, Assists, etc.)
        EXPECTED: * 'Odds/Add Player' button at the bottom with dynamic odds
        """
        pass

    def test_008_clicktap_on_the_oddsadd_player_buttonverify_the_5_a_side_overlay_content(self):
        """
        DESCRIPTION: Click/Tap on the 'Odds/Add Player' button.
        DESCRIPTION: Verify the '5-A-Side' overlay content.
        EXPECTED: * The player is added and displayed on the corresponding position on the 'Pitch View'
        EXPECTED: * 'Odds/Place Bet' button is disabled
        """
        pass

    def test_009_add_one_more_playerverify_the_5_a_side_overlay_content(self):
        """
        DESCRIPTION: Add one more Player.
        DESCRIPTION: Verify the '5-A-Side' overlay content.
        EXPECTED: * The players are added and displayed on the corresponding position on the 'Pitch View'
        EXPECTED: * 'Odds/Place Bet' button is active
        """
        pass
