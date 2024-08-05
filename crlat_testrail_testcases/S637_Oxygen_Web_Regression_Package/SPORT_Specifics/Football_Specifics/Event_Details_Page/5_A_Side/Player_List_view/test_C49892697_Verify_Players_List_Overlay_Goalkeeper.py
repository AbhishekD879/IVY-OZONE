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
class Test_C49892697_Verify_Players_List_Overlay_Goalkeeper(Common):
    """
    TR_ID: C49892697
    NAME: Verify Players List Overlay (Goalkeeper)
    DESCRIPTION: This test case verifies Players List Overlay when Goalkeeper is selected.
    DESCRIPTION: As per BMA-56377 This test case verifies that Stats (Markets are displayed) before selecting the Player
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
    PRECONDITIONS: - Goalkeeper have title: 'Goalkeeper' in /players response
    PRECONDITIONS: ![](index.php?/attachments/get/113960089)
    """
    keep_browser_open = True

    def test_001_select_a_player_position_from_a_pitch_overlay_goalkeeper(self):
        """
        DESCRIPTION: Select a Player position from a pitch overlay (Goalkeeper)
        EXPECTED: Player List View is displayed.
        """
        pass

    def test_002_verify_player_list_view_overlay_content(self):
        """
        DESCRIPTION: Verify Player List View overlay content.
        EXPECTED: Player List View overlay should contain:
        EXPECTED: - '<Back' Button.
        EXPECTED: - Title "Add a 'Position name'" below the 'Back' button (e.g 'Add a Goalkeeper'. Position name sets in the CMS)
        EXPECTED: - SubTitle is the name of the Statistic (e.g. To Make X Tackles, To Make X Passes etc. sets in the CMS) should be displayed in Blue with Chevron as per Zeplin
        EXPECTED: ![](index.php?/attachments/get/122292704)
        EXPECTED: - Buttons 'All Players'/'Home'/'Away' shouldn't be displayed.
        EXPECTED: - Event Name.
        EXPECTED: - The list of players.
        """
        pass

    def test_003_verify_that_goalkeepers_received_from_players_request_are_shown_in_the_players_list(self):
        """
        DESCRIPTION: Verify that goalkeepers received from /players request are shown in the Players List
        EXPECTED: All Goalkeepers are shown in the Players List
        EXPECTED: ![](index.php?/attachments/get/122292706)
        """
        pass

    def test_004_verify_a_player_card_content(self):
        """
        DESCRIPTION: Verify a player card content.
        EXPECTED: Player card should contain such details:
        EXPECTED: - Name of the player.
        EXPECTED: - Team name.
        EXPECTED: - Crest of the team made up of primary and secondary color set in CMS.
        EXPECTED: - Position playing (If available)in brackets.
        EXPECTED: - Stats of the player (If available from Datahub feed, eg. 'Avg Coals Conceded per game: 1.5').
        EXPECTED: - Chevron indicating the user can tap on the player (on the right of player card)
        """
        pass

    def test_005_click_on_the_back_button(self):
        """
        DESCRIPTION: Click on the 'Back' button.
        EXPECTED: User is returned to the pitch view.
        """
        pass

    def test_006_return_to_the_player_list_view_overlay_and_click_on_one_of_a_player_card(self):
        """
        DESCRIPTION: Return to the Player List View overlay and click on one of a player card.
        EXPECTED: User is redirected to the 'Player card' of the selected player.
        """
        pass
