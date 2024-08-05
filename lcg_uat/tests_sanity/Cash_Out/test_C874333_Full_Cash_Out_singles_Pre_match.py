import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result, wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.critical
@pytest.mark.bet_placement
@pytest.mark.cash_out
@pytest.mark.desktop
@pytest.mark.login
@pytest.mark.safari
@pytest.mark.hotfix
@pytest.mark.sanity
@pytest.mark.soc
@vtest
class Test_C874333_Full_Cash_Out_singles_Pre_match(BaseCashOutTest, BaseUserAccountTest):
    """
    TR_ID: C874333
    NAME: Full Cash Out singles Pre-match
    DESCRIPTION: Verify that the customer can perform a Full Cash Out (check balance and Bet History) for Pre-match (not In Play) bet
    PRECONDITIONS: * Login to Oxygen app and log in
    PRECONDITIONS: * Go to Sport landing page e.g. Football
    PRECONDITIONS: * Place a bet on Pre-Match event (not In Play) e.g. on 'Match Betting' market
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Create test football event, PROD: Find active Football events
        DESCRIPTION: Login as user that has funds to place a bet
        DESCRIPTION: Place bets
        """
        if tests.settings.backend_env == 'prod':
            additional_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
                simple_filter(LEVELS.EVENT, ATTRIBUTES.CLASS_ID, OPERATORS.NOT_INTERSECTS, '3092')
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         additional_filters=additional_filter,
                                                         all_available_events=True)
            selection_id = None
            for event in events:
                if selection_id:
                    break
                self.__class__.eventID = event['event']['id']

                self.__class__.market_name, match_result_market = next(((market['market']['name'], market['market']) for market in event['event']['children']
                                                                        if 'Match Betting' in market.get('market', {}).get('templateMarketName', '') and
                                                                        market.get('market', '').get('children')), ('', None))
                if not match_result_market:
                    continue
                outcomes = match_result_market.get('children')
                if not outcomes:
                    continue

                self.__class__.team1 = next((outcome['outcome']['name'] for outcome in outcomes if
                                             outcome.get('outcome', '').get('outcomeMeaningMinorCode') and
                                             outcome.get('outcome').get('outcomeMeaningMinorCode', '') == 'H'), None)
                if not self.team1:
                    continue

                self.__class__.created_event_name = normalize_name(event['event']['name'])

                selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
                if not selection_ids:
                    continue

                selection_id = selection_ids[self.team1]
                self._logger.debug(f'*** Found Event 1 "{self.created_event_name} with id "{self.eventID}". '
                                   f'Team name is "{self.team1}" selection ids {selection_ids}')
            if not selection_id:
                raise SiteServeException('No Live Football event with Cashout found')

        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.created_event_name = f'{event.team1} v {event.team2}'.strip()
            self.__class__.market_name = self.ob_config.football_config. \
                autotest_class.autotest_premier_league.market_name.replace('|', '')
            self.__class__.team1 = event.team1
            selection_id = event.selection_ids[self.team1]

        username = tests.settings.betplacement_user
        self.site.login(username=username, timeout=15)
        self.open_betslip_with_selections(selection_ids=selection_id)
        self.place_bet_on_all_available_stakes()

        self.check_bet_receipt_is_displayed()
        betreceipt_section = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertEqual(betreceipt_section.__len__(), 1, msg='There is more than one item in Bet Receipt')
        for section_name, section in betreceipt_section.items():
            self.__class__.bet_id = section.bet_id
        self.site.bet_receipt.footer.click_done()

    def test_001_navigate_to_cash_out_tab_for_coral_brand_or_open_bets_tab_for_ladbrokes_brand(self):
        """
        DESCRIPTION: Navigate to 'Cash Out' tab for **Coral** brand
        DESCRIPTION: or 'Open Bets' tab for **Ladbrokes** brand
        EXPECTED: * 'Cash Out'/'Open Bets' tab is loaded
        EXPECTED: * A list with COMB eligible bets is displayed
        EXPECTED: * The currency is as per user registration setting
        """
        currency = '£'
        self.site.open_my_bets_cashout()
        self.__class__.bet_name, self.__class__.bet = self.site.cashout.tab_content.accordions_list. \
            get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, number_of_bets=1)
        self.assertEqual(currency, self.bet.stake.currency,
                         msg=f'Bet: "{self.bet_name}" stake amount does not contain required currency symbol: {currency}')
        self.assertEqual(currency, self.bet.est_returns.currency,
                         msg=f'Bet: "{self.bet_name}" Est returns amount does not contain required currency symbol: {currency}')
        self.assertEqual(currency, self.bet.buttons_panel.full_cashout_button.amount.currency,
                         msg=f'Bet: "{self.bet_name}" Full Cashout button amount does not contain required currency symbol: {currency}')

    def test_002_tap_cash_out_currency_symbol_value_button_for_a_bet(self):
        """
        DESCRIPTION: Tap 'CASH OUT <currency symbol><value>' button for a bet
        EXPECTED: Green button 'CONFIRM CASH OUT <currency symbol><value>' is appeared instead of 'CASH OUT <currency symbol><value>' button
        """
        self.__class__.user_balance = self.site.header.user_balance

        self.__class__.cashout_amount = float(self.bet.buttons_panel.full_cashout_button.amount.value)
        self.bet.buttons_panel.full_cashout_button.click()
        confirmation_text = self.bet.buttons_panel.cashout_button.name
        expected_confirmation = vec.bet_history.CASHOUT_BET.confirm_cash_out + ' £{0:.2f}'.format(self.cashout_amount)
        self.assertEqual(expected_confirmation, confirmation_text,
                         msg=f'Expected confirmation text: "{expected_confirmation}" '
                             f'is not equal to actual: "{confirmation_text}"')

    def test_003_tap_confirm_cash_out_button(self):
        """
        DESCRIPTION: Tap 'CONFIRM CASH OUT' button
        """
        wait_for_result(lambda: self.bet.buttons_panel.full_cashout_button.is_displayed(),
                        timeout=5,
                        name='Confirmation text to disappear')

        self.__class__.start_stake = float(self.bet.stake.stake_value)
        self.__class__.start_est_returns_amount = float(str(self.bet.est_returns.stake_value).replace(',', ''))

        self.bet.buttons_panel.full_cashout_button.click()
        self.bet.buttons_panel.cashout_button.click()

        self._logger.warning(f"*** For test stability we run this test with pre match events, "
                             f"and there is no spinner for such events")
        self.bet.buttons_panel._spinner_wait(expected_result=True, timeout=1)

    def test_004_wait_until_button_with_spinner_disappears(self):
        """
        DESCRIPTION: Wait until button with spinner disappears
        EXPECTED: * The success message is displayed instead of 'CASH OUT' button and slider with the following information:
        EXPECTED: - A green box with "tick" in a circle and message of "Cash Out Successful" are shown below bet line details. The icon and text are centered within a green box.
        EXPECTED: * 'You Cashed Out: <currency icon> <cashout value>' message (with a green icon on the left side) is shown under bet header.
        EXPECTED: * Cashed Out bet is NOT disappeared from 'CashOut'/'Open Bets' tab.
        EXPECTED: * Cashed Out bet is disappeared ONLY after navigation from 'Cash Out'/'Open Bets' tab.
        EXPECTED: Design:
        EXPECTED: ![](index.php?/attachments/get/11084506)
        """
        result = self.bet.buttons_panel._spinner_wait(expected_result=False, timeout=25)
        self.assertFalse(result, msg='Spinner still present')

        # release-167.0.0 Enhancement - Bet Status Removed after Cashout
        # actual_status = self.bet.bet_status
        # expected_status = vec.betslip.CASHOUT_STAKE
        # self.assertEquals(actual_status, expected_status,
        #                   msg=f'Actual bet status: "{actual_status}" is not "{expected_status}"')

        self.assertTrue(self.bet.has_cashed_out_mark(),
                        msg='"Cashed out" mark is not present on Cashout page after cashout')

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
            get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.created_event_name)

    def test_007_check_the_bet_details(self):
        """
        DESCRIPTION: Check the bet details
        EXPECTED: * All the details of the bet are correct:
        EXPECTED: - 'event name';
        EXPECTED: - 'market name';
        EXPECTED: - 'selection name';
        EXPECTED: - 'Stake'
        EXPECTED: - 'You Cashed Out' value;
        EXPECTED: - 'Bet Receipt' number.
        EXPECTED: * The status of the bet is "Cashed Out"
        """
        wait_for_haul(3)
        self.assertEqual(self.settle_bet.bet_status, vec.betslip.CASHOUT_STAKE,
                         msg=f'Bet status: "{self.settle_bet.bet_status}" '
                         f'is not as expected: "{vec.betslip.CASHOUT_STAKE}"')
        actual_selection_name = self.settle_bet.selection_name.replace('(', '').replace(')', '')
        expected_selection_name = self.team1.replace('(', '').replace(')', '')
        self.assertEqual(actual_selection_name, expected_selection_name,
                         msg=f'Bet selection name: "{actual_selection_name}" '
                         f'is not as expected: "{expected_selection_name}"')
        actual_event_name = self.settle_bet.event_name
        self.assertEqual(actual_event_name, self.created_event_name,
                         msg=f'Bet event name: "{actual_event_name}" '
                         f'is not as expected: "{self.created_event_name}"')
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
        expected_stake = '£{0:.2f}'.format(self.bet_amount)
        self.assertEqual(self.settle_bet.stake.value, expected_stake,
                         msg=f'Actual stake "{self.settle_bet.stake.value}" '
                         f'does not match Expected: "{expected_stake}"')
        self.assertEqual(self.settle_bet.market_name, self.market_name,
                         msg=f'Actual market name "{self.settle_bet.market_name}" '
                         f'does not match Expected: "{self.market_name}"')
