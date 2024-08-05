import re
import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.helpers import normalize_name


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.user_journey_new_customer
@pytest.mark.user_journey_promo_1
@pytest.mark.user_journey_next_horse_race
@pytest.mark.user_journey_single_horse_race
@pytest.mark.quick_bet
@pytest.mark.bet_placement
@pytest.mark.event_details
@pytest.mark.mobile_only
@pytest.mark.critical
@pytest.mark.pipelines
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C883421_Verify_Bet_Receipt_within_Quick_Bet(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C883421
    VOL_ID: C9698084
    NAME: Verify Bet Receipt within Quick Bet
    DESCRIPTION: This test case verifies Bet Receipt within Quick Bet
    PRECONDITIONS: Quick Bet functionality should be enabled in CMS and user`s settings
    Quick Bet functionality is available for Mobile ONLY
    User is logged in and has positive balance
    """
    keep_browser_open = True
    event_params = None
    prices = {0: '3/16'}
    selection_name = None
    price = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Create test event, PROD: Find active horseracing event
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id)[0]
            self.__class__.eventID = event['event']['id']
            self.__class__.created_event_name = normalize_name(event['event']['name'])
            outcomes_resp = event['event']['children'][0]['market']['children']
            self.__class__.selection_name, price_resp = next(((i['outcome']['name'], i['outcome']['children'][0]['price'])
                                                              for i in outcomes_resp if
                                                              i['outcome'].get('children') and 'price' in i['outcome']['children'][0].keys()),
                                                             (outcomes_resp[0]['outcome']['name'], ''))
            self.__class__.price = f'{price_resp["priceNum"]}/{price_resp["priceDen"]}' if price_resp else 'SP'  # if price response is empty -> SP
            self.__class__.total_estimate_returns = '0.00' if price_resp else 'N/A'  # if price response is empty -> total est returns is N/A
            self._logger.info(f'*** Found Horse racing event "{self.created_event_name}" with id "{self.eventID}" '
                              f'and selection "{self.selection_name}" with price "{self.price}"')
        else:
            self.__class__.event_params = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=1,
                                                                             lp_prices=self.prices)
            self.__class__.eventID = self.event_params.event_id
            self.__class__.selection_name = list(self.event_params.selection_ids.keys())[0]
            self.__class__.created_event_name = '%s %s' % (self.event_params.event_off_time, self.horseracing_autotest_uk_name_pattern)
            self.__class__.price = list(self.prices.values())[0]

    def test_001_open_event(self):
        """
        DESCRIPTION: Open created event
        EXPECTED: EDP of event is opened
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')

    def test_002_log_in_to_oxygen(self):
        """
        DESCRIPTION: Log in to Oxygen application, get user balance
        """
        self.site.login(async_close_dialogs=False)
        self.__class__.user_balance = self.site.header.user_balance

    def test_003_tap_one_selection(self):
        """
        DESCRIPTION: Tap one <Sport>/<Race> selection
        EXPECTED: Quick Bet is displayed at the bottom of the page
        """
        current_market_tab = self.site.racing_event_details.tab_content.event_markets_list.current_market_tab_name
        if current_market_tab != vec.racing.RACING_EDP_MARKET_TABS.win_or_ew:
            market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
            if vec.racing.RACING_EDP_MARKET_TABS.win_or_ew in market_tabs.keys():
                market_tabs[vec.racing.RACING_EDP_MARKET_TABS.win_or_ew].click()
                self.site.wait_content_state_changed(timeout=5)

        self.add_selection_to_quick_bet(outcome_name=self.selection_name)

    def test_004_enter_value_in_stake_field(self):
        """
        DESCRIPTION: Enter value in 'Stake' field
        EXPECTED: 'Stake' field is populated with entered value
        """
        quick_bet_panel = self.site.quick_bet_panel
        quick_bet = quick_bet_panel.selection.content
        quick_bet.amount_form.input.value = self.bet_amount

        amount = float(quick_bet.amount_form.input.value)
        self.assertEqual(amount, self.bet_amount,
                         msg=f'Entered amount "{amount}" is not equal to expected "{self.bet_amount}"')

    def test_005_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'PLACE BET' button
        EXPECTED: Bet Receipt is displayed
        EXPECTED: Bet is placed successfully
        """
        self.site.quick_bet_panel.place_bet.click()
        bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
        self.__class__.bet_receipt = self.site.quick_bet_panel.bet_receipt
        expected_user_balance = self.user_balance - self.bet_amount
        self.verify_user_balance(expected_user_balance=expected_user_balance)
        self.__class__.user_balance = expected_user_balance

    def test_006_verify_bet_receipt(self):
        """
        DESCRIPTION: Verify Bet Receipt
        EXPECTED: Bet Receipt consists of:
        EXPECTED: - 'BET RECEIPT' header and 'X' button
        EXPECTED: - Selection name and handicap value (if available)
        EXPECTED: - Market name
        EXPECTED: - Event name
        EXPECTED: - 'Odds' label and value
        EXPECTED: - Bet receipt number
        EXPECTED: - 'Total Stake' label, corresponding currency, and value
        EXPECTED: - 'Total Est. Returns' label, corresponding currency, and value
        EXPECTED: - 'REUSE SELECTION' and 'DONE' buttons
        """
        quick_bet_panel_title = self.site.quick_bet_panel.header.title
        self.assertEquals(quick_bet_panel_title, tests.settings.betreceipt_title,
                          msg=f'Quick bet panel title: "{quick_bet_panel_title}" doesn\'t match with required "{tests.settings.betreceipt_title}"')
        self.assertTrue(self.site.quick_bet_panel.header.close_button.is_displayed(),
                        msg='"X" button not displayed on BET RECEIPT header')

        self.assertEqual(self.bet_receipt.name, self.selection_name,
                         msg=f'Actual Selection Name "{self.bet_receipt.name}" does not match expected "{self.selection_name}"')

        market_name = self.ob_config.horseracing_config.default_market_name.replace('|', '')
        self.assertEqual(self.bet_receipt.event_market, market_name,
                         msg=f'Actual Market Name "{self.bet_receipt.event_market}" does not match expected "{market_name}"')
        created_event_name_on_receipt = self.created_event_name.replace(',', '')  # w/a for BMA-54877
        self.assertEqual(self.bet_receipt.event_name, created_event_name_on_receipt,
                         msg=f'Actual Event Name "{self.bet_receipt.event_name}" does not match expected "{created_event_name_on_receipt}"')

        self.assertEqual(self.bet_receipt.odds, self.price,
                         msg=f'Actual odds "{self.bet_receipt.odds}" does not match expected "{self.price}"')

        self.assertTrue(self.bet_receipt.bet_id, msg='Bet Receipt number is not shown')

        actual_total_stake = f'£ {self.bet_receipt.total_stake}'
        amount = '{:.2f}'.format(float(self.bet_amount))
        expected_total_stake = f'£ {amount}'
        self.assertEqual(actual_total_stake, expected_total_stake,
                         msg=f'Actual total stake value: "{actual_total_stake}" doesn\'t match with expected: "{expected_total_stake}"')

        actual_estimate_returns = self.bet_receipt.estimate_returns
        self.verify_estimated_returns(est_returns=actual_estimate_returns,
                                      odds=[self.price],
                                      bet_amount=self.bet_amount)
        if self.price != 'SP':
            estimate_returns_currency = self.bet_receipt.estimate_returns_currency
            self.assertEqual('£', estimate_returns_currency,
                             msg=f'Actual estimate returns currency: "{estimate_returns_currency}" not match with requited "£"')

    def test_007_verify_bet_receipt_number(self):
        """
        DESCRIPTION: Verify Bet receipt number
        EXPECTED: The Bet receipt number starts with 'O' and contains only numeric values i.e. O/0123828/0000155
        """
        match = re.match(r'^O/\d+/\d+$', self.bet_receipt.bet_id)
        self.assertTrue(match, msg=f'Bet receipt number: "{self.bet_receipt.bet_id}" doesn\'t match with expected patten "O/0123828/0000155"')
