import pytest
import tests
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from random import choice
from crlat_siteserve_client.constants import LEVELS, OPERATORS, ATTRIBUTES
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.user_account
@pytest.mark.portal_dependant
@vtest
class Test_C14640142_Verify_balance_update_after_bet_placement_cash_out_action(BaseBetSlipTest):
    """
    TR_ID: C14640142
    NAME: Verify balance update after bet placement, cash out action
    DESCRIPTION: This test case verifies successful balance update after bet placement, cash out action, at betslip header.
    PRECONDITIONS: User is logged in.
    """
    keep_browser_open = True
    sport_name = vec.sb.FOOTBALL
    bet_amount = 0.3

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Create test event, PROD: Find active events
        DESCRIPTION: Log in with a user that has a positive balance
        """
        if tests.settings.backend_env == 'prod':
            additional_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_FALSE)
            event = self.get_active_events_for_category(
                category_id=self.ob_config.football_config.category_id, additional_filters=additional_filter)[0]
            self.__class__.event_name = normalize_name(event['event']['name'])
            self.__class__.event_id = event['event']['id']
            self.__class__.league = self.get_accordion_name_for_event_from_ss(event=event)
            self._logger.info(f'*** Found Football event "{self.event_name}" with ID "{self.event_id}"')
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.selection_id = list(all_selection_ids.values())[0]
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.event_name = f'{event.team1} v {event.team2}'
            self.__class__.event_id = event.event_id
            self.__class__.league = tests.settings.football_autotest_league
            self._logger.info(f'*** Created Football event "{self.event_name}" with ID "{self.event_id}"')
            self.__class__.selection_id = list(event.selection_ids.values())[0]

        self.site.login(username=tests.settings.betplacement_user)
        self.site.wait_content_state('homepage')
        self.__class__.user_balance = self.site.header.user_balance

    def test_001_tap_one_sportrace_selection(self):
        """
        DESCRIPTION: Tap one <Sport>/<Race> selection
        EXPECTED: Selected price/odds are highlighted in green
        EXPECTED: Quick Bet is displayed at the bottom of the page
        """
        sport_name = vec.sb.FOOTBALL.title()
        self.site.open_sport(name=sport_name)
        self.site.wait_content_state(state_name=sport_name)
        event = self.get_event_from_league(event_id=self.event_id,
                                           section_name=self.league)

        output_prices = event.get_active_prices()
        self.assertTrue(output_prices, msg=f'Could not find output prices for event "{self.event_name}"')

        selection = choice(list(output_prices.keys()))
        bet_button = output_prices.get(selection)
        self.assertTrue(bet_button, msg=f'Bet button for "{self.team1}" was not found')
        bet_button.click()
        self.assertTrue(bet_button.is_selected(), msg='Outcome button is not highlighted in green')
        if self.device_type == 'mobile':
            self.assertEqual(bet_button.background_color_value, vec.colors.SELECTED_BET_BUTTON_COLOR,
                             msg=f'Selected price/odds for "{bet_button}" background color "{bet_button.background_color_value}" is not highlighted in green {vec.colors.SELECTED_BET_BUTTON_COLOR}')
            quick_bet = self.site.quick_bet_panel
            self.assertEqual(quick_bet.header.title, vec.quickbet.QUICKBET_TITLE,
                             msg=f'Actual title "{quick_bet.header.title}" does not match expected "{vec.quickbet.QUICKBET_TITLE}"')

    def test_002_enter_value_in_stake_field(self):
        """
        DESCRIPTION: Enter value in 'Stake' field
        EXPECTED: 'Stake' field is populated with entered value
        """
        if self.device_type == 'mobile':
            quick_bet_panel = self.site.quick_bet_panel
            quick_bet = quick_bet_panel.selection.content
            quick_bet.amount_form.input.value = self.bet_amount

            amount = float(quick_bet.amount_form.input.value)
            self.assertEqual(amount, self.bet_amount,
                             msg=f'Entered amount "{amount}" is not equal to expected "{self.bet_amount}"')
        else:
            self.site.open_betslip()

    def test_003_tap_place_bet_buttontap_close_button(self):
        """
        DESCRIPTION: Tap 'PLACE BET' button
        DESCRIPTION: Tap 'Close' button
        EXPECTED: Bet is placed successfully
        EXPECTED: Bet Receipt is closed
        """
        if self.device_type == 'mobile':
            self.site.quick_bet_panel.place_bet.click()
            bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
            self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
            self.site.quick_bet_panel.header.close_button.click()
            self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is not closed')
        else:
            self.place_and_validate_single_bet()

    def test_004_verify_the_balance(self):
        """
        DESCRIPTION: Verify the balance
        EXPECTED: Balance is updated automatically after successful bet placement, it is decremented by entered stake
        """
        expected_user_balance = self.user_balance - self.bet_amount
        self.verify_user_balance(expected_user_balance=expected_user_balance)
        self.user_balance = expected_user_balance

    def test_005_add_one_selection_to_betsliptap_on_add_to_betslip_buttonclick_on_betslip_icon(self):
        """
        DESCRIPTION: Add one selection to Betslip
        DESCRIPTION: Tap on 'Add to betslip' button
        DESCRIPTION: Click on Betslip icon
        EXPECTED: Betslip view is opened. Balance is displayed in the header
        """
        event2 = self.get_event_from_league(event_id=self.event_id,
                                            section_name=self.league)
        output_prices2 = event2.get_active_prices()
        self.assertTrue(output_prices2, msg=f'Could not find output prices for created event "{self.event_name}"')
        name2, price2 = list(output_prices2.items())[1]
        self.assertTrue(price2, msg=f'Bet button "{name2}" is not found')
        price2.click()
        self.assertTrue(price2.is_selected(timeout=2), msg=f'Price "{name2}" was not selected after click')

        if self.site.wait_for_quick_bet_panel(timeout=2):
            self.site.quick_bet_panel.add_to_betslip_button.click()
            self.site.wait_for_quick_bet_panel(expected_result=False)
            self.site.wait_quick_bet_overlay_to_hide()
            self.site.open_betslip()
            betslip_content = self.get_betslip_content()
            self.assertTrue(betslip_content.header.has_user_balance,
                            msg='Balance is not displayed at the top right corner')

    def test_006_enter_value_in_stake_field(self):
        """
        DESCRIPTION: Enter value in 'Stake' field
        EXPECTED: 'Place Bet' button becomes enabled
        """
        self.place_and_validate_single_bet(number_of_stakes=1)
        self.__class__.bet_receipt = self.site.bet_receipt.footer

    def test_007_tap_on_place_bet_button_verify_the_balance_in_the_header_of_betslip_view(self):
        """
        DESCRIPTION: Tap on 'Place Bet' button. Verify the balance in the header of Betslip view
        EXPECTED: Balance is updated automatically, it is decremented by entered stake
        """
        expected_user_balance = self.user_balance - self.bet_amount
        self.verify_user_balance(expected_user_balance=expected_user_balance)
        self.__class__.user_balance = expected_user_balance

    def test_008_tap_on_go_betting_buttonverify_the_balance(self):
        """
        DESCRIPTION: Tap on 'GO BETTING' button
        DESCRIPTION: Verify the balance
        EXPECTED: Betslip view is closed after tapping 'GO BETTING' button
        EXPECTED: Balance is updated
        """
        self.bet_receipt.click_done()
        self.site.wait_content_state(state_name=self.sport_name)
        self.verify_user_balance(expected_user_balance=self.user_balance)

    def test_009_navigate_to_cash_out_tab_on_my_bets_page_coral__open_bets_page_ladbrokes(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page (Coral) / 'Open Bets' page (Ladbrokes)
        EXPECTED: 'Cash Out' tab is opened
        """
        self.site.open_my_bets_cashout()

    def test_010_tap_cash_out_button_for_last_added_bettap_confirm_cash_out_button(self):
        """
        DESCRIPTION: Tap 'CASH OUT' button for last added bet
        DESCRIPTION: Tap 'CONFIRM CASH OUT' button
        EXPECTED: Spinner appears on the button instead of the text 'CONFIRM CASH OUT'
        """
        self.user_balance = self.site.header.user_balance
        self.__class__.bet_name, self.__class__.bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type='SINGLE', event_names=self.event_name, number_of_bets=1)
        self.assertTrue(self.bet, msg=f'Event: "{self.event_name}" Single bet not found')
        self.__class__.cashout_amount = float(self.bet.buttons_panel.full_cashout_button.amount.value)
        self.bet.buttons_panel.full_cashout_button.click()
        confirmation_text = self.bet.buttons_panel.cashout_button.name
        expected_confirmation = vec.bet_history.CASHOUT_BET.confirm_cash_out + f' £{self.cashout_amount:.2f}'
        self.assertEqual(expected_confirmation, confirmation_text,
                         msg=f'Expected confirmation text: "{expected_confirmation}" '
                             f'is not equal to actual: "{confirmation_text}"')

        self.assertTrue(self.bet.buttons_panel.has_full_cashout_button(timeout=8),
                        msg=f'CASHOUT button was not found on bet: "{self.bet_name}" section')

        self.bet.buttons_panel.full_cashout_button.click()
        self.bet.buttons_panel.cashout_button.click()

        self._logger.warning(f"*** For test stability we run this test with pre match events, "
                             f"and there is no spinner for such events")
        self.bet.buttons_panel._spinner_wait(expected_result=True, timeout=1)

    def test_011_wait_until_button_with_spinner_disappears(self):
        """
        DESCRIPTION: Wait until button with spinner disappears
        EXPECTED: 'Cashed out' label is displayed ath the top right corner on the header
        EXPECTED: Green "tick" in a circle and message "You cashed out <currency> <value>" is shown below the header
        EXPECTED: Message "Cashout Successfully" with the green tick at the beginning are shown instead of 'cashout' button at the bottom of bet line
        """
        result = self.bet.buttons_panel._spinner_wait(expected_result=False, timeout=25)
        self.assertFalse(result, msg='Spinner still present')

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

    def test_012_verify_user_balance(self):
        """
        DESCRIPTION: Verify user balance
        EXPECTED: User balance is increased on full cash out value
        """
        self.verify_user_balance(expected_user_balance=float(self.user_balance) + float(self.cashout_amount),
                                 timeout=10)

    def test_013_place_one_more_betnavigate_to_cash_out_tab_on_my_bets_page(self):
        """
        DESCRIPTION: Place one more bet
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page
        EXPECTED: 'Cash Out' tab is opened
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.place_and_validate_single_bet(number_of_stakes=1)
        self.site.bet_receipt.close_button.click()
        self.site.open_my_bets_cashout()
        self.__class__.bet_name, self.__class__.bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type='SINGLE', event_names=self.event_name, number_of_bets=1)
        self.assertTrue(self.bet, msg=f'Event: "{self.event_name}" Single bet not found')
        self.assertTrue(self.bet.buttons_panel.has_partial_cashout_button(),
                        msg='"Partial Cashout button" is not displayed')

    def test_014_tap_partial_cashout_button_for_last_added_bet(self):
        """
        DESCRIPTION: Tap 'PARTIAL CASHOUT' button for last added bet
        EXPECTED: Sum of cash out is counted
        """
        self.bet.buttons_panel.partial_cashout_button.click()
        self.assertTrue(self.bet.buttons_panel.wait_for_cashout_slider(),
                        msg='"PARTIAL CASHOUT" slider was not appeared')

    def test_015_tap_cashout_buttontap_confirm_cash_out_button(self):
        """
        DESCRIPTION: Tap 'CASHOUT' button
        DESCRIPTION: Tap 'CONFIRM CASH OUT' button
        EXPECTED: Spinner appears on the button instead of the text 'CONFIRM CASH OUT'
        """
        self.__class__.user_balance = self.site.header.user_balance
        self.bet.buttons_panel.move_partial_cashout_slider(direction='right')
        sleep(2)
        self.__class__.cashout_amount = self.bet.buttons_panel.partial_cashout_button.amount.value
        self.bet.buttons_panel.partial_cashout_button.click()
        self.bet.buttons_panel.cashout_button.click()

    def test_016_wait_until_button_with_spinner_disappears(self):
        """
        DESCRIPTION: Wait until button with spinner disappears
        EXPECTED: The success message is displayed below 'CASH OUT' button "Partial Cash Out Successful"
        """
        self.assertTrue(self.bet.wait_for_message(message=vec.bet_history.PARTIAL_CASH_OUT_SUCCESS, timeout=30),
                        msg=f'Message "{vec.bet_history.PARTIAL_CASH_OUT_SUCCESS}" is not shown')

    def test_017_verify_user_balance(self):
        """
        DESCRIPTION: Verify user balance
        EXPECTED: User balance is increased on previously cashed out value
        """
        self.verify_user_balance(expected_user_balance=float(self.user_balance) + float(self.cashout_amount))
