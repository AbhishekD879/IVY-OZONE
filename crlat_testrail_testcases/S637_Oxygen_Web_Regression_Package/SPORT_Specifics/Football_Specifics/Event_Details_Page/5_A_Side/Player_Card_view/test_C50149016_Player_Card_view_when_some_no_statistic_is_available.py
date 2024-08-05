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
class Test_C50149016_Player_Card_view_when_some_no_statistic_is_available(Common):
    """
    TR_ID: C50149016
    NAME: 'Player Card' view when some/no statistic is available
    DESCRIPTION: This test case verifies 'Player Card' view when only some statistic is available/ no statistic is available
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Football event details page that has all 5-A-Side configs
    PRECONDITIONS: 3. Choose the '5-A-Side' tab
    PRECONDITIONS: 4. Click/Tap on 'Build' button
    PRECONDITIONS: 5. Click '+' (add) button on 'Pitch' view for selecting some player position with the configured statistic name via CMS
    PRECONDITIONS: *Please note that OPTA stats are mapping is not needed for this TC*
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
    PRECONDITIONS: - Player's statistic is taken from local storage 'scoreBoards_dev_prematch_eventId':
    PRECONDITIONS: ![](index.php?/attachments/get/61571599)
    PRECONDITIONS: - Players are taken from Banach provider and received in the following response:
    PRECONDITIONS: https://buildyourbet-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/api/v1/players?obEventId=XXXXX
    PRECONDITIONS: where
    PRECONDITIONS: XXXXX - Event ID
    PRECONDITIONS: ![](index.php?/attachments/get/62325587)
    """
    keep_browser_open = True

    def test_001_select_the_player_that_doesnt_have_all_statistics(self):
        """
        DESCRIPTION: Select the player that doesn't have all statistics
        EXPECTED: * All statistic labels are displayed
        EXPECTED: * Statistic value is '0' if statistic has not been received from Opta
        EXPECTED: (e.g. if 'Assists' statistic is not received, then 'Assists' has '0' value)
        """
        pass

    def test_002_select_the_player_that_has_no_statistics_at_all(self):
        """
        DESCRIPTION: Select the player that has NO statistics at all
        EXPECTED: * 'Position' is not displayed in the header of overlay
        EXPECTED: * Vertical slash between 'Team name' and 'Position' is not displayed
        EXPECTED: * All statistic labels are displayed
        EXPECTED: * All statistic values are '0'
        EXPECTED: ![](index.php?/attachments/get/87143695)
        """
        pass

    def test_003_verify_that_when_no_attendanceappearances_are_received_from_optavia_local_storage_and_the_message_is_displayed_on_player_card_view(self):
        """
        DESCRIPTION: Verify that when no 'Attendance:'Appearances'' are received from OPTA(via local storage) and the message is displayed on Player card view
        EXPECTED: **When BMA-54579 is implemented after OX104**
        EXPECTED: The message will be displayed:
        EXPECTED: *Player Statisics unavailable for the first game of a league season or first round of a cup competition*
        EXPECTED: ![](index.php?/attachments/get/118215113)
        """
        pass
