import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.bet_history_open_bets
@vtest
class Test_C22930125_Verify_Tennis_Live_scores_in_format_Team_Player_Game_Set_Point_for_Doubles_and_Long_Names_in_My_Bets_from_event_name(Common):
    """
    TR_ID: C22930125
    NAME: Verify Tennis Live scores in format Team/ Player  Game-Set-Point for Doubles and Long Names in 'My Bets' (from event name)
    DESCRIPTION: This test case verifies live scores displaying for <sport> with Doubles and Long Names in My Bets section (scores updates coming from event name in TI)
    DESCRIPTION: Sports related to this template: Tennis.
    DESCRIPTION: Sports listed against the templates can be used as examples for testing, but should not be limited to these sports. For example, Darts may appear in different formats depending on the event.
    DESCRIPTION: Related jira epic:
    DESCRIPTION: https://jira.egalacoral.com/browse/BMA-43300
    PRECONDITIONS: Backoffices:
    PRECONDITIONS: Ladbrokes: https://tst2-backoffice-lcm.ladbrokes.com
    PRECONDITIONS: Coral: https://backoffice-tst2.coral.co.uk/ti
    PRECONDITIONS: Confluence credentials:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=OpenBet+Systems
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Ladbrokes+Environments
    PRECONDITIONS: - User is logged in
    PRECONDITIONS: - User has placed single/multiple bets on live tennis event (with cashout available)
    PRECONDITIONS: - Event is started
    PRECONDITIONS: - Bet already has results (either market is resulted but event is not yet finished or bet is cashed out) - for verifying event in Settle Bets
    PRECONDITIONS: NOTE: in order to update event live scores, go to TI (backoffice) and update score in event name, that is in format:
    PRECONDITIONS: Team/Player A* (1) 1 30-30 2 (0) Team/Player B
    PRECONDITIONS: NOTE 2: team names and player names should NOT contain numbers in order to correctly display fallback scoreboards!
    PRECONDITIONS: Designs:
    PRECONDITIONS: Coral: https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3?seid=5c63e41624a2969ad0a0cbb8
    PRECONDITIONS: Ladbrokes: https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b?seid=5c62f42001bb399a4c863eca
    """
    keep_browser_open = True

    def test_001_navigate_to_opened_bets_tabbetslip_widget_in_my_bets_section(self):
        """
        DESCRIPTION: Navigate to 'Opened Bets tab'/Betslip widget in My bets section
        EXPECTED: Bets placed within this section are displayed.
        EXPECTED: - Scores are in format: Team/Player A*	(1) 1 30-30 2 (0)	Team/Player B
        EXPECTED: Scores are displayed correctly with Doubles/Long Names of event
        EXPECTED: Ladbrokes: ![](index.php?/attachments/get/36578)
        EXPECTED: Coral: ![](index.php?/attachments/get/36580)
        """
        pass

    def test_002_verify_multiple_selections_with_live_score_in_format_team_player__game_set_point_for_doubleslong_names(self):
        """
        DESCRIPTION: Verify Multiple selections with Live score in format Team/ Player  Game-Set-Point for Doubles/Long Names
        EXPECTED: Scores are displayed correctly with Doubles/Long Names of event
        """
        pass

    def test_003_repeat_steps_above_for_cash_out_tabbetslip_widget_in_my_bets_section(self):
        """
        DESCRIPTION: Repeat steps above for 'Cash Out' tab/Betslip widget in My bets section
        EXPECTED: 
        """
        pass

    def test_004_repeat_steps_above_for_settled_bet_tabbetslip_widget_in_my_bets_section(self):
        """
        DESCRIPTION: Repeat steps above for 'Settled Bet' tab/Betslip widget in My bets section
        EXPECTED: 
        """
        pass

    def test_005_repeat_steps_above_for_other_sports_from_preconditions(self):
        """
        DESCRIPTION: Repeat steps above for other sports from preconditions
        EXPECTED: 
        """
        pass
