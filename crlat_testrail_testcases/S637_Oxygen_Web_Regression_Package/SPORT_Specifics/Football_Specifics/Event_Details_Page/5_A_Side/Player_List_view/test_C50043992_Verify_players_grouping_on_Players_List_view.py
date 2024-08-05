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
class Test_C50043992_Verify_players_grouping_on_Players_List_view(Common):
    """
    TR_ID: C50043992
    NAME: Verify players grouping on 'Players List' view
    DESCRIPTION: This test case verifies players grouping on 'Players List' view.
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Football event details page that has all 5-A-Side configs
    PRECONDITIONS: 3. Choose the '5-A-Side' tab
    PRECONDITIONS: 4. Click/Tap on 'Build' button
    PRECONDITIONS: 5. Click '+' (add) button on 'Pitch' view for selecting some player position with the configured statistic name via CMS
    PRECONDITIONS: 6. Make sure that 'Player List' view is opened
    PRECONDITIONS: **5-A-Side config:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Formations are added in CMS -> BYB -> 5 A Side
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: - Player's statisctic takes from local storage 'scoreBoards_dev_prematch_eventId'(receivs from Bnah) and from response 'players?obEventId=773006'
    PRECONDITIONS: ![](index.php?/attachments/get/61571599)
    PRECONDITIONS: - Players are taken from Banach provider and received in the following response:
    PRECONDITIONS: https://buildyourbet-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/api/v1/players?obEventId=XXXXX
    PRECONDITIONS: where
    PRECONDITIONS: XXXXX - Event ID
    PRECONDITIONS: ![](index.php?/attachments/get/62325587)
    """
    keep_browser_open = True

    def test_001_licktap_on_the_all_players_button_for_all_positions_except_goalkeeperverify_that_list_of_players_on_the_player_list_fits_the_data_received_from_banach_use_response_mentioned_in_preconditions(self):
        """
        DESCRIPTION: Сlick/Tap on the 'All Players' button (For all positions except Goalkeeper).
        DESCRIPTION: Verify that list of players on the 'Player List' fits the data received from Banach (use response mentioned in preconditions)
        EXPECTED: * A list of players from both teams is displayed (Home and Away)
        EXPECTED: * A list of players received from Banach is displayed on the 'Player List' view
        """
        pass

    def test_002_licktap_on_the_homeaway_button_for_all_positions_except_goalkeeperverify_that_list_of_players_on_the_player_list_fits_the_data_received_from_banach_according_to_the_selected_team_use_response_mentioned_in_preconditions(self):
        """
        DESCRIPTION: Сlick/Tap on the 'Home/Away' button (For all positions except Goalkeeper).
        DESCRIPTION: Verify that list of players on the 'Player List' fits the data received from Banach according to the selected team (use response mentioned in preconditions)
        EXPECTED: * A list of players from the selected team is displayed (Home or Away)
        EXPECTED: * A list of players received from Banach is displayed on the 'Player List' view according to the selected team
        """
        pass
