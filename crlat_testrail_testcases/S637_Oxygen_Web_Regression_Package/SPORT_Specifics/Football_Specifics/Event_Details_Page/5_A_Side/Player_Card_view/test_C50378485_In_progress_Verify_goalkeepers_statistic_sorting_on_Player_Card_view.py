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
class Test_C50378485_In_progress_Verify_goalkeepers_statistic_sorting_on_Player_Card_view(Common):
    """
    TR_ID: C50378485
    NAME: [In progress] Verify goalkeeper's statistic  sorting on 'Player Card' view
    DESCRIPTION: This test case verifies the goalkeeper's statistic  sorting on 'Player Card' view
    DESCRIPTION: NOTE! Take into account the following when updating this TC:
    DESCRIPTION: From your data feed you should show the following for Goalkeepers:
    DESCRIPTION: Goals Conceded per game = [conceeded] / [appearances]
    DESCRIPTION: Clean Sheets = [clean sheets]
    DESCRIPTION: Saves per game = [totalSaves]/ [appearances]
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
    PRECONDITIONS: - Goalkeeper's statisctic takes from local storage 'scoreBoards_dev_prematch_eventId':
    PRECONDITIONS: ![](index.php?/attachments/get/61571599)
    PRECONDITIONS: - Goalkeepers are taken from Banach provider and received in the following response:
    PRECONDITIONS: https://buildyourbet-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/api/v1/players?obEventId=XXXXX
    PRECONDITIONS: where
    PRECONDITIONS: XXXXX - Event ID
    PRECONDITIONS: ![](index.php?/attachments/get/62325587)
    PRECONDITIONS: - Goalkeeper's stats label mapping according to stats name from CMS:
    PRECONDITIONS: ![](index.php?/attachments/get/63405661)
    """
    keep_browser_open = True

    def test_001_select_the_goalkeeper_from_the_player_list_viewverify_top_stat_displaying_relevant_to_the_selected_market(self):
        """
        DESCRIPTION: Select the goalkeeper from the 'Player List' view.
        DESCRIPTION: Verify top stat displaying relevant to the selected market.
        EXPECTED: The following stats could be displayed as a top:
        EXPECTED: - "Goals Conceded per game:"
        EXPECTED: - "Saves per game:"
        """
        pass

    def test_002_verify_the_goalkeeper_stats_sorting_on_the_player_card_view(self):
        """
        DESCRIPTION: Verify the goalkeeper stats sorting on the 'Player Card' view.
        EXPECTED: Goalkeeper stats are sorted by the following rules:
        EXPECTED: * Stat relevant to the selected market is displayed at the top
        EXPECTED: * The hardcoded stats list is displayed below but the stat relevant to the selected market is excluded:
        EXPECTED: - "Appearances:"
        EXPECTED: - "Goals Conceded per game:"
        EXPECTED: - "Saves per game:"
        EXPECTED: - "Penalty Saves:"
        EXPECTED: * Stat is not duplicated in the list
        """
        pass
