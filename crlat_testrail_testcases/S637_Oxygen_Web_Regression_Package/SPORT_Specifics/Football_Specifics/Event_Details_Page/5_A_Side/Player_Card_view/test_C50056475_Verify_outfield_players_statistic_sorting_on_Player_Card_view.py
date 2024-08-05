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
class Test_C50056475_Verify_outfield_players_statistic_sorting_on_Player_Card_view(Common):
    """
    TR_ID: C50056475
    NAME: Verify outfield player's statistic  sorting on 'Player Card' view
    DESCRIPTION: This test case verifies the outfield player's statistic sorting on 'Player Card' view
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Football event details page that has all 5-A-Side configs
    PRECONDITIONS: 3. Choose the '5-A-Side' tab
    PRECONDITIONS: 4. Click/Tap on 'Build' button
    PRECONDITIONS: 5. Click '+' (add) button on 'Pitch' view for selecting some player position with the configured statistic name via CMS
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
    PRECONDITIONS: - Player's statisctic takes from local storage 'scoreBoards_dev_prematch_eventId':
    PRECONDITIONS: ![](index.php?/attachments/get/61571599)
    PRECONDITIONS: - Players are taken from Banach provider and received in the following response:
    PRECONDITIONS: https://buildyourbet-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/api/v1/players?obEventId=XXXXX
    PRECONDITIONS: where
    PRECONDITIONS: XXXXX - Event ID
    PRECONDITIONS: ![](index.php?/attachments/get/62325587)
    PRECONDITIONS: - The Outfield player's stats label mapping according to stats name from CMS:
    PRECONDITIONS: ![](index.php?/attachments/get/90131239)
    """
    keep_browser_open = True

    def test_001_select_the_outfield_player_from_the_player_list_viewverify_top_stat_displaying_relevant_to_the_selected_market(self):
        """
        DESCRIPTION: Select the outfield player from the 'Player List' view.
        DESCRIPTION: Verify top stat displaying relevant to the selected market.
        EXPECTED: The following stats could be displayed as a top:
        EXPECTED: - "Tackles per game:"
        EXPECTED: - "Passes per game:"
        EXPECTED: - "Assists:"
        EXPECTED: - "Shots per game:"
        EXPECTED: - "Shots On Target per game:"
        EXPECTED: - "Goals:"
        EXPECTED: - "Cards:"
        """
        pass

    def test_002_select_the_outfield_player_from_the_player_list_viewverify_the_outfield_player_stats_sorting_on_the_player_card_view(self):
        """
        DESCRIPTION: Select the outfield player from the 'Player List' view.
        DESCRIPTION: Verify the outfield player stats sorting on the 'Player Card' view.
        EXPECTED: Outfield Players stats are sorted by the following rules:
        EXPECTED: * Stat relevant to the selected market is displayed at the top
        EXPECTED: * The hardcoded stats list is displayed below but the stat relevant to the selected market is excluded:
        EXPECTED: - "Appearances:"
        EXPECTED: - "Goals:"
        EXPECTED: - "Assists:"
        EXPECTED: - "Shots per game:"
        EXPECTED: - "Passes per game:"
        EXPECTED: * Stat is not duplicated in the list
        """
        pass
