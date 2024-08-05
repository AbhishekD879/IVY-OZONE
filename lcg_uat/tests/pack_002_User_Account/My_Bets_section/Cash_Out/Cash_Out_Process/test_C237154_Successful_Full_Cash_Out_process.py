import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.bet_placement
@pytest.mark.cash_out
@pytest.mark.portal_dependant
@pytest.mark.desktop
@pytest.mark.critical
@pytest.mark.pipelines
@pytest.mark.safari
@pytest.mark.login
@pytest.mark.reg167_fix
@vtest
class Test_C237154_Successful_Full_Cash_Out_process(BaseCashOutTest, BaseUserAccountTest):
    """
    TR_ID: C237154
    NAME: Successful Full Cash Out process
    DESCRIPTION: This test case verifies successful Full Cash Out process on 'Cash Out' tab
    DESCRIPTION: DESIGNS (available from OX 99):
    DESCRIPTION: Ladbrokes: https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b/screen/5c4f1ce639594ebeef05d0cc
    DESCRIPTION: Coral: https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3/screen/5c4f09b1d2815d60d0789631
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User has placed Singles and Multiple bets where Cash Out offer is available
    PRECONDITIONS: **CORAL**
    PRECONDITIONS: Delay for Singles and Multiple bets is set in the backoffice/admin -> Miscellaneous -> Openbet Config -> All Configuration groups -> CASHOUT_SINGLE_DELAY / CASHOUT_MULTI_DELAY
    PRECONDITIONS: Configurable Cashout values are used in "cashoutDelay" attribute in 'cashoutBet' response
    PRECONDITIONS: **Ladbrokes**
    PRECONDITIONS: Cashout values are used in "cashoutDelay" attribute in 'cashoutBet' response, the calculation is based on the BIR delay in the event (pre-play bets won't be a cashout delay, use only In-Play events for testing Timer, (Timer is available from OX 99))
    PRECONDITIONS: The highest set 'BIR Delay' value is used for Multiples In-play events
    PRECONDITIONS: Note: Readbet request/response is sent after successful full cashout of in-play events.
    PRECONDITIONS: CashoutBet request/response is sent after successful full cashout of pre-match events. (Currently works as for in-play events)
    PRECONDITIONS: **Currently CASH OUT option is available on back-end for Football, Tennis, Darts and Snooker (other sports will be added in future).**
    """
    keep_browser_open = True
    bet_names = None
    number_of_events = 2
    expected_user_balance = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Create test football event, PROD: Find active Football events
        DESCRIPTION: Automation Note: As we cannot get cashoutDelay value, we will not check timer so test will be done on Prematch events
        DESCRIPTION: Login as user that has funds to place a bet
        DESCRIPTION: Place bets
        """
        if tests.settings.backend_env == 'prod':
            found_events, all_selection_ids_both_events, found_events_start_times, teams = [], [], [], []
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         all_available_events=True,
                                                         additional_filters=cashout_filter)
            if len(events) < self.number_of_events:
                raise SiteServeException(f'Not enough events found, needed "{self.number_of_events}" Football '
                                         f'events with cashout available, but found "{self.number_of_events}"')
            for event in events:
                if len(found_events) >= self.number_of_events:
                    break
                event_id = event['event']['id']

                match_result_market = next((market['market'] for market in event['event']['children'] if
                                            market.get('market').get('templateMarketName') == 'Match Betting'), None)
                if not match_result_market:
                    continue
                outcomes = match_result_market['children']
                team = next((outcome['outcome']['name'] for outcome in outcomes if
                             outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
                if not team:
                    continue
                created_event_name = normalize_name(event['event']['name'])

                selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
                if not selection_ids:
                    continue

                start_time_local = self.convert_time_to_local(date_time_str=event['event']['startTime'],
                                                              ob_format_pattern=self.ob_format_pattern,
                                                              future_datetime_format=self.event_card_future_time_format_pattern,
                                                              ss_data=True)
                found_events.append(created_event_name)
                all_selection_ids_both_events.append(selection_ids)
                found_events_start_times.append(start_time_local)
                teams.append(team)

                self._logger.info(
                    f'*** Found Event "{created_event_name}" start time "{start_time_local}" with id "{event_id}". '
                    f'Team name is "{team}" with selection ids {selection_ids}')

            self.__class__.created_event_name, self.__class__.created_event_2_name = found_events
            start_time_local, start_time_local2 = found_events_start_times
            selection_ids, selection_ids2 = all_selection_ids_both_events
            self.__class__.team1, self.__class__.team2 = teams
            self.__class__.single_bet_name = f'{self.created_event_name} {start_time_local}'
            self.__class__.double_bet_name = f'{self.created_event_name} {start_time_local}, ' \
                                             f'{self.created_event_2_name} {start_time_local2}'
            selection_ids_both_events = [selection_ids[self.team1], selection_ids2[self.team2]]

        else:
            events = self.create_several_autotest_premier_league_football_events(number_of_events=self.number_of_events)
            start_time_local, start_time_local2 = events[0].local_start_time, events[1].local_start_time
            self.__class__.single_bet_name = f'{events[0].event_name} {start_time_local}'
            self.__class__.double_bet_name = f'{events[0].event_name} {start_time_local},' \
                                             f' {events[1].event_name} {start_time_local2}'
            selection_ids_both_events = [event.selection_ids[event.team1] for event in events]

        username = tests.settings.betplacement_user
        self.site.login(username=username, timeout=15)
        self.open_betslip_with_selections(selection_ids=selection_ids_both_events)
        self.place_bet_on_all_available_stakes()

        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

    def test_001_navigate_to_cash_out_tab_on_my_bets(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: 'Cash Out' tab is opened
        """
        self.site.open_my_bets_cashout()

    def test_002_go_to_single_cash_out_bet_line(self, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=None):
        """
        DESCRIPTION: Go to **Single** Cash Out bet line
        """
        event_names = self.single_bet_name if event_names is None else event_names
        self.__class__.user_balance = self.site.header.user_balance
        self.__class__.bet_name, self.__class__.bet = self.site.cashout.tab_content.accordions_list. \
            get_bet(event_names=event_names, bet_type=bet_type, number_of_bets=5)

    def test_003_tap_cash_out_button(self):
        """
        DESCRIPTION: Tap 'CASH OUT' button
        DESCRIPTION: Verify that green 'CONFIRM CASH OUT' button is shown
        EXPECTED: 'CONFIRM CASH OUT' button is shown
        """
        self.__class__.cashout_amount = float(self.bet.buttons_panel.full_cashout_button.amount.value)
        self.bet.buttons_panel.full_cashout_button.click()

        confirmation_text = self.bet.buttons_panel.cashout_button.name
        expected_confirmation = vec.bet_history.CASHOUT_BET.confirm_cash_out + ' £{0:.2f}'.format(self.cashout_amount)
        self.assertEqual(expected_confirmation, confirmation_text,
                         msg=f'Expected confirmation text: "{expected_confirmation}" '
                             f'is not equal to actual: "{confirmation_text}"')

    def test_004_trigger_happy_cash_out_path_and_tap_confirm_cash_out_button(self):
        """
        DESCRIPTION: Trigger happy cash out path (e.g. cash out value remains unchanged)
        DESCRIPTION: Tap 'CONFIRM CASH OUT' button
        EXPECTED: Spinner with count down timer (Timer is available from OX 99) in format XX:XX (countdown timer is
        EXPECTED:  taken from 'cashoutBet' response: 'cashoutDelay attribute value) appears on the button instead of the text 'CONFIRM CASH OUT'
        """
        wait_for_result(lambda: self.bet.buttons_panel.full_cashout_button.is_displayed(),
                        timeout=5,
                        name='Confirmation text to disappear')

        self.__class__.start_stake = 'N/A' if self.bet.stake.stake_value == 'N/A' else float(self.bet.stake.stake_value)
        self.__class__.start_est_returns_amount = 'N/A' if self.bet.est_returns.stake_value == 'N/A' else float(str(self.bet.est_returns.stake_value).replace(',', ''))

        self.bet.buttons_panel.full_cashout_button.click()
        self.bet.buttons_panel.cashout_button.click()

        """ imho we cannot automate wait for timer and spinner - sometimes cashoutDelay is too low"""
        # TODO VOL-5375
        # result = self.bet.buttons_panel._spinner_wait(expected_result=True, timeout=2)
        # self.assertTrue(result, msg='Spinner not found')
        #
        # if self.bet.buttons_panel.has_timer():
        #     pattern = re.compile("\d{2}:\d{2}")
        #     result_timer = wait_for_result(lambda: bool(pattern.match(self.bet.buttons_panel.timer.text)),
        #                                    name='Countdown timer to have expected format XX:XX',
        #                                    timeout=5)
        #     self.assertTrue(result_timer, msg='Timer not found')

    def test_005_wait_until_button_with_spinner_and_countdown_timer_disappears(self):
        """
        DESCRIPTION: Wait until button with spinner and count down timer  (Timer is available from OX 99) disappears
        EXPECTED: * 'Cashed out' label is displayed ath the top right corner on the header
        EXPECTED: *  Green "tick" in a circle and message "You cashed out <currency> <value>" is shown below the header
        EXPECTED: * Message "Cashout Successfully" with the green tick at the beginning are shown instead of 'cashout' button at the bottom of bet line
        """
        result = self.bet.buttons_panel._spinner_wait(expected_result=False, timeout=25)
        self.assertFalse(result, msg='Spinner still present')

        self.assertTrue(self.bet.has_cashed_out_mark(),
                        msg=f'"{vec.betslip.CASHOUT_STAKE}" mark is not present on Cashout page after cashout')
        # actual_status = self.bet.bet_status
        # expected_status = vec.betslip.CASHOUT_STAKE
        # self.assertEquals(actual_status, expected_status,
        #                   msg=f'Actual bet status: "{actual_status}" is not "{expected_status}"')
        actual_cashed_out_message = f'{self.bet.cashed_out_message.text} {self.bet.cashed_out_value.text}'
        expected_cashed_out_message = vec.bet_history.CASHED_OUT_LABEL.format(self.cashout_amount)
        self.assertEquals(actual_cashed_out_message, expected_cashed_out_message,
                          msg=f'Actual cashed out message: "{actual_cashed_out_message}" '
                              f'is not equal to expected: "{expected_cashed_out_message}"')

        result = wait_for_result(lambda: self.bet.cash_out_successful_icon.is_displayed(),
                                 timeout=2,
                                 name='Cash Out Successful icon to appear')
        self.assertTrue(result,
                        msg=f'Green "tick" near {vec.bet_history.FULL_CASH_OUT_SUCCESS} for {self.bet_name} have not appeared')

        self.assertTrue(self.bet.wait_for_message(message=vec.bet_history.FULL_CASH_OUT_SUCCESS, timeout=20),
                        msg=f'Message "{vec.bet_history.FULL_CASH_OUT_SUCCESS}" is not shown')

        wait_for_result(lambda: self.site.header.user_balance != self.user_balance,
                        timeout=10,
                        name='user balance to be changed')  # w/a to give more time for balance update

    def test_006_refresh_the_page_or_navigate_to_other_page_and_back(self, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
                                                                     event_names=None):
        """
        DESCRIPTION: Refresh the page (or navigate to other page and back)
        DESCRIPTION: Verify success message
        EXPECTED: The success message and bet are no longer displayed
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        if self.device_type != 'mobile':
            self.site.wait_content_state('Homepage', timeout=30)
            self.site.open_my_bets_cashout()
        event_names = self.single_bet_name if event_names is None else event_names
        bet_name, _ = self.site.cashout.tab_content.accordions_list.get_bet(event_names=event_names,
                                                                            bet_type=bet_type,
                                                                            raise_exceptions=False,
                                                                            number_of_bets=2)
        self.assertFalse(bet_name, msg=f'"{bet_name}" bet is present on Cashout page. It should not.')

    def test_007_verify_user_balance(self):
        """
        DESCRIPTION: Verify user balance
        EXPECTED: User balance is increased on full cash out value
        """
        self.verify_user_balance(expected_user_balance=float(self.user_balance) + float(self.cashout_amount),
                                 timeout=10)
        self.__class__.user_balance = float(self.user_balance) + float(self.cashout_amount)

    def test_008_go_to_multiple_cash_out_bet_lines(self):
        """
        DESCRIPTION: Go to **Multiple** Cash Out bet lines
        """
        self.test_002_go_to_single_cash_out_bet_line(bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE,
                                                     event_names=self.double_bet_name)

    def test_009_repeat_steps_3_7_for_multiple_cash_out_bet_lines(self):
        """
        DESCRIPTION: Repeat steps №3-7 for **Multiple** Cash Out bet lines
        """
        self.test_003_tap_cash_out_button()
        self.test_004_trigger_happy_cash_out_path_and_tap_confirm_cash_out_button()
        self.test_005_wait_until_button_with_spinner_and_countdown_timer_disappears()
        self.test_006_refresh_the_page_or_navigate_to_other_page_and_back(bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE,
                                                                          event_names=self.double_bet_name)
        self.test_007_verify_user_balance()
