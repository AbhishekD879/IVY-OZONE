import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.quick_bet
@pytest.mark.numeric_keyboard
@pytest.mark.mobile_only
@pytest.mark.critical
@vtest
class Test_C862081_C892300_Verify_entering_Stake_value(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C862081
    TR_ID: C892300
    VOL_ID: C9697760
    NAME: Verify entering Stake value
    DESCRIPTION: This test case verifies entering stake value in a 'Stake' field using numeric keyboard for Quick Bet
    PRECONDITIONS: Oxygen application is loaded
    """
    keep_browser_open = True
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_safari_default
    quick_bet = None
    number = '2.25'
    new_number = '86.86'
    number_under_1 = '.14'
    long_number = '148612345678.0987'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        DESCRIPTION: Open created event
        """
        if tests.settings.backend_env == 'prod':
            template_market_name = 'Match Betting'
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                        expected_template_market=template_market_name,
                                                        all_available_events=True)[0]
            event_id = event['event']['id']
            market_name = next(
                (normalize_name(market.get('market', {}).get('name', '')) for market in event['event']['children']
                 if market.get('market').get('templateMarketName') == template_market_name),
                None)
            outcomes = next(((market['market']['children']) for market in event['event']['children']
                            if market.get('market').get('templateMarketName') == template_market_name and market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.selection_name, _id = list(selection_ids.items())[0]
            self._logger.info(f'*** Found Football event "{event["event"]["name"]}" with id "{event_id}"')
        else:
            event = self.ob_config.add_football_event_to_italy_serie_a()
            event_id = event.event_id
            self.__class__.selection_name = event.team1
            market_name = self.ob_config.football_config.italy_serie_a.serie_a.market_name.replace('|', '')
        self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)

        self.navigate_to_edp(event_id=event_id)

    def test_001_select_one_sport_selection(self):
        """
        DESCRIPTION: Select one <Sport>/<Races> selection
        EXPECTED: Quick Bet is opened
        EXPECTED: Added selection is displayed
        EXPECTED: Numeric keyboard is collapsed by default
        """
        self.add_selection_from_event_details_to_quick_bet(selection_name=self.selection_name,
                                                           market_name=self.expected_market_name)

        self.__class__.quick_bet = self.site.quick_bet_panel.selection
        self.assertFalse(self.quick_bet.keyboard.is_displayed(name='Betslip keyboard shown',
                                                              timeout=3, expected_result=False),
                         msg='Keyboard is not collapsed by default')

    def test_002_tap_on_stake_field(self):
        """
        DESCRIPTION: Tap on 'Stake' field
        EXPECTED: Stake field is focused
        EXPECTED: Numeric keyboard is opened
        EXPECTED: 'ADD TO BETSLIP' button is enabled
        EXPECTED: 'PLACE BET' button is disabled
        """
        self.quick_bet.content.amount_form.input.click()
        self.assertTrue(self.quick_bet.content.amount_form.is_active(), msg='"Stake" box is not highlighted')
        self.assertTrue(self.quick_bet.keyboard.is_displayed(name='Betslip keyboard shown', timeout=10),
                        msg='Numeric keyboard is not opened')
        self.assertTrue(self.site.quick_bet_panel.add_to_betslip_button.is_enabled(),
                        msg='ADD TO BETSLIP buttons is not enabled')
        self.assertFalse(self.site.quick_bet_panel.place_bet.is_enabled(expected_result=False),
                         msg='PLACE BET button is not disabled')

    def test_003_in_stake_field_enter_numeric_values(self):
        """
        DESCRIPTION: In stake field enter numeric values
        EXPECTED: Entered numbers are displayed in the 'Stake' field
        EXPECTED: 'Estimated Returns' and 'Total Est. Returns' are changed according to the formula
        EXPECTED: 'ADD TO BETSLIP' buttons is enabled
        EXPECTED: 'PLACE BET' button becomes enabled
        """
        self.enter_value_using_keyboard(value=self.number, on_betslip=False)
        result = wait_for_result(lambda: self.quick_bet.content.amount_form.input.value == self.number,
                                 name=f'Amount to change to "{self.number}"',
                                 timeout=5)
        self.assertTrue(result, msg=f'Entered amount "{self.quick_bet.content.amount_form.input.value}" is '
                                    f'not equal to expected "{self.number}"')
        est_returns = self.quick_bet.bet_summary.total_estimate_returns
        odds = self.site.quick_bet_panel.selection.content.odds_value
        self.verify_estimated_returns(est_returns=est_returns,
                                      bet_amount=self.number,
                                      odds=[odds])

        self.assertTrue(self.site.quick_bet_panel.add_to_betslip_button.is_enabled(),
                        msg='ADD TO BETSLIP buttons is not enabled')
        self.assertTrue(self.site.quick_bet_panel.place_bet.is_enabled(), msg='PLACE BET button is not enabled')

    def test_004_tap_remove_button_on_numeric_keyboard(self):
        """
        DESCRIPTION: Tap 'Remove' button on numeric keyboard
        EXPECTED: Last entered symbol is deleted from 'Stake' field
        EXPECTED: '.' button on keyboard is greyed out (disabled) after removing the last digit of value (e.g. XX.X*X*)
        EXPECTED: '.' button on keyboard becomes enabled once ".X" value is removed  (e.g. XX*.X*)
        """
        self.enter_value_using_keyboard(value='delete', on_betslip=False)
        new_number = self.number[:-1]
        amount = self.quick_bet.content.amount_form.input.value
        self.assertEqual(amount, new_number, msg=f'Entered amount "{amount}" is not equal to entered "{new_number}"')

        keys = self.quick_bet.keyboard.keys
        self.assertFalse(keys['.'].is_enabled(timeout=2, expected_result=False),
                         msg='"." button on keyboard is not disabled')
        self.enter_value_using_keyboard(value='delete', on_betslip=False)
        self.assertTrue(keys['.'].is_enabled(timeout=10), msg='"." button on keyboard is not active')

    def test_005_enter_value_more_than_max_allowed_value_in_stake_field(self):
        """
        DESCRIPTION: Enter value more than max allowed  value in 'Stake' field
        EXPECTED: XXX,XXX,XXX,XXX.XX is the max value limitations for Stake field.
        EXPECTED: It is impossible to enter more than 12 digits and 2 decimals in 'Stake' field.
        """
        self.clear_input_using_keyboard(on_betslip=False)
        self.enter_value_using_keyboard(value=self.long_number, on_betslip=False)
        amount_number = self.long_number[:self.max_number_of_symbols_in_stake_input]
        amount = self.quick_bet.content.amount_form.input.value
        self.assertEqual(amount, amount_number,
                         msg=f'Entered amount "{amount}" is not equal to expected "{amount_number}"')

    def test_006_tap_return_button_on_numeric_keyboard(self):
        """
        DESCRIPTION: Tap 'Return' button on numeric keyboard
        EXPECTED: Stake field is NOT focused
        EXPECTED: '<currency symbol> stake value' is shown within box
        EXPECTED: Numeric keyboard is NOT shown
        """
        self.enter_value_using_keyboard(value='enter', on_betslip=False)
        self.assertFalse(self.quick_bet.content.amount_form.is_active(), msg='"Stake" box is highlighted')
        self.assertFalse(self.quick_bet.keyboard.is_displayed(name='Betslip keyboard shown', timeout=3),
                         msg='Numeric keyboard is not hidden')

    def test_007_set_cursor_over_stake_field_again(self):
        """
        DESCRIPTION: Set cursor over 'Stake' field again
        EXPECTED: 'Stake' field is focused
        EXPECTED: Numeric keyboard is shown
        EXPECTED: When user enters new value > new value is shown instead of an old one
        """
        self.quick_bet.content.amount_form.input.click()
        self.assertTrue(self.quick_bet.content.amount_form.is_active(), msg='"Stake" box is not highlighted')
        self.assertTrue(self.quick_bet.keyboard.is_displayed(name='Betslip keyboard shown', timeout=10),
                        msg='Numeric keyboard is not opened')
        self.enter_value_using_keyboard(value=self.new_number, on_betslip=False)
        amount = self.quick_bet.content.amount_form.input.value
        self.assertEqual(amount, self.new_number,
                         msg=f'Entered amount "{amount}" is not equal to expected "{self.new_number}"')

    def test_008_enter_value_under_1_in_decimal_format(self):
        """
        DESCRIPTION: Enter value under 1 in decimal format
        EXPECTED: 'Stake' field is automatically filled value in decimal format (e.g. '.2 = 0.2')
        EXPECTED: '.' button becomes greyed out (disabled) on keyboard
        """
        self.clear_input_using_keyboard(on_betslip=False)
        self.enter_value_using_keyboard(value=self.number_under_1, on_betslip=False)
        amount = float(self.quick_bet.content.amount_form.input.value)
        self.assertEqual(amount, float(self.number_under_1),
                         msg=f'Entered amount "{amount}" is not equal to expected "{self.number_under_1}"')
