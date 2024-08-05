import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C29139_NEEDS_TO_BE_UPDATEDTrader_rejects_the_Bet(Common):
    """
    TR_ID: C29139
    NAME: [NEEDS TO BE UPDATED]Trader rejects the Bet
    DESCRIPTION: This test case verifies receiving rejected bet by a trader
    DESCRIPTION: Instruction how to decline Overask bets: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190955
    DESCRIPTION: AUTOTEST [C528082]
    PRECONDITIONS: - For selected User Overask functionality is enabled in backoffice tool (see instruction: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983 )
    PRECONDITIONS: - User is logged in to application
    PRECONDITIONS: **Note:**
    PRECONDITIONS: Example how to update: https://ladbrokescoral.testrail.com/index.php?/cases/view/29124
    """
    keep_browser_open = True

    def test_001_add_selection_from_racing_events_to_the_betslip(self):
        """
        DESCRIPTION: Add selection from Racing events to the Betslip
        EXPECTED: Selection is successfully added
        """
        pass

    def test_002_enter_stake_value_which_is_higher_then_maximum_limit_for_added_selection(self):
        """
        DESCRIPTION: Enter stake value which is higher then maximum limit for added selection
        EXPECTED: 
        """
        pass

    def test_003_tap_bet_now_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' button
        EXPECTED: *   Overask is triggered for the User
        EXPECTED: *   The bet review notification is shown to the User
        """
        pass

    def test_004_trigger_bet_rejection_by_trader_and_verify_rejected_bet_displaying_in_betslip(self):
        """
        DESCRIPTION: Trigger Bet rejection by Trader and verify rejected Bet displaying in Betslip
        EXPECTED: *   Info message is displayed above 'GO BETTTING' button with text: 'This bet has not been accepted by traders!'
        EXPECTED: *   Rejected bet is disabled and user cannot place it
        EXPECTED: *   'Go Betting' button is present and enabled ('Reuse Selections' button is absent)
        """
        pass

    def test_005_tap_go_betting(self):
        """
        DESCRIPTION: Tap 'Go Betting'
        EXPECTED: - No bets are available within Betslip
        EXPECTED: - 'You have no selections in the slip.' message is shown
        """
        pass

    def test_006_add_few_selections_to_the_betslipand_for_one_of_them_enter_stake_value_which_will_trigger_overask_for_the_selection(self):
        """
        DESCRIPTION: Add few selections to the Betslip and for one of them enter stake value which will trigger Overask for the selection
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps 3-4
        EXPECTED: *   Info message is displayed above 'Go Betting' button with text: 'One or more of your bets have been declined'
        EXPECTED: *   Rejected bet is disabled and user cannot place it
        EXPECTED: *   All other Bets are disabled
        """
        pass

    def test_008_tap_continue(self):
        """
        DESCRIPTION: Tap 'Continue'
        EXPECTED: *   No bets are available within Betslip
        EXPECTED: *   'You have no selections in the slip.' message is shown
        """
        pass
