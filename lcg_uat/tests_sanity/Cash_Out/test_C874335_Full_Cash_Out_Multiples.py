import pytest
import tests
import voltron.environments.constants as vec
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.critical
@pytest.mark.cash_out
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.login
@pytest.mark.safari
@pytest.mark.hotfix
@pytest.mark.sanity
@vtest
class Test_C874335_Full_Cash_Out_Multiples(BaseCashOutTest, BaseUserAccountTest):
    """
    TR_ID: C874335
    NAME: Full Cash Out Multiples
    DESCRIPTION: Verify that the customer can perform a Full Cash Out (check balance and Bet History)
    DESCRIPTION: AUTOTEST [C48531944]
    """
    keep_browser_open = True
    number_of_events = 2

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login
        DESCRIPTION: * Place a multiple bet on any Pre-Match or In-Play events that have Cashout option
        """
        if tests.settings.backend_env == 'prod':
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'),\
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         number_of_events=self.number_of_events,
                                                         additional_filters=cashout_filter)
            # Event 1
            self.__class__.eventID = events[0]['event']['id']

            self.__class__.match_result_market = next((market['market'] for market in events[0]['event']['children'] if
                                                       market.get('market').get('templateMarketName') == 'Match Betting' and
                                                       market['market'].get('children')), None)
            if not self.match_result_market:
                raise SiteServeException(f'Event {self.eventID} does not have Match Result Market')
            outcomes = self.match_result_market['children']
            self.__class__.team1 = next((outcome['outcome']['name'].replace("(","").replace(")","") for outcome in outcomes if
                                         outcome['outcome'].get('outcomeMeaningMinorCode') and
                                         outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            if not self.team1:
                raise SiteServeException('No Home team present is SS response')
            self.__class__.created_event_name = normalize_name(events[0]['event']['name'])

            selection_ids = {i['outcome']['name'].replace("(","").replace(")",""): i['outcome']['id'] for i in outcomes}
            if not selection_ids:
                raise SiteServeException(f'Outcomes list is empty for event "{self.eventID}" "{self.created_event_name}"')

            self._logger.info(
                f'*** Found Event 1 "{self.created_event_name} with id "{self.eventID}". Team name is "{self.team1}" selection ids {selection_ids}')

            # Event 2
            self.__class__.eventID_2 = events[1]['event']['id']
            match_result_market = next((market['market'] for market in events[1]['event']['children'] if
                                        market.get('market').get('templateMarketName') == 'Match Betting' and
                                        market['market'].get('children')), None)
            if not match_result_market:
                raise SiteServeException(f'Event {self.eventID} does not have Match Result Market')
            outcomes_2 = match_result_market['children']
            self.__class__.team2 = next((outcome['outcome']['name'].replace("(","").replace(")","") for outcome in outcomes_2 if
                                         outcome['outcome'].get('outcomeMeaningMinorCode') and
                                         outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            if not self.team2:
                raise SiteServeException('No Home team present is SS response')

            self.__class__.created_event_2_name = normalize_name(events[1]['event']['name'])

            selection_ids2 = {i['outcome']['name']: i['outcome']['id'] for i in outcomes_2}
            if not selection_ids2:
                raise SiteServeException(f'Outcomes list is empty for event "{self.eventID_2}" "{self.created_event_2_name}"')
            utcoffset = -330 if self.device_type == 'mobile' and self.use_browser_stack else 60
            event1_start_time = self.convert_time_to_local(ob_format_pattern=self.ob_format_pattern,
                                                           future_datetime_format=self.event_card_future_time_format_pattern,
                                                           ss_data=True,
                                                           date_time_str=events[0]["event"]["startTime"],
                                                           utcoffset=utcoffset)
            event2_start_time = self.convert_time_to_local(ob_format_pattern=self.ob_format_pattern,
                                                           future_datetime_format=self.event_card_future_time_format_pattern,
                                                           ss_data=True,
                                                           date_time_str=events[1]["event"]["startTime"],
                                                           utcoffset=utcoffset)

            self.__class__.double_bet_name = \
                f'{vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE} - [{self.created_event_name} {event1_start_time}, ' \
                f'{self.created_event_2_name} {event2_start_time}]'
            selection_ids_both_events = [selection_ids[self.team1], selection_ids2[self.team2]]

            self._logger.info(
                f'*** Found Event 2 "{self.created_event_2_name} with id "{self.eventID_2}". Team name is "{self.team2}" selection ids {selection_ids2}')
        else:
            events = self.create_several_autotest_premier_league_football_events(number_of_events=self.number_of_events,
                                                                                 bir_delay=10, is_live=True)
            self.__class__.double_bet_name = f'{vec.betslip.DBL.upper()} - [{events[0].event_name}, {events[1].event_name}]'
            self.__class__.created_event_name = events[0].event_name
            self.__class__.match_result_market = self.expected_market_sections.match_result.title()
            self.__class__.team1 = events[0].team1
            self.__class__.team2 = events[1].team2
            selection_ids_both_events = [event.selection_ids[event.team1] for event in events]

        username = tests.settings.betplacement_user
        self.site.login(username=username, timeout=15)
        self.open_betslip_with_selections(selection_ids=selection_ids_both_events)
        self.place_multiple_bet(number_of_stakes=1)

        self.check_bet_receipt_is_displayed()

        betreceipt_section = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertEqual(len(betreceipt_section), 1, msg='There is more than one item in Bet Receipt')
        for section_name, section in betreceipt_section.items():
            self.__class__.bet_id = section.bet_id
        self.site.bet_receipt.footer.click_done()

    def test_001_navigate_to_cash_out_tab_for_coral_brand_or_open_bets_tab_for_ladbrokes_brand(self):
        """
        DESCRIPTION: Navigate to 'Cash Out' tab for **Coral** brand
        DESCRIPTION: or 'Open Bets' tab for **Ladbrokes** brand
        EXPECTED: * 'Cash Out'/'Open Bets' tab is loaded
        EXPECTED: * A list with COMB eligible bets is displayed
        EXPECTED: * **Verify that the event time in the cashout tab is the same as on the "In-Play" page**
        EXPECTED: * The currency is as per user registration setting
        """
        self.site.open_my_bets_cashout()

        self.__class__.user_balance = self.site.header.user_balance
        self.__class__.bet_name, self.__class__.bet = self.site.cashout.tab_content.accordions_list. \
            get_bet(event_names=self.double_bet_name, bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE,
                    number_of_bets=4)

        self.verify_cashout_currency_symbol(currency='£')

    def test_002_tap_cash_out_currency_symbol_value_button_for_a_bet(self):
        """
        DESCRIPTION: Tap 'CASH OUT <currency symbol><value>' button for a bet
        EXPECTED: Green button 'CONFIRM CASH OUT <currency symbol><value>' is appear instead of 'CASH OUT <currency symbol><value>' button
        """
        self.__class__.cashout_amount = float(self.bet.buttons_panel.full_cashout_button.amount.value)
        self.bet.buttons_panel.full_cashout_button.click()

        confirmation_text = self.bet.buttons_panel.cashout_button.name
        expected_confirmation = vec.bet_history.CASHOUT_BET.confirm_cash_out + f' £{self.cashout_amount:.2f}'
        self.assertEqual(expected_confirmation, confirmation_text,
                         msg=f'Expected confirmation text: "{expected_confirmation}" '
                         f'is not equal to actual: "{confirmation_text}"')

    def test_003_tap_confirm_cash_out_button(self):
        """
        DESCRIPTION: Tap 'CONFIRM CASH OUT' button
        EXPECTED: Spinner appears on the button instead of the text 'CONFIRM CASH OUT'
        """
        self.assertTrue(self.bet.buttons_panel.has_full_cashout_button(timeout=8),
                        msg=f'CASHOUT button was not found on bet: "{self.bet_name}" section')

        self.bet.buttons_panel.full_cashout_button.click()
        self.bet.buttons_panel.cashout_button.click()

        self._logger.warning(f"*** For test stability we run this test with pre match events, "
                             f"and there is no spinner for such events")
        self.bet.buttons_panel._spinner_wait(expected_result=True, timeout=1)

    def test_004_wait_until_button_with_spinner_disappears(self):
        """
        DESCRIPTION: Wait until button with spinner disappears
        EXPECTED: * The success message is displayed instead of 'CASH OUT' button and slider with the following information:
        EXPECTED: - Green box with "tick" in a circle and message of "Cash Out Successful" are shown below bet line details. The icon and text are centered within green box.
        EXPECTED: * Cashed Out bet remains displayed until page refresh or navigating away from the tab and then returning back
        """
        result = self.bet.buttons_panel._spinner_wait(expected_result=False, timeout=25)
        self.assertFalse(result, msg='Spinner still present')

        actual_cashed_out_message = f'{self.bet.cashed_out_message.text} {self.bet.cashed_out_value.text}'
        expected_cashed_out_message = vec.bet_history.CASHED_OUT_LABEL.format(self.cashout_amount)
        self.assertEquals(actual_cashed_out_message, expected_cashed_out_message,
                          msg=f'Actual cashed out message: "{actual_cashed_out_message}" '
                          f'is not equal to expected: "{expected_cashed_out_message}"')

        result = wait_for_result(lambda: self.bet.cash_out_successful_icon,
                                 timeout=2,
                                 name='Cash Out Successful icon to appear')
        self.assertTrue(result,
                        msg=f'Green "tick" near {vec.bet_history.FULL_CASH_OUT_SUCCESS} for {self.bet_name} have not appeared')

        self.assertTrue(self.bet.wait_for_message(message=vec.bet_history.FULL_CASH_OUT_SUCCESS, timeout=20),
                        msg=f'Message "{vec.bet_history.FULL_CASH_OUT_SUCCESS}" is not shown')

    def test_005_wait_for_balance_to_update(self):
        """
        DESCRIPTION: Wait for balance to update
        EXPECTED: The balance is updated in less than 1 min (should update within seconds)
        """
        self.verify_user_balance(expected_user_balance=float(self.user_balance) + float(self.cashout_amount),
                                 timeout=10)

    def test_006_go_to_settled_bets_tab(self):
        """
        DESCRIPTION: Go to 'Settled Bets' tab
        EXPECTED: The cashed-out bet is present with the tab
        """
        self.site.open_my_bets_settled_bets()
        bet_name, self.__class__.settle_bet = self.site.bet_history.tab_content.accordions_list.\
            get_bet(bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE, event_names=self.double_bet_name, number_of_bets=5)

    def test_007_expand_the_bet_in_order_to_check_the_bet_details(self):
        """
        DESCRIPTION: Expand the bet in order to check the bet details
        EXPECTED: * All the details of the bet are correct:
        EXPECTED: - 'event name' for each selection;
        EXPECTED: - 'market name' for each selection;
        EXPECTED: - 'selection name' for each selection;
        EXPECTED: - 'Stake';
        EXPECTED: - 'You Cashed Out' value;
        EXPECTED: - 'Bet Receipt' number.
        EXPECTED: * The status of the bet is "Cashed Out"
        """
        self.assertEqual(self.settle_bet.bet_status, vec.betslip.CASHOUT_STAKE,
                         msg=f'Bet status: "{self.settle_bet.bet_status}" '
                         f'is not as expected: "{vec.betslip.CASHOUT_STAKE}"')
        self.assertEqual(self.settle_bet.selection_name, self.team1.replace('(','').replace(')',''),
                         msg=f'Bet selection name: "{self.settle_bet.selection_name}" '
                         f'is not as expected: "{self.team1.replace("(","").replace(")","")}"')
        actual_message = f'{self.settle_bet.cashed_out_message.text} {self.settle_bet.cashed_out_value.text}'
        expected_message = f'{vec.bet_history.CASHED_OUT_LABEL_SETTLE_BET} {self.settle_bet.est_returns.value}'
        self.assertEqual(actual_message, expected_message,
                         msg=f'Bet message: "{actual_message}" '
                         f'is not as expected: "{expected_message}"')
        self.assertEqual(self.settle_bet.est_returns.value, self.settle_bet.cashed_out_value.text,
                         msg=f'Bet Returns value: "{self.settle_bet.est_returns.value}" '
                         f'is not as expected: "{self.settle_bet.cashed_out_value.text}"')

        self.assertEqual(self.settle_bet.bet_receipt_info.bet_receipt.value, self.bet_id,
                         msg=f'Actual Bet Receipt number "{self.settle_bet.bet_receipt_info.bet_receipt.value}" '
                         f'does not match Expected: "{self.bet_id}"')

        expected_stake = f'£{self.bet_amount:.2f}'
        self.assertEqual(self.settle_bet.stake.value, expected_stake,
                         msg=f'Actual stake "{self.settle_bet.stake.value}" '
                         f'does not match Expected: "{expected_stake}"')
        market_name = self.match_result_market["name"] if tests.settings.backend_env == 'prod' else self.match_result_market
        self.assertEqual(self.settle_bet.market_name, market_name,
                         msg=f'Actual market name "{self.settle_bet.market_name}" '
                         f'does not match Expected: "{market_name}"')
