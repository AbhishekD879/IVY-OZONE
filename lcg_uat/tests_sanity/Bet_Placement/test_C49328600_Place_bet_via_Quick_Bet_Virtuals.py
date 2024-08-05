import pytest
from crlat_ob_client.utils.date_time import validate_time

from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.voltron_exception import VoltronException
from random import choice
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter, SiteServeRequests
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_018_Virtual_Sports.BaseVirtualsTest import BaseVirtualsTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.waiters import wait_for_result


@pytest.mark.hl
@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.high
@pytest.mark.mobile_only
@pytest.mark.bet_placement
@pytest.mark.my_bets
@pytest.mark.quick_bet
@pytest.mark.virtual_sports
@pytest.mark.reg157_fix
@pytest.mark.login
@pytest.mark.numeric_keyboard
@pytest.mark.safari
@pytest.mark.sanity
@pytest.mark.soc
@vtest
class Test_C49328600_Place_bet_via_Quick_Bet_Virtuals(BaseRacing, BaseSportTest, BaseBetSlipTest, BaseVirtualsTest):
    """
    TR_ID: C49328600
    VOL_ID: C50103008
    NAME: Place bet via Quick Bet (Virtuals)
    DESCRIPTION: This test case verifies placing bet by using Quick Bet for Virtuals
    DESCRIPTION: NOTE! Quick Bet is NOT present for Desktop
    PRECONDITIONS: 1. Quick Bet functionality is enabled in CMS and user`s settings
    PRECONDITIONS: 2. Load the app
    PRECONDITIONS: 3. Log in with a user that has a positive balance
    PRECONDITIONS: 4. Navigate to Virtuals landing page
    """
    keep_browser_open = True
    device_name = 'Pixel 2 XL' if not tests.use_browser_stack else tests.default_pixel
    default_virtuals_market_name = 'Win or Each Way'
    enable_bs_performance_log = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Log in with a user that has a positive balance
        DESCRIPTION: Navigate to Virtuals landing page
        """
        virtuals_cms_class_ids = self.cms_virtual_sports_class_ids()
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.ob_config.virtuals_config.category_id)
        sports_list = ss_req.ss_class(query_builder=self.ss_query_builder.
                                      add_filter(simple_filter(LEVELS.CLASS,
                                                               ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS,
                                                               str(self.ob_config.virtuals_config.category_id))))
        if not sports_list:
            raise SiteServeException('There are no active virtual sports')
        event = None
        events = None
        for sport_class in sports_list:
            class_id = sport_class['class']['id']
            additional_filter = exists_filter(
                LEVELS.EVENT, simple_filter(LEVELS.MARKET,
                                            ATTRIBUTES.NCAST_TYPE_CODES, OPERATORS.INTERSECTS, 'CF,TC')), exists_filter(
                LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.IS_EACH_WAY_AVAILABLE, OPERATORS.IS_TRUE))
            events = self.get_active_event_for_class(class_id=class_id, additional_filters=additional_filter,
                                                     raise_exceptions=False)
            if not events:
                continue
            event = choice(events)
            ss_class_id = event['event']['classId']
            if ss_class_id not in virtuals_cms_class_ids:
                continue
            break
        if not event or not events:
            raise SiteServeException('There are no active virtual sport events')
        tab_name = self.cms_virtual_sport_tab_name_by_class_ids(class_ids=[ss_class_id])
        self.__class__.expected_tab = tab_name[0]

        self.site.login(username=tests.settings.betplacement_user)
        self.__class__.user_balance = self.site.header.user_balance
        self.site.open_sport(self.get_sport_title(category_id=self.ob_config.virtuals_config.category_id),
                             content_state='VirtualSports')

    def test_001_add_any_sport_or_race_lpsp_selection_from_virtuals_for_example_football_horse_racing(self):
        """
        DESCRIPTION: Add any <Sport> or <Race> LP/SP selection from Virtuals (for example, Football, Horse Racing)
        EXPECTED: Quick Bet is displayed at the bottom of the page:
        EXPECTED: * Quick Bet header and 'X' button
        EXPECTED: * Selection name, Market name and Event name
        EXPECTED: * 'Use Freebet' under event details (if available)
        EXPECTED: * Quick Stakes (For example, "+£5", "+£10" "+£50", "+£100")
        EXPECTED: * Price odds(LP/SP if available) and Stake box
        EXPECTED: * The button 'Add to betslip' is active and 'Place bet' is disabled
        EXPECTED: * 'Boost' button (if available)
        EXPECTED: * E/W box - for races, if available
        EXPECTED: * 'Total Stake', 'Estimated Returns' - Coral, 'Total Stake', 'Potential Returns' - Ladbrokes
        EXPECTED: Please note that Races may have 'E/W' boxes & SP' or 'LP' prices
        """
        # added new Virtual hub home page in FE,click on any one of top sport and navigate to main virtual sport page
        virtual_hub_home_page = self.cms_config.get_system_configuration_structure().get('VirtualHubHomePage')
        if virtual_hub_home_page.get('enabled') and (virtual_hub_home_page.get('topSports') or virtual_hub_home_page.get('otherSports') or virtual_hub_home_page.get('featureZone') ):
            wait_for_result(lambda: next(
                (section for section_name, section in self.site.virtual_sports_hub.items_as_ordered_dict.items() if
                 section_name.upper() != 'Next Events'), None) is not None, timeout=5,
                            name="waiting for top sport to available in front end")
            virtual_section = next(
                (section for section_name, section in self.site.virtual_sports_hub.items_as_ordered_dict.items() if
                 section_name.upper() == 'TOP SPORTS'), None)
            virtual_sport = list(virtual_section.items_as_ordered_dict.values())[0]
            if self.device_type == 'mobile' and self.use_browser_stack and 'iPhone' in self._device.device_args.get('device'):
                virtual_sport.link.click()
            else:
                virtual_sport.click()
        virtual_sports_list = self.site.virtual_sports
        open_tab = virtual_sports_list.sport_carousel.open_tab(self.expected_tab)
        self.assertTrue(open_tab, msg=f'Tab "{self.expected_tab}" is not opened')

        event_off_times_list = virtual_sports_list.tab_content.event_off_times_list
        self.assertTrue(event_off_times_list.is_displayed(), msg=f'No events of times found')
        items_list = event_off_times_list.items_as_ordered_dict.keys()
        self.assertTrue(items_list, msg='No market tabs are present for the event')
        event_off_time_tab = choice(list(items_list)[3:9])
        event_off_times_list.select_off_time(event_off_time_tab)

        self.__class__.event_name = f'{event_off_time_tab} {virtual_sports_list.tab_content.sport_event_name}'
        self.__class__.event_name_my_bets = f'{virtual_sports_list.tab_content.sport_event_name}'
        self.__class__.event_name_my_bets_full = f'{virtual_sports_list.tab_content.sport_event_name} {event_off_time_tab}, Today'

        sections = virtual_sports_list.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        name, runner_buttons = list(sections.items())[0]
        self.__class__.selection_name = name
        runner_buttons.bet_button.click()
        self.site.wait_for_quick_bet_panel()
        if self.is_safari:
            self.__class__.market_name = self.default_virtuals_market_name
        else:
            resp = self.get_web_socket_response_by_id(response_id=31001, delimiter='42')
            self.__class__.market_name = resp['data']['event']['markets'][0]['name']
        quick_bet = self.site.quick_bet_panel
        self.assertEqual(quick_bet.header.title, vec.quickbet.QUICKBET_TITLE,
                         msg=f'Actual title "{quick_bet.header.title}" does not match expected "{vec.quickbet.QUICKBET_TITLE}"')
        self.assertTrue(quick_bet.header.close_button.is_displayed(), msg='Quick Bet close button is not shown')
        self.assertEqual(quick_bet.selection.content.event_name, self.event_name,
                         msg=f'Actual Event Name "{quick_bet.selection.content.event_name}" does not '
                             f'match expected "{self.event_name}"')
        self.assertEqual(quick_bet.selection.content.market_name, self.market_name,
                         msg=f'Actual Market Name "{quick_bet.selection.content.market_name}" does not '
                             f'match expected "{self.market_name}"')
        self.assertEqual(quick_bet.selection.content.outcome_name, self.selection_name,
                         msg=f'Actual Outcome Name "{quick_bet.selection.content.outcome_name}" does not '
                             f'match expected "{self.selection_name}"')
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

    def test_002_tap_on_the_stake_field_and_enter_any_value(self):
        """
        DESCRIPTION: Tap on the 'Stake' field and enter any value
        EXPECTED: * The keyboard appears
        EXPECTED: * 'Stake' field is populated with entered value
        EXPECTED: * 'Total Stake', 'Estimated Returns' (Coral), 'Total Stake', 'Potential Returns' (Ladbrokes) are calculated
        EXPECTED: * The buttons 'Add to betslip' and 'Place bet' are active
        EXPECTED: * The 'Boost' button is active and can be boosted (if available)
        EXPECTED: Please note that the keyboard doesn't appear when using 'Quick Stake' buttons
        """
        quick_bet = self.site.quick_bet_panel.selection.content
        # this workaround for Virtual Sport input form
        if not self.is_safari:  # cannot trigger bma keyboard on safari
            try:
                self.enter_value_using_keyboard(value=self.bet_amount, on_betslip=False)
                self.assertTrue(self.site.quick_bet_panel.keyboard.is_displayed(
                    name='Quick Stake keyboard shown', expected_result=True, timeout=5),
                    msg='Numeric keyboard is not shown')
            except VoltronException:
                quick_bet.amount_form.enter_amount(value=self.bet_amount)
        else:
            quick_bet.amount_form.input.value = self.bet_amount

        self.assertEqual(float(quick_bet.amount_form.input.value), self.bet_amount,
                         msg=f'Actual amount "{float(quick_bet.amount_form.input.value)}" does not match '
                             f'expected "{self.bet_amount}"')
        if not self.is_safari:
            try:
                self.assertTrue(self.site.quick_bet_panel.keyboard.is_displayed(
                    name='Quick Stake keyboard shown', expected_result=True, timeout=5),
                    msg='Numeric keyboard is not shown')
            except Exception:
                self._logger.info(
                    f'***Numeric keyboard is not shown"')
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
        EXPECTED: * Type of bet @ price odds (for example, Single @ 1/1)
        EXPECTED: * Bet receipt ID
        EXPECTED: * Selection name
        EXPECTED: * Market name/Event name
        EXPECTED: * Cashout label (if available)
        EXPECTED: * Stake & Est. Returns - Coral, Stake for this bet, Potential returns - Ladbrokes
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
        self.assertEqual(bet_receipt.event_name, self.event_name,
                         msg=f'Actual Event Name "{bet_receipt.event_name}" does not match '
                             f'expected "{self.event_name}"')
        self.assertEqual(bet_receipt.event_market, self.market_name,
                         msg=f'Actual market name: "{bet_receipt.event_market}" '
                             f'is not as expected: "{self.market_name}"')
        self.assertEqual(bet_receipt.total_stake, f'{self.bet_amount:.2f}',
                         msg=f'Actual total stake value: "{bet_receipt.total_stake}" doesn\'t match '
                             f'with expected: "{self.bet_amount:.2f}"')
        actual_estimate_returns = bet_receipt.estimate_returns
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
        EXPECTED: * Type of bet (for example, Single)
        EXPECTED: * Selection @ price odds (for example, Adelaide Utd @ 1/1)
        EXPECTED: * Market name (with odds and places - for racing)
        EXPECTED: * Event name
        EXPECTED: * Time of the event in format HH:MM, DD Month(for example, 10:30, 17 Jan)
        EXPECTED: * The currency is as user set during registration
        EXPECTED: Stake & Est. Returns (Coral), Stake, Potential returns (Ladbrokes) - for sports
        EXPECTED: * Unit stake, Total Stake, Est. Returns/Potential returns - for races
        """
        today_date_pattern = '%H:%M, Today'
        bet_name, single_bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            timeout=60, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_name_my_bets_full,
            number_of_bets=1)

        self.assertEqual(single_bet.bet_type, vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
                         msg=f'Bet type: "{single_bet.bet_type}" '
                             f'is not as expected: "{vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE}"')
        self.assertEqual(single_bet.selection_name, self.selection_name,
                         msg=f'Selection Name: "{single_bet.selection_name}" '
                             f'is not as expected: "{self.selection_name}"')
        self.assertEqual(single_bet.odds_value, self.price,
                         msg=f'Odds value: "{single_bet.odds_value}" '
                             f'is not as expected: "{self.price}"')

        event_name = self.event_name_my_bets
        actual_event_name = (single_bet.event_name)[6:]
        self.assertEqual(actual_event_name, event_name,
                         msg=f'Event Name: "{actual_event_name}" is not as expected: "{event_name}"')
        self.assertIn(self.market_name, single_bet.market_name, msg=f'Bet market name: "{single_bet.market_name}" '
                                                                    f'not contain expected: "{self.market_name}"')
        bet_stake = f'£{self.bet_amount:.2f}'
        self.assertEqual(single_bet.stake.value, bet_stake,
                         msg=f'Bet Stake value: "{single_bet.stake.value}" '
                             f'is not as expected: "{bet_stake}"')
        currency = '£'
        self.assertEqual(single_bet.stake.currency, currency,
                         msg=f'Stake currency "{single_bet.stake.currency}" is not the same as expected "{currency}"')
        self.verify_estimated_returns(est_returns=single_bet.est_returns.stake_value,
                                      odds=[self.price],
                                      bet_amount=self.bet_amount)
        bet_legs = single_bet.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'Bet: "{bet_name}" leg not found')
        event_time = next(i.event_time for i in bet_legs.values())
        validate_time(event_time, today_date_pattern) if 'Today' in event_time else \
            validate_time(event_time, self.event_card_future_time_format_pattern)
