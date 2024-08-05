import pytest
import tests
import voltron.environments.constants as vec
from crlat_ob_client.utils.date_time import validate_time
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name


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
@pytest.mark.safari
@pytest.mark.sanity
@vtest
class Test_C1033074_Place_bet_via_Quick_Bet_Sports(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C1033074
    VOL_ID: C58668176
    NAME: Place bet via Quick Bet (Sports)
    DESCRIPTION: This test case verifies placing bet by using Quick Bet for Sports
    DESCRIPTION: NOTE! Quick Bet is NOT present for Desktop
    PRECONDITIONS: 1. Quick Bet functionality is enabled in CMS and user`s settings
    PRECONDITIONS: 2. Load the app
    PRECONDITIONS: 3. Log in with a user that has a positive balance
    """
    keep_browser_open = True
    device_name = 'Pixel 2 XL' if not tests.use_browser_stack else tests.default_pixel

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Create test event, PROD: Find active events
        DESCRIPTION: Log in with a user that has a positive balance
        """
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(
                category_id=self.ob_config.football_config.category_id, all_available_events=True)
            for event in events:
                self.__class__.event_id = event['event']['id']
                self.__class__.event_name = normalize_name(event['event']['name'])
                self.__class__.league = self.get_accordion_name_for_event_from_ss(event=event)
                self.__class__.market_name, outcomes = next(((market['market']['name'],market['market']['children']) for market in event['event']['children'] if
                                                              market['market'].get('children') and  market['market'].get('templateMarketName').title() in ['Match Betting','Match Result']), None)
                self.__class__.team1 = next((outcome['outcome']['name'] for outcome in outcomes if
                                             outcome['outcome'].get('outcomeMeaningMinorCode')), None)
                if self.team1:
                    break
            else:
                raise SiteServeException('No odds for team found')
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.event_name = f'{event.team1} v {event.team2}'
            self.__class__.event_id, self.__class__.team1 = event.event_id, event.team1
            self.__class__.league = tests.settings.football_autotest_league
            self.__class__.market_name = self.expected_market_sections.match_result.title()
        self._logger.info(f'*** Found Football event with name: "{self.event_name}" and id: "{self.event_id}"')
        self.site.login(username=tests.settings.betplacement_user)
        self.__class__.user_balance = self.site.header.user_balance

    def test_001_add_any_sport_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add any  <Sport>  selection to Quick Bet
        EXPECTED: Quick Bet is displayed at the bottom of the page:
        EXPECTED: * Quick Bet header and 'X' button
        EXPECTED: * Selection name, Market name and Event name
        EXPECTED: * 'Use Freebet' under event details (if available)
        EXPECTED: * Quick Stakes (For example, "+£5", "+£10" "+£50", "+£100")
        EXPECTED: * Price odds and Stake box
        EXPECTED: * 'Total Stake', 'Estimated Returns' - Coral, 'Total Stake', 'Potential Returns' - Ladbrokes
        EXPECTED: * The button 'Add to betslip' is active and Place bet' is disabled
        EXPECTED: * 'Boost' button (if available)
        """
        sport_name = vec.sb.FOOTBALL.title()
        self.site.open_sport(name=sport_name)
        self.site.wait_content_state(state_name=sport_name)

        event = self.get_event_from_league(event_id=self.event_id,
                                           section_name=self.league)
        output_prices = event.get_active_prices()
        self.assertTrue(output_prices, msg=f'Could not find output prices for event "{self.event_name}"')

        bet_button = output_prices.get(self.team1)
        #bet_button = output_prices.popitem()[1]
        self.assertTrue(bet_button, msg=f'Bet button for "{self.team1}" was not found')
        self.__class__.price = bet_button.outcome_price_text
        bet_button.click()
        self.assertTrue(bet_button.is_selected(), msg='Outcome button is not highlighted in green')
        quick_bet = self.site.quick_bet_panel
        quick_bet_title = vec.quickbet.QUICKBET_TITLE
        self.assertEqual(quick_bet.header.title, quick_bet_title,
                         msg=f'Actual title "{quick_bet.header.title}" does not match expected "{quick_bet_title}"')
        self.assertTrue(quick_bet.header.close_button.is_displayed(), msg='Quick Bet close button is not shown')
        self.assertEqual(quick_bet.selection.content.event_name, self.event_name,
                         msg=f'Actual Event Name "{quick_bet.selection.content.event_name}" does not '
                         f'match expected "{self.event_name}"')
        self.assertEqual(quick_bet.selection.content.market_name, self.market_name,
                         msg=f'Actual Market Name "{quick_bet.selection.content.market_name}" does not '
                             f'match expected "{self.market_name}"')
        actual_outcome_name = quick_bet.selection.content.outcome_name.replace('(', '').replace(')', '')
        expected_outcome_name = self.team1.replace('(', '').replace(')', '')
        self.assertEqual(actual_outcome_name, expected_outcome_name,
                         msg=f'Actual Outcome Name "{actual_outcome_name}" does not '
                             f'match expected "{expected_outcome_name}"')
        self.assertEqual(quick_bet.selection.content.odds, self.price,
                         msg=f'Actual price "{quick_bet.selection.content.odds}" '
                             f'does not match expected "{self.price}"')
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
        self.assertTrue(self.site.quick_bet_panel.add_to_betslip_button.is_enabled(),
                        msg='The button "Add to betslip" is not active')
        self.assertFalse(self.site.quick_bet_panel.place_bet.is_enabled(expected_result=False),
                         msg='The button "Place bet" is active')

    def test_002_tap_on_the_stake_field_and_enter_any_value(self):
        """
        DESCRIPTION: Tap on the 'Stake' field and enter any value
        EXPECTED: * The keyboard appears
        EXPECTED: * 'Stake' field is populated with entered value
        EXPECTED: * 'Total Stake', 'Estimated Returns' - Coral, 'Total Stake', 'Potential Returns' - Ladbrokes are calculated
        EXPECTED: * The buttons 'Add to betslip' and 'Place bet' are active
        EXPECTED: * The 'Boost' button is active and can be boosted (if available)
        EXPECTED: Please note The keyboard doesn't appear when using 'Quick Stake' buttons
        """
        quick_bet = self.site.quick_bet_panel.selection.content
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
        self.assertEqual(round(float(quick_bet.amount_form.input.value), 2), float(f'{self.bet_amount:.2f}'),
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

    def test_003_tap_on_place_bet_button(self):
        """
        DESCRIPTION: Tap on 'Place bet' button
        EXPECTED: * Spinner is displayed on 'Place bet' for a few seconds
        EXPECTED: * Bet is placed successfully
        EXPECTED: * User balance is decreased by stake entered on step #2
        """
        self.site.quick_bet_panel.place_bet.click()
        bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
        expected_user_balance = self.user_balance - self.bet_amount
        self.verify_user_balance(expected_user_balance=expected_user_balance)

    def test_004_verify_the_bet_receipt(self):
        """
        DESCRIPTION: Verify the Bet Receipt
        EXPECTED: Bet Receipt consists of:
        EXPECTED: * 'Bet Receipt' header and 'X' button
        EXPECTED: * The message '✓Bet Placed Successfully'
        EXPECTED: * Date and time of the placed bet (format DD/MM/YYYY, HH:MM)
        EXPECTED: * Type of bet @ price odds (for example, Single @  1/1)
        EXPECTED: * Bet receipt ID
        EXPECTED: * Selection name
        EXPECTED: * Market name/Event name
        EXPECTED: * Cashout label (if available)
        EXPECTED: * Stake & Est. Returns - Coral, Stake for this bet, Potential returns - Ladbrokes
        EXPECTED: * Message 'This bet has been boosted' (if the price was boosted)
        """
        self.__class__.bet_receipt = self.site.quick_bet_panel.bet_receipt

        quick_bet_panel_title = self.site.quick_bet_panel.header.title
        self.assertEquals(quick_bet_panel_title, tests.settings.betreceipt_title,
                          msg=f'Quick bet panel title: "{quick_bet_panel_title}" doesn\'t match with required '
                              f'"{tests.settings.betreceipt_title}"')
        self.assertTrue(self.site.quick_bet_panel.header.close_button.is_displayed(),
                        msg='"X" button not displayed on BET RECEIPT header')

        self.assertEqual(self.bet_receipt.header.bet_placed_text, vec.betslip.SUCCESS_BET,
                         msg=f'Text "{self.bet_receipt.header.bet_placed_text}" '
                             f'is not equal to expected "{vec.betslip.SUCCESS_BET}"')
        actual_date_time = self.bet_receipt.header.receipt_datetime
        self.assertRegex(actual_date_time, vec.regex.BET_DATA_TIME_FORMAT,
                         msg=f'Bet data and time: "{actual_date_time}" '
                             f'do not match expected pattern: {vec.regex.BET_DATA_TIME_FORMAT}')
        self.assertTrue(self.bet_receipt.bet_id, msg='Bet Receipt number is not shown')
        self.assertEqual(self.bet_receipt.name, self.team1,
                         msg=f'Actual Selection Name "{self.bet_receipt.name}" does not match expected "{self.team1}"')
        self.assertEqual(self.bet_receipt.event_name, self.event_name,
                         msg=f'Actual Event Name "{self.bet_receipt.event_name}" does not match '
                             f'expected "{self.event_name}"')
        self.assertEqual(self.bet_receipt.event_market, self.market_name,
                         msg=f'Actual market name: "{self.bet_receipt.event_market}" '
                             f'is not as expected: "{self.market_name}"')
        actual_total_stake = f'£ {self.bet_receipt.total_stake}'
        expected_total_stake = f'£ {self.bet_amount:.2f}'
        self.assertEqual(actual_total_stake, expected_total_stake,
                         msg=f'Actual total stake value: "{actual_total_stake}" doesn\'t match with '
                             f'expected: "{expected_total_stake}"')
        actual_estimate_returns = self.bet_receipt.estimate_returns
        self.verify_estimated_returns(est_returns=actual_estimate_returns,
                                      odds=[self.price],
                                      bet_amount=self.bet_amount)

    def test_005_click_on_the_x_button(self):
        """
        DESCRIPTION: Click on the 'X' button
        EXPECTED: The Quick Bet is closed
        """
        self.site.quick_bet_panel.header.close_button.click()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is not closed')

    def test_006_click_on_my_bets_button_from_the_header_for_coral_and_for_ladbrokes_my_account_my_bets(self):
        """
        DESCRIPTION: Click on 'My Bets' button from the header for Coral and for Ladbrokes 'My account' -> 'My Bets'
        EXPECTED: 'Open Bets' tab is opened
        """
        self.site.open_my_bets_open_bets()

    def test_007_go_to_the_bet_that_was_just_placed_and_verify_that_the_bet_receipt_fields_are_correct(self):
        """
        DESCRIPTION: Go to the bet that was just placed and verify that the Bet Receipt fields are correct
        EXPECTED: Check the following data correctness:
        EXPECTED: * Type of bet (for example, Single)
        EXPECTED: * Selection @ price odds (for example, Adelaide Utd @  1/1)
        EXPECTED: * Market name
        EXPECTED: * Event name
        EXPECTED: * Time of the event in format HH:MM, DD Month(for example, 10:30, 17 Jan)
        EXPECTED: * The currency is as user set during registration
        EXPECTED: * Full/Partial Cashout (if available)
        EXPECTED: * Stake & Est. Returns - Coral, Stake, Potential returns - Ladbrokes
        EXPECTED: * '>' Sign to navigate to event page
        """
        # EXPECTED: * '>' Sign to navigate to event page --> Can not be automated
        today_date_pattern = '%H:%M, Today'
        bet_name, single_bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            timeout=60, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_name, number_of_bets=1)

        self.assertEqual(single_bet.bet_type, vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
                         msg=f'Bet type: "{single_bet.bet_type}" '
                             f'is not as expected: "{vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE}"')
        actual_selection_name = single_bet.selection_name.replace('(', '').replace(')', '')
        expected_selection_name = self.team1.replace('(', '').replace(')', '')
        self.assertEqual(actual_selection_name, expected_selection_name,
                         msg=f'Selection Name: "{actual_selection_name}" '
                             f'is not as expected: "{expected_selection_name}"')
        self.assertEqual(single_bet.odds_value, self.price,
                         msg=f'Odds value: "{single_bet.odds_value}" '
                             f'is not as expected: "{self.price}"')
        self.assertEqual(single_bet.event_name, self.event_name,
                         msg=f'Event Name: "{single_bet.event_name}" is not as expected: "{self.event_name}"')
        self.assertEqual(single_bet.market_name, self.market_name,
                         msg=f'Bet market name: "{single_bet.market_name}" '
                             f'is not as expected: "{self.market_name}"')
        expected_stake = f'£{self.bet_amount:.2f}'
        self.assertEqual(single_bet.stake.value, expected_stake,
                         msg=f'Bet Stake value: "{single_bet.stake.value}" '
                             f'is not as expected: "{expected_stake}"')
        currency = '£'
        self.assertEqual(single_bet.stake.currency, currency,
                         msg=f'Stake currency "{single_bet.stake.currency}" is not the same as expected "{currency}"')
        self.verify_estimated_returns(est_returns=single_bet.est_returns.stake_value,
                                      odds=[self.price],
                                      bet_amount=self.bet_amount)
        bet_legs = single_bet.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'Bet: "{bet_name}" leg found')
        event_time = next(i.event_time for i in bet_legs.values())
        validate_time(event_time, today_date_pattern) if 'Today' in event_time else \
            validate_time(event_time, self.event_card_future_time_format_pattern)
