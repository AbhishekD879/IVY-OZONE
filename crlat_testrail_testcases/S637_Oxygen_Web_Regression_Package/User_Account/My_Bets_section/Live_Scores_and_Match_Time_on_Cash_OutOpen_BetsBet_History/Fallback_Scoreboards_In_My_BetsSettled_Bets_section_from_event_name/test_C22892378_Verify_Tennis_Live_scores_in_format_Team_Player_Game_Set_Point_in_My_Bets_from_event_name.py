import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C22892378_Verify_Tennis_Live_scores_in_format_Team_Player_Game_Set_Point_in_My_Bets_from_event_name(Common):
    """
    TR_ID: C22892378
    NAME: Verify Tennis Live scores in format Team/ Player  Game-Set-Point in 'My Bets' (from event name)
    DESCRIPTION: This test case verifies live scores displaying for <sport> in My Bets section (scores updates coming from event name in TI)
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
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has placed single/multiple bets on live tennis event (with cashout available)
    PRECONDITIONS: Event is started
    PRECONDITIONS: NOTE: in order to update event live scores, go to TI (backoffice) and update score in event name, that is in format:
    PRECONDITIONS: Team/Player A* (1) 1 30-30 2 (0) Team/Player B
    PRECONDITIONS: NOTE 2: team names and player names should NOT contain numbers in order to correctly display fallback scoreboards!
    PRECONDITIONS: Designs:
    PRECONDITIONS: Coral: https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3?seid=5c63e41624a2969ad0a0cbb8
    PRECONDITIONS: Ladbrokes: https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b?seid=5c62f42001bb399a4c863eca
    """
    keep_browser_open = True

    def test_001_navigate_to_open_bets_widget_in_opened_bets_tabbetslip_widget_in_my_bets_section(self):
        """
        DESCRIPTION: Navigate to 'Open Bets' widget in 'Opened Bets tab'/Betslip widget in My bets section
        EXPECTED: Bets placed within this section are displayed
        """
        pass

    def test_002_in_ti_update_the_score_in_event_name_for_teamplayer_ateamplayer_b_save_changesin_app_check_the_scores_are_updated(self):
        """
        DESCRIPTION: In TI: Update the score in event name (for Team/Player A/Team/Player B), save changes
        DESCRIPTION: In app: check the scores are updated
        EXPECTED: - Scores are updated immediately in real-time (without page refresh)
        EXPECTED: - Scores are in format: Team/Player A*	(1) 1 30-30 2 (0)	Team/Player B
        EXPECTED: Ladbrokes: ![](index.php?/attachments/get/36557)
        EXPECTED: Coral: ![](index.php?/attachments/get/36558)
        """
        pass

    def test_003_repeat_scores_update_several_times_from_ti_in_event_name(self):
        """
        DESCRIPTION: Repeat scores update several times from ti in event name
        EXPECTED: Scores get updated each time updates are made in backoffice in event name
        """
        pass

    def test_004_verify_multiple_selections_with_live_score_update(self):
        """
        DESCRIPTION: Verify Multiple selections with Live score update
        EXPECTED: Scores are updated for multiple selections in the same format
        """
        pass

    def test_005_verify_case_when_score_is_changed_before_application_is_opened(self):
        """
        DESCRIPTION: Verify case when score is changed before application is opened
        EXPECTED: If application was not started/opened and Score was changed for team/player, after opening application and verified event - updated Score is shown
        """
        pass

    def test_006_repeat_steps_above_for_cash_out_tabbetslip_widget_in_my_bets_section(self):
        """
        DESCRIPTION: Repeat steps above for 'Cash Out' tab/Betslip widget in My bets section
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_above_for_other_sports_from_preconditions(self):
        """
        DESCRIPTION: Repeat steps above for other sports from preconditions
        EXPECTED: 
        """
        pass
