import pytest
import tests
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.helpers import normalize_name
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.portal_dependant
@pytest.mark.cash_out
@pytest.mark.desktop
@vtest
class Test_C9608215_Verify_Partial_Cash_Out_History_dropdown(BaseCashOutTest):
    """
    TR_ID: C9608215
    NAME: Verify  'Partial Cash Out History' dropdown
    DESCRIPTION: This test case verifies 'Partial Cash Out History' dropdown and its updates
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Place SINGLE and MULTIPLE bets with cash out available
    PRECONDITIONS: Should be run on:
    PRECONDITIONS: - Open Bets tab
    PRECONDITIONS: - Bet History tab
    PRECONDITIONS: ![](index.php?/attachments/get/33901)
    PRECONDITIONS: ![](index.php?/attachments/get/33902)
    """
    keep_browser_open = True
    bet_amount = 3
    event_name_1 = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get/Create events with cashout available
        DESCRIPTION: Place a single and multiple bet
        """
        if tests.settings.backend_env == 'prod':
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'),\
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         number_of_events=2, additional_filters=cashout_filter)

            event_start_time_local_1 = self.convert_time_to_local(date_time_str=events[0]['event']['startTime'],
                                                                  ob_format_pattern=self.ob_format_pattern, ss_data=True,
                                                                  future_datetime_format=self.event_card_future_time_format_pattern)  # add/remove utcoffset if there is time difference due to DLS
            event_start_time_local_2 = self.convert_time_to_local(date_time_str=events[1]['event']['startTime'],
                                                                  ob_format_pattern=self.ob_format_pattern, ss_data=True,
                                                                  future_datetime_format=self.event_card_future_time_format_pattern)  # add/remove utcoffset if there is time difference due to DLS

            self.__class__.event_name_1 = f"{normalize_name(events[0]['event']['name'])} {event_start_time_local_1}"
            self.__class__.event_name_2 = f"{normalize_name(events[1]['event']['name'])} {event_start_time_local_2}"
            outcomes_1 = next(((market['market']['children']) for market in events[0]['event']['children'] if
                               market['market'].get('children')), None)
            outcomes_2 = next(((market['market']['children']) for market in events[1]['event']['children'] if
                               market['market'].get('children')), None)
            selection_1 = [i['outcome']['id'] for i in outcomes_1][0]
            selection_2 = [i['outcome']['id'] for i in outcomes_2][0]
            selection_ids = [selection_1, selection_2]
        else:
            events_params = self.create_several_autotest_premier_league_football_events(number_of_events=2)
            self.__class__.event_name_1 = '%s %s' % (events_params[0].event_name, events_params[0].local_start_time)
            self.__class__.event_name_2 = '%s %s' % (events_params[1].event_name, events_params[1].local_start_time)
            selection_ids = [event_params.selection_ids[event_params.team1] for event_params in events_params]

        self.site.login()
        self.open_betslip_with_selections(selection_ids=selection_ids)
        sections = self.get_betslip_sections().Singles
        selection1 = list(sections.values())[0]
        selection1.amount_form.enter_amount(value=self.bet_amount)
        self.place_multiple_bet()
        self.site.bet_receipt.footer.click_done()
        self.site.wait_content_state('HomePage')

    def test_001_navigate_to_my_betsopen_betsbet_historymake_partial_cash_out_for_single_betverify_partial_cash_out_history_dropdown(self, cashed_out_second_time=False, event_names=event_name_1, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE):
        """
        DESCRIPTION: Navigate to My Bets>Open Bets/Bet History
        DESCRIPTION: Make partial cash out for SINGLE bet
        DESCRIPTION: Verify Partial Cash Out History' dropdown
        EXPECTED: - 'Partial cashout successful' message is displayed below the cashout button
        EXPECTED: - 'Partial Cash Out History' dropdown appears with partial cash out data in the table after refresh or navigating back to the page (when success message is not shown)
        """
        self.site.open_my_bets_open_bets()
        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            event_names=event_names, bet_type=bet_type)
        bet.scroll_to()
        self.assertTrue(bet.buttons_panel.has_partial_cashout_button(), msg=f'PARTIAL CASHOUT button is not present for'
                                                                            f'"{bet_name}"')
        bet.buttons_panel.partial_cashout_button.click()
        self.assertTrue(bet.buttons_panel.wait_for_cashout_slider(), msg='PARTIAL CASHOUT slider has not appeared')
        bet.buttons_panel.partial_cashout_button.click()
        bet.buttons_panel.cashout_button.click()
        expected_message = vec.bet_history.PARTIAL_CASH_OUT_SUCCESS
        self.assertTrue(bet.wait_for_message(message=expected_message, timeout=20),
                        msg=f'Message "{expected_message}" is not shown')
        self.device.refresh_page()
        if self.device_type != 'mobile':
            self.site.open_my_bets_open_bets()
        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            event_names=event_names, bet_type=bet_type)
        bet.scroll_to()
        self.assertTrue(bet.partial_cash_out_history.is_displayed(),
                        msg='"Partial Cash Out History" section not displayed')
        bet.partial_cash_out_history.header.click()
        self.assertTrue(bet.partial_cash_out_history.has_content(),
                        msg='"Partial Cash Out History" content not found')
        table = bet.partial_cash_out_history.content.table
        if cashed_out_second_time:
            number_of_rows = list(table.items_as_ordered_dict.keys())
            self.assertEqual(len(number_of_rows), 2, msg='rows in the table are not updated')
        self.assertTrue(table.stake_used_label,
                        msg='"Stake Used" label not found in Partial Cash Out History table')
        self.assertTrue(table.cash_out_amount_label,
                        msg='"Cash Out Amount" label not found in Partial Cash Out History table')
        self.assertTrue(table.data_time_label,
                        msg='"Date/Time" label not found in Partial Cash Out History table')

    def test_002_make_partial_cash_out_one_more_time_for_single_betverify_that__new_data_is_added_to_partial_cash_out_history_dropdown(self):
        """
        DESCRIPTION: Make Partial cash out one more time for SINGLE bet
        DESCRIPTION: Verify that ' new data is added to 'Partial Cash Out History' dropdown
        EXPECTED: - 'Partial cashout successful' message is displayed below the cashout button
        EXPECTED: - After the message is no longer displayed a new row with partial cashout date is added to 'Partial Cash Out History' table
        """
        self.test_001_navigate_to_my_betsopen_betsbet_historymake_partial_cash_out_for_single_betverify_partial_cash_out_history_dropdown(cashed_out_second_time=True)

    def test_003_make_partial_cash_out_for_multiple_betverify_that_partial_cash_out_history_dropdown_appears(self):
        """
        DESCRIPTION: Make partial cash out for MULTIPLE bet
        DESCRIPTION: Verify that Partial Cash Out History' dropdown appears
        EXPECTED: 'Partial Cash Out History' dropdown appears with partial cash out data in the table (when the success message is no longer displayed - after refresh)
        """
        self.test_001_navigate_to_my_betsopen_betsbet_historymake_partial_cash_out_for_single_betverify_partial_cash_out_history_dropdown(event_names=[self.event_name_1, self.event_name_2], bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE)

    def test_004_make_partial_cash_out_one_more_time_for_multiple_betverify_that__new_data_is_added_to_partial_cash_out_history_dropdown(self):
        """
        DESCRIPTION: Make Partial cash out one more time for MULTIPLE bet
        DESCRIPTION: Verify that ' new data is added to 'Partial Cash Out History' dropdown
        EXPECTED: A new row with partial cash out date is added to 'Partial Cash Out History' table (when the success message is no longer displayed - after refresh)
        """
        self.test_001_navigate_to_my_betsopen_betsbet_historymake_partial_cash_out_for_single_betverify_partial_cash_out_history_dropdown(event_names=[self.event_name_1, self.event_name_2], bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE, cashed_out_second_time=True)
