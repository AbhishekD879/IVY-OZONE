import pytest
from crlat_ob_client.utils.date_time import validate_time

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name


@pytest.mark.hl
@pytest.mark.prod
# @pytest.mark.tst2  # disabled Partial Cashout tests on TST2/STG2 endpoints
# @pytest.mark.stg2  # due to offers constantly granted to user that prevents partial cashout appearance
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.bet_placement
@pytest.mark.open_bets
@pytest.mark.cash_out
@pytest.mark.portal_dependant
@pytest.mark.currency
@pytest.mark.bet_history_open_bets
@pytest.mark.slow
@pytest.mark.login
@vtest
class Test_C29213_Verify_Partial_Cash_Out_History_section_for_Single_Bet_on_Open_Bets_Settled_Bets(BaseCashOutTest):
    """
    TR_ID: C29213
    NAME: Verify 'Partial Cash Out History' section for Single Bet on Open Bets/Settled Bets
    DESCRIPTION: This test case verifies 'Partial Cash Out History' section of 'Regular' bets.
    DESCRIPTION: AUTOTEST [C41790483]
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. User has 'Pending' bets with available Partial Cash Out option
    PRECONDITIONS: 3. User has already made Partial Cash Out
    """
    keep_browser_open = True
    bet_amount = 1.0
    currency = '£'
    total_cashout_amount = 0.0
    cashout_amount = 0.0
    expected_total_cash_out_stake = 0.0

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login as Oxygen user, create test event, add selections with deep link and place single bets
        """
        username = tests.settings.betplacement_user
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,all_available_events=True)
            for event in events:
                event_start_time_local = self.convert_time_to_local(date_time_str=event['event']['startTime'],
                                                                    ob_format_pattern=self.ob_format_pattern, ss_data=True,
                                                                    future_datetime_format=self.event_card_future_time_format_pattern)
                self.__class__.event_name = f"{normalize_name(event['event']['name'])} {event_start_time_local}"

                outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                                 market['market'].get('children')), None)
                if outcomes is None:
                    raise SiteServeException('There are no available outcomes')
                # outcomeMeaningMinorCode: A - away, H - home, D - draw
                team1 = next((outcome['outcome']['name'] for outcome in outcomes if
                              outcome['outcome'].get('outcomeMeaningMinorCode') and
                              outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
                if team1:
                    break
            if not team1:
                raise SiteServeException('No Home team found')

            selections_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}.get(team1)

            self._logger.info(f'*** Found event "{self.event_name}" with selections {selections_ids}')
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.event_name = '%s v %s %s' % (event_params.team1, event_params.team2,
                                                        self.convert_time_to_local(date_time_str=event_params.event_date_time))
            selections_ids = event_params.selection_ids[event_params.team1]

        self.site.login(username=username)
        self.open_betslip_with_selections(selection_ids=selections_ids)
        self.place_single_bet()
        self.site.bet_receipt.footer.click_done()
        self.site.wait_content_state('HomePage')

    def test_001_go_to_my_bets(self):
        """
        DESCRIPTION: Tap on 'My Bets' item on Top Menu
        """
        self.site.open_my_bets_cashout()

    def test_002_do_partial_cash_out(self):
        """
        DESCRIPTION: Do partial cash out for placed bet in step 1
        """
        bet_name, bet = self.site.cashout.tab_content.accordions_list.get_bet(
            event_names=self.event_name, bet_type='SINGLE', number_of_bets=1)
        bet.buttons_panel.partial_cashout_button.click()
        bet.buttons_panel.wait_for_cashout_slider()
        self.__class__.cashout_amount = '{0:.2f}'.format(float(bet.buttons_panel.partial_cashout_button.amount.value))
        self.__class__.total_cashout_amount = '{0:.2f}'.format(float(self.total_cashout_amount) + float(self.cashout_amount))
        bet.buttons_panel.partial_cashout_button.click()
        bet.buttons_panel.wait_for_cashout_button(timeout=5)
        bet.buttons_panel.cashout_button.click()
        expected_message = vec.bet_history.PARTIAL_CASH_OUT_SUCCESS
        self.assertTrue(bet.wait_for_message(message=expected_message, timeout=20),
                        msg=f'Message "{expected_message}" is not shown')

    def test_003_tap_open_bets_tab(self):
        """
        DESCRIPTION: Tap 'Open Bets' tab
        """
        system_config = self.get_initial_data_system_configuration()
        cashout_cms = system_config.get('CashOut')
        if not cashout_cms:
            cashout_cms = self.cms_config.get_system_configuration_item('CashOut')
        if not cashout_cms:
            raise CmsClientException('CashOut section not found in System Configuration')
        is_cashout_tab_enabled = cashout_cms.get('isCashOutTabEnabled')
        if is_cashout_tab_enabled:
            self.site.open_my_bets_open_bets()
        else:
            self.site.open_my_bets_settled_bets()
            self.site.open_my_bets_open_bets()

    def test_004_verify_partial_cash_out_history_section(self):
        """
        DESCRIPTION: Verify 'Partial Cash Out History' section presence for Single bet
        EXPECTED: 'Partial Cash Out History' section is displayed above the 'Total Estimated Returns' field
        EXPECTED: Section is collapsed by default
        """
        bet_name, self.__class__.bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            event_names=self.event_name, bet_type='SINGLE', number_of_bets=1)
        self.assertTrue(self.bet.partial_cash_out_history.is_displayed(),
                        msg='"Partial Cash Out History" section not displayed')
        self.assertFalse(self.bet.partial_cash_out_history.header.is_selected(expected_result=False),
                         msg='"Partial Cash Out History" section header is active')
        self.assertFalse(self.bet.partial_cash_out_history.has_content(expected_result=False),
                         msg='"Partial Cash Out History" section not collapsed by default')

    def test_005_verify_stake_value(self):
        """
        DESCRIPTION: Verify Stake value
        EXPECTED: Stake value corresponds to **stake.value **(from the core of 'accountHistory' response)
        EXPECTED: Stake is displayed next to the 'Stake' field in format: '<currency symbol> X.XX'
        """
        self.__class__.expected_stake_amount = '{0:.2f}'.format(self.bet_amount / 2)
        self.assertEqual(self.bet.stake.currency, self.currency,
                         msg=f'Current Stake currency: "{self.bet.stake.currency}", expected: "{self.currency}"')
        self.assertEqual(self.bet.stake.stake_value, self.expected_stake_amount,
                         msg=f'Current Stake value: "{self.bet.stake.stake_value}", '
                             f'expected: "{self.expected_stake_amount}"')

    def test_006_verify_partial_cash_out_history_section_content(self):
        """
        DESCRIPTION: Verify 'Partial Cash Out History' section content
        EXPECTED: 'Partial Cash Out History' section contains:
        EXPECTED: - Table with 'Stake Used', 'Cash Out Amount' and 'Date/Time' values
        EXPECTED: - 'Remaining Stake', 'Total Cashed Out' and 'Total Cashed Out Stake' fields and corresponding values
        """
        # Expand 'Partial Cash Out History' section
        self.bet.partial_cash_out_history.header.click()
        bet_name, self.__class__.bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            event_names=self.event_name, bet_type='SINGLE', number_of_bets=1)
        self.assertTrue(self.bet.partial_cash_out_history.has_content(),
                        msg='"Partial Cash Out History" content not found')
        content = self.bet.partial_cash_out_history.content
        self.__class__.table = content.table
        # Table with 'Stake Used', 'Cash Out Amount' and 'Date/Time' values
        self.assertTrue(self.table.stake_used_label,
                        msg='"Stake Used" label not found in Partial Cash Out History table')
        self.assertTrue(self.table.cash_out_amount_label,
                        msg='"Cash Out Amount" label not found in Partial Cash Out History table')
        self.assertTrue(self.table.data_time_label,
                        msg='"Date/Time" label not found in Partial Cash Out History table')
        # 'Remaining Stake', 'Total Cashed Out' and 'Total Cashed Out Stake' fields and corresponding values
        self.assertTrue(content.remaining_stake.label,
                        msg='"Remaining Stake" label not found in Partial Cash Out History content')
        self.assertEqual(content.remaining_stake.value.amount, self.expected_stake_amount,
                         msg='"Remaining Stake" value: "%s", expected: "%s"'
                             % (content.remaining_stake.value.amount, self.expected_stake_amount))
        self.assertEqual(content.remaining_stake.value.currency, self.currency,
                         msg='"Remaining Stake" currency: "%s", expected: "%s"'
                             % (content.remaining_stake.value.currency, self.currency))
        self.assertTrue(content.total_cash_out.label,
                        msg='"Total Cashed Out" label not found in Partial Cash Out History content')
        self.assertEqual(content.total_cash_out.value.amount, self.total_cashout_amount,
                         msg='"Total Cashed Out" value: "%s", expected: "%s"'
                             % (content.total_cash_out.value.amount, self.total_cashout_amount))
        self.assertEqual(content.total_cash_out.value.currency, self.currency,
                         msg='"Total Cashed Out" currency: "%s", expected: "%s"'
                             % (content.total_cash_out.value.currency, self.currency))
        self.assertTrue(content.total_cash_out_stake.label,
                        msg='"Total Cashed Out Stake" label not found in Partial Cash Out History content')
        self.__class__.expected_total_cash_out_stake = '{0:.2f}'.format(float(self.expected_total_cash_out_stake) + float(self.expected_stake_amount))
        self.assertEqual(content.total_cash_out_stake.value.amount, self.expected_total_cash_out_stake,
                         msg='"Total Cashed Out Stake" value: "%s", expected: "%s"'
                             % (content.total_cash_out_stake.value.amount, self.expected_total_cash_out_stake))
        self.assertEqual(content.total_cash_out_stake.value.currency, self.currency,
                         msg='"Total Cashed Out Stake" currency: "%s", expected: "%s"'
                             % (content.total_cash_out_stake.value.currency, self.currency))

    def test_007_verify_correctness_of_table_data(self, num_of_partial_cash_outs=1):
        """
        DESCRIPTION: Verify correctness of table data
        EXPECTED: Stake Used = number of line in table betTermsChange [i-1].stake.value - betTermsChange[i].stake.value (value is shown in format:  '<currency symbol> XX.XX')
        EXPECTED: Cash Out Amount = amount of partial cash out. Corresponds to ****betTermsChange.**cashoutValue** attribute and is shown in format:  '<currency symbol> XX.XX'
        EXPECTED: Date/Time - time of partial cash out transaction. Corresponds to **betTermsChange.cashoutDate** value. Is shown in format: YYYY-MM-DD HH:MM:SS
        """
        table_lines = self.table.items_as_ordered_dict
        self.assertEqual(len(table_lines), num_of_partial_cash_outs,
                         msg='Number of lines in table: %s, expected: %s'
                             % (len(table_lines), num_of_partial_cash_outs))
        table_line_name, table_line = list(table_lines.items())[num_of_partial_cash_outs - 1]
        expected_stake_used = '{0:.2f}'.format(self.bet_amount - float(self.expected_stake_amount))
        self.assertEqual(table_line.stake_used.value, expected_stake_used,
                         msg='Stake Used value: "%s", expected: "%s"'
                             % (table_line.stake_used.value, expected_stake_used))
        self.assertEqual(table_line.stake_used.currency, self.currency,
                         msg='Stake Used currency: "%s", expected: "%s"'
                             % (table_line.stake_used.currency, self.currency))
        self.assertEqual(table_line.cash_out_amount.value, self.cashout_amount,
                         msg='Cash Out Amount value: "%s", expected: "%s"'
                             % (table_line.cash_out_amount.value, self.cashout_amount))
        self.assertEqual(table_line.cash_out_amount.currency, self.currency,
                         msg='Cash Out Amount currency: "%s", expected: "%s"'
                             % (table_line.cash_out_amount.currency, self.currency))
        validate = None
        format_pattern = '%d.%m.%Y, %H:%M %p'
        time = table_line.data_time.name
        try:
            validate = validate_time(actual_time=time, format_pattern=format_pattern)
        except Exception:
            pass
        self.assertTrue(validate, msg=f'"{time}" does not match pattern "{format_pattern}"')

    def test_008_go_to_cash_out_tab_and_do_one_more_partial_cash_out_of_tested_bet(self):
        """
        DESCRIPTION: Go to 'Cash Out' tab, make Partial Cash out of desired value
        EXPECTED: Partial Cash Out transaction has been successful
        """
        self.site.open_my_bets_cashout()

        self.__class__.bet_amount = self.bet_amount / 2
        self.test_002_do_partial_cash_out()

    def test_009_verify_bet_on_open_bets_tab(self):
        """
        DESCRIPTION: Go to the verified bet on the 'Open Bets' tab
        EXPECTED: Table within 'Partial Cash Out History' section is increased by one row
        """
        self.test_003_tap_open_bets_tab()
        self.test_004_verify_partial_cash_out_history_section()
        self.test_005_verify_stake_value()
        self.test_006_verify_partial_cash_out_history_section_content()
        self.test_007_verify_correctness_of_table_data(num_of_partial_cash_outs=2)
