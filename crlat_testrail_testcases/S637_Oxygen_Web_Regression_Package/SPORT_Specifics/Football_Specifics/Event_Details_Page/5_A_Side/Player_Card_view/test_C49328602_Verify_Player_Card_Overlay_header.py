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
class Test_C49328602_Verify_Player_Card_Overlay_header(Common):
    """
    TR_ID: C49328602
    NAME: Verify Player Card Overlay  header
    DESCRIPTION: This test case verifies Player Card Overlay header
    PRECONDITIONS: Feature epic: https://jira.egalacoral.com/browse/BMA-49261
    PRECONDITIONS: Feature invision: https://projects.invisionapp.com/share/ASHWPQ0DB8K#/screens/397567275
    PRECONDITIONS: Designs: https://app.zeplin.io/project/5e0a3b413cbeb61b6eb8f5c9/dashboard
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled in CMS -> BYB -> Banach Leagues
    PRECONDITIONS: - Banach leagues are enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - Banach 'Player Bets' market is added in CMS -> BYB -> BYB Markets на  'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: - User is on Football event EDP, '5 A Side' sub tab (event type described above)
    """
    keep_browser_open = True

    def test_001_click_on_build_a_team_button___click_on_plus_button_near_the_player_on_the_overlay___in_the_list_of_players_select_one_specific(self):
        """
        DESCRIPTION: Click on 'Build a team' button -> click on + button near the player on the overlay -> in the list of players select one specific
        EXPECTED: Player Card Overlay is displayed
        EXPECTED: ![](index.php?/attachments/get/59204747)
        EXPECTED: OX 103:
        EXPECTED: ![](index.php?/attachments/get/114763993)
        """
        pass

    def test_002_verify_header_of_the_player_overlay(self):
        """
        DESCRIPTION: Verify header of the player overlay
        EXPECTED: The header consists of:
        EXPECTED: -'Back' button at the top of the header on the left
        EXPECTED: - background color taken from Team Color hex code in the CMS (BYB section -> Asset Management)
        EXPECTED: ![](index.php?/attachments/get/114763998)
        EXPECTED: - Player name (received in response in Network tab: 'players?obEventId=773006')
        EXPECTED: - Team name below (received in response in Network tab: 'players?obEventId=773006')
        EXPECTED: - Player role (if received from Opta, eg. Keeper, located in: 'Application -> local storage -> scoreBoards_dev_prematch_773006)
        EXPECTED: ![](index.php?/attachments/get/61571600)
        EXPECTED: OX 103
        EXPECTED: - Player role (received in response in Network tab: 'players?obEventId=773006')
        """
        pass

    def test_003_verify_default_color_for_header_when_no_color_is_set_in_cms(self):
        """
        DESCRIPTION: Verify default color for header when no color is set in CMS
        EXPECTED: Default color of header is grey (#777777) with the gradient (as on the screen)
        EXPECTED: ![](index.php?/attachments/get/61407360)
        """
        pass

    def test_004_change_team_colour_hex_code_in_cms_byb_section___asset_management_and_reload_page_on_ui(self):
        """
        DESCRIPTION: Change Team Colour hex code in CMS (BYB section -> Asset Management) and reload page on UI
        EXPECTED: Color on UI changes accordingly (with the gradient)
        """
        pass

    def test_005_click_on_the_back_button(self):
        """
        DESCRIPTION: Click on the 'Back' button
        EXPECTED: User is returned to the Player List view
        """
        pass
