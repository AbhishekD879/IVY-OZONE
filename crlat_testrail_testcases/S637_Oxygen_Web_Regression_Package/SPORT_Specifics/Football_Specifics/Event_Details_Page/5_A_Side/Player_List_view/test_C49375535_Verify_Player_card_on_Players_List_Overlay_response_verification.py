import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.5_a_side
@vtest
class Test_C49375535_Verify_Player_card_on_Players_List_Overlay_response_verification(Common):
    """
    TR_ID: C49375535
    NAME: Verify Player card on Players List Overlay (response verification)
    DESCRIPTION: This test case verifies Player card on Players List Overlay (data taken from response).
    PRECONDITIONS: Feature epic: https://jira.egalacoral.com/browse/BMA-49261
    PRECONDITIONS: Feature invision: https://projects.invisionapp.com/share/ASHWPQ0DB8K#/screens/397567275
    PRECONDITIONS: Designs: https://app.zeplin.io/project/5e0a3b413cbeb61b6eb8f5c9/dashboard
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: - User is on Football event EDP, '5 A Side' sub tab (event type described above) -> User selected player position from pitch overlay-> User on the Players List View
    PRECONDITIONS: - Player data and statisctic takes from local storage 'scoreBoards_dev_prematch_eventId'(receivs from Bnah) and from response 'players?obEventId=773006'
    PRECONDITIONS: ![](index.php?/attachments/get/61571599)
    """
    keep_browser_open = True

    def test_001_load_app_open_players_list_view(self):
        """
        DESCRIPTION: Load App, Open Players List View.
        EXPECTED: Players list opened with such fields.
        EXPECTED: ![](index.php?/attachments/get/76520634)
        """
        pass

    def test_002_open_response_players_with_player_info_and_compare_with_displayed_data_on_uicheck_player_name(self):
        """
        DESCRIPTION: Open response (players) with player info and compare with displayed data on UI.
        DESCRIPTION: Check 'Player Name'
        EXPECTED: UI should display correct data.
        EXPECTED: ![](index.php?/attachments/get/75809187)
        """
        pass

    def test_003_open_response_players_with_player_info_and_compare_with_displayed_data_on_uicheck_team_name(self):
        """
        DESCRIPTION: Open response (players) with player info and compare with displayed data on UI.
        DESCRIPTION: Check 'Team Name'
        EXPECTED: UI should display correct data.
        EXPECTED: ![](index.php?/attachments/get/75809188)
        """
        pass

    def test_004_open_local_storage_scoreboards_dev_prematch_eventid_with_player_info_and_compare_with_displayed_data_on_uicheck_players_statistics(self):
        """
        DESCRIPTION: Open local storage (scoreBoards_dev_prematch_eventID) with player info and compare with displayed data on UI.
        DESCRIPTION: Check player's statistics.
        EXPECTED: UI should display correct data.
        EXPECTED: ![](index.php?/attachments/get/75809189)
        """
        pass

    def test_005_open_local_storage_scoreboards_dev_prematch_eventid_with_player_info_and_compare_with_displayed_data_on_uicheck_the_position_of_the_player(self):
        """
        DESCRIPTION: Open local storage (scoreBoards_dev_prematch_eventID) with player info and compare with displayed data on UI.
        DESCRIPTION: Check the position of the player.
        EXPECTED: UI should display correct data.
        EXPECTED: ![](index.php?/attachments/get/75809227)
        """
        pass

    def test_006_open_local_storage_scoreboards_dev_prematch_eventid_with_player_info_and_compare_with_displayed_data_on_uicheck_match_name(self):
        """
        DESCRIPTION: Open local storage (scoreBoards_dev_prematch_eventID) with player info and compare with displayed data on UI.
        DESCRIPTION: Check Match name.
        EXPECTED: UI should display correct data.
        EXPECTED: ![](index.php?/attachments/get/75809238)
        """
        pass

    def test_007_open_five_a_side_formations_response_and_compare_with_displayed_data_on_ui(self):
        """
        DESCRIPTION: Open 'five-a-side-formations' response and compare with displayed data on UI.
        EXPECTED: UI should display correct data.
        EXPECTED: ![](index.php?/attachments/get/76722451)
        """
        pass
