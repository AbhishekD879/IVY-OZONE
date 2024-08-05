import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.betslip
@pytest.mark.numeric_keyboard
@pytest.mark.mobile_only
@pytest.mark.slow
@pytest.mark.medium
@vtest
class Test_C29016_Stake_field_Validation(BaseBetSlipTest):
    """
    TR_ID: C29016
    VOL_ID: 12294284
    NAME: 'Stake' field Validation
    DESCRIPTION: This test case is for checking validation in a 'Stake' field
    DESCRIPTION: This test case is applied for **Mobile** and **Tablet** application.
    """
    keep_browser_open = True
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_safari_default

    selection_id = None

    def repeat_steps_7_9(self, stakes_to_verify, all_stakes=False):
        if all_stakes:
            section = self.get_betslip_sections().Singles
            stake = section.all_stakes_section
        else:
            stake_name, stake = list(stakes_to_verify.items())[0]
        stake.amount_form.input.click()
        self.clear_input_using_keyboard()
        self.test_007_tap_on_stake_field_and_enter_numeric_values(stakes_to_verify=stake)
        stake.amount_form.input.click()
        self.clear_input_using_keyboard()
        self.test_008_enter_value_under_1_in_decimal_format(stakes_to_verify=stake)
        stake.amount_form.input.click()
        self.clear_input_using_keyboard()
        self.test_009_enter_value_more_than_max_allowed_value_in_stake_field(stakes_to_verify=stake)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.event_name = f'{event_params.team1} v {event_params.team2}'
        self.__class__.event_id = event_params.event_id
        self.__class__.league1 = tests.settings.football_autotest_league
        selection_ids = self.ob_config.add_autotest_premier_league_football_event().selection_ids
        self.__class__.team, self.__class__.selection_id = list(selection_ids.items())[0]
        racing_event_params = self.ob_config.add_UK_racing_event(number_of_runners=3, forecast_available=True, tricast_available=True)
        self.__class__.selection_ids = racing_event_params.selection_ids
        self.__class__.eventID = racing_event_params.event_id

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_tap_sportraces_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Sport>/<Races> icon from the sports menu ribbon
        EXPECTED: <Sport>/<Races> landing page is opened
        """
        self.site.open_sport(name='FOOTBALL')

    def test_003_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the BetSlip
        EXPECTED: 1.  BetSlip counter is increased
        EXPECTED: 2.  Selected price button is highlighted in green
        """
        event = self.get_event_from_league(event_id=self.event_id,
                                           section_name=self.league1)
        output_prices = event.get_active_prices()
        self.assertTrue(output_prices,
                        msg=f'Could not find output prices for created event "{self.event_name}"')
        self.__class__.selection_name, selection_price = list(output_prices.items())[0]
        selection_price.click()
        self.site.wait_splash_to_hide()
        self.site.add_first_selection_from_quick_bet_to_betslip()
        self.assertTrue(selection_price.is_selected(),
                        msg=f'Bet button "{self.selection_name}" is not active after selection')

        self.verify_betslip_counter_change(expected_value=1)

    def test_004_go_to_the_betslip(self):
        """
        DESCRIPTION: Go to the BetSlip, 'Singles' section
        EXPECTED: Bet Slip is opened, selection is displayed
        EXPECTED: Numeric keyboard is NOT available
        """
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        self.__class__.stake_name, self.__class__.stake = list(singles_section.items())[0]
        self.assertTrue(singles_section, msg='No bets found')
        selections_count = self.get_betslip_content().selections_count
        self.assertEqual(int(selections_count), 1,
                         msg=f'BetSlip counter in section name {selections_count} and '
                         f'counter {1} doesn\'t match')
        self.assertFalse(self.get_betslip_content().keyboard.is_displayed(expected_result=False,
                                                                          name='Betslip keyboard shown',
                                                                          timeout=3),
                         msg='Betslip keyboard is not shown')

    def test_005_verify_default_value_in_stake_field(self):
        """
        DESCRIPTION: Verify default value in 'Stake' field
        EXPECTED: *Not Actual from OX 99* Stake field has currency sign pre-populated
        EXPECTED: *Actual from OX99* Stake field is empty
        """
        actual_value = self.stake.amount_form.input.value
        self.assertEqual(actual_value, "",
                         msg=f'Stake field is not empty actual value is "{actual_value}"')

    def test_006_tap_on_betslip_in_any_place_except_the_keypad(self):
        """
        DESCRIPTION: Tap on Betslip in any place except the keypad
        EXPECTED: Numeric keypad is closed (on devices)
        EXPECTED: *Not Actual from OX 99* Stake field has currency sign + Default value "0.00" pre-populated
        EXPECTED: *Actual from OX99* Stake field has default value "Stake" pre-populated
        """
        self.get_betslip_content().click()
        self.assertFalse(self.get_betslip_content().keyboard.is_displayed(expected_result=False,
                                                                          name='Betslip keyboard shown',
                                                                          timeout=3),
                         msg='Betslip keyboard is not shown')
        actual_value = self.stake.amount_form.input.placeholder
        self.assertEqual(actual_value, "Stake",
                         msg=f'Stake field is not empty actual value is "{actual_value}"')
        self.stake.amount_form.input.click()
        self.assertTrue(self.get_betslip_content().keyboard.is_displayed(name='Betslip keyboard shown', timeout=3),
                        msg='Betslip keyboard is not shown')

    def test_007_tap_on_stake_field_and_enter_numeric_values(self, stakes_to_verify=None):
        """
        DESCRIPTION: Tap on stake field and enter numeric values
        EXPECTED: 1.  Entered numbers are displayed in the 'Stake' field
        EXPECTED: 2.  'Estimated Returns' and 'Total Est. Returns' are changed according to the formula
        """
        stake = stakes_to_verify if stakes_to_verify else self.stake
        self.enter_value_using_keyboard(value=self.bet_amount)
        if not stakes_to_verify:
            self.verify_estimated_returns(est_returns=float(stake.est_returns),
                                          odds=[stake.odds],
                                          bet_amount=self.bet_amount)

    def test_008_enter_value_under_1_in_decimal_format(self, stakes_to_verify=None):
        """
        DESCRIPTION: Enter value under 1 in decimal format
        EXPECTED: 'Stake' field is automatically filled value in decimal format (e.g. '.2 = 0.2')
        """
        stake = stakes_to_verify if stakes_to_verify else self.stake
        self.clear_input_using_keyboard()
        self.enter_value_using_keyboard(value='.2')
        amount = stake.amount_form.input.value
        self.assertEqual(amount, '0.2', msg=f"Default value is not 0.2, actual is {amount}")

    def test_009_enter_value_more_than_max_allowed_value_in_stake_field(self, stakes_to_verify=None):
        """
        DESCRIPTION: Enter value more than max allowed  value in 'Stake' field.
        EXPECTED: 1. XXX,XXX,XXX,XXX.XX is the max value limitations for Stake field.
        EXPECTED: 2. It is impossible to enter more than 12 digits and 2 decimals in 'Stake' field.
        """
        stake = stakes_to_verify if stakes_to_verify else self.stake
        self.clear_input_using_keyboard()
        self.enter_value_using_keyboard(value='999999999999.999')
        amount = stake.amount_form.input.value
        self.assertEqual(amount, '999999999999.99',
                         msg=f"User is able to enter more than 12 digits and 2 decimals in 'Stake' field")

    def test_010_add_at_least_two_selections_from_different_events_to_the_bet_slip(self):
        """
        DESCRIPTION: Add at least two selections from different events to the Bet Slip
        EXPECTED: Selections are added
        """
        self.site.close_betslip()
        self.__class__.expected_betslip_counter_value += 1
        self.open_betslip_with_selections(selection_ids=self.selection_id)

    def test_011_repeat_steps_7_9_for_all_stakes_field_within_singles_section(self):
        """
        DESCRIPTION: Repeat steps #7-9 for 'All Stakes' field within 'Singles' section
        """
        if self.brand != 'ladbrokes':
            singles_section = self.get_betslip_sections().Singles
            self.repeat_steps_7_9(stakes_to_verify=singles_section, all_stakes=True)

    def test_012_go_to_bet_slip_multiples_section(self):
        """
        DESCRIPTION: Go to Bet Slip,'Multiples' section
        EXPECTED: *   'Multiples' and **Not actual from OX 99** 'Place your ACCA' (if available) section is shown
        EXPECTED: *   A list of available multiples bets is shown
        """
        self.__class__.multiples_section = self.get_betslip_sections(multiples=True).Multiples

    def test_013_repeat_steps_7_9(self):
        """
        DESCRIPTION: Repeat steps #7-9
        """
        stake = self.multiples_section['Double']
        stake_to_verify = {'Double': stake}
        self.repeat_steps_7_9(stakes_to_verify=stake_to_verify)

    def test_014_repeat_steps_7_9_for_forecast__tricast_bets(self):
        """
        DESCRIPTION: Repeat steps #7-9 for 'Forecast / Tricast' bets
        """
        self.get_betslip_content().remove_all_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_REMOVE_ALL)
        dialog.continue_button.click()
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        racing_event_tab_content = self.site.racing_event_details.tab_content.event_markets_list
        racing_event_tab_content.market_tabs_list.open_tab(vec.racing.RACING_EDP_TRICAST_MARKET_TAB)
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found for racing event tab')
        section_name, section = list(sections.items())[0]

        for index in range(0, 3):
            outcomes = list(section.items_as_ordered_dict.items())
            self.assertTrue(outcomes, msg=f'No one outcome was found in section: "{section_name}"')
            outcome_name, outcome = outcomes[index]
            runner_buttons = outcome.items_as_ordered_dict
            self.assertTrue(runner_buttons, msg=f'No runner buttons found for "{outcome_name}"')
            runner_bet_button = list(runner_buttons.values())[index]
            runner_bet_button.click()
        self.assertTrue(racing_event_tab_content.add_to_betslip_button.is_enabled(timeout=3),
                        msg=f'"{vec.quickbet.BUTTONS.add_to_betslip}" button is not clickable')
        racing_event_tab_content.add_to_betslip_button.click()
        self.site.open_betslip()
        sections = self.get_betslip_sections().Singles
        self.repeat_steps_7_9(stakes_to_verify=sections)
