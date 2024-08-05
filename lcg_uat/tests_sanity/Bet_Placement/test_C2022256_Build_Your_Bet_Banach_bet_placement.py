from datetime import datetime
import time
import pytest
from crlat_ob_client.utils.date_time import validate_time

import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.utils.waiters import wait_for_result
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.critical
@pytest.mark.build_your_bet
@pytest.mark.build_your_bet_dashboard
@pytest.mark.bet_placement
@pytest.mark.banach
@pytest.mark.desktop
@pytest.mark.login
@pytest.mark.safari
@pytest.mark.hotfix
@pytest.mark.sanity
@pytest.mark.soc
@vtest
class Test_C2022256_Build_Your_Bet_Banach_bet_placement(BaseBanachTest, BaseBetSlipTest):
    """
    TR_ID: C2022256
    NAME: Build Your Bet Banach bet placement
    DESCRIPTION: Test case verifies success flow of adding Banach(Match Market) selections to BYB betslip and placing a bet
    PRECONDITIONS: **TEST2 event: 8424205**
    PRECONDITIONS: CMS config:
    PRECONDITIONS: **Guide on CMS configuration for Banach and Digital Sport:**
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Banach
    PRECONDITIONS: 1) Build Your Bet tab is available on Event Details Page :
    PRECONDITIONS: a) Build Your Bet tab is available on Event Details Page : In CMS -> System-configuration -> YOURCALLICONSANDTABS -> 'enableTab' is selected
    PRECONDITIONS: b) Banach leagues are mapped in CMS: Your Call > YourCall leagues
    PRECONDITIONS: c) Event belonging to Banach league is mapped (on Banach side)
    PRECONDITIONS: 2) Match Markets switcher is turned on : BYB > BYB switchers > enable Match Markets
    PRECONDITIONS: HL requests:
    PRECONDITIONS: Request for Banach leagues: https://buildyourbet-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/api/v1/leagues
    PRECONDITIONS: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/leagues
    PRECONDITIONS: Request for Banach market groups: https://buildyourbet-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/api/v2/markets-grouped?obEventId=xxxxx
    PRECONDITIONS: Request for Banach selections: https://buildyourbet-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/api/v1/selections?marketIds=[ids]&obEventId=xxxxx
    PRECONDITIONS: Check the following WS for Adding selection to Quick bet and placing bet:
    PRECONDITIONS: wss://remotebetslip-dev1.coralsports.dev.cloud.ladbrokescoral.com/quickbet/?EIO=3&transport=websocket
    PRECONDITIONS: Build Your Bet tab on event details page is loaded and no selection added to dashboard
    """
    keep_browser_open = True
    proxy = None
    blocked_hosts = ['*spark-br.*']
    device_name = 'Nexus 5X' if not tests.use_browser_stack else tests.default_pixel
    bet_amount = 1
    switcher_name = '90 mins'
    expected_odds_sign = '@'
    currency = '£'
    is_today_event = False
    enable_bs_performance_log = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find active event with Banach markets
        DESCRIPTION: Use request https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/events
        """
        self.__class__.eventID = self.get_ob_event_with_byb_market()
        self.site.login(async_close_dialogs=False)
        format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_FRAC)
        self.assertTrue(format_changed, msg='Odds format is not changed to fractional')
        self.navigate_to_edp(event_id=self.eventID)
        self.assertTrue(self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet),
                        msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')

        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        event_start_time = event_resp[0]['event']['startTime']
        self._logger.info(f"Raw Event time {event_start_time} *********************")
        self._logger.info(f"Browser Time zone {self._device.driver.execute_script('return Intl.DateTimeFormat().resolvedOptions().timeZone')} ****************")
        is_dst = time.localtime().tm_isdst
        utc_offset = 0 if is_dst == 0 else 60
        #utc_offset = -330 if self.use_browser_stack and self.device_type == "mobile" else offset_time
        self.__class__.event_start_time_local = self.convert_time_to_local(date_time_str=event_start_time,
                                                                           ob_format_pattern=self.ob_format_pattern,
                                                                           future_datetime_format=self.event_card_future_time_format_pattern,
                                                                           ss_data=True, utcoffset=utc_offset)
        event_time_day_ob = self.event_start_time_local.split(', ')[1].lower()
        self.__class__.event_name = event_resp[0]['event']['name'].rstrip()
        self.__class__.detailed_event_name = f'{self.event_name} {self.event_start_time_local}'
        if event_time_day_ob == 'today':
            self.__class__.is_today_event = True

    def test_001_add_a_few_selections_from_different_markets_to_dashboard(self):
        """
        DESCRIPTION: Add a few selections from different markets to dashboard
        EXPECTED: Selections are added to the dashboard:
        EXPECTED: * The BYB overlay with the name of selections and teams
        EXPECTED: * Active "Place bet" button with odds
        EXPECTED: * The selections with delete buttons
        EXPECTED: * "Open"/"Close" buttons to expand and collapse the BYB overlay
        EXPECTED: ![](index.php?/attachments/get/56623626)
        """
        # Match betting selection
        match_betting = self.get_market(market_name=self.expected_market_sections.match_betting)
        match_betting_selection_names = match_betting.set_market_selection(selection_index=1, time=True)
        self.assertTrue(match_betting_selection_names, msg='No one selection added to Dashboard')
        match_betting.add_to_betslip_button.click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(),
                        msg='BYB Dashboard panel is not shown')
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            self.initial_counter)

#        team1 = match_betting.outcomes.items[0].name.upper().replace("FF", "").replace("FC", "").strip()
        self.__class__.summary_block = self.site.sport_event_details.tab_content.dashboard_panel.byb_summary
        team1 = self.summary_block.summary_description.dashboard_market_text.upper().\
            replace(self.expected_market_sections.match_betting.upper(), "").replace("90 MINS", "")
        self.__class__.match_betting_market_and_selection_name = [self.expected_market_sections.match_betting,
                                                                  team1.upper().strip()]

        self.__class__.initial_counter += 1

        # Both Teams To Score selection
        both_teams_to_score = self.get_market(market_name=self.expected_market_sections.both_teams_to_score)
        both_teams_to_score_names = both_teams_to_score.set_market_selection(selection_index=1, time=True)
        self.assertTrue(both_teams_to_score_names, msg='No one selection added to Dashboard')
        both_teams_to_score.add_to_betslip_button.click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(),
                        msg='BYB Dashboard panel is not shown')
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            self.initial_counter)

        self.__class__.both_teams_to_score_market_and_selection_name = [self.expected_market_sections.both_teams_to_score,
                                                                        'YES']

        added_selection_names = [f' {self.switcher_name} '.join(self.match_betting_market_and_selection_name),
                                 ' '.join(self.both_teams_to_score_market_and_selection_name)]

        self.__class__.initial_counter += 1

        self.summary_block = self.site.sport_event_details.tab_content.dashboard_panel.byb_summary
        self.assertEquals(self.summary_block.summary_description.dashboard_title,
                          vec.yourcall.DASHBOARD_TITLE,
                          msg=f'Dashboard title "{self.summary_block.summary_description.dashboard_title}" '
                              f'is not the same as expected "{vec.yourcall.DASHBOARD_TITLE}"')

        expected_added_selections = ', '.join(added_selection_names).upper()
        dashboard_markets_list = self.summary_block.summary_description.dashboard_market_text
        self.assertEqual(dashboard_markets_list, expected_added_selections,
                         msg=f'Dashboard Markets and selections list "{dashboard_markets_list}" '
                             f'is not equal to expected "{expected_added_selections}"')

        self.assertTrue(self.summary_block.place_bet.is_displayed(), msg='"Place bet" button is not displayed')
        self.assertEqual(self.summary_block.place_bet.text, vec.yourcall.PLACE_BET,
                         msg=f'Place bet button text: "{self.summary_block.place_bet.text}" '
                             f'is not the same as expected: "{vec.yourcall.PLACE_BET}"')
        self.assertTrue(self.summary_block.open_close_toggle_button.is_displayed(),
                        msg='"Open"/"Close" button is not displayed')

        odds = self.summary_block.place_bet.value
        self.assertTrue(odds, msg='Can not get odds for given selections')

        selections = self.get_byb_dashboard_outcomes()
        self.assertTrue(selections, msg='No selections found')
        self.assertEqual(len(selections), self.initial_counter,
                         msg=f'There are "{len(selections)}" selections on BYB dashboard, but '
                             f'{self.initial_counter} expected')
        for selection_name, selection in list(selections.items()):
            self.assertTrue(selection.has_remove_button(),
                            msg=f'Delete button is not displayed for "{selection_name}" selection')

    def test_002_tap_on_the_place_bet_button_with_odds(self):
        """
        DESCRIPTION: Tap on the "Place bet" button with odds
        EXPECTED: - BYB betslip appears:
        EXPECTED: * Betslip header and "X" button
        EXPECTED: * Selection and market names
        EXPECTED: * Price odds and Stake box
        EXPECTED: * Quick Stakes (For example, "+£5", "+£10" "+£50", "+£100")
        EXPECTED: * Total Stake & Estimated returns
        EXPECTED: * The button "Back" is active and "Place bet" is disabled
        EXPECTED: - In WS client sends message with code 50001 containing selections ids and receives message from quick bet with code 51001 with price
        EXPECTED: ![](index.php?/attachments/get/56623627)
        """
        self.summary_block.place_bet.scroll_to()
        self.summary_block.place_bet.click()
        self.assertTrue(self.site.wait_for_byb_betslip_panel(), msg='BYB Betslip not appears')

        self.__class__.byb_betslip_panel = self.site.byb_betslip_panel
        self.assertTrue(self.byb_betslip_panel.header.has_close_button(),
                        msg='BYB Betslip header does not have "Close" button')
        self.assertTrue(self.byb_betslip_panel.selection.quick_stakes.is_displayed(), msg='Quick Stakes are not shown')

        self.assertTrue(self.byb_betslip_panel.total_stake, msg='Total stake is not shown')

        content = self.byb_betslip_panel.selection.content
        self.assertTrue(content.odds, msg='Odds value not found')
        self.assertTrue(content.amount_form.is_displayed(), msg='Amount input field not displayed')

        selections = content.outcomes_section.items_as_ordered_dict
        self.assertTrue(selections, msg='No one selection found in BYB betslip')
        self.__class__.all_selection_names = list(selections.keys())

        self.assertTrue(self.byb_betslip_panel.back_button.is_enabled(expected_result=True),
                        msg='"BACK" button is not active')
        self.assertTrue(self.byb_betslip_panel.place_bet.is_displayed(), msg='"PLACE BET" button not displayed')
        if not self.is_safari:
            request = wait_for_result(
                lambda: self.get_web_socket_response_by_id(response_id=self.response_50001, delimiter='42'),
                name=f'WS message with code {self.response_50001} to appear',
                timeout=120,
                poll_interval=2)
            self.assertTrue(request, msg=f'Response with frame ID #{self.response_50001} not received')
            self._logger.debug(f'*** Request data "{request}" for "{self.response_50001}"')
            self.assertTrue(request.get('selectionIds'), msg='Received response does not contain selections ids')

            request = wait_for_result(
                lambda: self.get_web_socket_response_by_id(response_id=self.response_51001, delimiter='42'),
                name=f'WS message with code {self.response_51001} to appear',
                timeout=30,
                poll_interval=1)
            self.assertTrue(request, msg=f'Response with frame ID #{self.response_51001} not received')
            self._logger.debug(f'*** Request data "{request}" for "{self.response_51001}"')
            request_data = request.get('data')
            self.assertTrue(request_data, msg='Received response does not contain data')
            self.assertTrue(request_data.get('priceNum'), msg='Received response does not contain price info')
            self.assertTrue(request_data.get('priceDen'), msg='Received response does not contain price info')
        else:
            self._logger.warning('WS response verification cannot be done on Safari browser')

    def test_003_tap_on_the_stake_field_and_enter_any_value(self):
        """
        DESCRIPTION: Tap on the "Stake" field and enter any value
        EXPECTED: * The keyboard appears
        EXPECTED: * "Stake" field is populated with entered value
        EXPECTED: * The buttons "Back" and "Place bet" are active
        EXPECTED: Please note The keyboard doesn't appear when using "Quick Stake" buttons
        """
        self.__class__.user_balance = self.site.header.user_balance
        if self.device_type == 'mobile' and not self.is_safari:
            self.byb_betslip_panel.selection.content.amount_form.click()
            keyboard = self.byb_betslip_panel.keyboard
            try:
                self.enter_value_using_keyboard(value=self.bet_amount, on_betslip=False)
                self.assertTrue(keyboard.is_displayed(name='Numeric keyboard shown', timeout=3),
                                msg='Numeric keyboard is not shown')
            except VoltronException:
                self.byb_betslip_panel.selection.content.amount_form.enter_amount(value=self.bet_amount)


        else:
            self.site.byb_betslip_panel.selection.content.amount_form.enter_amount(value=self.bet_amount)

        self.assertTrue(self.byb_betslip_panel.back_button.is_enabled(), msg='"BACK" button not is not active')
        self.assertTrue(self.byb_betslip_panel.place_bet.is_enabled(), msg='"PLACE BET" button is not active')

    def test_004_tap_on_place_bet_button(self):
        """
        DESCRIPTION: Tap on "Place bet" button
        EXPECTED: * Spinner is displayed on "Place bet" for a few seconds
        EXPECTED: * Bet is placed successfully
        EXPECTED: * User balance is decreased by stake entered on step #3
        EXPECTED: - In WS client sends message with code 50011 containing price, stake, currency info and receives message with from quick bet with code 51101 containing "response code":1, bet id, receipt, stake.
        """
        self.byb_betslip_panel.place_bet.click()

        if not self.is_safari:

            ws_client_response_structure = ['price', 'stake', 'currency']
            request = wait_for_result(lambda: self.get_web_socket_response_by_id(response_id=self.response_50011,
                                                                                 delimiter='42'),
                                      name=f'WS message with code {self.response_50011} to appear',
                                      timeout=45,
                                      poll_interval=1)

            self.assertTrue(request, msg=f'Response with frame ID #{self.response_50011} not received')
            self._logger.debug(f'*** Request data "{request}" for "{self.response_50011}"')
            self.assertTrue(all(request.get(item) for item in ws_client_response_structure),
                            msg=f'Actual request data "{request.keys()}" does not contain '
                                f'expected info "{ws_client_response_structure}"')

            ws_client_response_structure = ['betId', 'receipt', 'totalStake']
            request = wait_for_result(lambda: self.get_web_socket_response_by_id(response_id=self.response_51101,
                                                                                 delimiter='42'),
                                      name=f'WS message with code {self.response_51101} to appear',
                                      timeout=45,
                                      poll_interval=1)
            self.assertTrue(request, msg=f'Response with frame ID #{self.response_51101} not received')
            self._logger.debug(f'*** Request data "{request}" for "{self.response_51101}"')
            actual_response_code = request['data']['responseCode']
            self.assertEqual(actual_response_code, 1, msg=f'Response code "{actual_response_code}" is not equalt to "1"')
            request_data = request['data']['betPlacement']
            self.assertTrue(all(request_data[0].get(item) for item in ws_client_response_structure),
                            msg=f'Actual request data "{request_data[0].keys()}" does not contain '
                                f'expected info "{ws_client_response_structure}"')
        else:
            self._logger.warning('WS response verification cannot be done on Safari browser')

        self.assertTrue(self.site.wait_for_byb_bet_receipt_panel(timeout=25),
                        msg='Build Your Bet Receipt is not displayed')
        expected_user_balance = float(self.user_balance) - float(self.bet_amount)
        self.verify_user_balance(expected_user_balance=expected_user_balance)

    def test_005_verify_the_bet_receipt(self):
        """
        DESCRIPTION: Verify the Bet Receipt
        EXPECTED: Bet Receipt consists of:
        EXPECTED: * "Bet Receipt" header and "X" button
        EXPECTED: * The message "✓Bet Placed Successfully"
        EXPECTED: * Date and time of the placed bet (format DD/MM/YYYY, HH:MM)
        EXPECTED: * Selection & Market names
        EXPECTED: * Odds
        EXPECTED: * Bet receipt ID
        EXPECTED: * Stake & Est. Returns
        EXPECTED: ![](index.php?/attachments/get/56623629)
        """
        byb_bet_receipt_panel = self.site.byb_bet_receipt_panel
        self.assertEqual(byb_bet_receipt_panel.header.title, tests.settings.betreceipt_title,
                         msg=f'Bet Receipt title: "{byb_bet_receipt_panel.header.title}" doesn\'t match with required '
                             f'"{tests.settings.betreceipt_title}"')
        self.assertTrue(byb_bet_receipt_panel.header.has_close_button(),
                        msg='Bet Receipt header does not have "Close" button')

        bet_receipt_header = byb_bet_receipt_panel.bet_receipt.header
        self.assertEqual(bet_receipt_header.bet_placed_text, vec.betslip.SUCCESS_BET,
                         msg=f'Text "{bet_receipt_header.bet_placed_text}" is not equal to expected '
                             f'"{vec.betslip.SUCCESS_BET}"')
        self.assertTrue(bet_receipt_header.check_icon.is_displayed(), msg='"Check" icon is not displayed')
        self.assertRegex(bet_receipt_header.receipt_datetime, vec.regex.BET_DATA_TIME_FORMAT,
                         msg=f'Bet receipt data and time: "{bet_receipt_header.receipt_datetime}" '
                             f'do not match expected pattern: {vec.regex.BET_DATA_TIME_FORMAT}')

        bet_receipt_selection = byb_bet_receipt_panel.selection
        bet_receipt_content = bet_receipt_selection.content
        selections = bet_receipt_content.outcomes_section.items_as_ordered_dict
        self.assertTrue(selections, msg='No one selection found in Build Your Bet receipt')

        selection_keys = list(selections.keys())
        expected_selection_keys = self.all_selection_names
        self.assertListEqual(selection_keys, expected_selection_keys,
                             msg=f'Incorrect market names.\nActual list: {selection_keys}'
                                 f'\nExpected list: {expected_selection_keys}')

        self.assertTrue(bet_receipt_content.odds, msg='Odds value not found')

        self.assertEqual(bet_receipt_content.bet_id_label, vec.betslip.BET_ID,
                         msg=f'Bet id label text is: "{bet_receipt_content.bet_id_label}" expecting "{vec.betslip.BET_ID}"')
        self.assertTrue(bet_receipt_content.bet_id_value, msg='Bet ID value not found')

        self.assertEqual(bet_receipt_selection.total_stake_label, vec.quickbet.TOTAL_STAKE_LABEL_RECEIPT,
                         msg=f'Total Stake label text is: "{bet_receipt_selection.total_stake_label}", '
                             f'instead of "{vec.quickbet.TOTAL_STAKE_LABEL_RECEIPT}"')
        self.assertIn(self.currency, bet_receipt_selection.total_stake)
        self.assertEqual(float(bet_receipt_selection.total_stake_value), self.bet_amount,
                         msg=f'Actual Total Stake value: "{float(bet_receipt_selection.total_stake_value)}" '
                             f'not match with expected: "{self.bet_amount}"')
        self.assertEqual(bet_receipt_selection.total_est_returns_label, vec.bet_history.TOTAL_RETURN,
                         msg=f'Total Est. Returns label text is: "{bet_receipt_selection.total_est_returns_label}", '
                             f'instead of "{vec.bet_history.TOTAL_RETURN}"')
        self.assertIn(self.currency, bet_receipt_selection.total_est_returns,
                      msg=f'Currency sign "{self.currency}" not found in Total estimate return: '
                          f'"{bet_receipt_selection.total_est_returns}"')
        self.assertTrue(bet_receipt_selection.total_est_returns_value, msg='Total Est. Returns value not found')

    def test_006_click_on_the_x_button(self):
        """
        DESCRIPTION: Click on the "X" button
        EXPECTED: The Quick Bet is closed
        """
        self.site.byb_bet_receipt_panel.header.close_button.click()
        self.assertFalse(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(expected_result=False),
                         msg='Build Your Bet Dashboard is still shown')

    def test_007_click_on_my_bets_button_from_the_header(self):
        """
        DESCRIPTION: Click on My Bets button from the header
        EXPECTED: Check the following data correctness:
        EXPECTED: * Type of bet (for example, BUILD YOUR BET)
        EXPECTED: * Selection & Market name @odds (for example, Match Betting ASTON VILLA, Both Teams to Score YES @4/1)
        EXPECTED: * Build Your Bet
        EXPECTED: * Event name
        EXPECTED: * Time of the event in format HH:MM, DD Month(for example, 10:30, 17 Jan)
        EXPECTED: * The currency is as user set during registration
        EXPECTED: * Stake & Est. Returns
        EXPECTED: * Cashout button (if available)
        EXPECTED: ![](index.php?/attachments/get/56623621)
        """
        self.site.open_my_bets_open_bets()

        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=self.my_bets_single_build_your_bet_title,
            event_names=self.detailed_event_name,
            number_of_bets=1,
            timeout=30)
        self.assertEqual(bet.bet_type, self.my_bets_single_build_your_bet_title,
                         msg=f'Bet type "{bet.bet_type}" is not the same as expected '
                             f'"{self.my_bets_single_build_your_bet_title}"')

        bet_legs = bet.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'No one bet leg was found for bet: "{bet_name}"')
        betleg_name, betleg = list(bet_legs.items())[0]

        expected_outcome_name = ' '.join([' '.join(self.match_betting_market_and_selection_name),
                                         ' '.join(self.both_teams_to_score_market_and_selection_name)])
        expected_outcome_name = sorted(expected_outcome_name.title().lower())

        outcome_name = sorted(' '.join(betleg.byb_selections.items_as_ordered_dict.keys()).lower())
        self.assertEqual(outcome_name, expected_outcome_name,
                         msg=f'Outcome name "{outcome_name}" is not '
                             f'the same as expected "{expected_outcome_name}"')
        odds_sign = betleg.odds_sign.strip('"').strip()
        self.assertEqual(odds_sign, self.expected_odds_sign, msg=f'Odds sign "{odds_sign}" is not equal to expected '
                                                                 f'{self.expected_odds_sign}')
        odds = betleg.odds_value
        self.assertTrue(odds, msg='Odds value is not displayed')
        self.assertEqual(betleg.market_name.upper(), vec.yourcall.DASHBOARD_TITLE,
                         msg=f'Market name "{betleg.market_name.upper()}" is not the same as '
                             f'expected "{vec.yourcall.DASHBOARD_TITLE}"')
        self.assertEqual(betleg.event_name, self.event_name,
                         msg=f'Event name "{betleg.event_name}" is not the same as expected "{self.event_name}"')
        self.assertEqual(betleg.event_time, self.event_start_time_local,
                         msg=f'Event time "{betleg.event_time}" is not the same as expected "{self.event_start_time_local}"')
        self._logger.debug(f'****************** printing betleg.event_time = "{betleg.event_time}"')
        event_time_modified = betleg.event_time
        if self.is_today_event:
            date_string = datetime.now().strftime('%d %b')
            event_hours_and_minutes = betleg.event_time.split(', ')[0]
            event_time_day = betleg.event_time.split(', ')[1].lower()
            if event_time_day == 'today':
                event_time_day = date_string
            event_time_modified = f'{event_hours_and_minutes}, {event_time_day}'
            self._logger.debug(f'****************** printing event_time_modified = "{betleg.event_time}"')
        validate_time(actual_time=f'{event_time_modified}', format_pattern='%H:%M, %d %b')
        self.assertEqual(bet.stake.currency, self.currency,
                         msg=f'Stake currency "{bet.stake.currency}" is not the same '
                             f'as expected "{self.currency}"')
        expected_stake = f'{self.bet_amount:.2f}'
        self.assertEqual(bet.stake.stake_value, expected_stake,
                         msg=f'Stake amount value "{bet.stake.stake_value}" is not the same '
                             f'as expected "{expected_stake}"')

        self.verify_estimated_returns(est_returns=float(bet.est_returns.stake_value),
                                      odds=odds, bet_amount=self.bet_amount)

        self.assertEqual(bet.est_returns.currency, self.currency,
                         msg=f'Est. Returns currency "{bet.est_returns.currency}" is not the same'
                             f' as expected "{self.currency}"')
