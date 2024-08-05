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
class Test_C52155793_Verify_Stats_displaying_on_Player_card_in_Players_List_view_if_No_Stats_available_for_this_Player(Common):
    """
    TR_ID: C52155793
    NAME: Verify Stats displaying on Player card in 'Players List' view if No Stats available for this Player
    DESCRIPTION: This test case verifies Player card on Players List Overlay if No Stats available
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Football event details page that has all 5-A-Side configs
    PRECONDITIONS: 3. Choose the '5-A-Side' tab
    PRECONDITIONS: 4. Click/Tap on 'Build' button
    PRECONDITIONS: 5. Click '+' (add) button on 'Pitch' view for selecting some player position with the configured statistic name via CMS
    PRECONDITIONS: 6. Make sure no OPTA stats are mapped
    PRECONDITIONS: 7. Make sure that 'Player List' view is opened
    PRECONDITIONS: Please note that the
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

    def test_001_verify_stats_displaying_on_player_card_in_player_list__when_stats_for_that_player_is_not_received_from_opta(self):
        """
        DESCRIPTION: Verify Stats displaying on Player Card in Player list  when stats for that player is NOT received from Opta
        EXPECTED: * Stats label is displayed with 'N/A' value
        EXPECTED: ![](index.php?/attachments/get/74408401)
        """
        pass

    def test_002_verify_position_not_displaying_on_player_card_in_player_list__when_position_for_that_player_is_not_received_from_opta(self):
        """
        DESCRIPTION: Verify 'Position' not displaying on Player Card in Player list  when position for that player is NOT received from Opta
        EXPECTED: * 'Position' is not displayed
        EXPECTED: ![](index.php?/attachments/get/75297744)
        """
        pass

    def test_003_verify_that_when_no_attendanceappearances_are_received_from_optavia_local_storage_and_the_message_is_displayed_on_player_list_view(self):
        """
        DESCRIPTION: Verify that when no 'Attendance:'Appearances'' are received from OPTA(via local storage) and the message is displayed on Player List View
        EXPECTED: **When BMA-54579 is implemented after OX104**
        EXPECTED: The message will be displayed:
        EXPECTED: *Player Statisics unavailable for the first game of a league season or first round of a cup competition*
        EXPECTED: ![](index.php?/attachments/get/118215108)
        """
        pass
