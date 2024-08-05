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
class Test_C15229214_Verify_Place_Bet_button_when_there_are_too_many_selections_to_display_on_one_page_actual_from_Release_OX_99(Common):
    """
    TR_ID: C15229214
    NAME: Verify Place Bet button when there are too many selections to display on one page [actual from Release OX 99]
    DESCRIPTION: This test case verifies displaying of Place Bet button when there are too many selections to display on one page.
    PRECONDITIONS: User isn't logged in
    PRECONDITIONS: Load Oxygen App
    """
    keep_browser_open = True

    def test_001__mobile__add_few_selections_to_betslip_so_that_there_are_too_many_selections_to_be_displayed_on_one_page_desktop__add_few_selections_to_betslip(self):
        """
        DESCRIPTION: _Mobile:_ Add few selections to Betslip, so that there are too many selections to be displayed on one page.
        DESCRIPTION: _Desktop:_ Add few selections to Betslip
        EXPECTED: 
        """
        pass

    def test_002_open_betslip_and_verify_view_of_place_bet_button(self):
        """
        DESCRIPTION: Open Betslip and verify view of Place Bet button.
        EXPECTED: Place Bet button is disabled.
        EXPECTED: _Coral:_
        EXPECTED: * _Mobile_: Place bet button is displayed at the bottom of the page.
        EXPECTED: _Desktop_: Place bet button is displayed under Bet Slip section.
        EXPECTED: * All the selections can be scrolled above the Place bet button area.
        EXPECTED: * Text on button is "LOGIN & PLACE BET"
        EXPECTED: _Ladbrokes:_
        EXPECTED: * Place bet button is displayed under the last selection in the Betslip.
        EXPECTED: * Text on button is "LOGIN AND PLACE BET"
        """
        pass

    def test_003__mobile__open_keyboard(self):
        """
        DESCRIPTION: _Mobile:_ Open keyboard.
        EXPECTED: Place Bet button is placed under keyboard area.
        EXPECTED: _Coral:_ Text on button is "LOGIN & PLACE BET"
        EXPECTED: _Ladbrokes:_ Text on button is "LOGIN AND PLACE BET"
        """
        pass

    def test_004_enter_stake_value_for_any_bet(self):
        """
        DESCRIPTION: Enter Stake value for any bet.
        EXPECTED: Place Bet button becomes enabled.
        EXPECTED: _Coral:_ Text on button is "LOGIN & PLACE BET"
        EXPECTED: _Ladbrokes:_ Text on button is "LOGIN AND PLACE BET"
        """
        pass

    def test_005_clear_stake_entered_in_step_4(self):
        """
        DESCRIPTION: Clear Stake entered in Step 4.
        EXPECTED: Place Bet button is disabled.
        """
        pass

    def test_006_log_in_to_app(self):
        """
        DESCRIPTION: Log in to App
        EXPECTED: 
        """
        pass

    def test_007_open_betslip_and_verify_view_of_place_bet_button(self):
        """
        DESCRIPTION: Open Betslip and verify view of Place Bet button.
        EXPECTED: Place Bet button is disabled.
        EXPECTED: _Coral:_
        EXPECTED: * _Mobile:_ Place bet button is displayed at the bottom of the page.
        EXPECTED: _Desktop:_ Place bet button is displayed under Bet Slip section.
        EXPECTED: * All the selections can be scrolled above the Place bet button area.
        EXPECTED: * Text on button is "PLACE BET"
        EXPECTED: _Ladbrokes:_
        EXPECTED: * Place bet button is displayed under the last selection in the Betslip.
        EXPECTED: * Text on button is "PLACE BET"
        """
        pass

    def test_008__mobile__open_keyboard(self):
        """
        DESCRIPTION: _Mobile:_ Open keyboard.
        EXPECTED: Place Bet button is placed under keyboard area.
        EXPECTED: _Coral:_ Text on button is "PLACE BET"
        EXPECTED: _Ladbrokes:_ Text on button is "PLACE BET"
        """
        pass

    def test_009_enter_stake_value_for_any_bet(self):
        """
        DESCRIPTION: Enter Stake value for any bet.
        EXPECTED: Place Bet button becomes enabled.
        EXPECTED: _Coral:_ Text on button is "PLACE BET"
        EXPECTED: _Ladbrokes:_ Text on button is "PLACE BET"
        """
        pass
