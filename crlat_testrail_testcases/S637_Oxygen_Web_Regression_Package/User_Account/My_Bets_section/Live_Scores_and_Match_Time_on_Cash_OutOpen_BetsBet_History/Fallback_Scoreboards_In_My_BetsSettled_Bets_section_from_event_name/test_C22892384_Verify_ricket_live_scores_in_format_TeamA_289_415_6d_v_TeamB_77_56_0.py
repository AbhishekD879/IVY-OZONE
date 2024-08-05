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
class Test_C22892384_Verify_ricket_live_scores_in_format_TeamA_289_415_6d_v_TeamB_77_56_0(Common):
    """
    TR_ID: C22892384
    NAME: Verify Сricket live scores in format '|TeamA| 289 415/6d v |TeamB| 77 56/0'
    DESCRIPTION: This test case verifies live scores displaying for Cricket in My Bets section (scores updates coming from event name in TI)
    DESCRIPTION: Sport Cricket can be used as examples for testing, but should not be limited to this sport. For example, Darts!!! may appear in different formats depending on the event.
    DESCRIPTION: Related jira epic:
    DESCRIPTION: https://jira.egalacoral.com/browse/BMA-43300
    PRECONDITIONS: Backoffices:
    PRECONDITIONS: Ladbrokes: https://tst2-backoffice-lcm.ladbrokes.com
    PRECONDITIONS: Coral: https://backoffice-tst2.coral.co.uk/ti
    PRECONDITIONS: Confluence credentials:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=OpenBet+Systems
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Ladbrokes+Environments
    PRECONDITIONS: - User is logged in
    PRECONDITIONS: - User has placed single/multiple bets on live cricket event (with cashout available)
    PRECONDITIONS: - Event is started
    PRECONDITIONS: NOTE: in order to update event live scores, go to TI (backoffice) and update score in event name, that is in formats:
    PRECONDITIONS: |Home A| 123 234/45 v |Away A|
    PRECONDITIONS: |Home A| 123 v |Away A| 234/5d
    PRECONDITIONS: |Home A| 123 345/9d v |Away A| 234/5d
    PRECONDITIONS: |Home A| 123 345/9d v |Away A| 234/5d 430/10
    PRECONDITIONS: Designs:
    PRECONDITIONS: Coral: https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3/screen/5c63e3fe7a9de29a336f6966
    PRECONDITIONS: Ladbrokes: https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b/screen/5c62f4121737de9aefb0d368
    """
    keep_browser_open = True

    def test_001_navigate_to_cashout_tabbet_slip_widget_in_my_bets_section(self):
        """
        DESCRIPTION: Navigate to 'Cashout' tab/'Bet Slip' widget in My bets section
        EXPECTED: Bets placed within this section are displayed
        """
        pass

    def test_002_in_ti_update_the_score_in_event_name_for_team_ateam_bin_such_format__homea_123_23445_v_away_a_save_changesin_app_check_the_scores_are_updated(self):
        """
        DESCRIPTION: In TI: Update the score in event name (for team A/team B)in such format  **'|HomeA| 123 234/45 v |Away A|'**, save changes
        DESCRIPTION: In app: check the scores are updated
        EXPECTED: - Scores are updated immediately in real time (without page refresh)
        EXPECTED: - Scores are in format: HomeA v AwayA **234/45|- - **
        EXPECTED: ![](index.php?/attachments/get/36551)
        """
        pass

    def test_003_in_ti_update_the_score_in_event_name_for_team_ateam_bin_such_format__homea_123_v_away_a_2345d_save_changesin_app_check_the_scores_are_updated(self):
        """
        DESCRIPTION: In TI: Update the score in event name (for team A/team B)in such format  **'|HomeA| 123 v |Away A| 234/5d'**, save changes
        DESCRIPTION: In app: check the scores are updated
        EXPECTED: - Scores are updated immediately in real time (without page refresh)
        EXPECTED: - Scores are in format: **HomeA v AwayA 123|234/5d **
        """
        pass

    def test_004_in_ti_update_the_score_in_event_name_for_team_ateam_bin_such_format__teama_289_4156d_v_teamb_77_560_save_changesin_app_check_the_scores_are_updated(self):
        """
        DESCRIPTION: In TI: Update the score in event name (for team A/team B)in such format  **'|TeamA| 289 415/6d v |TeamB| 77 56/0'**, save changes
        DESCRIPTION: In app: check the scores are updated
        EXPECTED: - Scores are updated immediately in real time (without page refresh)
        EXPECTED: - Scores are in format:TeamA v TeamB **289 415/6d|77 56/0**
        EXPECTED: - Appears '2nd' label which indicates that 2nd inning stars. (When the second inning starts you will see additional score of 415/6d for the second inning (next to the previous day score of 289)
        EXPECTED: ![](index.php?/attachments/get/36552)
        """
        pass

    def test_005_in_ti_update_the_score_in_event_name_for_team_ateam_bin_such_formatshome_a_123_23445_v_away_ahome_a_123_v_away_a_2345dhome_a_123_3459d_v_away_a_2345dhome_a_123_3459d_v_away_a_2345d_43010(self):
        """
        DESCRIPTION: In TI: Update the score in event name (for team A/team B)in such formats:
        DESCRIPTION: **|Home A| 123 234/45 v |Away A|**
        DESCRIPTION: **|Home A| 123 v |Away A| 234/5d**
        DESCRIPTION: **|Home A| 123 345/9d v |Away A| 234/5d**
        DESCRIPTION: **|Home A| 123 345/9d v |Away A| 234/5d 430/10**
        EXPECTED: - Scores are updated immediately in real time (without page refresh)
        """
        pass

    def test_006_repeat_scores_update_several_times_from_ti_in_event_name(self):
        """
        DESCRIPTION: Repeat scores update several times from TI in event name
        EXPECTED: Scores get updated each time updates are made in backoffice in event name
        """
        pass

    def test_007_verify_multiple_selections_with_live_score_update(self):
        """
        DESCRIPTION: Verify Multiple selections with Live score update
        EXPECTED: Scores are updated for multiple selections in same format
        """
        pass

    def test_008_verify_case_when_score_is_changed_before_application_is_opened(self):
        """
        DESCRIPTION: Verify case when score is changed before application is opened
        EXPECTED: If application was not started/opened and Score was changed for HOME/AWAY team, after opening application and verified event - updated Score is shown
        """
        pass

    def test_009_repeat_steps_above_for_open_bets(self):
        """
        DESCRIPTION: Repeat steps above for Open Bets
        EXPECTED: 
        """
        pass
