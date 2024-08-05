import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C29148_Maximum_Stake_functionality_when_Overask_is_disabled_for_User(Common):
    """
    TR_ID: C29148
    NAME: Maximum Stake functionality when Overask is disabled for User
    DESCRIPTION: This test case verifies Maximum Stake functionality when Overask is disabled for User
    DESCRIPTION: JIRA Tickets:
    DESCRIPTION: BMA-9296 Overask - Display Max Bet message if Overask is disabled for the Customer
    DESCRIPTION: BMA-21529 New betslip - Max bet alert
    PRECONDITIONS: To enable/disable Overask for the Customer/Event type please follow this path:
    PRECONDITIONS: Backoffice Tool -> Trader Interface -> Customer -> (Search by Username) -> Click on the Account name -> Account Rules -> Select No Intercept value in the Control column  -> click Update
    """
    keep_browser_open = True

    def test_001_login_to_oxygen_application_and_add_selection_to_betslip(self):
        """
        DESCRIPTION: Login to Oxygen application and add selection to betslip
        EXPECTED: 
        """
        pass

    def test_002_enter_stake_value_which_is_higher_then_maximum_allowed_stake_for_this_bet(self):
        """
        DESCRIPTION: Enter Stake value which is higher then maximum allowed Stake for this bet
        EXPECTED: 
        """
        pass

    def test_003_tapclick_on_bet_now_button(self):
        """
        DESCRIPTION: Tap/Click on 'Bet now' button
        EXPECTED: *   Bet is NOT placed
        EXPECTED: *   'Maximum stake of <currency><amount>' error message is displayed above stake section
        EXPECTED: *   Place Bet button is active
        """
        pass

    def test_004_add_multiple_bets_to_betslip(self):
        """
        DESCRIPTION: Add multiple bets to Betslip
        EXPECTED: 
        """
        pass

    def test_005_repeat_steps_2_3(self):
        """
        DESCRIPTION: Repeat steps 2-3
        EXPECTED: *   Bet is NOT placed
        EXPECTED: *   'Maximum stake of <currency><amount>' error message is displayed above stake section
        EXPECTED: *   Place Bet button is active
        """
        pass

    def test_006_add_forecaststricasts_to_betslip(self):
        """
        DESCRIPTION: Add Forecasts/Tricasts to Betslip
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_2_3(self):
        """
        DESCRIPTION: Repeat steps 2-3
        EXPECTED: *   Bet is NOT placed
        EXPECTED: *   'Maximum stake of <currency><amount>' error message is displayed above stake section
        EXPECTED: *   Place Bet button is active
        """
        pass
