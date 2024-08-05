import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from voltron.utils.helpers import normalize_name
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.waiters import wait_for_result
from voltron.utils.helpers import get_cashout_value


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.critical
@pytest.mark.cash_out
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.safari
@pytest.mark.hotfix
@pytest.mark.sanity
@pytest.mark.soc
@vtest
class Test_C874332_Partial_Cash_Out_singles(BaseCashOutTest, BaseUserAccountTest):
    """
    TR_ID: C874332
    NAME: Partial Cash Out singles
    DESCRIPTION: Verify that the customer can perform a Partial Cash Out (check balance and Bet History)
    DESCRIPTION: is covered in AUTOTESTS [C48912230]
    """
    keep_browser_open = True
    enable_bs_performance_log = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: * Login to Oxygen
        DESCRIPTION: * Place a single bet on any Pre-Match or In-Play event e.g. on 'Match Betting' market
        """
        if tests.settings.backend_env == 'prod':
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                        additional_filters=cashout_filter)[0]
            self.__class__.eventID = event['event']['id']

            self.__class__.market_name = next((market['market']['name'] for market in event['event']['children']
                                               if 'Match Betting' in market['market']['templateMarketName'] and
                                               market['market'].get('children')), '')

            match_result_market = next((market['market'] for market in event['event']['children'] if
                                        market.get('market').get('templateMarketName') == 'Match Betting' and
                                        market['market'].get('children')), None)
            if not match_result_market:
                raise SiteServeException(f'Event "{self.eventID}" does not have Match Result Market')
            outcomes = match_result_market['children']
            if not outcomes:
                raise SiteServeException('No Outcomes for market present is SS response')

            self.__class__.team1 = next((outcome['outcome']['name'].replace('(','').replace(')','') for outcome in outcomes if
                                         outcome['outcome'].get('outcomeMeaningMinorCode') and
                                         outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            if not self.team1:
                raise SiteServeException('No Home team present is SS response')

            self.__class__.created_event_name = normalize_name(event['event']['name'])

            selection_ids = {i['outcome']['name'].replace('(','').replace(')',''): i['outcome']['id'] for i in outcomes}
            if not selection_ids:
                raise SiteServeException(f'Outcomes list is empty for event "{self.eventID}" "{self.created_event_name}"')
            self._logger.info(
                f'*** Found Event 1 "{self.created_event_name} with id "{self.eventID}". Selection ids: "{selection_ids}"')

            self.__class__.single_bet_name = f'{vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE} - [{self.created_event_name}]'
            selection_id = selection_ids[self.team1]

        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.created_event_name = f'{event.team1} v {event.team2}'.strip()
            self.__class__.team1 = event.team1
            selection_id = event.selection_ids[self.team1]
            self.__class__.market_name = self.ob_config.football_config.autotest_class.autotest_premier_league.\
                market_name.replace('|', '')

        self.site.login(timeout=15)
        self.open_betslip_with_selections(selection_ids=selection_id)
        self.__class__.bet_info = self.place_and_validate_single_bet()

        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

    def test_001_navigate_to_cash_out_tab_for_coral_brandor_open_bets_tab_for_ladbrokes_brand(self):
        """
        DESCRIPTION: Navigate to 'Cash Out' tab for **Coral** brand
        DESCRIPTION: or 'Open Bets' tab for **Ladbrokes** brand
        EXPECTED: * 'Cash Out'/'Open Bets' tab is loaded
        EXPECTED: * A list with COMB eligible bets is displayed
        EXPECTED: * The currency is as per user registration setting
        """
        self.site.open_my_bets_cashout()
        self.__class__.bet_name, self.__class__.bet = self.site.cashout.tab_content.accordions_list. \
            get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.created_event_name, number_of_bets=1)

        self.verify_cashout_currency_symbol(currency='£')

    def test_002_click_on_partial_cash_out_button_on_cash_out_bar_for_a_single_bet(self):
        """
        DESCRIPTION: Click on 'Partial Cash Out' button on 'Cash Out' bar for a single bet
        EXPECTED: * Partial Cash Out slider bar is displayed
        EXPECTED: * The percentage selected by default is 50%
        EXPECTED: * The 'Partial Cash Out' value is displayed on the 'Cash Out' button
        """
        self.assertTrue(self.bet.buttons_panel.has_partial_cashout_button(timeout=7), msg='PARTIAL CASHOUT is not present')
        self.bet.buttons_panel.partial_cashout_button.click()
        self.assertTrue(self.bet.buttons_panel.wait_for_cashout_slider(), msg='PARTIAL CASHOUT slider has not appeared')

        self.__class__.partial_cashout_amount = self.bet.buttons_panel.partial_cashout_button.amount.value
        expected_partial_cashout_amount = format(round(float(get_cashout_value())/2, 2), ".2f")
        self.assertEqual(str(self.partial_cashout_amount), expected_partial_cashout_amount,
                         msg=f'Actual default partial cash out amount: "{self.partial_cashout_amount}", '
                             f'expected: "{expected_partial_cashout_amount}"')

    def test_003_click_on_the_cash_out_button_again(self):
        """
        DESCRIPTION: Click on the 'Cash Out' button again
        EXPECTED: 'CONFIRM CASHOUT' green button is displayed (instead of 'Partial Cash Out' slider bar)
        """
        self.__class__.user_balance = self.site.header.user_balance

        self.__class__.cashout_amount = float(self.partial_cashout_amount)
        self.bet.buttons_panel.partial_cashout_button.click()
        expected_confirmation = vec.bet_history.CASHOUT_BET.confirm_cash_out + f' £{self.cashout_amount:.2f}'

        result = wait_for_result(lambda: self.bet.buttons_panel.cashout_button.name == expected_confirmation,
                                 expected_result=True,
                                 name=f'Button text to change to "{expected_confirmation}"',
                                 timeout=3)
        self.assertTrue(result,
                        msg=f'Expected confirmation text: "{expected_confirmation}" is not found')

    def test_004_click_on_confirm_cashout_green_button_in_order_to_confirm_the_partial_cash_out(self):
        """
        DESCRIPTION: Click on 'CONFIRM CASHOUT' green button in order to confirm the Partial Cash Out
        EXPECTED: * The Partial cash Out is now in Progress
        EXPECTED: * 'Partial Cash Out Successful' message is displayed when the COMB delay ends and the message does not disappear from the tab
        EXPECTED: * 'Stake' and 'Est.Returns'/'Potential Returns' values are decreased
        """
        start_stake = float(self.bet.stake.stake_value)
        start_est_returns_amount = float(str(self.bet.est_returns.stake_value).replace(',', ''))

        self.bet.buttons_panel.partial_cashout_button.click()
        self.bet.buttons_panel.cashout_button.click()
        result = self.bet.buttons_panel._spinner_wait(expected_result=False, timeout=25)
        self.assertFalse(result, msg='Spinner still present')
        success_message = vec.bet_history.PARTIAL_CASH_OUT_SUCCESS if self.brand == 'ladbrokes' \
            else vec.bet_history.FULL_CASH_OUT_SUCCESS
        self.assertTrue(self.bet.wait_for_message(message=success_message, timeout=10),
                        msg=f'Message "{success_message}" was not shown')

        result = wait_for_result(lambda: float(self.bet.stake.stake_value) < start_stake,
                                 name='Stake value to decrease',
                                 timeout=3)
        self.assertTrue(result, msg=f'New stake value: "{float(self.bet.stake.stake_value)}" was not decreased: "{start_stake}"')
        actual_est_returns_amount = float(str(self.bet.est_returns.stake_value).replace(',', ''))
        self.assertTrue(actual_est_returns_amount < start_est_returns_amount,
                        msg=f'New est.returns value: "{actual_est_returns_amount}" was not decreased: "{start_est_returns_amount}"')

    def test_005_wait_for_the_balance_to_update(self):
        """
        DESCRIPTION: Wait for the balance to update
        EXPECTED: The balance should update in a couple of seconds (but no longer than 1 min)
        """
        self.verify_user_balance(expected_user_balance=float(self.user_balance) + float(self.partial_cashout_amount),
                                 timeout=10)

    def test_006_go_to_open_bets_tab_on_coral_brand_or_refresh_page_on_ladbrokes_brand_and_go_to_cashed_out_bet(self):
        """
        DESCRIPTION: Go to 'Open Bets' tab on **Coral** brand or refresh page on **Ladbrokes** brand and go to cashed out bet
        EXPECTED: * All the details of the bet are correct:
        EXPECTED: - 'event name';
        EXPECTED: - 'market name';
        EXPECTED: - 'selection name';
        EXPECTED: - 'Odds';
        EXPECTED: * 'Show Partial Cash Out History' link is displayed at the bottom of the bet details
        """
        self.navigate_to_page('/')
        if self.brand == 'ladbrokes' and self.device_name != 'mobile':
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
        self.site.open_my_bets_open_bets()
        bet_name, self.__class__.bet = self.site.open_bets.tab_content.accordions_list.\
            get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.created_event_name, number_of_bets=1)

        self.assertEqual(self.bet.selection_name, self.team1,
                         msg=f'Bet selection name: "{self.bet.selection_name}" '
                         f'is not as expected: "{self.team1}"')
        self.assertEqual(self.bet.market_name, self.market_name,
                         msg=f'Actual market name "{self.bet.market_name}" '
                         f'does not match Expected: "{self.market_name}"')
        actual_event_name = self.bet.event_name
        self.assertEqual(actual_event_name, self.created_event_name,
                         msg=f'Bet event name: "{actual_event_name}" '
                         f'is not as expected: "{self.created_event_name}"')
        self.assertTrue(self.bet.partial_cash_out_history.header.is_displayed(),
                        msg='"Partial Cash Out History" section not displayed')

        bet_info = self.bet_info.get(self.team1)
        self.assertEqual(self.bet.odds_value, bet_info.get('odds'),
                         msg=f'Selection Name: "{self.bet.bet_type}" is not as expected: "{bet_info.get("odds")}"')

    def test_007_tap_the_show_partial_cash_out_history_link(self):
        """
        DESCRIPTION: Tap the 'Show Partial Cash Out History' link
        EXPECTED: * 'Show Partial Cash Out History' link becomes 'Hide Partial Cash Out History'
        EXPECTED: * Details regarding the Partial Cash Out are displayed in a table view
        EXPECTED: ![](index.php?/attachments/get/11918122)
        """
        self.bet.partial_cash_out_history.header.click()

        bet_name, self.__class__.bet = self.site.open_bets.tab_content.accordions_list.\
            get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.created_event_name, number_of_bets=1)
        self.assertTrue(self.bet.partial_cash_out_history.has_content(),
                        msg='"Partial Cash Out History" content not found')

        new_title = self.bet.partial_cash_out_history.header.title
        self.assertEqual(new_title, vec.betslip.HIDE_CASH_HISTORY,
                         msg=f'"{vec.betslip.SHOW_CASH_HISTORY}" link changed to "{new_title}", '
                         f'but should on "{vec.betslip.HIDE_CASH_HISTORY}"')

    def test_008_tap_the_hide_partial_cash_out_history_link(self):
        """
        DESCRIPTION: Tap the 'Hide Partial Cash Out History' link
        EXPECTED: * 'Hide Partial Cash Out History' link becomes 'Show Partial Cash Out History'
        EXPECTED: * Details regarding the Partial Cash Out are no more displayed
        """
        self.bet.partial_cash_out_history.header.click()

        bet_name, self.__class__.bet = self.site.open_bets.tab_content.accordions_list.\
            get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.created_event_name, number_of_bets=1)

        self.assertFalse(self.bet.partial_cash_out_history.has_content(expected_result=False),
                         msg='"Partial Cash Out History" content found')
