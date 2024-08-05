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
class Test_C50044875_Verify_outfield_players_sorting_on_Players_List_view(Common):
    """
    TR_ID: C50044875
    NAME: Verify outfield player's sorting on 'Players List' view
    DESCRIPTION: This test case verifies outfield player's sorting on the 'Players List' view based on received stats
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
    PRECONDITIONS: - Statistic is mapped for the particular event. Use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=91089483#OPTA/BWINScoreboardmappingtoanOBevent-Appendix_A
    PRECONDITIONS: - Player's statisctic takes from local storage 'scoreBoards_dev_prematch_eventId'(receivs from Bnah) and from response 'players?obEventId=773006'
    PRECONDITIONS: ![](index.php?/attachments/get/61571599)
    PRECONDITIONS: - Players are taken from Banach provider and received in the following response:
    PRECONDITIONS: https://buildyourbet-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/api/v1/players?obEventId=XXXXX
    PRECONDITIONS: where
    PRECONDITIONS: XXXXX - Event ID
    PRECONDITIONS: ![](index.php?/attachments/get/62325587)
    """
    keep_browser_open = True

    def test_001_licktap_on_the_all_players_button_for_all_positions_except_goalkeeperverify_outfield_players_sorting_on_the_player_list_view(self):
        """
        DESCRIPTION: Сlick/Tap on the 'All Players' button (For all positions except Goalkeeper).
        DESCRIPTION: Verify outfield players sorting on the 'Player List' view.
        EXPECTED: Outfield Players are sorted by the following rules:
        EXPECTED: - the highest value for the selected stats
        EXPECTED: - alphabetically by player name in case the stats values are equal_
        EXPECTED: - alphabetically by player name in case the stats are not received at all
        """
        pass

    def test_002_licktap_on_the_homeaway_button_for_all_positions_except_goalkeeperverify_outfield_players_sorting_on_the_player_list_view(self):
        """
        DESCRIPTION: Сlick/Tap on the 'Home/Away' button (For all positions except Goalkeeper).
        DESCRIPTION: Verify outfield players sorting on the 'Player List' view.
        EXPECTED: Outfield Players are sorted by the following rules:
        EXPECTED: - the highest value for the selected stats
        EXPECTED: - alphabetically by player name in case the stats values are equals
        EXPECTED: - alphabetically by player name in case the stats are not received at all
        """
        pass
