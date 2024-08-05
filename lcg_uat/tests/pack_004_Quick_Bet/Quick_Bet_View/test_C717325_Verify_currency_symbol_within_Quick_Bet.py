import pytest
import tests
from time import sleep
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter, exists_filter
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.horseracing
@pytest.mark.racing
@pytest.mark.quick_bet
@pytest.mark.currency
@pytest.mark.reg157_fix
@pytest.mark.mobile_only
@pytest.mark.high
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C717325_Verify_currency_symbol_within_Quick_Bet(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C717325
    NAME: Verify currency symbol within Quick Bet
    DESCRIPTION: This test case verifies currency symbol within Quick Bet
    PRECONDITIONS: 1. Quick Bet functionality should be enabled in CMS
    PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 3. Make sure you have users with next currency:
    PRECONDITIONS: * 'GBP': symbol = **£**;
    PRECONDITIONS: * 'USD': symbol = **$**;
    PRECONDITIONS: * 'EUR': symbol = **€**;
    PRECONDITIONS: 4. Application is loaded
    """
    keep_browser_open = True
    selection_name = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        if tests.settings.backend_env == 'prod':
            additional_filter = exists_filter(LEVELS.EVENT, simple_filter(
                LEVELS.MARKET, ATTRIBUTES.PRICE_TYPE_CODES, OPERATORS.INTERSECTS, 'LP'))
            events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                         additional_filters=additional_filter,
                                                         all_available_events=True)
            event = None
            for event in events:
                market = next((market for market in event['event']['children']
                               if market['market']['templateMarketName'] == 'Win or Each Way'), None)
                if not market:
                    continue
                outcomes_resp = market['market']['children']
                for outcome in outcomes_resp:
                    for child in outcome.get('outcome', {}).get('children', []):
                        if child.get('price') and 'LP' in child.get('price', {}).get('priceType', ''):
                            self.__class__.selection_name = outcome['outcome']['name']
                            break
                    if self.selection_name:
                        break
                if self.selection_name:
                    break
            if not self.selection_name:
                raise SiteServeException('There are no selections with LP prices')

            self.__class__.eventID = event['event']['id']
            self._logger.debug(f'*** Found Horse racing event with id "{self.eventID}"')
        else:
            event = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices={0: '1/17'})
            self.__class__.eventID = event.event_id
            self.__class__.selection_name = list(event.selection_ids.keys())[0]

    def test_001_log_in_with_user_that_has_gbp_currency(self):
        """
        DESCRIPTION: Log in with user that has 'GBP' currency
        EXPECTED: User is logged in
        """
        username = tests.settings.betplacement_user
        self.site.login(username=username)

    def test_002_add_one_selection_to_quickbet(self):
        """
        DESCRIPTION: Add one selection to QuickBet
        EXPECTED: Quick Bet is displayed at the bottom of page
        """
        self.__class__.betslip_counter = int(self.site.header.bet_slip_counter.counter_value)
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab('WIN OR E/W')
        self.add_selection_to_quick_bet(outcome_name=self.selection_name)

    def test_003_verify_currency_set_within_quick_bet_section(self, currency='£'):
        """
        DESCRIPTION: Verify currency set within Quick Bet section
        EXPECTED: 'GBP' currency is displayed next to:
        EXPECTED: * 'Quick Stake' buttons
        EXPECTED: * 'Total Stake' and 'Estimated Returns' **CORAL** / 'Potential Returns' **Ladbrokes** labels
        """
        sleep(3)
        self.__class__.quick_bet = self.site.quick_bet_panel
        self.site.wait_splash_to_hide(3)
        quick_stakes_fe = self.quick_bet.selection.quick_stakes.items_as_ordered_dict
        quick_stakes_cms = self.cms_config.get_system_configuration_structure()['PredefinedStakes']['quickbet_stakes'].split(',')
        if len(quick_stakes_cms) != 4:
            quick_stakes_cms = self.cms_config.get_system_configuration_structure()['PredefinedStakes']['global_stakes'].split(',')
        for stake in quick_stakes_cms:
            expected_key = ('+' + currency + str(stake))
            self.assertIn(expected_key, quick_stakes_fe.keys(),
                          msg=f'"{expected_key}" not found in "{list(quick_stakes_fe.keys())}"')
        current_est_returns = self.quick_bet.selection.bet_summary.total_estimate_returns_currency
        self.assertEqual(current_est_returns, currency, msg=f'Actual Est Returns currency "{current_est_returns}" '
                                                            f'does not match expected "{currency}"')
        current_total_stake = self.quick_bet.selection.bet_summary.total_stake_currency
        self.assertEqual(current_total_stake, currency, msg=f'Actual Total Stake currency "{current_total_stake}" '
                                                            f'does not match expected "{currency}"')

    def test_004_enter_value_in_stake_field(self, currency='£'):
        """
        DESCRIPTION: Enter value in 'Stake' field
        EXPECTED: * No currency symbol within 'Stake' field
        EXPECTED: * "Stake" text is displayed within 'Stake' field
        """
        actual_value = self.quick_bet.selection.content.amount_form.input.placeholder
        self.assertEqual(actual_value, "Stake",
                         msg=f'text: "Stake" is not displayed within stake field')
        self.quick_bet.selection.content.amount_form.input.value = self.bet_amount
        quick_bet_value = self.quick_bet.selection.content.amount_form.input.value
        self.assertNotIn(currency, quick_bet_value,
                         msg=f'Currency symbol "{currency}" is shown in stake field of quick bet panel "{quick_bet_value}"')

    def test_005_close_quick_bet_section_via_x_button(self):
        """
        DESCRIPTION: Close Quick Bet section via 'X' button
        EXPECTED: Quick Bet section is not displayed
        EXPECTED: After release of BMA-54870 Expected result will be:
        EXPECTED: * Quick Bet is closed automatically
        EXPECTED: * Selection is added to Betslip
        EXPECTED: * Betslip counter is increased by 1
        EXPECTED: * Selection is the same as was added by Quick bet
        EXPECTED: * 'Stake' field contains added value from Quick bet
        """
        self.quick_bet.header.close_button.click()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is not closed')
        updated_betslip_counter = int(self.site.header.bet_slip_counter.counter_value)
        expected_betslip_counter = self.betslip_counter + 1
        self.assertEqual(updated_betslip_counter, expected_betslip_counter,
                         msg=f'Updated betslip counter value "{updated_betslip_counter}" '
                             f'is not same as Expected betslip counter value "{expected_betslip_counter}"')
        self.site.header.bet_slip_counter.click()
        sections = self.get_betslip_sections().Singles
        self.assertTrue(sections, msg=f'"{sections}" is not added to the betslip')
        self.assertIn(self.selection_name, sections,
                      msg=f'Added selection "{self.selection_name}" is not present in Betslip sections "{sections}"')
        stake = list(sections.values())[0]
        stake_value = stake.amount_form.input.value
        self.assertEqual(float(stake_value), float(self.bet_amount),
                         msg='Current stake value: "%s" does not match with expected: "%s"'
                             % (float(stake_value), float(self.bet_amount)))

    def test_006_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: User is logged out
        """
        self.clear_betslip()
        self.site.logout(timeout=5)

    def test_007_log_in_with_user_that_has_usd_currency_and_repeat_steps_2_6(self):
        """
        DESCRIPTION: Log in with user that has 'USD' currency and repeat steps #2-6
        EXPECTED:
        """
        username = tests.settings.user_with_usd_currency_and_card
        self.site.login(username=username)
        self.test_002_add_one_selection_to_quickbet()
        self.test_003_verify_currency_set_within_quick_bet_section(currency='$')
        self.test_004_enter_value_in_stake_field(currency='$')
        self.test_005_close_quick_bet_section_via_x_button()
        self.test_006_log_out()

    def test_008_log_in_with_user_that_has_eur_currency_and_repeat_steps_2_6(self):
        """
        DESCRIPTION: Log in with user that has 'EUR' currency and repeat steps #2-6
        EXPECTED:
        """
        username = tests.settings.user_with_euro_currency_and_card
        self.site.login(username=username)
        self.test_002_add_one_selection_to_quickbet()
        self.test_003_verify_currency_set_within_quick_bet_section(currency='€')
        self.test_004_enter_value_in_stake_field(currency='€')
        self.test_005_close_quick_bet_section_via_x_button()
        self.test_006_log_out()
