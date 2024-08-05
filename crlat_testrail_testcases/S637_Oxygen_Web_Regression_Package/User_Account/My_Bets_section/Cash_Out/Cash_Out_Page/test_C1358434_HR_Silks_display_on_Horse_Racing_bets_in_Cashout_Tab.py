import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C1358434_HR_Silks_display_on_Horse_Racing_bets_in_Cashout_Tab(Common):
    """
    TR_ID: C1358434
    NAME: HR Silks display on Horse Racing bets in Cashout Tab
    DESCRIPTION: This test case verifies that HR Silks are displayed on Horse Racing bets in the Cashout tab
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: [BMA-24366 CashOut / Open Bets: Include Horse Racing Silks] [1]
    DESCRIPTION: [BMA-27242 Open Bets / Bet History : Include Horse Racing Silks for Forecast / Tricast Bets] [2]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-24366
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-27242
    DESCRIPTION: AUTOTEST [C9698116]
    DESCRIPTION: AUTOTEST [C10582964]
    PRECONDITIONS: User is logged in;
    PRECONDITIONS: User has placed bets on **Horse Racing** races with silks (Singles, EW, TC/FC bets);
    PRECONDITIONS: User has placed bets on **Horse Racing** races without silks (Singles, EW, TC/FC bets);
    """
    keep_browser_open = True

    def test_001_navigate_to_cashout_tab_on_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cashout' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: 
        """
        pass

    def test_002_verify_single_horse_racing_bet_available(self):
        """
        DESCRIPTION: Verify Single horse racing bet available
        EXPECTED: Correct silk is displayed for placed bet
        """
        pass

    def test_003_verify_single_horse_racing_ew_bet_available(self):
        """
        DESCRIPTION: Verify Single horse racing EW bet available
        EXPECTED: Correct silk is displayed for placed bet
        """
        pass

    def test_004_repeat_steps_2_3_for_bets_placed_on_races_without_silks(self):
        """
        DESCRIPTION: Repeat steps 2-3 for bets placed on races without silks
        EXPECTED: * Generic silks are displayed for Singles & EW Single bets
        EXPECTED: * Generic silks are displayed for TC/FC bets
        """
        pass

    def test_005_verify_bet_placed_on_unnamed_favourite(self):
        """
        DESCRIPTION: Verify bet placed on Unnamed Favourite
        EXPECTED: Generic silk is displayed
        """
        pass

    def test_006_repeat_this_test_case_for_bet_slip_widget_for_tabletdesktop(self):
        """
        DESCRIPTION: Repeat this test case for:
        DESCRIPTION: * 'Bet Slip' widget (for Tablet/Desktop)
        EXPECTED: 
        """
        pass
