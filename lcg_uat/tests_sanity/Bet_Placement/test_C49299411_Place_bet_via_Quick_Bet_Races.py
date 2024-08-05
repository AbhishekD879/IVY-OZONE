from time import sleep
import pytest
import tests
import voltron.environments.constants as vec
from collections import OrderedDict
from crlat_ob_client.utils.date_time import validate_time
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.mobile_only
@pytest.mark.bet_placement
@pytest.mark.my_bets
@pytest.mark.quick_bet
@pytest.mark.login
@pytest.mark.races
@pytest.mark.safari
@pytest.mark.numeric_keyboard
@pytest.mark.sanity
@vtest
class Test_C49299411_Place_bet_via_Quick_Bet_Races(BaseBetSlipTest, BaseRacing, BaseSportTest):
    """
    TR_ID: C49299411
    VOL_ID: C49504610
    NAME: Place bet via Quick Bet (Races)
    DESCRIPTION: This test case verifies placing bet by using Quick Bet for races (Horse racing, Greyhounds - SP/LP prices)
    DESCRIPTION: NOTE! Quick Bet is NOT present for Desktop
    PRECONDITIONS: 1. Quick Bet functionality is enabled in CMS and user`s settings
    PRECONDITIONS: 2. Load the app
    PRECONDITIONS: 3. Log in with a user that has a positive balance
    PRECONDITIONS: 4. Navigate to any racing landing page (for example, Horse racing or Greyhounds)
    """
    keep_browser_open = True
    device_name = 'Pixel 2 XL' if not tests.use_browser_stack else tests.default_pixel

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Create test event, PROD: Find active events
        DESCRIPTION: Log in with a user that has a positive balance
        """
        if tests.settings.backend_env == 'prod':
            additional_filter = exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.PRICE_TYPE_CODES,
                                                                          OPERATORS.INTERSECTS, 'LP'))
            events = self.get_active_events_for_category(
                category_id=self.ob_config.horseracing_config.category_id, additional_filters=additional_filter, all_available_events=True)

            event = None
            for potential_event in events:
                for market in potential_event['event']['children']:
                    if market['market'].get('children') and market.get('market').get('templateMarketName') == 'Win or Each Way':
                        outcomes_resp = market['market']['children']
                        for outcome in outcomes_resp:
                            if outcome['outcome'].get('children'):
                                for child in outcome['outcome']['children']:
                                    if child.get('price'):
                                        if 'SP' not in child.get('price').get('priceType'):
                                            event = potential_event
                                break
                        break
                break

            if not event:
                raise SiteServeException('There are no Event where selections is with LP prices only')

            self.__class__.event_id = event['event']['id']
            self.__class__.event_name = normalize_name(event['event']['name'])
            self.__class__.league = self.get_accordion_name_for_event_from_ss(event=event)
            self.__class__.market_name = event['event']['children'][0]['market']['name']
            for market in event['event']['children']:
                if market['market']['name'] == 'Win or Each Way' and market['market'].get('children'):
                    outcomes = market['market']['children']
                    self.__class__.each_way_coef = \
                        int(market['market']['eachWayFactorNum']) / int(market['market']['eachWayFactorDen'])

            selection_ids_all = [(i['outcome']['name'], i['outcome']['id']) for i in outcomes
                                 if 'Unnamed' not in i['outcome']['name']]
            selection_ids = OrderedDict(selection_ids_all)
        else:
            prices = {0: '1/2', 1: '2/3'}
            event = self.ob_config.add_UK_racing_event(
                ew_terms=self.ew_terms, number_of_runners=2, time_to_start=1, lp_prices=prices)
            self.__class__.event_name = f'{event.event_off_time} {self.horseracing_autotest_uk_name_pattern}'
            self.__class__.event_id = event.event_id
            self.__class__.league = tests.settings.football_autotest_league
            self.__class__.market_name = \
                self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.market_name.replace('|', '')
            selection_ids = event.selection_ids
            self.__class__.each_way_coef = 0.0625  # 1/16 from self.ew_terms
        self.__class__.selection_name = list(selection_ids.keys())[0]
        self._logger.info(f'*** Found Racing event with name: "{self.event_name}" and id: "{self.event_id}"')
        self.site.login(username=tests.settings.betplacement_user)
        self.__class__.user_balance = self.site.header.user_balance

    def test_001_add_any_race_lpsp_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add any <Race> LP/SP selection to Quick Bet
        EXPECTED: Quick Bet is displayed at the bottom of the page:
        EXPECTED: * Quick Bet header and 'X' button
        EXPECTED: * Selection name, Market name and Event name
        EXPECTED: * 'Use Freebet' under event details (if available)
        EXPECTED: * Quick Stakes (For example, "+£5", "+£10" "+£50", "+£100")
        EXPECTED: * Price odds 'SP' or 'LP' and Stake box
        EXPECTED: * The button 'Add to betslip' is active and 'Place bet' is disabled
        EXPECTED: * E/W box
        EXPECTED: * 'Boost' button (if available, for LP)
        EXPECTED: * 'Total Stake', 'Estimated Returns' - Coral, 'Total Stake', 'Potential Returns' - Ladbrokes
        EXPECTED: Please note that some prices can be switched between SP/LP (it depends on set up in backoffice)
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.win_or_ew)
        self.add_selection_to_quick_bet(outcome_name=self.selection_name)
        quick_bet = self.site.quick_bet_panel
        self.assertEqual(quick_bet.header.title, vec.quickbet.QUICKBET_TITLE,
                         msg=f'Actual title "{quick_bet.header.title}" does not match expected "{vec.quickbet.QUICKBET_TITLE}"')
        self.assertTrue(quick_bet.header.close_button.is_displayed(), msg='Quick Bet close button is not shown')
        self.assertEqual(quick_bet.selection.content.event_name.replace(' - ', ' ').replace(' v ', ' '),
                         self.event_name.replace(' - ', ' '),
                         msg=f'Actual Event Name "{quick_bet.selection.content.event_name.replace(" - ", " ").replace(" v ", " ")}" does not '
                             f'match expected "{self.event_name.replace(" - ", " ")}"')
        self.assertEqual(quick_bet.selection.content.market_name, self.market_name,
                         msg=f'Actual Market Name "{quick_bet.selection.content.market_name}" does not '
                             f'match expected "{self.market_name}"')
        self.assertEqual(quick_bet.selection.content.outcome_name, self.selection_name,
                         msg=f'Actual Outcome Name "{quick_bet.selection.content.outcome_name}" does not '
                             f'match expected "{self.selection_name}"')
        wait_for_result(lambda: quick_bet.selection.content.odds, name='Odds to appear on Quick Bet')
        self.__class__.price = quick_bet.selection.content.odds
        self.assertTrue(self.price, msg=f'Price is not displayed for "{self.event_name}"')
        self.assertEqual(quick_bet.selection.content.amount_form.default_value, vec.quickbet.DEFAULT_AMOUNT_VALUE,
                         msg=f'Actual default amount value "{quick_bet.selection.content.amount_form.default_value}" '
                             f'does not match expected "{vec.quickbet.DEFAULT_AMOUNT_VALUE}"')
        self.assertTrue(quick_bet.selection.quick_stakes.is_enabled(), msg='Quick Stakes buttons are not shown')
        self.assertEqual(quick_bet.selection.bet_summary.total_stake, '0.00',
                         msg=f'Actual default Total Stake amount value "{quick_bet.selection.bet_summary.total_stake}" '
                             f'does not match expected "0.00"')
        self.assertEqual(quick_bet.selection.bet_summary.total_estimate_returns, '0.00',
                         msg=f'Actual default Est Returns "{quick_bet.selection.bet_summary.total_estimate_returns}" '
                             f'does not match expected "0.00"')
        self.assertTrue(self.site.quick_bet_panel.each_way_checkbox.is_displayed(), msg='E/W box is not displayed')
        self.assertTrue(self.site.quick_bet_panel.add_to_betslip_button.is_enabled(),
                        msg='The button "Add to betslip" is not active')
        self.assertFalse(self.site.quick_bet_panel.place_bet.is_enabled(expected_result=False),
                         msg='The button "Place bet" is active')

    def test_002_tap_on_the_stake_field_enter_any_value(self):
        """
        DESCRIPTION: Tap on the 'Stake' field &  enter any value
        EXPECTED: * The keyboard appears
        EXPECTED: * 'Stake' field is populated with entered value
        EXPECTED: * 'Total Stake', 'Estimated Returns'  (Coral), 'Total Stake', 'Potential Returns' (Ladbrokes) are calculated
        EXPECTED: * The buttons 'Add to betslip' and 'Place bet' are active
        EXPECTED: * The 'Boost' button is active and can be boosted (if available)
        EXPECTED: Please note The keyboard doesn't appear when using 'Quick Stake' buttons
        """
        quick_bet = self.site.quick_bet_panel.selection.content
        if quick_bet.has_odds_boost_tooltip():
            sleep(10)
        quick_bet.amount_form.input.click()
        if not self.is_safari:
            try:
                self.enter_value_using_keyboard(value=self.bet_amount, on_betslip=False)
                self.assertTrue(self.site.quick_bet_panel.keyboard.is_displayed(
                    name='Quick Stake keyboard shown', expected_result=True, timeout=5),
                    msg='Numeric keyboard is not shown')
            except VoltronException:
                quick_bet.amount_form.enter_amount(value=self.bet_amount)
        else:
            quick_bet.amount_form.enter_amount(value=self.bet_amount)

        self.assertEqual(round(float(quick_bet.amount_form.input.value),2), float(f'{self.bet_amount:.2f}'),
                         msg=f'Actual amount "{quick_bet.amount_form.input.value}" does not match '
                             f'expected f"{self.bet_amount:.2f}"')
        actual_est_returns = self.site.quick_bet_panel.selection.bet_summary.total_estimate_returns
        self.verify_estimated_returns(est_returns=float(actual_est_returns),
                                      odds=[self.price],
                                      bet_amount=self.bet_amount)
        actual_stake = self.site.quick_bet_panel.selection.bet_summary.total_stake
        self.assertEqual(actual_stake, f'{self.bet_amount:.2f}',
                         msg=f'Actual "Total Stake" value "{actual_stake}" != Expected "{self.bet_amount:.2f}"')
        self.assertTrue(self.site.quick_bet_panel.add_to_betslip_button.is_enabled(),
                        msg='The button "Add to betslip" is not active')
        self.assertTrue(self.site.quick_bet_panel.place_bet.is_enabled(), msg='The button "Place bet" is not active')

    def test_003_check_the_ew_box(self):
        """
        DESCRIPTION: Check the 'E/W' box
        EXPECTED: * The 'E/W' box is checked
        EXPECTED: * The keyboard is not shown anymore
        """
        self.site.quick_bet_panel.each_way_checkbox.click()
        self.assertTrue(self.site.quick_bet_panel.each_way_checkbox.is_selected(),
                        msg='Each Way checkbox is not selected')
        self.assertFalse(self.site.quick_bet_panel.keyboard.is_displayed(
            expected_result=False, name='Quick Stake keyboard shown', timeout=5),
            msg='Numeric keyboard is shown')

    def test_004_tap_on_place_bet_button(self):
        """
        DESCRIPTION: Tap on 'Place bet' button
        EXPECTED: * Spinner is displayed on 'Place bet' for a few seconds
        EXPECTED: * Bet is placed successfully
        EXPECTED: * User balance is decreased by stake entered on step #2
        """
        self.site.quick_bet_panel.place_bet.click()
        bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
        expected_user_balance = self.user_balance - self.bet_amount * 2
        self.verify_user_balance(expected_user_balance=expected_user_balance)

    def test_005_verify_the_bet_receipt(self):
        """
        DESCRIPTION: Verify the Bet Receipt
        EXPECTED: * 'Bet Receipt' header and 'X' button
        EXPECTED: * The message '✓Bet Placed Successfully'
        EXPECTED: * Date and time of the placed bet (format DD/MM/YYYY, HH:MM)
        EXPECTED: * Type of bet @ price odds (for example, Single @ 1/1)
        EXPECTED: * Bet receipt ID
        EXPECTED: * Selection name
        EXPECTED: * Market name/Event name
        EXPECTED: * E/W odds are mentioned with places(for example, 'Each Way Odds 1/2 Places 1-2')
        EXPECTED: * The number of lines are mentioned with stakes(for example, '2 lines at £1 per line')
        EXPECTED: * Cashout label (if available)
        EXPECTED: * Stake & Est. Returns - Coral, Stake for this bet, Potential returns - Ladbrokes
        EXPECTED: * Message 'This bet has been boosted' (if the price was boosted)
        """
        bet_receipt = self.site.quick_bet_panel.bet_receipt
        quick_bet_panel_title = self.site.quick_bet_panel.header.title
        self.assertEquals(quick_bet_panel_title, tests.settings.betreceipt_title,
                          msg=f'Quick bet panel title: "{quick_bet_panel_title}" doesn\'t match with '
                              f'required "{tests.settings.betreceipt_title}"')
        self.assertTrue(self.site.quick_bet_panel.header.close_button.is_displayed(),
                        msg='"X" button not displayed on BET RECEIPT header')

        self.assertEqual(bet_receipt.header.bet_placed_text, vec.betslip.SUCCESS_BET,
                         msg=f'Text "{bet_receipt.header.bet_placed_text}" '
                             f'is not equal to expected "{vec.betslip.SUCCESS_BET}"')
        actual_date_time = bet_receipt.header.receipt_datetime
        self.assertRegex(actual_date_time, vec.regex.BET_DATA_TIME_FORMAT,
                         msg=f'Bet data and time: "{actual_date_time}" '
                             f'do not match expected pattern: {vec.regex.BET_DATA_TIME_FORMAT}')
        self.assertTrue(bet_receipt.bet_id, msg='Bet Receipt number is not shown')
        self.assertEqual(bet_receipt.name, self.selection_name,
                         msg=f'Actual Selection Name "{bet_receipt.name}" does not match '
                             f'expected "{self.selection_name}"')
        self.event_name = self.event_name.replace(',', '')
        self.assertEqual(bet_receipt.event_name.replace(' v ', ' ').replace(' - ', ' '),
                         self.event_name.replace(' - ', ' '),
                         msg=f'Actual Event Name "{bet_receipt.event_name.replace(" v ", " ").replace(" - ", " ")}" does not match '
                             f'expected "{self.event_name.replace(" - ", " ")}"')
        self.assertEqual(bet_receipt.event_market, self.market_name,
                         msg=f'Actual market name: "{bet_receipt.event_market}" '
                             f'is not as expected: "{self.market_name}"')
        self.assertTrue(bet_receipt.places.is_displayed(), msg='E/W odds with places are not shown')
        self.assertTrue(bet_receipt.lines.is_displayed(), msg='The number of lines with stakes are not shown')
        actual_total_stake = bet_receipt.total_stake
        expected_total_stake = f'{(self.bet_amount * 2):.2f}'
        self.assertEqual(actual_total_stake, expected_total_stake,
                         msg=f'Actual total stake value: "{actual_total_stake}" doesn\'t match '
                             f'with expected: "{expected_total_stake}"')
        actual_estimate_returns = bet_receipt.estimate_returns
        self.verify_estimated_returns(est_returns=actual_estimate_returns,
                                      odds=[self.price],
                                      each_way_coef=self.each_way_coef,
                                      bet_amount=self.bet_amount)

    def test_006_click_on_the_x_button(self):
        """
        DESCRIPTION: Click on the 'X' button
        EXPECTED: The Quick Bet is closed
        """
        self.site.quick_bet_panel.header.close_button.click()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is not closed')

    def test_007_click_on_my_bets_button_from_the_header_for_coral_and_for_ladbrokes_my_account_my_bets(self):
        """
        DESCRIPTION: Click on 'My Bets' button from the header for Coral and for Ladbrokes 'My account' -> 'My Bets'
        EXPECTED: The 'Open Bets' tab is opened
        """
        self.site.open_my_bets_open_bets()

    def test_008_go_to_the_bet_that_was_just_placed_and_verify_that_the_bet_receipt_fields_are_correct(self):
        """
        DESCRIPTION: Go to the bet that was just placed and verify that the Bet Receipt fields are correct
        EXPECTED: Check the following data correctness:
        EXPECTED: * Type of bet (for example, Single(Each Way))
        EXPECTED: * Selection @ price odds (for example, Adelaide Utd @ 1/1)
        EXPECTED: * Market name with odds and places
        EXPECTED: * Event name
        EXPECTED: * Time of the event in format HH:MM, DD Month(for example, 10:30, 17 Jan)
        EXPECTED: * The currency is as user set during registration
        EXPECTED: * Unit stake, Total Stake, Est. Returns/Potential returns
        EXPECTED: * Full/Partial Cashout buttons - if available
        EXPECTED: * 'Watch'/'Watch Live' label (if the event is live with streaming)
        EXPECTED: * '>' Sign to navigate to event page
        """
        # EXPECTED: * '>' Sign to navigate to event page : Cann't be automated.
        today_date_pattern = '%H:%M, Today'
        bet_name, single_bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            timeout=60, bet_type=vec.bet_history.SINGLE_EACH_WAY_BET_TYPE, event_names=self.event_name, number_of_bets=1)

        self.assertEqual(single_bet.bet_type, vec.bet_history.SINGLE_EACH_WAY_BET_TYPE,
                         msg=f'Bet type: "{single_bet.bet_type}" '
                             f'is not as expected: "{vec.bet_history.SINGLE_EACH_WAY_BET_TYPE}"')
        self.assertEqual(single_bet.selection_name, self.selection_name,
                         msg=f'Selection Name: "{single_bet.selection_name}" '
                             f'is not as expected: "{self.selection_name}"')
        self.assertEqual(single_bet.odds_value, self.price,
                         msg=f'Odds value: "{single_bet.odds_value}" '
                             f'is not as expected: "{self.price}"')
        self.assertEqual(single_bet.event_name, self.event_name,
                         msg=f'Event Name: "{single_bet.event_name}" is not as expected: "{self.event_name}"')
        self.assertIn(self.market_name, single_bet.market_name, msg=f'Bet market name: "{single_bet.market_name}" '
                                                                    f'not contain expected: "{self.market_name}"')
        expected_stake = f'£{(self.bet_amount * 2):.2f}'
        self.assertEqual(single_bet.stake.value, expected_stake,
                         msg=f'Bet Stake value: "{single_bet.stake.value}" '
                             f'is not as expected: "{expected_stake}"')
        currency = '£'
        self.assertEqual(single_bet.stake.currency, currency,
                         msg=f'Stake currency "{single_bet.stake.currency}" is not the same as expected "{currency}"')
        self.verify_estimated_returns(est_returns=single_bet.est_returns.stake_value,
                                      odds=[self.price],
                                      each_way_coef=self.each_way_coef,
                                      bet_amount=self.bet_amount)
        bet_legs = single_bet.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'Bet: "{bet_name}" leg not found')
        event_time = next(i.event_time for i in bet_legs.values())
        validate_time(event_time, today_date_pattern) if 'Today' in event_time else \
            validate_time(event_time, self.event_card_future_time_format_pattern)
