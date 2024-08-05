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
class Test_C11547283_Verify_Place_Bet_button_when_all_selections_are_displayed_on_one_page_actual_from_Release_OX_99(Common):
    """
    TR_ID: C11547283
    NAME: Verify Place Bet button when all selections are displayed on one page [actual from Release OX 99]
    DESCRIPTION: This test case verifies displaying of Place Bet button when all selections are displayed on one page.
    PRECONDITIONS: 1. User isn't logged in
    PRECONDITIONS: 2. Load Oxygen App
    """
    keep_browser_open = True

    def test_001__mobile__add_one_or_few_selections_to_betslip_so_that_all_selections_can_be_displayed_on_one_page_desktop__add_one_selection_to_betslip(self):
        """
        DESCRIPTION: _Mobile:_ Add one or few selections to Betslip, so that all selections can be displayed on one page.
        DESCRIPTION: _Desktop:_ Add one selection to Betslip
        EXPECTED: 
        """
        pass

    def test_002_open_betslip_and_verify_view_of_place_bet_button(self):
        """
        DESCRIPTION: Open Betslip and verify view of Place Bet button.
        EXPECTED: Place Bet button is disabled.
        EXPECTED: _Coral:_ Place Bet button is stuck to the bottom of the page. Text on button is "LOGIN & PLACE BET"
        EXPECTED: _Ladbrokes:_ Place Bet button is displayed under the last selection in the Betslip. Text on button is "LOGIN AND PLACE BET"
        EXPECTED: _Desktop:_ Place Bet button is displayed under the selection. Text on button corresponds to text for Mobile
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

    def test_007__mobile__add_one_or_few_selections_to_betslip_so_that_all_selections_can_be_displayed_on_one_page_desktop__add_one_selection_to_betslip(self):
        """
        DESCRIPTION: _Mobile:_ Add one or few selections to Betslip, so that all selections can be displayed on one page.
        DESCRIPTION: _Desktop:_ Add one selection to Betslip
        EXPECTED: 
        """
        pass

    def test_008_open_betslip_and_verify_view_of_place_bet_button(self):
        """
        DESCRIPTION: Open Betslip and verify view of Place Bet button.
        EXPECTED: Place Bet button is disabled.
        EXPECTED: _Coral:_ Place Bet button is stuck to the bottom of the page. Text on button is "PLACE BET"
        EXPECTED: _Ladbrokes:_ Place Bet button is displayed under the last selection in the Betslip. Text on button is "PLACE BET"
        EXPECTED: _Desktop:_ Place Bet button is displayed under the selection. Text on button corresponds to text for Mobile
        """
        pass

    def test_009__mobile__open_keyboard(self):
        """
        DESCRIPTION: _Mobile:_ Open keyboard.
        EXPECTED: Place Bet button is placed under keyboard area.
        EXPECTED: _Coral:_ Text on button is "PLACE BET"
        EXPECTED: _Ladbrokes:_ Text on button is "PLACE BET"
        """
        pass

    def test_010_enter_stake_value_for_any_bet(self):
        """
        DESCRIPTION: Enter Stake value for any bet.
        EXPECTED: Place Bet button becomes enabled.
        EXPECTED: _Coral:_ Text on button is "PLACE BET"
        EXPECTED: _Ladbrokes:_ Text on button is "PLACE BET"
        """
        pass

    def test_011_clear_stake_entered_in_step_4(self):
        """
        DESCRIPTION: Clear Stake entered in Step 4.
        EXPECTED: Place Bet button is disabled.
        """
        pass
