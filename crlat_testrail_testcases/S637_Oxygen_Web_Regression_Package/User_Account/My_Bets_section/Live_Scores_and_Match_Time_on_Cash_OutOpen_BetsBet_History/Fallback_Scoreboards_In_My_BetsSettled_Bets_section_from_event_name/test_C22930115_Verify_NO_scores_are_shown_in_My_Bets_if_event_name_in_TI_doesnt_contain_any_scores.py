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
class Test_C22930115_Verify_NO_scores_are_shown_in_My_Bets_if_event_name_in_TI_doesnt_contain_any_scores(Common):
    """
    TR_ID: C22930115
    NAME: Verify NO scores are shown in My Bets if event name  in TI doesn't contain any scores
    DESCRIPTION: This test case verifies that NO scores will be shown in My Bets if event name in TI doesn't contain any scores
    DESCRIPTION: This test case is valid for all sports.
    DESCRIPTION: Related jira epic:
    DESCRIPTION: https://jira.egalacoral.com/browse/BMA-43300
    PRECONDITIONS: Backoffices:
    PRECONDITIONS: Ladbrokes: https://tst2-backoffice-lcm.ladbrokes.com
    PRECONDITIONS: Coral: https://backoffice-tst2.coral.co.uk/ti
    PRECONDITIONS: Confluence credentials:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=OpenBet+Systems
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Ladbrokes+Environments
    PRECONDITIONS: - User is logged in
    PRECONDITIONS: - User has placed single/multiple bets on live event (with cashout available)
    PRECONDITIONS: - Event is started
    PRECONDITIONS: - No Scores available in the event name in TI
    PRECONDITIONS: - Bet already has results (either market is resulted but event is not yet finished or bet is cashed out) - for verifying event in Settle Bets
    """
    keep_browser_open = True

    def test_001_navigate_to_open_bets_tabbetslip_widget_in_my_bets_section(self):
        """
        DESCRIPTION: Navigate to Open Bets tab/Betslip widget in My bets section
        EXPECTED: Bets placed within this section are displayed.
        EXPECTED: No scores are displayed.
        """
        pass

    def test_002_verify_multiple_selections_where_one_of_the_events_hasnt_score(self):
        """
        DESCRIPTION: Verify Multiple selections where one of the events hasn't score.
        EXPECTED: No scores are displayed for event that hasn't template scores in name in TI
        """
        pass

    def test_003_repeat_steps_above_for_cash_out_tabbetslip_widget_in_my_bets_section(self):
        """
        DESCRIPTION: Repeat steps above for Cash Out tab/Betslip widget in My bets section
        EXPECTED: 
        """
        pass

    def test_004_repeat_steps_above_for_settle_bets_tabbetslip_widget_in_my_bets_section(self):
        """
        DESCRIPTION: Repeat steps above for Settle Bets tab/Betslip widget in My bets section
        EXPECTED: 
        """
        pass
