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
class Test_C49328603_Verify_Players_List_Overlay(Common):
    """
    TR_ID: C49328603
    NAME: Verify Players List Overlay
    DESCRIPTION: This test case verifies Players List Overlay.
    PRECONDITIONS: Feature epic: https://jira.egalacoral.com/browse/BMA-49261
    PRECONDITIONS: Feature invision: https://projects.invisionapp.com/share/ASHWPQ0DB8K#/screens/397567275
    PRECONDITIONS: Designs: https://app.zeplin.io/project/5e0a3b413cbeb61b6eb8f5c9/dashboard
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: - User is on Football event EDP, '5 A Side' sub tab (event type described above)
    PRECONDITIONS: - Player data and statisctic takes from local storage 'scoreBoards_dev_prematch_eventId'(receivs from Bnah) and from response 'players?obEventId=773006'
    PRECONDITIONS: ![](index.php?/attachments/get/61571599)
    """
    keep_browser_open = True

    def test_001_select_a_player_position_from_a_pitch_overlay(self):
        """
        DESCRIPTION: Select a Player position from a pitch overlay
        EXPECTED: Player List View is displayed.
        """
        pass

    def test_002_verify_player_list_view_overlay_content(self):
        """
        DESCRIPTION: Verify Player List View overlay content.
        EXPECTED: Player List View overlay should contain:
        EXPECTED: - '<Back' Button.
        EXPECTED: - Title "Add a 'Position name'" below the 'Back' button (e.g 'Add a Cruncher'. Position name sets in the CMS)
        EXPECTED: - SubTitle is the name of the Statistic (e.g. To Win X Tackles, To Make X Passes etc. sets in the CMS)
        EXPECTED: - Buttons 'All Players'(selected by default), 'Home', 'Away'.(For all positions except Goalkeeper).
        EXPECTED: - Event Name.
        EXPECTED: - The list of players.
        EXPECTED: ![](index.php?/attachments/get/59126054)
        EXPECTED: ![](index.php?/attachments/get/59126055)
        """
        pass

    def test_003_lick_on_the_home__away_button_for_all_positions_except_goalkeeper(self):
        """
        DESCRIPTION: Сlick on the Home / Away button. (For all positions except Goalkeeper)
        EXPECTED: A list of players from the selected team is displayed (Home or Away) with corresponding chevrons.
        """
        pass

    def test_004_lick_on_the_all_players_button_for_all_positions_except_goalkeeper(self):
        """
        DESCRIPTION: Сlick on the 'All Players' button. (For all positions except Goalkeeper)
        EXPECTED: A list of players from both teams is displayed (Home and Away).
        """
        pass

    def test_005_verify_a_player_card_content(self):
        """
        DESCRIPTION: Verify a player card content.
        EXPECTED: Player card should contain such details:
        EXPECTED: - Name of a player.
        EXPECTED: - Team name.
        EXPECTED: - Crest of the team made up of primary and secondary color set in CMS.
        EXPECTED: - Position playing (If received from Opta) [Goalkeeper -(GK), Defender - (DF), Midfielder - (MF), Forward -()].
        EXPECTED: - Stats of the player (If received from Opta).
        EXPECTED: - Chevron indicating the user can tap on the player  - when tapped launch the player card.
        """
        pass

    def test_006_click_on_the_back_button(self):
        """
        DESCRIPTION: Click on the 'Back' button.
        EXPECTED: User is returned to the pitch view.
        """
        pass

    def test_007_return_to_the_player_list_view_overlay_and_click_on_one_of_players_card(self):
        """
        DESCRIPTION: Return to the Player List View overlay and click on one of players card.
        EXPECTED: User is redirected to the 'Player card' of the selected player.
        """
        pass
