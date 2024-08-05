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
class Test_C50155078_Players_mapping_on_Players_List_view(Common):
    """
    TR_ID: C50155078
    NAME: Players mapping on 'Players List' view
    DESCRIPTION: This test case verifies how players from 2 providers (Banach and OPTA Scoreboards) are mapped, what player name is used to display in frontend and what happens when mapping is unsuccessful
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Football event details page that has all 5-A-Side configs
    PRECONDITIONS: 3. Choose the '5-A-Side' tab
    PRECONDITIONS: 4. Click/Tap on 'Build' button
    PRECONDITIONS: 5. Click '+' (add) button on 'Pitch' view
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

    def test_001_verify_list_of_players_displayed(self):
        """
        DESCRIPTION: Verify list of players displayed
        EXPECTED: * Only players from 'players?obEventId=YYYYY' response are displayed
        EXPECTED: * Players from OPTA Scoreboards that are not received form Banach won't be displayed:
        EXPECTED: ![](index.php?/attachments/get/63136299)
        """
        pass

    def test_002_verify_player_displaying_when_mapping_successfulie_name_property_from_banach_and_matchname_property_from_opta_scoreboards_match(self):
        """
        DESCRIPTION: Verify player displaying when mapping successful
        DESCRIPTION: (i.e. **name** property from Banach and **matchName** property from OPTA Scoreboards match)
        EXPECTED: * Player is displayed
        EXPECTED: * Player name corresponds to **name** property from Banach
        EXPECTED: * Statistics for that player is shown
        """
        pass

    def test_003_verify_player_displaying_when_mapping_unsuccessfulie_names_from_banach_and_opta_do_not_matchnote_can_be_triggered_using_charles_tool_edit_player_name_in_playersobeventidyyyyy_response(self):
        """
        DESCRIPTION: Verify player displaying when mapping unsuccessful
        DESCRIPTION: (i.e. names from Banach and OPTA do not match)
        DESCRIPTION: NOTE! Can be triggered, using Charles tool: edit player name in 'players?obEventId=YYYYY' response
        EXPECTED: * Player remains displayed
        EXPECTED: * Player name corresponds to **name** property from Banach
        EXPECTED: * Statistics for that player is 'N/A'
        EXPECTED: * Position for that player is NOT displayed
        EXPECTED: ![](index.php?/attachments/get/87034363)
        """
        pass

    def test_004_verify_player_displaying_when_mapping_unsuccessful_in_case_data_absence_from_opta_scoreboardsnote_check_the_case_when_players_parameter_from_scoreboards_dev_prematch_eventid_is_received_empty_eg_players(self):
        """
        DESCRIPTION: Verify player displaying when mapping unsuccessful in case data absence from Opta Scoreboards
        DESCRIPTION: **NOTE:** Check the case when 'Players' parameter from 'scoreBoards_dev_prematch_eventId' is received empty. (e.g. 'Players':{}))
        EXPECTED: * Players remain displayed
        EXPECTED: * Player names correspond to **name** property from Banach
        EXPECTED: * Statistics for players is 'N/A'
        EXPECTED: * Position for players is NOT displayed
        EXPECTED: ![](index.php?/attachments/get/120998673)
        """
        pass
