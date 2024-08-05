import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C15229214_Verify_Place_Bet_button_when_there_are_too_many_selections_to_display_on_one_page_actual_from_Release_OX_99(BaseBetSlipTest):
    """
    TR_ID: C15229214
    NAME: Verify Place Bet button when there are too many selections to display on one page [actual from Release OX 99]
    DESCRIPTION: This test case verifies displaying of Place Bet button when there are too many selections to display on one page.
    PRECONDITIONS: User isn't logged in
    PRECONDITIONS: Load Oxygen App
    """
    keep_browser_open = True
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_safari_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find two selections to be added into betslip
        """
        self.__class__.is_mobile = True if self.device_type == 'mobile' else False
        if tests.settings.backend_env == 'prod':
            selection_ids = self.get_active_event_selections_for_category(category_id=self.ob_config.football_config.category_id)
            self.__class__.selection_id = list(selection_ids.values())[0]
        else:
            event_params1 = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.selection_id = list(event_params1.selection_ids.values())[0]
        self._logger.info(f'*** Using selections "{self.selection_id}"')

    def test_001__mobile__add_few_selections_to_betslip_so_that_there_are_too_many_selections_to_be_displayed_on_one_page_desktop__add_few_selections_to_betslip(self):
        """
        DESCRIPTION: _Mobile:_ Add few selections to Betslip, so that there are too many selections to be displayed on one page.
        DESCRIPTION: _Desktop:_ Add few selections to Betslip
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)

    def test_002_open_betslip_and_verify_view_of_place_bet_button(self, bet_button_name=vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION):
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
        betnow_btn = self.get_betslip_content().bet_now_button
        self.assertFalse(betnow_btn.is_enabled(expected_result=False), msg='Bet Now button is not disabled')
        if isinstance(bet_button_name, (list, tuple)):
            self.assertTrue(any(True for i in bet_button_name if betnow_btn.name == i),
                            msg=f'Button text "{betnow_btn.name}" does not match any of expected "{bet_button_name}"')
        else:
            self.assertEqual(betnow_btn.name, bet_button_name,
                             msg=f'Button text "{betnow_btn.name}" does not match expected "{bet_button_name}"')

    def test_003__mobile__open_keyboard(self, bet_button_name=vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION):
        """
        DESCRIPTION: _Mobile:_ Open keyboard.
        EXPECTED: Place Bet button is placed under keyboard area.
        EXPECTED: _Coral:_ Text on button is "LOGIN & PLACE BET"
        EXPECTED: _Ladbrokes:_ Text on button is "LOGIN AND PLACE BET"
        """
        singles_section = self.get_betslip_sections().Singles
        self.__class__.stake_name, self.__class__.stake = list(singles_section.items())[0]
        if self.is_mobile:
            self.stake.amount_form.input.click()
            self.assertTrue(
                self.get_betslip_content().keyboard.is_displayed(name='Betslip keyboard shown', timeout=3),
                msg='Betslip keyboard is not shown')
            betnow_btn = self.get_betslip_content().bet_now_button
            self.assertTrue(betnow_btn.is_displayed(), msg='Bet Now button is not disabled')
            if isinstance(bet_button_name, (list, tuple)):
                self.assertTrue(any(True for i in bet_button_name if betnow_btn.name == i),
                                msg=f'Button text "{betnow_btn.name}" does not match any of expected "{bet_button_name}"')
            else:
                self.assertEqual(betnow_btn.name, bet_button_name,
                                 msg=f'Button text "{betnow_btn.name}" does not match expected "{bet_button_name}"')

    def test_004_enter_stake_value_for_any_bet(self, bet_button_name=vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION):
        """
        DESCRIPTION: Enter Stake value for any bet.
        EXPECTED: Place Bet button becomes enabled.
        EXPECTED: _Coral:_ Text on button is "LOGIN & PLACE BET"
        EXPECTED: _Ladbrokes:_ Text on button is "LOGIN AND PLACE BET"
        """
        self.enter_stake_amount(stake=(self.stake_name, self.stake))
        betnow_btn = self.get_betslip_content().bet_now_button
        self.assertTrue(betnow_btn.is_enabled(timeout=2), msg='Bet Now button is not enabled')
        if isinstance(bet_button_name, (list, tuple)):
            self.assertTrue(any(True for i in bet_button_name if betnow_btn.name == i),
                            msg=f'Button text "{betnow_btn.name}" does not match any of expected "{bet_button_name}"')
        else:
            self.assertEqual(betnow_btn.name, bet_button_name,
                             msg=f'Button text "{betnow_btn.name}" does not match expected "{bet_button_name}"')

    def test_005_clear_stake_entered_in_step_4(self):
        """
        DESCRIPTION: Clear Stake entered in Step 4.
        EXPECTED: Place Bet button is disabled.
        """
        if self.is_mobile:
            self.clear_input_using_keyboard()
        else:
            self.stake.amount_form.input.clear()
        betnow_btn = self.get_betslip_content().bet_now_button
        self.assertFalse(betnow_btn.is_enabled(expected_result=False), msg='Bet Now button is not disabled')
        self.site.close_betslip()
        self.site.wait_content_state('Homepage')

    def test_006_log_in_to_app(self):
        """
        DESCRIPTION: Log in to App
        """
        self.site.login()

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
        self.site.open_betslip()
        self.site.close_all_dialogs()
        self.test_002_open_betslip_and_verify_view_of_place_bet_button(bet_button_name=(vec.betslip.BET_NOW, vec.betslip.ACCEPT_BET))

    def test_008__mobile__open_keyboard(self):
        """
        DESCRIPTION: _Mobile:_ Open keyboard.
        EXPECTED: Place Bet button is placed under keyboard area.
        EXPECTED: _Coral:_ Text on button is "PLACE BET"
        EXPECTED: _Ladbrokes:_ Text on button is "PLACE BET"
        """
        self.test_003__mobile__open_keyboard(bet_button_name=(vec.betslip.BET_NOW, vec.betslip.ACCEPT_BET))

    def test_009_enter_stake_value_for_any_bet(self):
        """
        DESCRIPTION: Enter Stake value for any bet.
        EXPECTED: Place Bet button becomes enabled.
        EXPECTED: _Coral:_ Text on button is "PLACE BET"
        EXPECTED: _Ladbrokes:_ Text on button is "PLACE BET"
        """
        singles_section = self.get_betslip_sections().Singles
        self.__class__.stake_name, self.__class__.stake = list(singles_section.items())[0]
        self.test_004_enter_stake_value_for_any_bet(bet_button_name=(vec.betslip.BET_NOW, vec.betslip.ACCEPT_BET))
